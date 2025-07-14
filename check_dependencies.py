"""
Script para verificar e instalar dependências automaticamente
"""
import subprocess
import sys
import importlib

def install_package(package):
    """Instala um pacote usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_packages():
    """Verifica se os pacotes estão instalados e instala se necessário"""
    packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'plotly': 'plotly',
        'streamlit': 'streamlit',
        'openpyxl': 'openpyxl',
        'faker': 'faker'
    }
    
    missing_packages = []
    
    print("🔍 Verificando dependências...")
    
    for import_name, pip_name in packages.items():
        try:
            importlib.import_module(import_name)
            print(f"✅ {import_name} já instalado")
        except ImportError:
            print(f"❌ {import_name} não encontrado")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n📦 Instalando {len(missing_packages)} pacotes faltantes...")
        
        for package in missing_packages:
            print(f"Instalando {package}...")
            if install_package(package):
                print(f"✅ {package} instalado com sucesso")
            else:
                print(f"❌ Falha ao instalar {package}")
    else:
        print("\n🎉 Todas as dependências estão instaladas!")
    
    return len(missing_packages) == 0

def test_imports():
    """Testa se todas as importações funcionam"""
    print("\n🧪 Testando importações...")
    
    try:
        import pandas as pd
        print("✅ pandas OK")
        
        import numpy as np
        print("✅ numpy OK")
        
        import plotly.express as px
        print("✅ plotly OK")
        
        import streamlit as st
        print("✅ streamlit OK")
        
        import openpyxl
        print("✅ openpyxl OK")
        
        from faker import Faker
        print("✅ faker OK")
        
        import sqlite3
        print("✅ sqlite3 OK (built-in)")
        
        print("\n🎉 Todos os módulos funcionando corretamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Configurador automático - Projeto iFood Analytics")
    print("=" * 50)
    
    # Verificar e instalar pacotes
    dependencies_ok = check_and_install_packages()
    
    # Testar importações
    imports_ok = test_imports()
    
    if dependencies_ok and imports_ok:
        print("\n✅ Ambiente configurado com sucesso!")
        print("\nPróximos passos:")
        print("1. Execute: python data_generator.py")
        print("2. Execute: streamlit run dashboard.py")
        print("3. Execute: python generate_reports.py")
    else:
        print("\n❌ Alguns problemas foram encontrados.")
        print("Tente instalar manualmente com:")
        print("pip install pandas numpy plotly streamlit openpyxl faker")
    
    input("\nPressione Enter para continuar...")
