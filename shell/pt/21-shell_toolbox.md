# 21. Construindo Sua Caixa de Ferramentas Shell de IA

---

## 21.1 Por Que Você Precisa de uma Caixa de Ferramentas

Quando você se pega fazendo a mesma coisa repetidamente, é hora de automatizar e coletar em uma caixa de ferramentas.

A IA é especialmente boa em:
- Criar ferramentas rapidamente
- Envolver fluxos de trabalho complexos em comandos simples
- Melhorar continuamente scripts comumente usados

---

## 21.2 Estrutura de Diretório da Caixa de Ferramentas

```
~/bin/
├── lib/              # Bibliotecas compartilhadas
│   ├── logging.sh
│   ├── utils.sh
│   └── colors.sh
├── project/          # Modelos de projetos
│   ├── python/
│   ├── nodejs/
│   └── static-site/
├── scripts/          # Scripts de ferramentas
│   ├── git-clean
│   ├── docker-clean
│   ├── backup
│   └── log-parse
└── bin/
    ├── greet         # Ferramenta executável
    └── monitor       # Ferramenta executável
```

---

## 21.3 Criando Sua Biblioteca

### logging.sh

```bash
cat > ~/bin/lib/logging.sh << 'EOF'
#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $@"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $@"; }
log_error() { echo -e "${RED}[ERROR]${NC} $@" >&2; }
EOF

source ~/bin/lib/logging.sh
```

### utils.sh

```bash
cat > ~/bin/lib/utils.sh << 'EOF'
#!/bin/bash

need_command() {
    command -v "$1" &>/dev/null || {
        echo "Comando necessário: $1"
        exit 1
    }
}

need_file() {
    [[ -f "$1" ]] || {
        echo "Arquivo necessário: $1"
        exit 1
    }
}

need_dir() {
    [[ -d "$1" ]] || {
        echo "Diretório necessário: $1"
        exit 1
    }
}
EOF
```

---

## 21.4 Ferramenta Prática: git-clean

```bash
cat > ~/bin/git-clean << 'EOF'
#!/bin/bash
set -euo pipefail

DRY_RUN=false
while [[ $# -gt 0 ]]; do
    case "$1" in
        -n|--dry-run) DRY_RUN=true; shift ;;
        *) shift ;;
    esac
done

if $DRY_RUN; then
    echo "[DRY-RUN] Excluiria:"
fi

git branch --merged main | grep -v "main\|master\|develop" | while read branch; do
    if $DRY_RUN; then
        echo "  Excluir branch: $branch"
    else
        git branch -d "$branch"
        echo "Excluído: $branch"
    fi
done

git clean -n -d
EOF

chmod +x ~/bin/git-clean
```

---

## 21.5 Ferramenta Prática: docker-clean

```bash
cat > ~/bin/docker-clean << 'EOF'
#!/bin/bash
set -euo pipefail

echo "Parando todos os containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "Removendo containers parados..."
docker container prune -f

echo "Removendo imagens não usadas..."
docker image prune -af

echo "Removendo redes não usadas..."
docker network prune -f

echo "Removendo cache de build..."
docker builder prune -af

echo "✅ Limpeza do Docker concluída"
docker system df
EOF

chmod +x ~/bin/docker-clean
```

---

## 21.6 Disponibilizando Ferramentas no PATH

```bash
# Verificar se ~/bin está no PATH
echo $PATH | grep -q "$HOME/bin" && echo "Configurado" || echo "Não configurado"

# Adicionar ao PATH (adicionar ao ~/.bashrc ou ~/.zshrc)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 21.7 Deixe a IA Ajudar a Expandir a Caixa de Ferramentas

```bash
# Humano: me ajude a criar uma ferramenta para analisar logs de acesso do Nginx

# IA:
cat > ~/bin/nginx-analyze << 'EOF'
#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Uso: $0 <arquivo_log_acesso>"
    exit 1
fi

FILE=$1

echo "=== Análise Nginx: $FILE ==="
echo ""

echo "Tamanho do arquivo: $(du -h "$FILE" | cut -f1)"
echo "Total de linhas: $(wc -l < "$FILE")"
echo ""

echo "=== Top 10 IPs ==="
awk '{print $1}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Top 10 URLs ==="
awk '{print $7}' "$FILE" | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Distribuição de Códigos de Status ==="
awk '{print $9}' "$FILE" | sort | uniq -c | sort -rn
EOF

chmod +x ~/bin/nginx-analyze
```

---

## 21.8 Melhoria Contínua

```bash
# Revisar caixa de ferramentas anualmente
# - Quais ferramentas são pouco usadas? Excluir
# - Quais ferramentas podem ser melhoradas?
# - Quais tarefas repetitivas podem ser automatizadas?

# Versionar sua caixa de ferramentas
cd ~/bin
git init
git add .
git commit -m "Versão inicial"
```

---

## 21.9 Exercícios

1. Criar sua estrutura de diretório ~/bin
2. Escrever funções comumente usadas em bibliotecas reutilizáveis
3. Escrever uma ferramenta para tarefas que você repete diariamente
4. Fazer a IA ajudar a criar uma ferramenta de análise de logs Nginx
5. Colocar sua caixa de ferramentas sob controle de versão Git