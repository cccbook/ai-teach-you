# 10. Analise de Argumentos e Ferramentas CLI

---

## 10.1 Basico de Argumentos de Linha de Comando

```bash
#!/bin/bash

echo "Script: $0"
echo "Primeiro arg: $1"
echo "Segundo arg: $2"
echo "Terceiro arg: ${3:-padrao}"  # valor padrao
echo "Contagem de args: $#"
echo "Todos os args: $@"
```

### Execucao

```bash
./script.sh foo bar
# Saida:
# Script: ./script.sh
# Primeiro arg: foo
# Segundo arg: bar
# Terceiro arg: padrao
# Contagem de args: 2
# Todos os args: foo bar
```

---

## 10.2 Analise Simples de Argumentos

### Parametros Posicionais

```bash
#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Uso: $0 <arquivo>"
    exit 1
fi

ARQUIVO="$1"

if [[ ! -f "$ARQUIVO" ]]; then
    echo "Erro: arquivo nao existe"
    exit 1
fi

echo "Processando $ARQUIVO..."
```

### Lidando com Argumentos Opcionais

```bash
#!/bin/bash

VERBOSE=false
SAIDA=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--output)
            SAIDA="$2"
            shift 2
            ;;
        -*)
            echo "Opcao desconhecida: $1"
            exit 1
            ;;
        *)
            ARQUIVO="$1"
            shift
            ;;
    esac
done

$VERBOSE && echo "modo verboso ativado"
[[ -n "$SAIDA" ]] && echo "Saida para: $SAIDA"
```

---

## 10.3 `getopts`: Analise Padrao de Opcoes

```bash
#!/bin/bash

while getopts "hv:o:" opt; do
    case $opt in
        h)
            echo "Informacoes de ajuda"
            exit 0
            ;;
        v)
            echo "modo verboso: $OPTARG"
            ;;
        o)
            echo "arquivo de saida: $OPTARG"
            ;;
        \?)
            echo "Opcao invalida: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

shift $((OPTIND - 1))

echo "Argumentos restantes: $@"
```

### Referencia de Formato de Opcoes

| Formato | Significado |
|---------|-------------|
| `getopts "hv:"` | `-h` sem arg, `-v` precisa de arg |
| `OPTARG` | Valor do argumento da opcao atual |
| `OPTIND` | Indice do proximo argumento |

---

## 10.4 Entrada Interativa

### `read`: Ler Entrada do Usuario

```bash
#!/bin/bash

# Leitura basica
read -p "Digite seu nome: " nome
echo "Ola, $nome"

# Senha (oculta)
read -sp "Digite a senha: " senha
echo

# Ler multiplos valores
read -p "Digite nome e idade: " nome idade
echo "$nome tem $idade anos"

# Timeout
read -t 5 -p "Digite em 5 segundos: " valor
```

### Prompt de Confirmacao

```bash
confirmar() {
    read -p "$1 (s/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Ss]$ ]]
}

if confirmar "Deletar este arquivo?"; then
    echo "Deletando..."
fi
```

---

## 10.5 Interface de Menu

```bash
#!/bin/bash

PS3="Selecione a operacao: "

select escolha in "Criar projeto" "Deletar projeto" "Sair"; do
    case $escolha in
        "Criar projeto")
            echo "Criando..."
            ;;
        "Deletar projeto")
            echo "Deletando..."
            ;;
        "Sair")
            echo "Ate mais!"
            exit 0
            ;;
        *)
            echo "Escolha invalida"
            ;;
    esac
done
```

---

## 10.6 Referencia Rapida

| Sintaxe | Descricao |
|---------|-----------|
| `$0` | Nome do script |
| `$1`, `$2`... | Parametros posicionais |
| `$#` | Contagem de argumentos |
| `${var:-padrao}` | Valor padrao |
| `getopts "hv:" opt` | Analisar opcoes |
| `$OPTARG` | Arg da opcao atual |
| `read -p "prompt:" var` | Ler entrada |
| `read -s var` | Entrada oculta (senha) |
| `read -t 5 var` | Timeout de 5 segundos |
| `select` | Interface de menu |

---

## 10.7 Exercicios

1. Escreva uma ferramenta CLI que aceite `-n` para contagem, `-v` para modo verboso
2. Use `getopts` para analisar opcoes `-h` (ajuda), `-o` (arquivo de saida)
3. Escreva uma funcao de confirmacao que so prossiga com resposta s
4. Crie uma calculadora simples com menu usando `select`
