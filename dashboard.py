import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Dashboard Executivo iFood",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded"
)

class IFoodDashboard:
    def __init__(self, db_path='ifood_data.db'):
        self.db_path = db_path
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def load_data(self):
        """Carrega dados principais para o dashboard"""
        conn = self.get_connection()
        
        # Dados de pedidos com informações de restaurantes
        query_pedidos = """
        SELECT 
            p.*,
            r.nome as restaurante_nome,
            r.categoria,
            r.cidade,
            r.rating as restaurante_rating,
            u.segmento as usuario_segmento
        FROM pedidos p
        JOIN restaurantes r ON p.restaurante_id = r.id
        JOIN usuarios u ON p.usuario_id = u.id
        """
        
        self.df_pedidos = pd.read_sql(query_pedidos, conn)
        self.df_pedidos['data_pedido'] = pd.to_datetime(self.df_pedidos['data_pedido'])
        
        conn.close()
        return self.df_pedidos
    
    def calculate_kpis(self):
        """Calcula KPIs principais"""
        df = self.df_pedidos
        
        # Filtrar apenas pedidos entregues para KPIs principais
        df_entregues = df[df['status'] == 'Entregue']
        
        # Verificar se há dados
        total_pedidos = len(df)
        total_entregues = len(df_entregues)
        
        kpis = {
            'total_pedidos': total_pedidos,
            'total_receita': df_entregues['valor_pedido'].sum() if total_entregues > 0 else 0,
            'ticket_medio': df_entregues['valor_pedido'].mean() if total_entregues > 0 else 0,
            'tempo_medio_entrega': df_entregues['tempo_entrega'].mean() if total_entregues > 0 else 0,
            'taxa_cancelamento': (len(df[df['status'] == 'Cancelado']) / total_pedidos * 100) if total_pedidos > 0 else 0,
            'rating_medio': df_entregues['avaliacao'].mean() if total_entregues > 0 else 0,
            'restaurantes_ativos': df['restaurante_id'].nunique() if total_pedidos > 0 else 0,
            'usuarios_ativos': df['usuario_id'].nunique() if total_pedidos > 0 else 0
        }
        
        # Tratar valores NaN
        for key, value in kpis.items():
            if pd.isna(value):
                kpis[key] = 0
        
        return kpis
    
    def create_revenue_chart(self):
        """Gráfico de receita ao longo do tempo"""
        df_entregues = self.df_pedidos[self.df_pedidos['status'] == 'Entregue'].copy()
        
        # Verificar se há dados
        if len(df_entregues) == 0:
            # Criar gráfico vazio
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Receita Mensal (R$)', 'Volume de Pedidos'),
                vertical_spacing=0.1
            )
            fig.update_layout(
                title="Evolução de Receita e Volume",
                height=500,
                showlegend=False,
                annotations=[
                    dict(
                        text="Nenhum dado disponível para os filtros selecionados",
                        x=0.5,
                        y=0.5,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=16)
                    )
                ]
            )
            return fig
        
        df_entregues['mes'] = df_entregues['data_pedido'].dt.to_period('M')
        
        receita_mensal = df_entregues.groupby('mes').agg({
            'valor_pedido': 'sum',
            'id': 'count'
        }).reset_index()
        
        receita_mensal['mes'] = receita_mensal['mes'].astype(str)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Receita Mensal (R$)', 'Volume de Pedidos'),
            vertical_spacing=0.1
        )
        
        # Receita
        fig.add_trace(
            go.Scatter(
                x=receita_mensal['mes'],
                y=receita_mensal['valor_pedido'],
                mode='lines+markers',
                name='Receita',
                line=dict(color='#FF6B35', width=3)
            ),
            row=1, col=1
        )
        
        # Volume de pedidos
        fig.add_trace(
            go.Bar(
                x=receita_mensal['mes'],
                y=receita_mensal['id'],
                name='Pedidos',
                marker_color='#004E89'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Evolução de Receita e Volume",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_category_performance(self):
        """Performance por categoria de restaurante"""
        df_entregues = self.df_pedidos[self.df_pedidos['status'] == 'Entregue']
        
        # Verificar se há dados
        if len(df_entregues) == 0:
            fig = px.scatter(
                title="Performance por Categoria de Restaurante",
                labels={
                    'x': 'Ticket Médio (R$)',
                    'y': 'Volume de Pedidos'
                }
            )
            fig.add_annotation(
                text="Nenhum dado disponível para os filtros selecionados",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(height=500)
            return fig
        
        performance = df_entregues.groupby('categoria').agg({
            'valor_pedido': ['sum', 'mean', 'count'],
            'tempo_entrega': 'mean',
            'avaliacao': 'mean'
        }).round(2)
        
        performance.columns = ['Receita Total', 'Ticket Médio', 'Total Pedidos', 'Tempo Médio', 'Rating Médio']
        performance = performance.reset_index()
        
        # Gráfico de bolhas
        fig = px.scatter(
            performance,
            x='Ticket Médio',
            y='Total Pedidos',
            size='Receita Total',
            color='Rating Médio',
            hover_name='categoria',
            title="Performance por Categoria de Restaurante",
            labels={
                'Ticket Médio': 'Ticket Médio (R$)',
                'Total Pedidos': 'Volume de Pedidos',
                'Rating Médio': 'Avaliação Média'
            },
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=500)
        return fig
    
    def create_city_analysis(self):
        """Análise por cidade"""
        df_entregues = self.df_pedidos[self.df_pedidos['status'] == 'Entregue']
        
        # Verificar se há dados
        if len(df_entregues) == 0:
            empty_df = pd.DataFrame(columns=['cidade', 'Receita', 'Pedidos por Restaurante'])
            fig = px.bar(
                empty_df,
                x='Receita',
                y='cidade',
                orientation='h',
                title="Receita por Cidade",
                labels={'Receita': 'Receita Total (R$)', 'cidade': 'Cidade'}
            )
            fig.add_annotation(
                text="Nenhum dado disponível para os filtros selecionados",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(height=400)
            return fig, empty_df
        
        city_performance = df_entregues.groupby('cidade').agg({
            'valor_pedido': 'sum',
            'id': 'count',
            'restaurante_id': 'nunique',
            'usuario_id': 'nunique'
        }).round(2)
        
        city_performance.columns = ['Receita', 'Pedidos', 'Restaurantes', 'Usuários']
        city_performance['Pedidos por Restaurante'] = city_performance['Pedidos'] / city_performance['Restaurantes']
        city_performance = city_performance.reset_index()
        
        fig = px.bar(
            city_performance.sort_values('Receita', ascending=True),
            x='Receita',
            y='cidade',
            orientation='h',
            title="Receita por Cidade",
            labels={'Receita': 'Receita Total (R$)', 'cidade': 'Cidade'}
        )
        
        fig.update_layout(height=400)
        return fig, city_performance
    
    def create_user_segmentation(self):
        """Análise de segmentação de usuários"""
        df_entregues = self.df_pedidos[self.df_pedidos['status'] == 'Entregue']
        
        # Verificar se há dados
        if len(df_entregues) == 0:
            empty_df = pd.DataFrame(columns=['usuario_segmento', 'Receita Total', 'Ticket Médio', 'Total Pedidos', 'Total Usuários', 'Pedidos por Usuário'])
            fig = px.pie(
                empty_df,
                values='Receita Total',
                names='usuario_segmento',
                title="Distribuição de Receita por Segmento de Usuário"
            )
            fig.add_annotation(
                text="Nenhum dado disponível para os filtros selecionados",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(height=400)
            return fig, empty_df
        
        segmentation = df_entregues.groupby('usuario_segmento').agg({
            'valor_pedido': ['sum', 'mean', 'count'],
            'usuario_id': 'nunique'
        }).round(2)
        
        segmentation.columns = ['Receita Total', 'Ticket Médio', 'Total Pedidos', 'Total Usuários']
        segmentation['Pedidos por Usuário'] = segmentation['Total Pedidos'] / segmentation['Total Usuários']
        segmentation = segmentation.reset_index()
        
        # Gráfico de pizza para receita por segmento
        fig = px.pie(
            segmentation,
            values='Receita Total',
            names='usuario_segmento',
            title="Distribuição de Receita por Segmento de Usuário"
        )
        
        fig.update_layout(height=400)
        return fig, segmentation

def main():
    st.title("🍴 Dashboard Executivo iFood")
    st.markdown("### Análise Estratégica do Mercado de Delivery")
    
    # Inicializar dashboard
    dashboard = IFoodDashboard()
    
    # Verificar se existe banco de dados
    try:
        df_pedidos = dashboard.load_data()
    except:
        st.error("⚠️ Base de dados não encontrada. Execute primeiro o script data_generator.py")
        st.code("python data_generator.py")
        return
    
    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de data
    min_date = df_pedidos['data_pedido'].min().date()
    max_date = df_pedidos['data_pedido'].max().date()
    
    date_range = st.sidebar.date_input(
        "Período de Análise",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtro de cidade
    cidades_disponiveis = ['Todas'] + sorted(df_pedidos['cidade'].unique().tolist())
    cidade_selecionada = st.sidebar.selectbox("Cidade", cidades_disponiveis)
    
    # Filtro de categoria
    categorias_disponiveis = ['Todas'] + sorted(df_pedidos['categoria'].unique().tolist())
    categoria_selecionada = st.sidebar.selectbox("Categoria", categorias_disponiveis)
    
    # Aplicar filtros
    df_filtered = df_pedidos.copy()
    
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['data_pedido'].dt.date >= date_range[0]) & 
            (df_filtered['data_pedido'].dt.date <= date_range[1])
        ]
    
    if cidade_selecionada != 'Todas':
        df_filtered = df_filtered[df_filtered['cidade'] == cidade_selecionada]
        
    if categoria_selecionada != 'Todas':
        df_filtered = df_filtered[df_filtered['categoria'] == categoria_selecionada]
    
    # Verificar se há dados após filtros
    if len(df_filtered) == 0:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Tente alterar os filtros.")
        st.stop()
    
    # Atualizar dados do dashboard
    dashboard.df_pedidos = df_filtered
    
    # KPIs
    kpis = dashboard.calculate_kpis()
    
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total de Pedidos",
            value=f"{kpis['total_pedidos']:,}",
        )
        
    with col2:
        st.metric(
            label="💰 Receita Total",
            value=f"R$ {kpis['total_receita']:,.2f}",
        )
        
    with col3:
        st.metric(
            label="🎯 Ticket Médio",
            value=f"R$ {kpis['ticket_medio']:.2f}",
        )
        
    with col4:
        st.metric(
            label="⭐ Rating Médio",
            value=f"{kpis['rating_medio']:.1f}",
        )
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="🚚 Tempo Médio Entrega",
            value=f"{kpis['tempo_medio_entrega']:.0f} min",
        )
        
    with col6:
        st.metric(
            label="❌ Taxa Cancelamento",
            value=f"{kpis['taxa_cancelamento']:.1f}%",
            delta=f"-{kpis['taxa_cancelamento']:.1f}%" if kpis['taxa_cancelamento'] < 10 else None
        )
        
    with col7:
        st.metric(
            label="🏪 Restaurantes Ativos",
            value=f"{kpis['restaurantes_ativos']:,}",
        )
        
    with col8:
        st.metric(
            label="👥 Usuários Ativos",
            value=f"{kpis['usuarios_ativos']:,}",
        )
    
    # Gráficos
    st.markdown("## 📈 Análises Detalhadas")
    
    # Evolução temporal
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_chart = dashboard.create_revenue_chart()
        st.plotly_chart(revenue_chart, use_container_width=True)
    
    with col2:
        category_chart = dashboard.create_category_performance()
        st.plotly_chart(category_chart, use_container_width=True)
    
    # Análise por cidade
    st.markdown("### 🌍 Performance por Cidade")
    city_chart, city_data = dashboard.create_city_analysis()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(city_chart, use_container_width=True)
    
    with col2:
        st.markdown("**Top 5 Cidades por Receita**")
        top_cities = city_data.nlargest(5, 'Receita')[['cidade', 'Receita', 'Pedidos por Restaurante']]
        st.dataframe(top_cities, hide_index=True)
    
    # Segmentação de usuários
    st.markdown("### 👥 Segmentação de Usuários")
    segmentation_chart, segmentation_data = dashboard.create_user_segmentation()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(segmentation_chart, use_container_width=True)
    
    with col2:
        st.markdown("**Métricas por Segmento**")
        st.dataframe(segmentation_data, hide_index=True)
    
    # Insights e Recomendações
    st.markdown("## 💡 Insights Estratégicos")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        st.markdown("""
        **🎯 Oportunidades Identificadas:**
        
        1. **Expansão Geográfica**: Cidades com alta demanda por restaurante
        2. **Categorias Premium**: Foco em categorias com maior ticket médio
        3. **Retenção de Usuários**: Programas de fidelidade para segmento Premium
        4. **Otimização Logística**: Redução do tempo de entrega em 15%
        """)
    
    with insights_col2:
        st.markdown("""
        **📊 Ações Recomendadas:**
        
        1. **Curto Prazo**: Campanhas de reativação para usuários ocasionais
        2. **Médio Prazo**: Investimento em tecnologia de roteamento
        3. **Longo Prazo**: Parcerias estratégicas com restaurantes premium
        4. **Monitoramento**: KPIs de satisfação e eficiência operacional
        """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("📧 **Desenvolvido para demonstrar competências em análise de dados e storytelling**")

if __name__ == "__main__":
    main()
