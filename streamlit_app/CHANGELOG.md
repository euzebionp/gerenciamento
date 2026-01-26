# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-01-26

### 🎉 Lançamento Inicial

Primeira versão completa do Sistema de Gestão de Frota com Streamlit.

### ✨ Adicionado

#### Autenticação e Segurança
- Sistema de login com autenticação segura
- Criptografia de senhas com bcrypt
- Gerenciamento de sessão
- Controle de acesso baseado em roles (Admin/User)
- Validação de sessão em todas as páginas protegidas

#### Dashboard
- Página inicial com métricas em tempo real
- KPIs principais:
  - Total de veículos
  - Veículos ativos
  - Total de motoristas
  - Viagens em andamento
- Layout responsivo com 4 colunas

#### Gestão de Veículos
- Listagem completa de veículos cadastrados
- Formulário de cadastro de novos veículos
- Validação de placas únicas
- Campos: Placa, Modelo, Capacidade, Tipo, Status
- Status disponíveis: ATIVO, MANUTENCAO, INATIVO
- Tipos de veículos: Carro, Van, Ônibus, Caminhão

#### Gestão de Motoristas
- Listagem de motoristas cadastrados
- Formulário de cadastro com validações
- Validação de CPF (11 dígitos)
- Validação de CNH (mínimo 9 dígitos)
- Atualização rápida de status
- Status disponíveis: ATIVO, FERIAS, AFASTADO
- Campos únicos: CPF e CNH

#### Gestão de Viagens
- **Viagens Ativas:**
  - Visualização de viagens planejadas e em andamento
  - Atualização de status em tempo real
  - Informações detalhadas (veículo, motorista, datas, distância)
- **Histórico:**
  - Filtros por status
  - Filtros por período (data)
  - Visualização tabular completa
  - Exportação para CSV
- **Nova Viagem:**
  - Seleção de veículo ativo
  - Seleção de motorista ativo
  - Campos: Origem, Destino, Distância, Data/Hora
  - Status: PLANEJADA, AGENDADA, EM_ANDAMENTO, CONCLUIDA, CANCELADA

#### Relatórios e Análises
- Filtro por período customizável
- KPIs dinâmicos do período selecionado
- **Gráficos Interativos (Plotly):**
  - Distribuição de viagens por status (gráfico de pizza)
  - Análise por veículo (gráficos de barras)
  - Performance por motorista com taxa de conclusão
  - Tendências ao longo do tempo (gráficos de linha)
- Exportação de relatórios completos em CSV
- Tabelas detalhadas para cada análise

#### Banco de Dados
- SQLite para portabilidade
- SQLAlchemy ORM
- Modelos: User, Vehicle, Driver, Trip
- Relacionamentos entre entidades
- Timestamps automáticos (created_at, updated_at)
- Validações de unicidade (CPF, CNH, Placa)

#### Scripts Utilitários
- `seed.py`: Inicialização do banco e criação do admin
- `add_sample_data.py`: População com dados de exemplo
- Dados de exemplo: 5 veículos, 5 motoristas, 7 viagens

#### Interface do Usuário
- Design limpo e intuitivo
- Navegação por menu lateral
- Tabs para organização de conteúdo
- Forms para entrada de dados
- Dataframes interativos
- Feedback visual (success, error, info, warning)
- Animações (balloons) para ações bem-sucedidas
- Layout responsivo

#### Documentação
- README.md completo com badges e screenshots
- INSTALL.md com guia detalhado de instalação
- CONTRIBUTING.md com diretrizes para contribuidores
- LICENSE (MIT)
- .gitignore configurado
- Configuração Streamlit (.streamlit/config.toml)

### 🔒 Segurança

- Senhas hasheadas com bcrypt
- Proteção contra SQL Injection via ORM
- Validação rigorosa de entrada de dados
- Campos únicos para evitar duplicatas
- XSRF Protection habilitado

### 📦 Dependências

- streamlit >= 1.31.0
- sqlalchemy >= 2.0.0
- pandas >= 2.0.0
- bcrypt >= 4.0.0
- plotly >= 5.18.0
- watchdog >= 3.0.0

---

## [Unreleased]

### 🚧 Planejado para v2.0

#### Funcionalidades
- [ ] Edição de veículos, motoristas e viagens
- [ ] Exclusão de registros com confirmação
- [ ] Upload de documentos (CNH, CRLV)
- [ ] Notificações de CNH vencida
- [ ] Controle de manutenções preventivas
- [ ] Gestão de combustível e custos
- [ ] Histórico de manutenções por veículo

#### Melhorias de UX
- [ ] Busca e filtros avançados
- [ ] Paginação para grandes volumes de dados
- [ ] Modo escuro (dark mode)
- [ ] Exportação em múltiplos formatos (Excel, PDF)
- [ ] Dashboard customizável

#### Técnicas
- [ ] Testes automatizados (pytest)
- [ ] CI/CD com GitHub Actions
- [ ] Docker containerization
- [ ] Logs de auditoria
- [ ] API REST para integrações
- [ ] Backup automático do banco de dados

---

## Tipos de Mudanças

- `Adicionado` para novas funcionalidades
- `Modificado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas

---

**Legenda de Versões:**
- **Major (X.0.0)**: Mudanças incompatíveis com versões anteriores
- **Minor (0.X.0)**: Novas funcionalidades compatíveis
- **Patch (0.0.X)**: Correções de bugs

[1.0.0]: https://github.com/seu-usuario/gestao-frota/releases/tag/v1.0.0
[Unreleased]: https://github.com/seu-usuario/gestao-frota/compare/v1.0.0...HEAD
