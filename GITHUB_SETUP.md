# 🚀 COMO FAZER UPLOAD PARA O GITHUB

## 📋 Passo a Passo Completo

### 1. **Crie uma conta no GitHub** (se não tiver)
- Acesse: https://github.com
- Clique em "Sign up"
- Use um username profissional

### 2. **Crie um novo repositório**
- Clique no botão "+" no canto superior direito
- Selecione "New repository"
- **Nome do repositório:** `ifood-analytics-dashboard`
- **Descrição:** `📊 Dashboard executivo para análise do mercado de delivery com Python, SQL, Streamlit e storytelling baseado em dados`
- ✅ Marque como **Public** (para portfólio)
- ❌ **NÃO** inicialize com README (já temos um)
- Clique em "Create repository"

### 3. **Configure o Git no seu computador**

#### Opção A: Use o script automático
```bash
# Execute o script que criei para você
git_setup.bat
```

#### Opção B: Manual
```bash
# Navegue até a pasta do projeto
cd "c:\Users\kayan\OneDrive\Documents\projeto_ifood"

# Configure seu nome e email (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"

# Inicialize o repositório
git init

# Adicione todos os arquivos
git add .

# Faça o commit inicial
git commit -m "🍴 Projeto completo: Dashboard Executivo iFood Analytics"
```

### 4. **Conecte ao GitHub e faça upload**
```bash
# Conecte ao repositório remoto (substitua SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/ifood-analytics-dashboard.git

# Defina a branch principal
git branch -M main

# Faça o upload
git push -u origin main
```

### 5. **Configure o repositório no GitHub**

#### 5.1 Adicione Topics (Tags)
- Vá para seu repositório no GitHub
- Clique na engrenagem ⚙️ ao lado de "About"
- Adicione os topics:
  ```
  python, streamlit, plotly, sql, data-analysis, 
  dashboard, business-intelligence, ifood, 
  food-tech, portfolio, data-visualization
  ```

#### 5.2 Configure a URL do Website
- Na seção "About", adicione:
- **Website:** Link do Streamlit Cloud (quando fizer deploy)
- **Description:** `📊 Dashboard executivo para análise do mercado de delivery com Python, SQL, Streamlit e storytelling baseado em dados`

### 6. **Deploy no Streamlit Cloud (Opcional)**

#### 6.1 Acesse o Streamlit Cloud
- Vá para: https://share.streamlit.io/
- Faça login com sua conta do GitHub

#### 6.2 Conecte seu repositório
- Clique em "New app"
- Selecione seu repositório: `ifood-analytics-dashboard`
- **Main file path:** `dashboard.py`
- Clique em "Deploy!"

#### 6.3 Atualize o README
Após o deploy, atualize o link no README:
```markdown
### 🌐 Demo Online
🔗 **Dashboard**: https://[seu-app].streamlit.app/
```

## 🎯 **RESULTADO FINAL**

Seu portfólio no GitHub terá:

### ✅ **Repositório Profissional**
- README atrativo com badges
- Código bem documentado
- Estrutura organizada
- Licença MIT

### ✅ **Demo Online**
- Dashboard funcionando 24/7
- Link direto para recrutadores
- Experiência completa

### ✅ **Visibilidade**
- Tags relevantes para descoberta
- Descrição otimizada
- Projeto em destaque

## 📱 **PARA COMPARTILHAR**

### No LinkedIn:
```
🍴 Novo projeto no meu portfólio! 

Criei um dashboard executivo completo para análise do mercado de delivery, demonstrando habilidades em:

📊 Análise de dados com Python/SQL
🎨 Visualização interativa 
💡 Storytelling baseado em dados
🎯 Pensamento estratégico

Link: https://github.com/[SEU-USUARIO]/ifood-analytics-dashboard

#DataAnalytics #Python #SQL #Dashboard #FoodTech
```

### No currículo:
```
📊 Dashboard Executivo iFood Analytics
Tecnologias: Python, SQL, Streamlit, Plotly
Link: https://github.com/[SEU-USUARIO]/ifood-analytics-dashboard
```

## 🚀 **DICAS FINAIS**

1. **Pin o repositório** no seu perfil GitHub
2. **Adicione screenshots** na descrição do repositório
3. **Mantenha commits organizados** com mensagens claras
4. **Documente melhorias** em releases
5. **Responda issues** se houver

**Agora seu projeto está pronto para impressionar recrutadores! 🎯**
