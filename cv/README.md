# CV Executivo — Ícaro Leão

Geração automatizada do currículo executivo de Ícaro Leão em português (PT) e inglês (EN), nos formatos HTML e PDF, a partir de uma única fonte de dados YAML.

## Estrutura

```
cv/
├── data/
│   └── profile.yaml          # Fonte única de dados PT+EN
├── templates/
│   ├── executive_pt.html     # Template Jinja2 português
│   ├── executive_en.html     # Template Jinja2 inglês
│   └── styles/
│       └── executive.css     # CSS premium A4 (grid 2 colunas)
├── scripts/
│   ├── build_cv.py           # Script de build
│   └── requirements.txt      # Dependências Python
├── output/
│   ├── Icaro_Leao_CV_PT.html
│   ├── Icaro_Leao_CV_PT.pdf
│   ├── Icaro_Leao_CV_EN.html
│   └── Icaro_Leao_CV_EN.pdf
└── README.md
```

## Pré-requisitos

**Python 3.11+** — https://www.python.org/downloads/

### Windows
Instale o GTK3 Runtime (necessário para WeasyPrint):
- https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

### Linux (Ubuntu/Debian)
```bash
sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz0b
```

## Instalação

```bash
pip install -r cv/scripts/requirements.txt
```

## Build

```bash
python cv/scripts/build_cv.py
```

Os arquivos gerados serão salvos em `cv/output/`.

## Personalização

### Cor de acento
Edite a variável `--accent` em `cv/templates/styles/executive.css` (padrão: `#14213D`):

```css
:root {
  --accent: #14213D; /* azul-marinho profundo */
}
```

### Dados do perfil
Edite `cv/data/profile.yaml` — as chaves `pt` e `en` controlam cada idioma de forma independente.

## Fallback sem WeasyPrint

Se WeasyPrint não estiver disponível, o script tenta automaticamente Playwright. Se ambos falharem:

1. Abra o HTML gerado em `cv/output/` no **Google Chrome**
2. Pressione `Ctrl+P` (ou `Cmd+P` no Mac)
3. Configure: **Destino → Salvar como PDF**, **Tamanho → A4**, **Margens → Mínimas**
4. Marque **"Gráficos de fundo"**
5. Clique em **Salvar**

## Design

- **Tipografia:** Playfair Display (serif) nos títulos + Inter (sans-serif) no corpo
- **Cor de acento única:** `#14213D` (azul-marinho profundo EY-style)
- **Layout:** Grid 2 colunas A4 — sidebar 32% + conteúdo 68%
- **Visual:** Estilo executivo premium, zero emojis, zero cores saturadas
