# 11. Registro e Saida

---

## 11.1 Por que o Registro e Importante

Sem registro:
- Voce nao sabe onde o script esta
- Nao sabe por que falhou
- Nao sabe o que fez em caso de sucesso

Com registro:
- Pode acompanhar o progresso
- Tem informacoes suficientes para depurar falhas
- Pode auditar o historico de execucao

---

## 11.2 Niveis de Log Basicos

```bash
#!/bin/bash

DEBUG=0
INFO=1
WARN=2
ERROR=3

LOG_LEVEL=${LOG_LEVEL:-$INFO}

log() {
    local nivel=$1
    shift
    local mensagem="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [[ $nivel -ge $LOG_LEVEL ]]; then
        echo "[$timestamp] $mensagem"
    fi
}

log $DEBUG "Isso e debug"
log $INFO "Isso e info"
log $WARN "Isso e aviso"
log $ERROR "Isso e erro"
```

---

## 11.3 Saida Colorida

```bash
#!/bin/bash

VERMELHO='\033[0;31m'
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
AZUL='\033[0;34m'
SEM_COR='\033[0m'  # Sem Cor

log_info() { echo -e "${VERDE}[INFO]${SEM_COR} $@"; }
log_warn() { echo -e "${AMARELO}[AVISO]${SEM_COR} $@"; }
log_error() { echo -e "${VERMELHO}[ERRO]${SEM_COR} $@" >&2; }

log_info "Instalacao concluida"
log_warn "Usando padroes"
log_error "Conexao falhou"
```

---

## 11.4 Saida para Arquivo

```bash
#!/bin/bash

ARQUIVO_LOG="/var/log/meuapp.log"

log() {
    local mensagem="[$(date '+%Y-%m-%d %H:%M:%S')] $@"
    echo "$mensagem"
    echo "$mensagem" >> "$ARQUIVO_LOG"
}

log "Aplicativo iniciado"
```

---

## 11.5 `tee`: Saida para Tela e Arquivo

```bash
# Exibir e salvar simultaneamente
echo "Ola" | tee saida.txt

# Modo anexar
echo "Mundo" | tee -a saida.txt

# Capturar stderr tambem
./script.sh 2>&1 | tee saida.log
```

---

## 11.6 Indicadores de Progresso

### Pontos Simples

```bash
echo -n "Processando"
for i in {1..10}; do
    echo -n "."
    sleep 0.2
done
echo " Feito"
```

### Barra de Progresso

```bash
desenhar_progresso() {
    local atual=$1
    local total=$2
    local largura=40
    local percentual=$((atual * 100 / total))
    local chars=$((largura * atual / total))
    
    printf "\r[%s%s] %3d%%" \
        "$(printf '%*s' $chars | tr ' ' '=')" \
        "$(printf '%*s' $((largura - chars)) | tr ' ' '-')" \
        "$percentual"
    
    [[ $atual -eq $total ]] && echo
}
```

---

## 11.7 Explicacao de `2>&1`

```bash
# 1 = stdout, 2 = stderr

# Redirecionar stderr para stdout
comando 2>&1

# Redirecionar stdout para arquivo, stderr para tela
comando > saida.txt

# Redirecionar ambos para arquivo
comando > saida.txt 2>&1

# Redirecionar ambos para /dev/null (ocultar)
comando > /dev/null 2>&1
```

---

## 11.8 Referencia Rapida

| Sintaxe | Descricao |
|---------|-----------|
| `echo "texto"` | Saida basica |
| `echo -e "\033[31m"` | Saida colorida |
| `2>&1` | Redirecionar stderr para stdout |
| `> arquivo` | Sobrescrever arquivo |
| `>> arquivo` | Anexar ao arquivo |
| `tee arquivo` | Saida e salvar |
| `tee -a arquivo` | Modo anexar |
| `/dev/null` | Descartar saida |

---

## 11.9 Exercicios

1. Escreva um script que exiba mensagens INFO, AVISO, ERRO em cores diferentes
2. Use `tee` para exibir e salvar saida em um arquivo de log simultaneamente
3. Crie um script de processamento de arquivos com barra de progresso
4. Construa uma biblioteca de registro que suporte saida em arquivo e niveis de log
