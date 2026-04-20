# CV Executivo — Ícaro Leão

Geração automatizada do currículo executivo de Ícaro Leão em português (PT) e inglês (EN), nos formatos HTML e PDF, a partir de uma única fonte de dados YAML.

## Estrutura

```
cv/
├── data/
│   └── profile.yaml              # Fonte única de dados PT+EN (não editar estrutura)
├── templates/
│   ├── executive_pt.html         # Template Jinja2 português
│   ├── executive_en.html         # Template Jinja2 inglês
│   └── styles/
│       ├── executive.css         # CSS premium A4 — paleta executiva
│       └── fonts/                # Fontes locais (bundled)
│           ├── Inter-Regular.ttf          # Sans-serif (corpo)
│           ├── LiberationSerif-Regular.ttf
│           ├── LiberationSerif-Bold.ttf
│           ├── LiberationSerif-Italic.ttf
│           └── LiberationSerif-BoldItalic.ttf
├── scripts/
│   ├── build_cv.py               # Script de build (WeasyPrint + Playwright fallback)
│   └── requirements.txt          # Dependências Python
├── output/
│   ├── Icaro_Leao_CV_PT.html
│   ├── Icaro_Leao_CV_PT.pdf
│   ├── Icaro_Leao_CV_EN.html
│   └── Icaro_Leao_CV_EN.pdf
└── README.md
```

## Pré-requisitos

**Python 3.11+** — https://www.python.org/downloads/

### Linux (Ubuntu/Debian)
WeasyPrint requer as bibliotecas de renderização de texto do sistema:
```bash
sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
                 libharfbuzz0b libfontconfig1 libcairo2
```

### Windows
Instale o GTK3 Runtime (necessário para WeasyPrint):
- https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

### macOS
```bash
brew install pango
```

## Instalação

```bash
pip install -r cv/scripts/requirements.txt
```

## Build

```bash
python cv/scripts/build_cv.py
```

Os arquivos HTML e PDF gerados são salvos em `cv/output/`. O script registra:
- Versão do WeasyPrint em uso
- Fontes detectadas no diretório `fonts/`
- Caminho de cada arquivo gerado

## Personalização

### Paleta de cores
Edite as variáveis CSS em `cv/templates/styles/executive.css`:

```css
:root {
  --accent: #1f2a44;  /* navy — títulos e destaque */
  --ink:    #1a1a1a;  /* quase-preto — corpo */
  --mid:    #555555;  /* cinza médio — metadados */
  --light:  #888888;  /* cinza claro — labels */
  --rule:   #dddddd;  /* linha divisória */
}
```

### Tipografia
Para substituir as fontes, adicione arquivos TTF/WOFF2 em `cv/templates/styles/fonts/`
e atualize os blocos `@font-face` no início de `executive.css`.

- **Serif** (`CVSerif`): usado no nome, empresa, cabeçalhos principais
- **Sans-serif** (`Inter`): usado em todo o resto

### Dados do perfil
Edite `cv/data/profile.yaml` — as chaves `pt` e `en` controlam cada idioma de forma independente. **Não altere a estrutura das chaves.**

## Fallback sem WeasyPrint

Se WeasyPrint não estiver disponível, o script tenta automaticamente Playwright. Se ambos falharem:

1. Abra o HTML gerado em `cv/output/` no **Google Chrome**
2. Pressione `Ctrl+P` (ou `Cmd+P` no Mac)
3. Configure: **Destino → Salvar como PDF**, **Tamanho → A4**, **Margens → Mínimas**
4. Marque **"Gráficos de fundo"**
5. Clique em **Salvar**

## Design

- **Tipografia:** Liberation Serif (serif, semelhante a Times New Roman) nos títulos e nomes de empresas + Inter (sans-serif) no corpo
- **Paleta:** Navy `#1f2a44` como acento único; escala de cinzas para hierarquia
- **Layout:** Tabela CSS 2 colunas A4 — sidebar 30% + conteúdo 70%
- **Competências:** exibidas como chips/tags com borda fina
- **Marcadores de lista:** traço longo (—) em cinza médio
- **Paginação:** `X / Y` centralizado no rodapé via CSS `@page`
