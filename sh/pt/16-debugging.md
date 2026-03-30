# 16. Técnicas de Depuração

---

## 16.1 Mentalidade de Depuração da IA

Quando humanos encontram erros: pânico, pesquisa online, copy-paste
Quando IA encontra erros: analisar mensagem, inferir causa, executar correção

Fluxo de depuração da IA:
```
Observar saída de erro → Entender tipo de erro → Localizar problema → Corrigir → Verificar
```

---

## 16.2 `bash -x`: Rastrear Execução

Depuração mais simples: adicionar sinal `-x`

```bash
bash -x script.sh
```

Mostra cada linha executada com prefixo `+`:

```bash
+ mkdir -p test
+ cd test
+ echo 'Hello'
Hello
```

### Depurar Apenas Uma Seção

```bash
#!/bin/bash

echo "Isso não será mostrado"
set -x
# Depuração começa aqui
name="Alice"
echo "Olá, $name"
set +x
# Depuração termina aqui
echo "Isso não será mostrado"
```

---

## 16.3 Erros Comuns e Correções

### Erro 1: Permissão Negada

```bash
# Erro
./script.sh
# Saída: Permission denied

# Correção
chmod +x script.sh
./script.sh
```

### Erro 2: Comando Não Encontrado

```bash
# Erro
python script.py
# Saída: command not found: python

# Correção: usar caminho completo
/usr/bin/python3 script.py
```

### Erro 3: Variável Não Definida

```bash
#!/bin/bash
set -u

echo $undefined_var
# Saída: bash: undefined_var: unbound variable

# Correção: fornecer valor padrão
echo ${undefined_var:-default}
```

---

## 16.4 Depuração com `echo`

Quando `-x` não é suficiente, adicionar `echo` manualmente:

```bash
#!/bin/bash

echo "DEBUG: Entrando na função"
echo "DEBUG: Parâmetro = $@"

process() {
    echo "DEBUG: Em process"
    local result=$(expensive_command)
    echo "DEBUG: result = $result"
}
```

---

## 16.5 Referência Rápida

| Comando | Descrição |
|---------|------------|
| `bash -n script.sh` | Verificar sintaxe apenas |
| `bash -x script.sh` | Rastrear execução |
| `set -x` | Habilitar modo de depuração |
| `set +x` | Desabilitar modo de depuração |
| `trap 'echo cmd' DEBUG` | Rastrear cada comando |

---

## 16.6 Exercícios

1. Execute um script com `bash -x` e observe o formato de saída
2. Use `set -x` em um script para depurar apenas uma função específica
3. Encontre um comando que falha, analise a mensagem de erro e corrija-o
4. Crie tratamento de erros graceful com `trap`