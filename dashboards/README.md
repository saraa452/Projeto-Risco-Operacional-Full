# 📊 Dashboard de Risco Operacional - Streamlit

Interface interativa e profissional para visualização de análises de riscos operacionais bancários.

## 🚀 Inicio Rápido

### Pré-requisitos
- ✅ Pipeline ETL já executado (`make run-etl`)
- ✅ Dependências instaladas (`pip install -r requirements.txt`)
- ✅ Data Warehouse SQLite disponível (`dw/risk_dw.sqlite`)

### Executar Dashboard

```bash
# Ativar ambiente virtual (se necessário)
source .venv/bin/activate

# Iniciar dashboard
streamlit run dashboards/streamlit_app.py
```

A aplicação abrirá em [http://localhost:8501](http://localhost:8501)

## 📋 Funcionalidades

### 1. **KPIs Principais** 📈
- Total de incidentes
- Perdas totais (R$)
- Quantidade de incidentes críticos
- MTTR (Mean Time To Restore) médio
- Comparação entre altos e críticos

### 2. **Gráficos Interativos** 📊

#### Análise de Tendências
- **Perdas por Mês**: Série temporal com cores gradientes
- **Distribuição de Severidade**: Pizza chart com cores por nível

#### Ranking de Riscos
- **Top Áreas por Perda**: Horizontal bar chart dinâmico (5-20 áreas)
- **Top Sistemas por Impacto**: Horizontal bar chart dinâmico (5-20 sistemas)

#### Análises Adicionais
- **Incidentes por Área**: Contagem de eventos
- **Timeline Diária**: Evolução temporal de incidentes
- **Duração vs Impacto**: Scatter plot com análise de correlação

### 3. **Filtros Avançados** 🔧

Na barra lateral esquerda:
- 📅 **Período**: Intervalo de datas customizável
- 🏢 **Áreas**: Selecionar múltiplas áreas
- 🚨 **Severidade**: Filtrar por nível (Baixa, Média, Alta, Crítica)
- 💻 **Sistemas**: Escolher quais sistemas incluir

Todos os gráficos atualizam em tempo real ao alterar filtros!

### 4. **Tabela de Detalhes** 📋

- Busca por texto (área ou sistema)
- Customizável (10-100 linhas)
- Ordenação por data (mais recentes primeiro)
- Formatação de valores monetários
- Exibição de status e duração

## 🎨 Design e UX

- **Layout Responsivo**: Adapta-se a qualquer tamanho de tela
- **Temas**: Utiliza padrão de cores profissional
- **Interatividade**: Todos os gráficos são interativos (zoom, pan, hover info)
- **Performance**: Cache automático de dados (TTL: 1 hora)
- **Metadados**: Exibição de período selecionado e quantidade de registros

## ⚙️ Configuração Avançada

### Variáveis de Ambiente

Criar arquivo `.env` para customizar:

```bash
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
DATABASE_URL=sqlite:///dw/risk_dw.sqlite
```

### Cache

O dashboard implementa cache automático:
- `@st.cache_resource`: Conexão com banco (não expira)
- `@st.cache_data`: Dados tabelados (TTL: 1 hora)

Para limpar cache manualmente:
```bash
rm -rf ~/.streamlit/cache
```

### Customization

Editar cores em `plot_severity_distribution()`:
```python
colors = {
    "Baixa": "#2ecc71",     # Verde
    "Média": "#f39c12",     # Laranja
    "Alta": "#e74c3c",      # Vermelho
    "Crítica": "#c0392b"    # Vermelho escuro
}
```

## 📊 Dados Exibidos

### Métricas Calculadas
- Soma de perdas por período
- Contagem de incidentes por severidade
- MTTR (duração média em minutos)
- Máximo e mínimo de impactos

### Fonte
Todos os dados vêm da tabela `fato_incidentes_operacionais` do SQLite.

Dimensões relacionadas:
- `dim_area` - Código e nome das áreas
- `dim_system` - Código e nome dos sistemas
- `dim_date` - Informações de data (ano, mês, dia, quarter, week)

## 🔍 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução**: Instalar dependências
```bash
pip install -r requirements.txt
```

### Erro: "Arquivo de banco de dados não encontrado"

**Solução**: Executar pipeline ETL primeiro
```bash
make run-etl
```

### Dashboard muito lento

**Solução**: Reduzir período de filtro ou limpar cache
```bash
streamlit cache clear
```

### Gráficos não carregam

**Solução**: Verificar conexão com banco de dados
```bash
sqlite3 dw/risk_dw.sqlite ".tables"
```

## 🚀 Deploy em Produção

### Streamlit Cloud (Gratuito)

1. Fazer fork do repositório no GitHub
2. Ir para [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conectar repositório
4. Configurar variáveis de ambiente
5. Deploy automático

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "dashboards/streamlit_app.py"]
```

```bash
docker build -t dashboard-risco .
docker run -p 8501:8501 dashboard-risco
```

## 📈 Próximas Melhorias

- [ ] Exportar dados para Excel/PDF
- [ ] Configurar alertas automáticos
- [ ] Integração com APIs externas
- [ ] Autenticação de usuários
- [ ] histórico de alterações
- [ ] Comparação período-a-período
- [ ] Previsões com ML

## 📚 Recursos Úteis

- [Documentação Streamlit](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas API](https://pandas.pydata.org/docs/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)

## 🤝 Suporte

Para dúvidas ou sugestões:
- 📧 Abra uma [issue](../../issues)
- 💬 Use [Discussions](../../discussions)
- 📖 Consulte [README.md](../README.md)

---

**Versão**: 1.0  
**Última atualização**: 10 de março de 2026  
**Status**: ✅ Pronto para produção
