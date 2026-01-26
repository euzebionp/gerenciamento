# ⚡ Guia Rápido de Início

Comece a usar o Sistema de Gestão de Frota em menos de 5 minutos!

## 🚀 Instalação Express

```bash
# Clone e entre no diretório
git clone https://github.com/seu-usuario/gestao-frota.git
cd gestao-frota/streamlit_app

# Instale e configure
pip install -r requirements.txt
python seed.py
python add_sample_data.py

# Execute
streamlit run main.py
```

## 🔐 Primeiro Acesso

1. Abra seu navegador em: **http://localhost:8501**
2. Faça login:
   - **Usuário:** `admin`
   - **Senha:** `pmnp@123`

## 📱 Navegação Rápida

### 📊 Dashboard
**Menu:** Dashboard
- Veja métricas em tempo real da sua frota

### 🚙 Cadastrar Veículo
**Menu:** Veículos → Aba "Adicionar Novo"
1. Preencha: Placa, Modelo, Capacidade, Tipo
2. Selecione o Status
3. Clique em "Salvar Veículo"

### 👨‍✈️ Cadastrar Motorista
**Menu:** Motoristas → Aba "Adicionar Novo"
1. Preencha: Nome, CPF (11 dígitos), CNH, Telefone
2. Selecione o Status
3. Clique em "Salvar Motorista"

### 🗺️ Registrar Viagem
**Menu:** Viagens → Aba "Nova Viagem"
1. Preencha: Origem, Destino, Distância
2. Selecione: Veículo e Motorista
3. Defina: Data e Hora de Início
4. Clique em "Registrar Viagem"

### 📈 Ver Relatórios
**Menu:** Relatórios
1. Selecione o período desejado
2. Explore os gráficos interativos
3. Baixe relatórios em CSV

## 💡 Dicas Rápidas

### ✅ Validações Importantes
- **CPF:** Deve ter exatamente 11 dígitos
- **CNH:** Mínimo de 9 dígitos
- **Placa:** Formato AAA-0000 (único)

### 🔄 Atualizar Status
- **Motoristas:** Use a seção "Editar Status" na aba "Lista de Motoristas"
- **Viagens:** Atualize na aba "Viagens Ativas"

### 📥 Exportar Dados
- **Viagens:** Aba "Histórico" → Botão "Exportar para CSV"
- **Relatórios:** Página "Relatórios" → Botão "Baixar Relatório Completo"

## 🎯 Fluxo de Trabalho Recomendado

```
1. Cadastre Veículos
   ↓
2. Cadastre Motoristas
   ↓
3. Registre Viagens
   ↓
4. Acompanhe no Dashboard
   ↓
5. Gere Relatórios
```

## 🆘 Problemas Comuns

### Não consigo fazer login
- Verifique se executou `python seed.py`
- Use as credenciais: admin / pmnp@123

### Erro ao cadastrar motorista
- CPF deve ter 11 dígitos (apenas números)
- CNH deve ter no mínimo 9 dígitos
- CPF e CNH devem ser únicos

### Não vejo veículos/motoristas na lista
- Execute `python add_sample_data.py` para dados de exemplo
- Ou cadastre manualmente

### Aplicação não abre
- Verifique se a porta 8501 está livre
- Tente: `streamlit run main.py --server.port 8502`

## 📚 Próximos Passos

- 📖 Leia o [README completo](README.md)
- 🔧 Veja o [Guia de Instalação](INSTALL.md)
- 🤝 Contribua seguindo o [Guia de Contribuição](CONTRIBUTING.md)
- 📝 Acompanhe mudanças no [Changelog](CHANGELOG.md)

## 🎉 Pronto!

Você está pronto para gerenciar sua frota! 

**Dúvidas?** Abra uma [issue](https://github.com/seu-usuario/gestao-frota/issues)

---

**Desenvolvido com ❤️ usando Streamlit**
