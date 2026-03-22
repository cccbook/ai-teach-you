# 9. Tratamento de Erros

---

## 9.1 Por que o Tratamento de Erros e Importante

Sem tratamento de erros:
- Apos um comando falhar, continuar com operacoes erradas
- Pode deletar arquivos errados
- Pode sobrescrever dados importantes
- Pode deixar o sistema em estado inconsistente

Com tratamento de erros:
- Parar imediatamente em erro
- Fornecer mensagens de erro significativas
- Limpar antes de sair

---

## 9.2 Codigos de Saida

Todo comando retorna um codigo de saida apos a execucao:

- `0`: sucesso
- `nao-zero`: falha

```bash
# Verificar codigo de saida do ultimo comando
ls /tmp
echo $?  # Saida: 0 (se bem-sucedido)

ls /inexistente
echo $?  # Saida: 2 (se falhou)
```

---

## 9.3 `set -e`: Parar em Erro

```bash
#!/bin/bash
set -e

mkdir -p backup
cp importante.txt backup/  # Se isso falhar, o script para aqui
rm importante.txt          # Nao chegara aqui
```

### Quando Usar

Quase todos os scripts devem usar `set -e`:
- Scripts de inicializacao
- Scripts de implantacao
- Scripts de teste automatizado

---

## 9.4 `set -u`: Erro em Variaveis Indefinidas

```bash
#!/bin/bash
set -u

echo $variavel_indefinida
# Saida: bash: variavel_indefinida: variavel nao atribuida
```

### Uso Combinado

```bash
#!/bin/bash
set -euo pipefail

# -e: parar em erro
# -u: erro em variavel indefinida
# -o pipefail: pipe falha se qualquer comando falhar
```

**Este e o cabecalho padrao de scripts da IA!**

---

## 9.5 `trap`: Tratamento de Erros Elegante

### Uso Basico

```bash
#!/bin/bash
set -euo pipefail

limpar() {
    echo "Limpando..."
    rm -f /tmp/arquivo_temporario
}

trap limpar EXIT

# Programa principal
echo "Iniciando processo..."
```

### Capturar Erros

```bash
#!/bin/bash
set -euo pipefail

manipulador_erro() {
    local codigo_saida=$?
    echo "✗ Script falhou na linha $1, codigo de saida: $codigo_saida"
    exit $codigo_saida
}

trap 'manipulador_erro $LINENO' ERR
```

---

## 9.6 Funcoes de Erro Personalizadas

```bash
#!/bin/bash
set -euo pipefail

die() {
    echo "✗ $@" >&2
    exit 1
}

warn() {
    echo "⚠️ $@"
}

precisa_comando() {
    command -v "$1" &>/dev/null || die "Comando necessario: $1"
}

precisa_arquivo() {
    [[ -f "$1" ]] || die "Arquivo necessario: $1"
}
```

---

## 9.7 Referencia Rapida

| Comando | Descricao |
|---------|-----------|
| `$?` | Codigo de saida do ultimo comando |
| `set -e` | Parar em erro |
| `set -u` | Erro em variavel indefinida |
| `set -o pipefail` | Pipe falha se qualquer comando falhar |
| `set -euo pipefail` | Combinado (recomendado) |
| `trap 'func' EXIT` | Executar ao sair |
| `trap 'func' ERR` | Executar em erro |
| `trap 'func' INT` | Executar em Ctrl+C |
| `exit 1` | Sair com codigo de erro 1 |

---

## 9.8 Exercicios

1. Escreva um script com `set -euo pipefail` que exiba "Ocorreu um erro" em caso de falha
2. Crie uma funcao `die()` que imprima mensagem e saia
3. Use `trap` para exibir "Adeus" quando o script sair
4. Escreva um script de implantacao com rollback automatico em caso de falha
