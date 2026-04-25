# Estrutura Organizada de Treinamentos EY

> ⚠️ **Para recrutadores e visualização externa**, use a versão canônica em `cv/`:
> - 🎓 [`cv/Cursos_e_Certificacoes.md`](../../../cv/Cursos_e_Certificacoes.md) — listagem estruturada por área
> - 📊 [`cv/Cursos_e_Certificacoes.csv`](../../../cv/Cursos_e_Certificacoes.csv) — planilha filtrável
>
> Este diretório (`docs/archive/estruturado/`) preserva os **dados brutos pré-processados** do EY Learning report. É insumo do builder, não material de portfólio.

Este diretório contém os dados de treinamentos do `report.csv` organizados em formatos úteis para atualização de CV e LinkedIn.

## Arquivos Gerados

### 1. `treinamentos_consolidado.csv`
Planilha limpa com apenas as colunas relevantes:
- **categoria**: Agrupamento temático (IA, Compliance, Técnico, etc.)
- **titulo**: Nome do treinamento
- **data_conclusao**: Data no formato YYYY-MM-DD
- **ano**: Ano de conclusão
- **nota**: Nota obtida (se aplicável)
- **tipo**: Tipo de item (ELEARNING, DOCUMENT, etc.)
- **status**: Status de conclusão

**Uso**: Importe no Excel/Google Sheets e filtre por categoria ou ano.

### 2. `resumo_por_categoria.txt`
Agrupamento visual de todos os treinamentos por categoria temática.

**Uso**: Consulta rápida para ver quais treinamentos você tem em cada área.

### 3. `linkedin_highlights.txt`
Lista dos treinamentos mais relevantes dos últimos 3 anos, priorizados por categoria.

**Uso**: Copie e cole na seção "Licenses & Certifications" do LinkedIn ou use como base para o About.

## Como Usar

### Para atualizar o CV:
1. Abra `treinamentos_consolidado.csv` no Excel
2. Filtre por categoria relevante para a vaga
3. Selecione os 5-8 mais importantes
4. Copie os títulos para a seção "Formação Complementar" do CV

### Para atualizar o LinkedIn:
1. Consulte `linkedin_highlights.txt`
2. Priorize as categorias:
   - Governança de IA (destaque atual do mercado)
   - AML & Financial Crime (crítico para compliance)
   - Data Protection & InfoSec (essencial para GRC)
   - Setoriais (demonstra conhecimento do setor)

### Para reprocessar os dados:
```bash
cd docs/archive
python3 process_training_data.py
```

## Categorias Definidas

- **Governança de IA**: AI Now, Copilot, GenAI
- **AML & Financial Crime**: Anticorrupção, Lavagem de Dinheiro, AML
- **Data Protection & InfoSec**: LGPD, Cybersecurity, Data Protection
- **Ética & Independência**: Code of Conduct, Independence Updates
- **Setoriais**: Banking, Insurance, Payments, FSO
- **Consulting & Transformation**: Consulting, Transformation Realized
- **Técnico & Dados**: Excel, Power BI, Data Visualization, RPA
- **Leadership & Soft Skills**: Emotional Intelligence, Coaching, Team Building
- **Compliance Geral**: Segurança no Trabalho, Ergonomia, Jornada
- **Outros**: Demais treinamentos

## Observações

- Badges foram removidos (já estão em `profile.yaml`)
- Apenas treinamentos concluídos são incluídos
- Ordenação por data de conclusão (mais recente primeiro)
- Total de 100+ horas certificadas entre 2022-2026
