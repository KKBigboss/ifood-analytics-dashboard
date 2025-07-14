import pandas as pd
import sqlite3
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ReportGenerator:
    def __init__(self, db_path='ifood_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        
    def generate_executive_summary(self):
        """Gera resumo executivo com principais métricas"""
        
        # Carregar dados principais
        query = """
        SELECT 
            p.*,
            r.nome as restaurante_nome,
            r.categoria,
            r.cidade as restaurante_cidade,
            u.segmento as usuario_segmento,
            u.cidade as usuario_cidade
        FROM pedidos p
        JOIN restaurantes r ON p.restaurante_id = r.id
        JOIN usuarios u ON p.usuario_id = u.id
        """
        
        df = pd.read_sql(query, self.conn)
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])
        
        # Calcular métricas principais
        df_entregues = df[df['status'] == 'Entregue']
        
        metrics = {
            'total_pedidos': len(df),
            'pedidos_entregues': len(df_entregues),
            'receita_total': df_entregues['valor_pedido'].sum(),
            'ticket_medio': df_entregues['valor_pedido'].mean(),
            'tempo_medio_entrega': df_entregues['tempo_entrega'].mean(),
            'taxa_cancelamento': (len(df[df['status'] == 'Cancelado']) / len(df)) * 100,
            'rating_medio': df_entregues['avaliacao'].mean(),
            'total_restaurantes': df['restaurante_id'].nunique(),
            'total_usuarios': df['usuario_id'].nunique(),
            'total_cidades': df['restaurante_cidade'].nunique()
        }
        
        return metrics, df, df_entregues
    
    def create_excel_report(self):
        """Cria relatório executivo em Excel"""
        
        print("Gerando relatório executivo...")
        
        metrics, df, df_entregues = self.generate_executive_summary()
        
        # Criar arquivo Excel com múltiplas abas
        with pd.ExcelWriter('Relatorio_Executivo_iFood.xlsx', engine='openpyxl') as writer:
            
            # Aba 1: Resumo Executivo
            summary_data = {
                'Métrica': [
                    'Total de Pedidos',
                    'Pedidos Entregues',
                    'Receita Total (R$)',
                    'Ticket Médio (R$)',
                    'Tempo Médio de Entrega (min)',
                    'Taxa de Cancelamento (%)',
                    'Rating Médio',
                    'Total de Restaurantes',
                    'Total de Usuários',
                    'Total de Cidades'
                ],
                'Valor': [
                    f"{metrics['total_pedidos']:,}",
                    f"{metrics['pedidos_entregues']:,}",
                    f"R$ {metrics['receita_total']:,.2f}",
                    f"R$ {metrics['ticket_medio']:.2f}",
                    f"{metrics['tempo_medio_entrega']:.1f}",
                    f"{metrics['taxa_cancelamento']:.1f}%",
                    f"{metrics['rating_medio']:.1f}",
                    f"{metrics['total_restaurantes']:,}",
                    f"{metrics['total_usuarios']:,}",
                    f"{metrics['total_cidades']:,}"
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Resumo Executivo', index=False)
            
            # Aba 2: Performance por Categoria
            category_performance = df_entregues.groupby('categoria').agg({
                'valor_pedido': ['sum', 'mean', 'count'],
                'tempo_entrega': 'mean',
                'avaliacao': 'mean',
                'restaurante_id': 'nunique'
            }).round(2)
            
            category_performance.columns = [
                'Receita Total', 'Ticket Médio', 'Total Pedidos', 
                'Tempo Médio Entrega', 'Rating Médio', 'Qtd Restaurantes'
            ]
            category_performance = category_performance.reset_index()
            category_performance['Pedidos por Restaurante'] = (
                category_performance['Total Pedidos'] / category_performance['Qtd Restaurantes']
            ).round(1)
            
            category_performance.to_excel(writer, sheet_name='Performance por Categoria', index=False)
            
            # Aba 3: Performance por Cidade
            city_performance = df_entregues.groupby('restaurante_cidade').agg({
                'valor_pedido': ['sum', 'mean', 'count'],
                'tempo_entrega': 'mean',
                'avaliacao': 'mean',
                'restaurante_id': 'nunique',
                'usuario_id': 'nunique'
            }).round(2)
            
            city_performance.columns = [
                'Receita Total', 'Ticket Médio', 'Total Pedidos',
                'Tempo Médio Entrega', 'Rating Médio', 'Qtd Restaurantes', 'Qtd Usuários'
            ]
            city_performance = city_performance.reset_index()
            city_performance.columns = ['Cidade'] + city_performance.columns[1:].tolist()
            
            city_performance.to_excel(writer, sheet_name='Performance por Cidade', index=False)
            
            # Aba 4: Segmentação de Usuários
            user_segmentation = df_entregues.groupby('usuario_segmento').agg({
                'valor_pedido': ['sum', 'mean', 'count'],
                'usuario_id': 'nunique'
            }).round(2)
            
            user_segmentation.columns = ['Receita Total', 'Ticket Médio', 'Total Pedidos', 'Qtd Usuários']
            user_segmentation = user_segmentation.reset_index()
            user_segmentation['Pedidos por Usuário'] = (
                user_segmentation['Total Pedidos'] / user_segmentation['Qtd Usuários']
            ).round(1)
            user_segmentation['% da Receita'] = (
                user_segmentation['Receita Total'] / user_segmentation['Receita Total'].sum() * 100
            ).round(1)
            
            user_segmentation.to_excel(writer, sheet_name='Segmentação Usuários', index=False)
            
            # Aba 5: Análise Temporal
            df_entregues['mes'] = df_entregues['data_pedido'].dt.to_period('M')
            temporal_analysis = df_entregues.groupby('mes').agg({
                'valor_pedido': ['sum', 'mean', 'count'],
                'tempo_entrega': 'mean',
                'avaliacao': 'mean'
            }).round(2)
            
            temporal_analysis.columns = [
                'Receita Mensal', 'Ticket Médio', 'Total Pedidos',
                'Tempo Médio Entrega', 'Rating Médio'
            ]
            temporal_analysis = temporal_analysis.reset_index()
            temporal_analysis['mes'] = temporal_analysis['mes'].astype(str)
            
            # Calcular crescimento mês a mês
            temporal_analysis['Crescimento Receita %'] = temporal_analysis['Receita Mensal'].pct_change() * 100
            temporal_analysis['Crescimento Pedidos %'] = temporal_analysis['Total Pedidos'].pct_change() * 100
            
            temporal_analysis.to_excel(writer, sheet_name='Análise Temporal', index=False)
            
            # Aba 6: Top Restaurantes
            top_restaurants = df_entregues.groupby(['restaurante_nome', 'categoria', 'restaurante_cidade']).agg({
                'valor_pedido': ['sum', 'mean', 'count'],
                'tempo_entrega': 'mean',
                'avaliacao': 'mean'
            }).round(2)
            
            top_restaurants.columns = [
                'Receita Total', 'Ticket Médio', 'Total Pedidos',
                'Tempo Médio Entrega', 'Rating Médio'
            ]
            top_restaurants = top_restaurants.reset_index()
            top_restaurants = top_restaurants.sort_values('Receita Total', ascending=False).head(20)
            
            top_restaurants.to_excel(writer, sheet_name='Top 20 Restaurantes', index=False)
        
        print("✅ Relatório Excel gerado: Relatorio_Executivo_iFood.xlsx")
        
    def create_insights_document(self):
        """Cria documento com insights e recomendações"""
        
        metrics, df, df_entregues = self.generate_executive_summary()
        
        insights_content = f"""
# 📊 RELATÓRIO DE INSIGHTS ESTRATÉGICOS - IFOOD
**Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## 🎯 RESUMO EXECUTIVO

### Métricas Principais
- **Total de Pedidos:** {metrics['total_pedidos']:,}
- **Receita Total:** R$ {metrics['receita_total']:,.2f}
- **Ticket Médio:** R$ {metrics['ticket_medio']:.2f}
- **Taxa de Cancelamento:** {metrics['taxa_cancelamento']:.1f}%
- **Rating Médio:** {metrics['rating_medio']:.1f}/5.0
- **Tempo Médio de Entrega:** {metrics['tempo_medio_entrega']:.1f} minutos

## 🔍 ANÁLISES PRINCIPAIS

### 1. Performance por Categoria
{self._get_category_insights(df_entregues)}

### 2. Análise Geográfica
{self._get_city_insights(df_entregues)}

### 3. Segmentação de Usuários
{self._get_user_insights(df_entregues)}

### 4. Eficiência Operacional
{self._get_operational_insights(df_entregues)}

## 💡 INSIGHTS ESTRATÉGICOS

### 🚀 Oportunidades de Crescimento
1. **Expansão Premium:** Categorias com alto ticket médio mostram potencial
2. **Otimização Logística:** Redução de 15% no tempo pode aumentar satisfação
3. **Retenção de Clientes:** Foco em usuários ocasionais para conversão
4. **Parcerias Estratégicas:** Restaurantes com alta performance merecem incentivos

### ⚠️ Pontos de Atenção
1. **Taxa de Cancelamento:** Monitorar categorias com alta taxa
2. **Disparidade Regional:** Equalizar experiência entre cidades
3. **Tempo de Entrega:** Algumas regiões acima da média desejada
4. **Satisfação:** Manter rating acima de 4.5 como meta

## 📈 RECOMENDAÇÕES ESTRATÉGICAS

### Curto Prazo (1-3 meses)
- Implementar campanhas de reativação para usuários inativos
- Otimizar rotas de entrega nas cidades com maior tempo médio
- Criar programa de incentivos para restaurantes com baixa performance

### Médio Prazo (3-6 meses)
- Expandir operação em cidades com alta demanda por restaurante
- Desenvolver produtos específicos para segmento Premium
- Implementar sistema de predição de demanda

### Longo Prazo (6-12 meses)
- Investir em tecnologia de IA para otimização de rotas
- Criar ecossistema de parcerias com restaurantes exclusivos
- Desenvolver programa de fidelidade abrangente

## 📊 KPIs RECOMENDADOS PARA MONITORAMENTO

### Operacionais
- Tempo médio de entrega por cidade/categoria
- Taxa de cancelamento por motivo
- Eficiência dos entregadores

### Financeiros
- Receita por usuário ativo (ARPU)
- Lifetime Value (LTV) por segmento
- Margem de contribuição por categoria

### Satisfação
- Net Promoter Score (NPS)
- Taxa de retenção mensal
- Rating médio por touchpoint

---
**Nota:** Este relatório foi gerado automaticamente com base nos dados disponíveis.
Para análises mais detalhadas, consulte o dashboard interativo.
        """
        
        with open('Insights_Estrategicos_iFood.md', 'w', encoding='utf-8') as f:
            f.write(insights_content)
        
        print("✅ Documento de insights gerado: Insights_Estrategicos_iFood.md")
    
    def _get_category_insights(self, df):
        """Gera insights sobre categorias"""
        category_perf = df.groupby('categoria').agg({
            'valor_pedido': ['sum', 'mean', 'count']
        })
        category_perf.columns = ['receita', 'ticket_medio', 'pedidos']
        
        top_category = category_perf.sort_values('receita', ascending=False).index[0]
        best_ticket = category_perf.sort_values('ticket_medio', ascending=False).index[0]
        
        return f"""
- **Categoria Líder em Receita:** {top_category}
- **Maior Ticket Médio:** {best_ticket}
- **Total de Categorias Ativas:** {len(category_perf)}
- **Oportunidade:** Categorias premium mostram potencial de crescimento
        """
    
    def _get_city_insights(self, df):
        """Gera insights sobre cidades"""
        city_perf = df.groupby('restaurante_cidade').agg({
            'valor_pedido': 'sum',
            'restaurante_id': 'nunique'
        })
        city_perf['pedidos_por_restaurante'] = df.groupby('restaurante_cidade').size() / city_perf['restaurante_id']
        
        top_city = city_perf.sort_values('valor_pedido', ascending=False).index[0]
        best_efficiency = city_perf.sort_values('pedidos_por_restaurante', ascending=False).index[0]
        
        return f"""
- **Cidade Líder em Receita:** {top_city}
- **Maior Eficiência por Restaurante:** {best_efficiency}
- **Total de Cidades Ativas:** {len(city_perf)}
- **Potencial de Expansão:** Cidades com alta demanda por restaurante
        """
    
    def _get_user_insights(self, df):
        """Gera insights sobre usuários"""
        user_segments = df.groupby('usuario_segmento').agg({
            'valor_pedido': ['sum', 'mean', 'count'],
            'usuario_id': 'nunique'
        })
        
        premium_revenue = user_segments.loc['Premium', ('valor_pedido', 'sum')] if 'Premium' in user_segments.index else 0
        total_revenue = user_segments[('valor_pedido', 'sum')].sum()
        premium_pct = (premium_revenue / total_revenue * 100) if total_revenue > 0 else 0
        
        return f"""
- **Segmento Premium:** Representa {premium_pct:.1f}% da receita total
- **Total de Segmentos:** {len(user_segments)}
- **Oportunidade:** Converter usuários ocasionais em regulares
- **Fidelização:** Programas específicos por segmento
        """
    
    def _get_operational_insights(self, df):
        """Gera insights operacionais"""
        avg_delivery_time = df['tempo_entrega'].mean()
        avg_rating = df['avaliacao'].mean()
        
        return f"""
- **Tempo Médio de Entrega:** {avg_delivery_time:.1f} minutos
- **Satisfação Média:** {avg_rating:.1f}/5.0
- **Meta de Tempo:** Reduzir para menos de 45 minutos
- **Meta de Satisfação:** Manter acima de 4.5
        """
    
    def close(self):
        """Fecha conexão com banco"""
        self.conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando geração de relatórios...")
    
    generator = ReportGenerator()
    
    try:
        generator.create_excel_report()
        generator.create_insights_document()
        print("\n✅ Todos os relatórios foram gerados com sucesso!")
        print("\nArquivos criados:")
        print("- Relatorio_Executivo_iFood.xlsx")
        print("- Insights_Estrategicos_iFood.md")
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatórios: {e}")
        print("Certifique-se de que o arquivo ifood_data.db existe.")
        print("Execute primeiro: python data_generator.py")
    
    finally:
        generator.close()
