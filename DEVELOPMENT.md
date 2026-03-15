# Guia de Desenvolvimento

Instruções completas para configurar o ambiente de desenvolvimento local.

## ⚙️ Pré-requisitos

- **Git**: 2.34+
- **Python**: 3.9+
- **pip**: 21.0+
- **make**: 4.3+ (opcional, para usar Makefile)

## 🛠️ Setup Inicial

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/risco-operacional.git
cd risco-operacional
```

### 2. Criar Ambiente Virtual

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
# Dependências base
pip install -r requirements.txt

# Incluindo ferramentas de desenvolvimento
pip install -e ".[dev,jupyter]"
```

Ou via Makefile:
```bash
make install-dev
```

### 4. Verificar Instalação

```bash
python --version  # Python 3.9+
pip list          # Mostrar pacotes instalados
which python      # Confirmar venv ativo
```

## 📁 Estrutura do Projeto

```
risco-operacional/
├── .git/                  # Repositório Git
├── .github/               # Configurações GitHub
├── .gitignore
├── .editorconfig
├── etl/                   # Pipeline ETL
│   ├── extracao.py
│   ├── tratamento.py
│   ├── carga.py
│   └── README.md
├── analise/               # Análises
│   ├── risco_operacional_analysis.py
│   ├── perdas.py
│   └── README.md
├── dados/                 # Dados (ignorado no Git)
├── dw/                    # Data Warehouse SQLite
├── plots/                 # Gráficos gerados
├── logs/                  # Logs da aplicação
├── tests/                 # Testes
├── sql/                   # Scripts SQL
├── config.py              # Conf. centralizadas
├── requirements.txt
├── pyproject.toml
├── Makefile
├── README.md
├── CONTRIBUTING.md
└── DEVELOPMENT.md         # Este arquivo
```

## 🚀 Primeiros Passos

### 1. Explorar Repositório

```bash
# Ver estrutura
tree -L 2 -a

# Ver configurações
cat config.py
cat pyproject.toml
```

### 2. Preparar Dados de Teste

```bash
# Gerar dados sintéticos
python analise/perdas.py --start-month 2024-01-01 --end-month 2025-12-01 > dados/perdas_mensais_por_area.csv

# Ou use dados reais (colocar em dados/)
cp /caminho/dos/dados/*.csv dados/
```

### 3. Executar Pipeline ETL

```bash
# Opção 1: Makefile
make run-etl

# Opção 2: Manualmente
python etl/extracao.py
python etl/tratamento.py
python etl/carga.py

# Verificar resultado
ls -la dw/
ls -la dados/clean/
```

### 4. Executar Análises

```bash
make analyze
# Ou
python analise/risco_operacional_analysis.py

# Ver gráficos
ls -la plots/
```

## 💻 Desenvolvimento

### Editar Código

```bash
# Abrir em seu editor favorito
code .           # VS Code
vim etl/carga.py # Vim
```

### Verificar Qualidade

```bash
# Lint (verificar problemas)
make lint

# Format (formatar automaticamente)
make format

# Type check
mypy .

# Todos os checks
make ci
```

### Rodar Testes

```bash
# Todos os testes
make test

# Teste rápido
make test-quick

# Com cobertura
pytest --cov=. --cov-report=html
```

### Debug

#### Usando breakpoint

```python
# Em algum script
import pdb; pdb.set_trace()

# Ou Python 3.7+
breakpoint()
```

#### Usando logging

```python
import config
logger = config.get_logger(__name__)

logger.debug("Valor de x:", x)
logger.info("Processamento concluído")
logger.error("Erro encontrado", exc_info=True)
```

#### Ver logs da aplicação

```bash
tail -f logs/app.log
```

## 🔄 Git Workflow

### Criar Feature

```bash
# Atualizar main
git checkout main
git pull origin main

# Criar branch da feature
git checkout -b feature/minha-feature

# Fazer commits
git add arquivo_modificado.py
git commit -m "feat: Adiciona função de alert"

# Push
git push origin feature/minha-feature

# Abrir PR no GitHub
```

### Atualizar com Main

```bash
git fetch origin
git rebase origin/main

# Se houver conflitos, resolver e fazer:
git add .
git rebase --continue
```

### Limpar branches locais

```bash
# Ver branches
git branch -a

# Deletar branch local
git branch -d feature/completa

# Deletar branch remota
git push origin --delete feature/completa
```

## 📊 Usando Jupyter Notebook

```bash
# Ativar ambiente
source venv/bin/activate

# Iniciar Jupyter
jupyter notebook

# Ou para lab
jupyter lab
```

Exemplo de notebook:
```python
import config
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(config.DATABASE_URL)
df = pd.read_sql_table('fato_incidentes_operacionais', engine)

display(df.head())
display(df.describe())
```

## 🔐 Variáveis de Ambiente

Criar arquivo `.env` (não commitar):

```bash
# .env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
SOURCE_INCIDENTES=/caminho/local/incidentes.csv
SOURCE_PERDAS=/caminho/local/perdas.csv
```

Carregar:
```python
import os
from dotenv import load_dotenv

load_dotenv()
ambiente = os.getenv("ENVIRONMENT", "development")
```

## 🧹 Limpeza

```bash
# Limpar cache Python
make clean

# Limpar TUDO (incluindo venv)
make clean-all

# Remover arquivos específicos
rm -rf __pycache__ .pytest_cache .mypy_cache
```

## 📚 Documentação

### Gerar Docs (com Sphinx - futuro)

```bash
# Será implementado
# sphinx-quickstart docs/
```

### Atualizar README

```bash
# Editar README.md
# Commitar com mensagem: docs: Atualiza README
```

## ✅ Checklist antes de commitar

- [ ] Código segue PEP 8 (`make lint`)
- [ ] Tipos de dados verificados (`mypy .`)
- [ ] Docstrings presentes
- [ ] Logging adicionado
- [ ] Testes passando (`make test`)
- [ ] Nenhum arquivo grande/sensível commitado
- [ ] Mensagem de commit clara e descritiva

## 🆘 Troubleshooting

### Erro: Module not found

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Verificar Python correto
which python
python -c "import pandas; print(pandas.__version__)"
```

### Erro: Database locked

```bash
# SQLite travado, remover arquivo
rm dw/risk_dw.sqlite
python etl/carga.py
```

### Erro: Permission denied

```bash
# Dar permissão para diretórios
chmod -R 755 dados/ dw/ plots/ logs/
```

### Conflict ao fazer rebase

```bash
# Resolver manualmente os arquivos
# Depois:
git add conflito_resolvido.py
git rebase --continue
```

## 📞 Suporte

- **Issues**: Abra no GitHub
- **Discussions**: Para dúvidas gerais
- **Logs**: Verifique `logs/app.log`
- **Docs**: Consulte READMEs em cada diretório

---

**Última atualização**: 10 de março de 2026
