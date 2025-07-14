@echo off
echo 🚀 Preparando projeto para upload no GitHub...

REM Inicializar repositório Git
echo Inicializando repositório Git...
git init

REM Adicionar arquivos ao staging
echo Adicionando arquivos...
git add .

REM Fazer commit inicial
echo Fazendo commit inicial...
git commit -m "🍴 Projeto completo: Dashboard Executivo iFood Analytics

✨ Características principais:
- 📊 Dashboard interativo com Streamlit
- 🔍 Análises SQL avançadas (CTEs, Window Functions)
- 📈 Relatórios executivos em Excel
- 💡 Insights estratégicos e recomendações
- 🎯 20.000+ registros de dados sintéticos
- 📋 Documentação completa

🎯 Demonstra habilidades em:
- Análise de dados e SQL
- Storytelling e visualização
- Pensamento estratégico
- Organização e documentação
- Python e bibliotecas de dados

🚀 Projeto pronto para apresentação em entrevistas!"

echo.
echo ✅ Repositório Git inicializado!
echo.
echo 📋 Próximos passos:
echo 1. Crie um repositório no GitHub com o nome: ifood-analytics-dashboard
echo 2. Execute os comandos abaixo:
echo.
echo git remote add origin https://github.com/[SEU-USUARIO]/ifood-analytics-dashboard.git
echo git branch -M main
echo git push -u origin main
echo.
echo 🌟 Substitua [SEU-USUARIO] pelo seu username do GitHub
echo.
pause
