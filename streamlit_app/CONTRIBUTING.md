# Guia de Contribuição

Obrigado por considerar contribuir com o Sistema de Gestão de Frota! 🎉

## 📋 Código de Conduta

Este projeto segue um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e inclusivo.

## 🚀 Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor:

1. Verifique se o bug já não foi reportado nas [Issues](https://github.com/seu-usuario/gestao-frota/issues)
2. Se não encontrar, crie uma nova issue incluindo:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. comportamento atual
   - Screenshots (se aplicável)
   - Informações do ambiente (OS, versão Python, etc.)

### Sugerindo Melhorias

Sugestões são sempre bem-vindas! Para propor uma nova funcionalidade:

1. Abra uma issue com o título começando com `[FEATURE]`
2. Descreva detalhadamente a funcionalidade
3. Explique por que ela seria útil
4. Se possível, sugira uma implementação

### Pull Requests

1. **Fork o repositório**
```bash
git clone https://github.com/seu-usuario/gestao-frota.git
cd gestao-frota
```

2. **Crie uma branch para sua feature**
```bash
git checkout -b feature/minha-feature
```

3. **Faça suas alterações**
   - Escreva código limpo e bem documentado
   - Siga as convenções de código Python (PEP 8)
   - Adicione comentários quando necessário

4. **Teste suas alterações**
```bash
# Execute a aplicação
streamlit run main.py

# Verifique se tudo funciona corretamente
```

5. **Commit suas mudanças**
```bash
git add .
git commit -m "feat: adiciona funcionalidade X"
```

**Convenção de Commits:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Formatação, ponto e vírgula, etc.
- `refactor:` Refatoração de código
- `test:` Adição de testes
- `chore:` Tarefas de manutenção

6. **Push para sua branch**
```bash
git push origin feature/minha-feature
```

7. **Abra um Pull Request**
   - Descreva suas alterações
   - Referencie issues relacionadas
   - Aguarde review

## 🎨 Padrões de Código

### Python

- Siga o [PEP 8](https://pep8.org/)
- Use nomes descritivos para variáveis e funções
- Máximo de 100 caracteres por linha
- Use type hints quando possível

```python
def calcular_distancia(origem: str, destino: str) -> float:
    """
    Calcula a distância entre dois pontos.
    
    Args:
        origem: Cidade de origem
        destino: Cidade de destino
        
    Returns:
        Distância em quilômetros
    """
    # Implementação
    pass
```

### Streamlit

- Mantenha as páginas organizadas e intuitivas
- Use st.cache_data para otimizar performance
- Adicione mensagens de feedback (success, error, info)
- Valide entradas do usuário

### Banco de Dados

- Use SQLAlchemy ORM para queries
- Sempre faça rollback em caso de erro
- Feche conexões após uso
- Use relacionamentos adequados

## 🧪 Testes

Embora ainda não tenhamos testes automatizados, ao contribuir:

1. Teste manualmente todas as funcionalidades afetadas
2. Verifique se não quebrou funcionalidades existentes
3. Teste com dados válidos e inválidos
4. Verifique a responsividade da interface

## 📚 Documentação

- Atualize o README.md se necessário
- Documente novas funcionalidades
- Adicione comentários em código complexo
- Atualize o CHANGELOG.md (se existir)

## 🔍 Checklist do Pull Request

Antes de submeter, verifique:

- [ ] O código segue os padrões do projeto
- [ ] Testei as alterações localmente
- [ ] Adicionei/atualizei documentação
- [ ] Não há conflitos com a branch main
- [ ] O commit message segue as convenções
- [ ] Não há arquivos desnecessários (logs, cache, etc.)

## 💡 Dicas

- Comece com issues marcadas como `good first issue`
- Não hesite em pedir ajuda nos comentários
- Mantenha PRs pequenos e focados
- Seja paciente durante o review

## 📞 Dúvidas?

Se tiver dúvidas sobre como contribuir:

- Abra uma issue com a tag `question`
- Entre em contato via email: seu.email@example.com

---

**Obrigado por contribuir! 🙌**
