@echo off
echo 🚀 Configurando ambiente para projeto iFood Analytics...

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências básicas primeiro
echo Instalando dependências básicas...
pip install pandas numpy plotly streamlit openpyxl faker

REM Se falhar, tentar uma por uma
if %errorlevel% neq 0 (
    echo Instalação falhou, tentando uma por uma...
    pip install pandas
    pip install numpy
    pip install plotly
    pip install streamlit
    pip install openpyxl
    pip install faker
)

echo ✅ Ambiente configurado!
echo.
echo Para usar o projeto:
echo 1. Execute: call venv\Scripts\activate.bat
echo 2. Execute: python data_generator.py
echo 3. Execute: streamlit run dashboard.py
echo.
pause
