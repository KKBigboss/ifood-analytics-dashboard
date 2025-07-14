# 🚀 Guia de Execução - Projeto iFood Analytics

## 📋 Pré-requisitos
- Python 3.8 ou superior
- Git (opcional, para versionamento)

## 🛠️ Configuração do Ambiente

### Opção 1: Instalação Automática (Recomendada)
```powershell
# Navegue até o diretório do projeto
cd "c:\Users\kayan\OneDrive\Documents\projeto_ifood"

# Execute o configurador automático
python check_dependencies.py
```

### Opção 2: Instalação Manual
```powershell
# Navegue até o diretório do projeto
cd "c:\Users\kayan\OneDrive\Documents\projeto_ifood"

# Instale as dependências uma por uma
pip install pandas
pip install numpy
pip install plotly
pip install streamlit
pip install openpyxl
pip install faker
```

### Opção 3: Script Batch (Windows)
```powershell
# Execute o script de setup
setup.bat
```

### Opção 4: Ambiente Virtual
```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements_basic.txt
```

### 2. Gerar Base de Dados
```powershell
# Execute o gerador de dados (primeira vez)
python data_generator.py
```

### 3. Executar Dashboard
```powershell
# Inicie o dashboard interativo
streamlit run dashboard.py
```

### 4. Gerar Relatórios
```powershell
# Gere relatórios Excel e insights
python generate_reports.py
```

## 📁 Estrutura do Projeto
```
projeto_ifood/
├── README.md                      # Documentação principal
├── requirements.txt               # Dependências Python
├── data_generator.py             # Gerador de dados sintéticos
├── dashboard.py                  # Dashboard interativo
├── generate_reports.py           # Gerador de relatórios
├── sql_queries.sql              # Consultas SQL avançadas
├── INSTRUÇÕES.md                # Este arquivo
├── ifood_data.db                # Base de dados (gerada automaticamente)
├── Relatorio_Executivo_iFood.xlsx    # Relatório Excel (gerado)
└── Insights_Estrategicos_iFood.md    # Insights (gerado)
```

## 🎯 Como Demonstrar o Projeto

### 1. Para Recrutadores Técnicos
- **Mostre o código:** Destaque a qualidade do código Python e SQL
- **Explique a arquitetura:** Base de dados, processamento, visualização
- **Execute queries SQL:** Demonstre conhecimento avançado em SQL

### 2. Para Stakeholders de Negócio
- **Dashboard interativo:** Navegue pelos KPIs e filtros
- **Relatório Excel:** Apresente análises estruturadas
- **Storytelling:** Use os insights para contar uma história

### 3. Para Equipe Técnica
- **Metodologia:** Explique a abordagem de análise de dados
- **Escalabilidade:** Mostre como o projeto pode crescer
- **Melhores práticas:** Código limpo, documentação, estrutura

## 📊 Principais Demonstrações

### 1. Análise SQL Avançada
- Consultas complexas com JOINs e CTEs
- Análise de cohort e retenção
- Cálculos de KPIs de negócio

### 2. Visualização de Dados
- Dashboard responsivo e interativo
- Gráficos relevantes para tomada de decisão
- Filtros dinâmicos por período, cidade, categoria

### 3. Storytelling com Dados
- Insights acionáveis para o negócio
- Recomendações estratégicas
- Apresentação clara de resultados

## 🎤 Roteiro de Apresentação (15 minutos)

### Introdução (2 min)
- "Criei um sistema completo de análise para o mercado de delivery"
- "Demonstra habilidades em SQL, Python, storytelling e pensamento estratégico"

### Demonstração Técnica (8 min)
1. **SQL (2 min):** Mostre queries complexas no arquivo sql_queries.sql
2. **Dashboard (3 min):** Navegue pelo Streamlit, explique KPIs
3. **Relatórios (2 min):** Abra o Excel, mostre análises estruturadas
4. **Código (1 min):** Destaque qualidade e organização do código

### Insights de Negócio (4 min)
- Apresente 3-4 insights principais do arquivo de insights
- Explique como cada insight se conecta com estratégia do iFood
- Demonstre pensamento crítico e propostas de solução

### Conclusão (1 min)
- "Este projeto demonstra minha capacidade de transformar dados em valor"
- "Estou pronto para contribuir com a estratégia data-driven do iFood"

## 🔧 Troubleshooting

### Erro: "CREATE_VENV.PIP_FAILED_INSTALL_REQUIREMENTS"
**Causa:** Problema no arquivo requirements.txt (sqlite3 não é instalável via pip)
**Solução:**
```powershell
# Use o arquivo requirements básico
pip install -r requirements_basic.txt

# OU execute o configurador automático
python check_dependencies.py
```

### Erro: "Base de dados não encontrada"
```powershell
python data_generator.py
```

### Erro: "Módulo não encontrado"
```powershell
# Instale o módulo específico
pip install [nome-do-modulo]

# OU execute instalação completa
python check_dependencies.py
```

### Dashboard não carrega
```powershell
# Verifique se o Streamlit está instalado
pip install streamlit

# Teste se funciona
streamlit --version

# Execute novamente
streamlit run dashboard.py
```

### Problemas com Excel
- Certifique-se de ter o openpyxl: `pip install openpyxl`
- Feche arquivos Excel abertos antes de gerar relatórios

### Erro de Permissões
- Execute o PowerShell como Administrador
- OU use `pip install --user [pacote]`

### Versões Incompatíveis
```powershell
# Use versões básicas sem especificação
pip install pandas numpy plotly streamlit openpyxl faker --upgrade
```

## 📈 Próximos Passos (Para Impressionar)

### Melhorias Sugeridas
1. **Machine Learning:** Adicionar modelos de previsão de demanda
2. **API:** Criar endpoints REST para integração
3. **Real-time:** Dashboard com dados em tempo real
4. **Mobile:** Versão responsiva para dispositivos móveis

### Expansões Possíveis
1. **A/B Testing:** Framework para experimentos
2. **Geolocalização:** Análise espacial avançada
3. **NLP:** Análise de sentimento em reviews
4. **Integração:** Conectar com APIs reais do iFood

## 📞 Contato
Desenvolvido por [Seu Nome] - Candidato para posição no iFood
Email: [seu.email@example.com]
LinkedIn: [seu-linkedin]
