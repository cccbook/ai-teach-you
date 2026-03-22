# 8. Variaveis e Funcoes

---

## 8.1 Basico de Variaveis

### Atribuicao Basica

```bash
# String
nome="Alice"
saudacao="Ola, Mundo!"

# Numero
idade=25
contagem=0

# Vazio
vazio=
vazio2=""
```

### Lendo Variaveis

```bash
echo $nome
echo ${nome}    # Forma recomendada, mais explicita

# Em aspas duplas
echo "Meu nome e ${nome}"
```

### Erros Comuns

```bash
# Errado: espacos ao redor de =
nome = "Alice"   # Interpretado como comando

# Errado: sem aspas
saudacao=Ola Mundo  # So ecoa "Ola"

# Correto:
nome="Alice"
saudacao="Ola Mundo"
```

---

## 8.2 A Arte das Aspas

### Aspas Duplas `"`
Expande variaveis e substituicao de comandos

```bash
nome="Alice"
echo "Ola, $nome"           # Ola, Alice
echo "Hoje e $(date +%Y)"     # Hoje e 2026
```

### Aspas Simples `'`
Saida literal, nao expande nada

```bash
nome="Alice"
echo 'Ola, $nome'           # Ola, $nome
echo 'Hoje e $(date +%Y)'     # Hoje e $(date +%Y)
```

### Sem Aspas
Evite a menos que tenha certeza que a variavel nao contem espacos

---

## 8.3 Variaveis Especiais

```bash
$0          # Nome do script
$1, $2...   # Parametros posicionais
$#          # Contagem de argumentos
$@          # Todos os argumentos (individuais)
$*          # Todos os argumentos (como uma string)
$?          # Codigo de saida do ultimo comando
$$          # PID do processo atual
$!          # PID do ultimo processo em background
$-          # Opcoes atuais do shell
```

---

## 8.4 Arrays

### Uso Basico

```bash
# Definir array
cores=("vermelho" "verde" "azul")

# Ler elementos
echo ${cores[0]}    # vermelho
echo ${cores[1]}    # verde

# Ler todos
echo ${cores[@]}    # vermelho verde azul

# Tamanho do array
echo ${#cores[@]}   # 3
```

### Arrays Associativos (Bash 4+)

```bash
declare -A usuario
usuario["nome"]="Alice"
usuario["email"]="alice@exemplo.com"

echo ${usuario["nome"]}    # Alice
```

---

## 8.5 Basico de Funcoes

### Definindo Funcoes

```bash
# Metodo 1: palavra-chave function
function saudar {
    echo "Ola!"
}

# Metodo 2: definicao direta (recomendado)
saudar() {
    echo "Ola!"
}
```

### Parametros de Funcao

```bash
saudar() {
    echo "Ola, $1!"
}

saudar "Alice"    # Ola, Alice!
```

### Valores de Retorno

```bash
# return: para codigo de saida (0-255)
verificar() {
    if [[ $1 -gt 10 ]]; then
        return 0  # sucesso
    else
        return 1  # falha
    fi
}

if verificar 15; then
    echo "Maior que 10"
fi
```

---

## 8.6 Variaveis Locais

```bash
contador() {
    local contagem=0
    ((contagem++))
    echo $contagem
}
```

---

## 8.7 Bibliotecas de Funcoes

### Criar Biblioteca

```bash
cat > lib.sh << 'EOF'
#!/bin/bash

log() {
    echo "[$(date +%H:%M:%S)] $@"
}

erro() {
    echo "[$(date +%H:%M:%S)] ERRO: $@" >&2
}

confirmar() {
    read -p "$1 (s/n) " -n 1 -r
    echo
    [[ $REPLY =~ ^[Ss]$ ]]
}
EOF
```

### Usar Biblioteca

```bash
#!/bin/bash

source lib.sh

log "Iniciando processo"
erro "Algo deu errado"
confirmar "Continuar?" && echo "Continuando"
```

---

## 8.8 Referencia Rapida

| Topico | Sintaxe | Descricao |
|--------|---------|-----------|
| Atribuicao | `var=valor` | Sem espacos ao redor de = |
| Leitura | `$var` ou `${var}` | Use `${var}` |
| Aspas duplas | `"..."` | Expande variaveis |
| Aspas simples | `'...'` | Sem expansao |
| Argumentos | `$1`, `$2`, `$@` | Obter parametros |
| Funcao | `nome() { }` | definicao recomendada |
| Var local | `local var=valor` | apenas em funcao |
| Array | `arr=(a b c)` | indexado e associativo |
| source | `source arquivo.sh` | Carregar biblioteca |

---

## 8.9 Exercicios

1. Escreva um script que aceite parametros nome e idade, e exiba "Ola, Y, voce tem X anos!"
2. Crie uma biblioteca com funcoes `log` e `erro`, use-a em outro script
3. Escreva uma funcao recursiva para calcular numeros de Fibonacci
4. Use `mapfile` para ler um arquivo linha por linha em um array, depois exiba em ordem reversa
