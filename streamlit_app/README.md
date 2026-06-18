# 🚗 Sistema de Gestão de Frota

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema completo de gerenciamento de frota desenvolvido com Streamlit**

[Funcionalidades](#-funcionalidades) • [Instalação](#-instalação) • [Uso](#-como-usar) • [Documentação](#-documentação) • [Contribuindo](#-contribuindo)

</div>

---

## 📖 Sobre o Projeto

Sistema web moderno e intuitivo para gestão completa de frotas de veículos, permitindo o controle de veículos, motoristas, viagens e geração de relatórios analíticos com visualizações interativas.

### 🎯 Principais Características

- 🔐 **Autenticação Segura**: Sistema de login com criptografia bcrypt
- 📊 **Dashboard Interativo**: Métricas em tempo real da frota
- 🚙 **Gestão de Veículos**: Cadastro, edição e controle de status
- 👨‍✈️ **Gestão de Motoristas**: Controle completo com validações de CPF e CNH
- 🗺️ **Gestão de Viagens**: Planejamento, acompanhamento e histórico detalhado
- 📈 **Relatórios Avançados**: Gráficos interativos e análises de performance
- 💾 **Exportação de Dados**: Download de relatórios em formato CSV

---

## ✨ Funcionalidades

### 🏠 Página Principal
- Sistema de autenticação seguro
- Gerenciamento de sessão
- Controle de acesso baseado em roles (Admin/User)

### 📊 Dashboard
- **Métricas em Tempo Real:**
  - Total de veículos cadastrados
  - Veículos ativos
  - Total de motoristas
  - Viagens em andamento

### 🚙 Gestão de Veículos
- Listagem completa de veículos
- Cadastro de novos veículos
- **✨ Edição de veículos cadastrados**
- **✨ Exclusão de veículos (com proteção contra viagens vinculadas)**
- Validação de placas únicas
- Controle de status (Ativo, Manutenção, Inativo)
- Informações: Placa, Modelo, Capacidade, Tipo

### 👨‍✈️ Gestão de Motoristas
- Listagem de motoristas cadastrados
- Cadastro com validações robustas
- **✨ Edição de motoristas cadastrados**
- **✨ Exclusão de motoristas (com proteção contra viagens vinculadas)**
- Validação de CPF (11 dígitos)
- Validação de CNH (mínimo 9 dígitos)
- Status: Ativo, Férias, Afastado

### 🗺️ Gestão de Viagens
- **Viagens Ativas:**
  - Visualização de viagens planejadas e em andamento
  - Atualização de status em tempo real
  - Detalhes completos (veículo, motorista, datas, distância)

- **Histórico:**
  - Filtros por status e período
  - Exportação para CSV
  - Visualização tabular completa

- **Nova Viagem:**
  - Seleção de veículo ativo
  - Seleção de motorista ativo
  - Definição de origem e destino
  - Cálculo de distância
  - Agendamento de data/hora

### 📈 Relatórios e Análises
- **Filtros por Período:** Seleção flexível de datas
- **KPIs Dinâmicos:** Métricas calculadas automaticamente
- **Gráficos Interativos (Plotly):**
  - 📊 Distribuição de viagens por status (Pizza)
  - 📊 Análise por veículo (Barras)
  - 📊 Performance por motorista (Barras horizontais)
  - 📈 Tendências temporais (Linhas)
- **Exportação:** Relatórios completos em CSV

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/gestao-frota.git
cd gestao-frota/streamlit_app
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Inicialize o banco de dados**
```bash
python seed.py
```

5. **(Opcional) Adicione dados de exemplo**
```bash
python add_sample_data.py
```

6. **Execute a aplicação**
```bash
streamlit run main.py
```

7. **Acesse no navegador**
```
http://localhost:8501
```

---

## 🔑 Como Usar

### Primeiro Acesso

1. Acesse `http://localhost:8501`
2. Faça login com as credenciais padrão:
   - **Usuário:** `admin`
   - **Senha:** `pmnp@123`
3. Navegue pelo menu lateral para acessar as diferentes funcionalidades

### Fluxo de Trabalho Recomendado

1. **Cadastre Veículos** → Página **🚗 Veículos**
2. **Cadastre Motoristas** → Página **👨‍✈️ Motoristas**
3. **Registre Viagens** → Página **🗺️ Viagens** ➔ Aba "Nova Viagem"
4. **Acompanhe Viagens Ativas** → Página **🗺️ Viagens** ➔ Aba "Viagens Ativas"
5. **Gere Relatórios** → Página **📈 Relatórios**

---

## 📦 Como Gerar Executável (.exe) e Instalador

Você pode compilar o projeto em um executável independente que não exige a instalação manual do Python na máquina de destino.

### Método A: Execução Local Rápida (`iniciar.bat`)
Para usuários locais, basta dar dois cliques no arquivo **`iniciar.bat`**. Ele criará automaticamente o ambiente virtual, instalará as dependências necessárias e iniciará a aplicação.

### Método B: Executável Autônomo (PyInstaller)
Para gerar uma pasta independente com o executável e todas as dependências embutidas:
1. Com o ambiente virtual ativo, certifique-se de que o PyInstaller está instalado:
   ```bash
   pip install pyinstaller
   ```
2. Compile a aplicação usando o script auxiliar [run_app.py](file:///c:/Users/KENIELLY/Desktop/gerenciamento/streamlit_app/run_app.py):
   ```bash
   python -m PyInstaller --name="GestaoDeFrota" --onedir --clean --add-data "pages;pages" --add-data ".streamlit;.streamlit" --add-data "main.py;." --add-data "fleet.db;." --collect-all streamlit run_app.py
   ```
3. O aplicativo autônomo será gerado em `dist/GestaoDeFrota/GestaoDeFrota.exe`.

### Método C: Criar um Instalador Windows (.exe) com Inno Setup
Para distribuir o sistema como um instalador convencional que instala na pasta de programas do usuário, cria atalhos na Área de Trabalho e adiciona opção de desinstalação:
1. Instale o [Inno Setup](https://jrsoftware.org/isdl.php).
2. Abra o arquivo de configuração **[installer_config.iss](file:///c:/Users/KENIELLY/Desktop/gerenciamento/streamlit_app/installer_config.iss)**.
3. No painel superior, clique em **Build** ➔ **Compile** (ou pressione `Ctrl + F9`).
4. O instalador unificado estará pronto em `dist/Instalador_Gestao_Frota.exe`.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal
- **SQLAlchemy**: ORM para gerenciamento do banco de dados
- **SQLite**: Banco de dados relacional leve e portátil
- **bcrypt**: Criptografia de senhas

### Frontend
- **Streamlit**: Framework web para Python
- **Plotly**: Biblioteca de visualização de dados interativa
- **Pandas**: Manipulação e análise de dados

### Outras Bibliotecas
- **watchdog**: Monitoramento de arquivos

---

## 📁 Estrutura do Projeto

```
streamlit_app/
│
├── main.py                 # Página principal com autenticação
├── database.py             # Modelos SQLAlchemy e configuração do BD
├── auth.py                 # Funções de autenticação (hash/verify)
├── seed.py                 # Script para criar usuário admin
├── add_sample_data.py      # Script para dados de exemplo
├── run_app.py              # Script de entrada para empacotamento com PyInstaller
├── iniciar.bat             # Inicializador automático em 1-clique
├── installer_config.iss    # Script de configuração do Inno Setup
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
│
├── pages/                 # Páginas da aplicação
│   ├── 1_📊_Dashboard.py  # Dashboard com métricas
│   ├── 2_🚗_Veículos.py   # Gestão de veículos
│   ├── 3_👨‍✈️_Motoristas.py  # Gestão de motoristas
│   ├── 4_🗺️_Viagens.py     # Gestão de viagens
│   └── 5_📈_Relatórios.py  # Relatórios e análises
│
└── fleet.db               # Banco de dados SQLite (criado após seed.py)
```

---

## 💾 Banco de Dados

### Modelo de Dados

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Vehicle   │         │    Trip     │         │   Driver    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id          │◄────────│ vehicle_id  │────────►│ id          │
│ plate       │         │ driver_id   │         │ name        │
│ model       │         │ origin      │         │ cpf         │
│ capacity    │         │ destination │         │ cnh         │
│ type        │         │ distance_km │         │ phone       │
│ status      │         │ start_date  │         │ status      │
└─────────────┘         │ end_date    │         └─────────────┘
                        │ status      │
                        └─────────────┘
```

### Tabelas

#### **users**
- Gerenciamento de usuários do sistema
- Senhas criptografadas com bcrypt
- Suporte a roles (ADMIN, USER)

#### **vehicles**
- Cadastro completo de veículos
- Status: ATIVO, MANUTENCAO, INATIVO
- Tipos: Carro, Van, Ônibus, Caminhão

#### **drivers**
- Informações dos motoristas
- Validação de CPF e CNH únicos
- Status: ATIVO, FERIAS, AFASTADO

#### **trips**
- Registro de viagens
- Relacionamento com veículos e motoristas
- Status: PLANEJADA, AGENDADA, EM_ANDAMENTO, CONCLUIDA, CANCELADA

---

## 🔒 Segurança

- ✅ Senhas hasheadas com bcrypt (salt rounds)
- ✅ Validação de sessão em todas as páginas protegidas
- ✅ Proteção contra SQL Injection via SQLAlchemy ORM
- ✅ Validação rigorosa de entrada de dados
- ✅ Campos únicos (CPF, CNH, Placa) para evitar duplicatas

---

## 📊 Dados de Exemplo

O script `add_sample_data.py` cria dados realistas para teste:

### 5 Veículos
- Fiat Uno (Carro, 4 passageiros)
- Volkswagen Kombi (Van, 8 passageiros)
- Mercedes-Benz Sprinter (Van, 15 passageiros)
- Iveco Daily (Ônibus, 20 passageiros)
- Ford Cargo (Caminhão, 2 passageiros)

### 5 Motoristas
- João Silva, Maria Santos, Pedro Oliveira, Ana Costa, Carlos Souza
- Com CPF, CNH e telefones válidos

### 7 Viagens
- Rotas variadas (SP, RJ, Campinas, Santos, etc.)
- Diferentes status e períodos
- Distâncias realistas

---

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Dashboard+com+Métricas)

### Gestão de Veículos
![Veículos](https://via.placeholder.com/800x400/2ca02c/ffffff?text=Gestão+de+Veículos)

### Relatórios
![Relatórios](https://via.placeholder.com/800x400/ff7f0e/ffffff?text=Relatórios+Interativos)

---

## 🚧 Roadmap

### Versão 2.0
- [x] ~~Edição e exclusão de registros~~ ✅ **Implementado na v1.1.0**
- [ ] Upload de documentos (CNH, CRLV)
- [ ] Notificações de CNH vencida
- [ ] Controle de manutenções preventivas
- [ ] Gestão de combustível e custos
- [ ] Edição e exclusão de viagens

### Versão 3.0
- [ ] Sistema de permissões granular
- [ ] Logs de auditoria
- [ ] API REST para integrações
- [ ] Aplicativo mobile
- [ ] Notificações por email/SMS

### Melhorias Técnicas
- [ ] Testes automatizados (pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Docker containerization
- [ ] Deploy em cloud (Heroku/AWS)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções de código Python (PEP 8)
- Atualize a documentação quando necessário

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Seu Nome**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- Email: seu.email@example.com

---

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io/) - Framework incrível para aplicações web
- [Plotly](https://plotly.com/) - Visualizações interativas
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso e flexível

---

## 📞 Suporte

Encontrou um bug ou tem uma sugestão? 

- Abra uma [issue](https://github.com/seu-usuario/gestao-frota/issues)
- Entre em contato via email: seu.email@example.com

---

<div align="center">

**Desenvolvido com ❤️ usando Streamlit**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>
