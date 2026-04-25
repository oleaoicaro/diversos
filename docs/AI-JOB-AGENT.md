# AI Job Agent — Guia de Uso

Integração do [AkbarDevop/ai-job-agent](https://github.com/AkbarDevop/ai-job-agent) com o currículo deste repositório para automatizar candidaturas a vagas no LinkedIn.

---

## Pré-requisitos

- Git
- Node.js ≥ 18
- Python ≥ 3.10
- Conta no LinkedIn

---

## Configuração Inicial

### 1. Inicializar o submódulo

```bash
git submodule update --init --recursive
```

### 2. Instalar dependências do agente

```bash
cd ai-job-agent
bash setup.sh
cd ..
```

### 3. Instalar dependências do CV (geração de PDF)

```bash
pip install -r cv/scripts/requirements.txt
```

---

## Gerar o PDF do Currículo

O agente consome diretamente o PDF gerado pelo build do CV em `cv/output/Icaro_Leao_CV_PT.pdf`:

```bash
python cv/scripts/build_cv.py
```

O script gera HTML + PDF em PT e EN dentro de `cv/output/`. O template `config/linkedin-config.template.json` já aponta `resumePath` para `../cv/output/Icaro_Leao_CV_PT.pdf`.

---

## Configurar o Agente

### 4. Copiar e preencher os templates

```bash
cp config/linkedin-config.template.json config/linkedin-config.json
cp config/candidate-profile.template.md config/candidate-profile.md
cp config/answer-bank.template.md config/answer-bank.md
```

Edite cada arquivo com seus dados reais:

- **`config/linkedin-config.json`** — credenciais e preferências de busca
- **`config/candidate-profile.md`** — seu perfil completo em português
- **`config/answer-bank.md`** — respostas para perguntas frequentes

> **Atenção:** Esses arquivos estão no `.gitignore` e **não serão commitados** — eles contêm dados sensíveis.

---

## Executar o Agente

### Modo dry-run (sem submeter candidaturas)

Recomendado para testar antes de usar de verdade:

```bash
node ai-job-agent/scripts/linkedin-easy-apply.js \
  "https://www.linkedin.com/jobs/search/?keywords=Analista&location=Brasil" \
  --config config/linkedin-config.json \
  --dry-run
```

### Modo real (submete candidaturas)

Após validar o dry-run, edite `config/linkedin-config.json` e defina `"autoSubmit": true` e `"dryRun": false`, então:

```bash
node ai-job-agent/scripts/linkedin-easy-apply.js \
  "https://www.linkedin.com/jobs/search/?keywords=Analista&location=Brasil" \
  --config config/linkedin-config.json
```

---

## Estrutura de Arquivos

```
.
├── ai-job-agent/                  # Submódulo — agente de candidaturas
├── config/
│   ├── linkedin-config.template.json   # Template de configuração (commitado)
│   ├── linkedin-config.json            # Sua config real (ignorado pelo git)
│   ├── candidate-profile.template.md  # Template de perfil (commitado)
│   ├── candidate-profile.md            # Seu perfil real (ignorado pelo git)
│   ├── answer-bank.template.md        # Template de respostas (commitado)
│   └── answer-bank.md                  # Suas respostas reais (ignoradas pelo git)
├── cv/
│   ├── scripts/
│   │   ├── build_cv.py                # Build HTML + PDF (PT/EN) — fonte do resumo
│   │   └── requirements.txt           # Dependências Python (jinja2, pyyaml, weasyprint…)
│   └── output/
│       ├── Icaro_Leao_CV_PT.html
│       ├── Icaro_Leao_CV_PT.pdf       # PDF consumido pelo agente (resumePath)
│       ├── Icaro_Leao_CV_EN.html
│       └── Icaro_Leao_CV_EN.pdf
└── docs/
    └── AI-JOB-AGENT.md                # Este documento
```

---

## Dicas

- Execute o agente pela manhã, quando há mais vagas novas publicadas.
- Revise `config/answer-bank.md` antes de cada sessão para garantir que as respostas estão atualizadas.
- O tracker de candidaturas (`application-tracker.csv`) e os logs diários (`daily-log-*.md`) são gerados automaticamente pelo agente e estão no `.gitignore`.
- Para atualizar o submódulo para a versão mais recente do agente:
  ```bash
  cd ai-job-agent && git pull origin main && cd ..
  git add ai-job-agent && git commit -m "chore: update ai-job-agent submodule"
  ```
