.PHONY: help install setup clean test run-etl analyze all lint format dev docs ci dashboard

help:
	@echo "🚀 Projeto: Monitor de Risco Operacional Bancário"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make setup          - Criar venv e instalar dependências"
	@echo "  make install        - Instalar dependências"
	@echo "  make install-dev    - Instalar dependências de desenvolvimento"
	@echo "  make format         - Formatar código (black, isort)"
	@echo "  make lint           - Verificar qualidade do código (flake8, pylint)"
	@echo "  make test           - Rodar testes"
	@echo "  make run-etl        - Executar pipeline ETL"
	@echo "  make analyze        - Executar análises"
	@echo "  make dashboard      - Iniciar dashboard Streamlit"
	@echo "  make all            - Executar ETL + Análises"
	@echo "  make clean          - Limpar arquivos temporários"
	@echo "  make help           - Mostrar esta mensagem"

# Setup Inicial
setup:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev,jupyter]"

# Limpeza
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .mypy_cache/ .coverage htmlcov/
	rm -rf plots/*.png plots/*.pdf

clean-all: clean
	rm -rf venv/ env/
	rm -rf dw/*.sqlite

# Quality Checks
format:
	@echo "🎨 Formatando código..."
	black .
	isort .
	@echo "✅ Código formatado!"

lint:
	@echo "🔍 Verificando qualidade do código..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	pylint etl/ analise/ || true
	mypy . --ignore-missing-imports || true
	@echo "✅ Verificação concluída!"

# Testing
test:
	@echo "🧪 Rodando testes..."
	pytest tests/ -v --cov=. --cov-report=html
	@echo "✅ Testes concluídos!"

test-quick:
	pytest tests/ -v

# ETL Pipeline
run-etl:
	@echo "📊 Executando pipeline ETL..."
	python etl/extracao.py
	python etl/tratamento.py
	python etl/carga.py
	@echo "✅ Pipeline ETL concluído!"

# Análises
analyze:
	@echo "📈 Executando análises..."
	python analise/risco_operacional_analysis.py
	python analise/perdas.py
	@echo "✅ Análises concluídas!"

# Executar Tudo
all: run-etl analyze
	@echo "🎉 Todas as etapas executadas com sucesso!"

# Desenvolvimento
dev:
	jupyter notebook

docs:
	@echo "📚 Gerando documentação..."
	@echo "Documentação disponível em: docs/"

# Dashboard
dashboard:
	@echo "🌐 Iniciando Dashboard Streamlit..."
	.venv/bin/streamlit run dashboards/streamlit_app.py

# CI/CD simulate
ci: lint test clean
	@echo "✅ CI checks passed!"
