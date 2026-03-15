# Contribuindo para o Projeto

Obrigado pelo interesse em contribuir! Este documento fornece diretrizes para colaborar com o projeto de Análise de Risco Operacional.

## 📋 Código de Conduta

- Seja respeitoso e inclusivo
- Critique a ideia, não a pessoa
- Aceite críticas construtivas
- Foque em contribuições de qualidade

## 🚀 Como Contribuir

### 1. Reportar Bugs

Abra uma issue descrevendo:

- **Título descritivo**: "ETL falha ao processar arquivos com encoding UTF-8"
- **Passo-a-passo para reproduzir**
- **Comportamento esperado vs observado**
- **Ambiente**: Sistema operacional, Python versão, etc.
- **Logs**: Cole saída relevante de `logs/app.log`

Exemplo:
```
Título: Script extracao.py falha quando arquivo não existe

Passos:
1. Criar arquivo vazio incidentes_operacionais.csv
2. Executar: python etl/extracao.py
3. Observar erro

Erro esperado: Mensagem clara sobre arquivo não encontrado
Erro obtido: FileNotFoundError com caminho incompleto

Sistema: Linux Ubuntu 22.04, Python 3.9.13
```

### 2. Sugerir Melhorias

- Descreva o problema que a melhoria resolve
- Explique como a solução deveria funcionar
- Aponte exemplos/referências se possível

### 3. Implementar Features

1. **Abra uma issue** primeiro para discussão
2. **Faça fork** do repositório
3. **Crie uma branch**: `git checkout -b feature/minha-feature`
4. **Implemente** seguindo padrões do projeto
5. **Commit com mensagens claras**: `git commit -m "Add: Novo módulo de alertas"`
6. **Push da branch**: `git push origin feature/minha-feature`
7. **Abra um Pull Request**

## 💻 Padrões de Código

### Python Style Guide

Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/) com algumas customizações:

```python
# ✅ Bom
def calcular_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula KPIs do mês mais recente.
    
    Args:
        df: DataFrame com dados de incidentes
    
    Returns:
        Dicionário com KPIs calculados
    """
    logger.info("Calculando KPIs...")
    return {}

# ❌ Ruim
def calckpis(df):
    x = df.groupby('area').sum()
    return x
```

### Docstrings

Usar Google-style docstrings:

```python
def exemplo_funcao(param1: str, param2: int) -> bool:
    """
    Descrição breve em uma linha.
    
    Descrição longa se necessário, explicando o propósito,
    comportamento e qualquer detalhe importante.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando param1 é vazio
        TypeError: Quando param2 não é inteiro
    
    Example:
        >>> resultado = exemplo_funcao("test", 42)
        >>> resultado
        True
    """
    pass
```

### Type Hints

Sempre usar type hints:

```python
from typing import Optional, List, Dict

def processar_dados(
    arquivo: Path,
    filtro_area: Optional[str] = None
) -> List[Dict[str, any]]:
    """..."""
    pass
```

### Logging

```python
import config

logger = config.get_logger(__name__)

logger.info("Mensagem informativa")
logger.warning("Aviso importante")
logger.error("Erro crítico")
```

### Commits

Use mensagens convencionais:

- `feat: Adiciona novo módulo de alertas`
- `fix: Corrige bug no cálculo de KPI`
- `docs: Atualiza README com exemplos`
- `test: Adiciona testes para tratamento.py`
- `refactor: Melhora estrutura de config.py`
- `chore: Atualiza dependências`

## 🧪 Testando Seu Código

### Executar Testes

```bash
make test
```

### Verificar Qualidade

```bash
make lint
make format
```

### Antes de Submeter PR

```bash
make clean
make lint
make test
```

## 📝 Pull Requests

### Template e Checklist

```markdown
## Description
[Descrição do que foi implementado]

## Tipo de Mudança
- [ ] Bug fix (não quebra funcionalidades)
- [ ] Nova feature (não quebra funcionalidades)
- [ ] Breaking change (pode quebrar funcionalidades)

## Como foi testado?
[Descrever testes executados]

## Checklist
- [ ] Meu código segue os padrões do projeto
- [ ] Adicionei docstrings
- [ ] Adicionei type hints
- [ ] Executei `make lint` com sucesso
- [ ] Adicionei testes (se aplicável)
- [ ] Atualizei documentação
- [ ] Não há conflitos com main/develop

## Related Issues
Closes #123
```

## 🗂️ Estrutura de Diretórios

```
.
├── etl/             # Pipeline de extração/transformação
├── analise/         # Scripts de análise
├── sql/             # Queriescontribuição
├── tests/           # Testes unitários/integração
├── config.py        # Configurações centralizadas
└── README.md        # Documentação
```

## 📚 Recursos Úteis

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 🤝 Processo de Review

1. **Automated Checks**: CI/CD valida código
2. **Code Review**: Usuários e maintainers reviewam
3. **Approval**: Aprovação de pelo menos 1 revisor
4. **Merge**: Branch é mergeada para main

## 📮 Contatar Maintainers

- Issues: Use a aba "Issues" do GitHub
- Discussions: Use "Discussions" para perguntas
- Email: [email para contato se houver]

## 🎉 Agradecimentos

Obrigado por ajudar a tornar este projeto melhor!

---

**Última atualização**: 10 de março de 2026
