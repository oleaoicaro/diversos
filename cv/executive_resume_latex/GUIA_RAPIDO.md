# ⚡ GUIA RÁPIDO — Compilar PDF Executivo

## 🚀 Método 1: Overleaf (RECOMENDADO — Mais Rápido)

### Passo a Passo (3 minutos):

1. **Acesse:** https://www.overleaf.com/
   - Criar conta gratuita (se necessário)

2. **Upload do arquivo:**
   - Clique em **"New Project"** → **"Upload Project"**
   - Faça upload do arquivo `icaro_leao_executive.tex`

3. **Configurar compilador:**
   - Clique em **Menu** (canto superior esquerdo)
   - **Compiler** → Selecione **XeLaTeX**
   - Clique em **Recompile**

4. **Download PDF:**
   - Clique no ícone de download ao lado de **"Recompile"**
   - Arquivo gerado: `icaro_leao_executive.pdf`

**✅ PRONTO!** Você tem seu CV Tier 1 em PDF.

---

## 🖥️ Método 2: Compilação Local (Windows)

### Instalar MiKTeX (one-time setup):
1. Download: https://miktex.org/download
2. Executar instalador → Next → Next → Install
3. Tempo: ~10 minutos

### Compilar:
```cmd
cd cv\executive_resume_latex
xelatex icaro_leao_executive.tex
```

Na primeira compilação, MiKTeX vai baixar packages automaticamente (aceite sempre).

### Executar 2x para resolver referências:
```cmd
xelatex icaro_leao_executive.tex
```

**✅ PDF gerado:** `icaro_leao_executive.pdf`

---

## 🍎 Método 3: Compilação Local (Mac)

### Instalar MacTeX (one-time setup):
```bash
brew install --cask mactex
```
Tempo: ~15 minutos (download é grande: 4.5GB)

### Compilar:
```bash
cd cv/executive_resume_latex
xelatex icaro_leao_executive.tex
xelatex icaro_leao_executive.tex  # 2x para resolver referências
```

**✅ PDF gerado:** `icaro_leao_executive.pdf`

---

## 🐧 Método 4: Compilação Local (Linux)

### Instalar TeX Live:
```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-fonts-extra
```

### Compilar:
```bash
cd cv/executive_resume_latex
xelatex icaro_leao_executive.tex
xelatex icaro_leao_executive.tex  # 2x
```

**✅ PDF gerado:** `icaro_leao_executive.pdf`

---

## 🎨 Personalização Rápida

### Mudar Cor de Acento:
Editar **linha 26** em `icaro_leao_executive.tex`:

```latex
\definecolor{ExecutiveNavy}{HTML}{14213D}
```

**Opções Tier 1:**
- Deep Navy (atual): `#14213D` — Autoridade conservadora
- Charcoal: `#2C2C2C` — Minimalismo tech
- Dark Teal: `#004D4D` — Inovação sustentável
- Burgundy: `#5E1F1F` — Tradição institucional

Salvar e recompilar.

---

## ❓ Troubleshooting

### ❌ Erro: "Font 'EB Garamond' not found"
**Solução:** Use **Overleaf** (fontes já instaladas) ou instale fontes localmente (ver README.md).

### ❌ Erro: "xelatex: command not found"
**Solução:** Instalar TeX Live completo (não minimal).

### ❌ PDF com acentos estranhos
**Solução:** Garantir arquivo UTF-8 + usar **XeLaTeX** (não pdflatex).

---

## 📦 Arquivos Entregues

```
cv/executive_resume_latex/
├── icaro_leao_executive.tex           # 👈 Documento LaTeX fonte
├── README.md                           # Documentação completa
├── ANALISE_TRANSFORMACAO.md            # Análise das 7 falhas corrigidas
└── GUIA_RAPIDO.md                      # Este arquivo
```

---

**Tempo estimado (Overleaf):** 3 minutos
**Tempo estimado (Local, primeira vez):** 15-20 minutos (setup) + 1 minuto (compilação)
**Tempo estimado (Local, segunda vez em diante):** 30 segundos

**Recomendação:** Use **Overleaf** para primeira compilação (zero setup).
