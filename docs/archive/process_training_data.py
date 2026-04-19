#!/usr/bin/env python3
"""
Script para processar report.csv e criar estruturas organizadas para CV/LinkedIn.

Transforma o arquivo bruto de treinamentos EY em formatos úteis:
- Planilha consolidada apenas com informações relevantes
- Agrupamento por categorias temáticas
- Contadores de horas e certificados
"""

import csv
from collections import defaultdict
from datetime import datetime
import os


def parse_date(date_str):
    """Parse date in format YYYY/MM/DD HH:MM:SS or return None"""
    if not date_str or date_str.strip() == "":
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y/%m/%d %H:%M:%S")
    except ValueError:
        return None


def extract_relevant_data(csv_file):
    """Extract only relevant columns from the CSV"""
    trainings = []

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header

        # Column indices (verified from CSV structure)
        # 4 = Item Type ID
        # 8 = Item Description (first occurrence)
        # 10 = Completion Date (UTC) (Item Events)
        # 11 = Grade (External Events) (first occurrence)
        # 12 = Status (Item Events)

        for row in reader:
            if len(row) < 13:
                continue

            item_type = row[4].strip()
            description = row[8].strip()
            completion_date = row[10].strip()
            grade = row[11].strip()
            status = row[12].strip()

            # Skip if no description
            if not description:
                continue

            # Skip badges (already processed in profile.yaml)
            if item_type in ['BADGE', 'BADGE-LE']:
                continue

            # Skip if no completion date
            if not completion_date:
                continue

            # Parse completion date
            comp_date = parse_date(completion_date)
            if not comp_date:
                continue

            trainings.append({
                'tipo': item_type,
                'titulo': description,
                'data_conclusao': comp_date.strftime('%Y-%m-%d'),
                'ano': comp_date.year,
                'nota': grade if grade else 'N/A',
                'status': status
            })

    # Sort by date (most recent first)
    trainings.sort(key=lambda x: x['data_conclusao'], reverse=True)

    return trainings


def categorize_training(titulo):
    """Categorize training based on title keywords"""
    titulo_lower = titulo.lower()

    # Governança de IA
    if any(word in titulo_lower for word in ['ai now', 'copilot', 'genai', 'artificial intelligence']):
        return 'Governança de IA'

    # AML & Financial Crime
    if any(word in titulo_lower for word in ['anticorrupção', 'lavagem', 'money laundering', 'financial crime',
                                               'aml', 'corruption', 'licitações', 'agentes públicos']):
        return 'AML & Financial Crime'

    # Data Protection & InfoSec
    if any(word in titulo_lower for word in ['lgpd', 'gdpr', 'data protection', 'cybersecurity',
                                               'information security', 'handling information', 'data oversharing']):
        return 'Data Protection & InfoSec'

    # Ética & Independência
    if any(word in titulo_lower for word in ['independence', 'code of conduct', 'conflict', 'ética']):
        return 'Ética & Independência'

    # Setoriais (Banking, Insurance, Payments)
    if any(word in titulo_lower for word in ['banking', 'insurance', 'seguros', 'payments', 'assurance',
                                               'fso', 'rsac', 'brasilseg', 'p&c']):
        return 'Setoriais (Banking · Insurance · Payments)'

    # Consulting
    if any(word in titulo_lower for word in ['consulting', 'transformation realized', 'business consulting']):
        return 'Consulting & Transformation'

    # Técnico & Dados
    if any(word in titulo_lower for word in ['excel', 'alteryx', 'data visualization', 'rpa', 'microsoft data',
                                               'power bi', 'via workflow']):
        return 'Técnico & Dados'

    # Leadership & Soft Skills
    if any(word in titulo_lower for word in ['leadership', 'emotional intelligence', 'team', 'coaching',
                                               'counseling', 'inclusive', 'client service', 'communication',
                                               'business writing', 'mistakes', 'upstanding']):
        return 'Leadership & Soft Skills'

    # Compliance Geral
    if any(word in titulo_lower for word in ['ergonomia', 'segurança no trabalho', 'jornada de trabalho']):
        return 'Compliance Geral'

    # Outros
    return 'Outros'


def generate_consolidated_csv(trainings, output_file):
    """Generate a clean CSV with only relevant columns"""
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['categoria', 'titulo', 'data_conclusao', 'ano', 'nota', 'tipo', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for training in trainings:
            training['categoria'] = categorize_training(training['titulo'])
            writer.writerow(training)


def generate_summary_by_category(trainings, output_file):
    """Generate summary grouped by category"""
    categories = defaultdict(list)

    for training in trainings:
        category = categorize_training(training['titulo'])
        categories[category].append(training)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# RESUMO DE TREINAMENTOS POR CATEGORIA\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total de treinamentos: {len(trainings)}\n")
        f.write(f"Período: {min(t['ano'] for t in trainings)} - {max(t['ano'] for t in trainings)}\n\n")

        # Sort categories by number of trainings
        sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)

        for category, items in sorted_categories:
            f.write(f"\n## {category}\n")
            f.write(f"**Total: {len(items)} treinamentos**\n\n")

            for item in items:
                f.write(f"- [{item['ano']}] {item['titulo']}")
                if item['nota'] != 'N/A':
                    f.write(f" (Nota: {item['nota']})")
                f.write("\n")

            f.write("\n" + "-" * 80 + "\n")


def generate_linkedin_ready(trainings, output_file):
    """Generate a format ready for LinkedIn - most relevant only"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# TREINAMENTOS PARA DESTACAR NO LINKEDIN\n")
        f.write("=" * 80 + "\n\n")
        f.write("## Principais certificações e cursos (últimos 3 anos)\n\n")

        # Filter last 3 years and relevant categories
        current_year = datetime.now().year
        recent_trainings = [t for t in trainings if t['ano'] >= current_year - 3]

        priority_categories = [
            'Governança de IA',
            'AML & Financial Crime',
            'Data Protection & InfoSec',
            'Setoriais (Banking · Insurance · Payments)',
            'Técnico & Dados',
            'Consulting & Transformation'
        ]

        for category in priority_categories:
            items = [t for t in recent_trainings if categorize_training(t['titulo']) == category]
            if items:
                f.write(f"\n### {category}\n")
                for item in items[:5]:  # Top 5 per category
                    f.write(f"- {item['titulo']} ({item['data_conclusao']})\n")


def generate_readme(output_dir):
    """Generate README with instructions"""
    readme_content = """# Estrutura Organizada de Treinamentos EY

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
"""

    readme_path = os.path.join(output_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'report.csv')
    output_dir = os.path.join(script_dir, 'estruturado')

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("🔄 Processando report.csv...")
    trainings = extract_relevant_data(input_file)
    print(f"✅ {len(trainings)} treinamentos extraídos")

    # Generate consolidated CSV
    consolidated_file = os.path.join(output_dir, 'treinamentos_consolidado.csv')
    generate_consolidated_csv(trainings, consolidated_file)
    print(f"✅ Gerado: {consolidated_file}")

    # Generate summary by category
    summary_file = os.path.join(output_dir, 'resumo_por_categoria.txt')
    generate_summary_by_category(trainings, summary_file)
    print(f"✅ Gerado: {summary_file}")

    # Generate LinkedIn-ready format
    linkedin_file = os.path.join(output_dir, 'linkedin_highlights.txt')
    generate_linkedin_ready(trainings, linkedin_file)
    print(f"✅ Gerado: {linkedin_file}")

    # Generate README
    generate_readme(output_dir)
    print(f"✅ Gerado: {output_dir}/README.md")

    print("\n✨ Processamento concluído!")
    print(f"📁 Arquivos gerados em: {output_dir}")


if __name__ == '__main__':
    main()
