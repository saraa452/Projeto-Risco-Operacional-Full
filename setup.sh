#!/bin/bash
# Script de Setup do Projeto - Risco Operacional

echo "🚀 Configurando Projeto de Análise de Risco Operacional"
echo "======================================================"
echo ""

# 1. Criar ambiente virtual
echo "1️⃣  Criando ambiente virtual..."
python3 -m venv .venv

# 2. Ativar e instalar dependências
echo "2️⃣  Instalando dependências..."
.venv/bin/pip install -q -r requirements.txt

# 3. Gerar dados de teste (se não existirem)
if [ ! -f "dados/incidentes_operacionais.csv" ]; then
    echo "3️⃣  Gerando dados sintéticos de teste..."
    .venv/bin/python gerar_dados_teste.py
else
    echo "✓ Dados já existem (pulando geração)"
fi

# 4. Executar pipeline ETL
echo "4️⃣  Executando pipeline ETL..."
.venv/bin/python etl/extracao.py && \
.venv/bin/python etl/tratamento.py && \
.venv/bin/python etl/carga.py

if [ $? -eq 0 ]; then
    echo ""
    echo "5️⃣  Executando análises..."
    .venv/bin/python analise/risco_operacional_analysis.py
else
    echo "❌ Falha no ETL. Abortando."
    exit 1
fi

echo ""
echo "======================================================"
echo "✅ Setup Concluído com Sucesso!"
echo "======================================================"
echo ""
echo "📊 Arquivos Gerados:"
echo "  • Data Warehouse: dw/risk_dw.sqlite"
echo "  • Dados Limpos: dados/clean/incidentes_operacionais_clean.csv"
echo "  • Gráficos: plots/*.png"
echo "  • Logs: logs/app.log"
echo ""
echo "🚀 Próximos Passos:"
echo "  • Ativar ambiente: source .venv/bin/activate"
echo "  • Rodar análises: python analise/risco_operacional_analysis.py"
echo "  • Ver logs: tail -f logs/app.log"
echo "  • Usar Jupyter: jupyter notebook"
echo ""
echo "📚 Documentação:"
echo "  • README.md - Overview do projeto"
echo "  • DEVELOPMENT.md - Guia de desenvolvimento"
echo "  • CONTRIBUTING.md - Como contribuir"
echo "  • etl/README.md - Documentação do ETL"
echo "  • analise/README.md - Documentação de análises"
