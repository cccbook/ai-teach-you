# 18. Lendo e Modificando Scripts de Outros

---

## 18.1 Por Que Ler Scripts de Outros

- Assumir manutenção de projetos
- Usar ferramentas open source
- Depurar problemas
- Aprender novas técnicas

A IA encontra scripts desconhecidos diariamente, então aprender a entender rapidamente scripts Shell escritos por outros é essencial.

---

## 18.2 Observação Inicial

### Passo 1: Verificar shebang

```bash
head -1 script.sh
```

```bash
#!/bin/bash      # Usar bash
#!/bin/sh        # Usar POSIX sh (mais compatível)
```

### Passo 2: Verificar permissões e tamanho

```bash
ls -la script.sh
wc -l script.sh
```

### Passo 3: Verificação rápida de sintaxe

```bash
bash -n script.sh  # Verificar sintaxe apenas, não executar
```

---

## 18.3 Entendendo a Estrutura

### Estrutura Típica

```bash
#!/bin/bash
# Comentário: descrição do script

# Configuração
set -euo pipefail
VAR="value"

# Definições de funções
function help() { ... }

# Fluxo principal
main() { ... }

# Execução
main "$@"
```

### Encontrar Fluxo Principal

```bash
# Ver últimas linhas
tail -20 script.sh

# Encontrar definições de funções
grep -n "^function\|^[[:space:]]*[a-z_]*\(" script.sh
```

---

## 18.4 Comandos de Análise Comuns

```bash
# Encontrar todas as definições de funções
grep -n "^[[:space:]]*function" script.sh

# Encontrar todos os condicionais
grep -n "if\|\[\[" script.sh

# Encontrar todos os loops
grep -n "for\|while\|do\|done" script.sh

# Encontrar substituições de comandos
grep -n '\$(' script.sh

# Encontrar todas as saídas
grep -n "exit" script.sh
```

---

## 18.5 Verificações de Segurança

```bash
# Encontrar comandos perigosos
grep -n "rm -rf" script.sh
grep -n "sudo" script.sh
grep -n "eval" script.sh

# Verificar riscos de injeção de variáveis
grep -n '\$[A-Za-z_][A-Za-z0-9_]*[^"}]' script.sh
```

---

## 18.6 Exercícios

1. Analisar um script Shell existente com `grep` e `awk`
2. Encontrar todas as variáveis em um script e entender seus propósitos
3. Usar `bash -n` para verificar a sintaxe de um script
4. adicionar comentários a um script sem comentários explicando cada seção