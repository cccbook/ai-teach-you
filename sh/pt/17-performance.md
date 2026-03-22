# 17. Otimização de Desempenho

---

## 17.1 Por Que o Desempenho do Shell Importa

Scripts de Shell são frequentemente usados para:
- Processamento em lote de grandes quantidades de arquivos
- Tarefas de automação
- Pipelines de CI/CD

Um script lento pode atrasar todo o processo por horas. Otimizar scripts Shell pode melhorar grandemente a eficiência.

---

## 17.2 Evitar Comandos Externos

```bash
# Lento: comandos externos
for f in *.txt; do
    name=$(basename "$f")
    echo "$name"
done

# Rápido: builtins do Shell
for f in *.txt; do
    echo "${f##*/}"
done
```

### Builtin vs Externo

| Lento | Rápido | Descrição |
|-------|--------|-----------|
| `$(cat file)` | `$(<file)` | Leitura direta |
| `$(basename $f)` | `${f##*/}` | Expansão de parâmetros |
| `$(expr $a + $b)` | `$((a + b))` | Aritmética |
| `$(echo $var)` | `"$var"` | Uso direto |

---

## 17.3 Usar `while read` em vez de `for`

```bash
# Lento: for + substituição de comando
for line in $(cat file.txt); do
    process "$line"
done

# Rápido: while read
while IFS= read -r line; do
    process "$line"
done < file.txt
```

---

## 17.4 Processamento Paralelo

### Usar `&` e `wait`

```bash
#!/bin/bash

task1 &
task2 &
task3 &

wait

echo "Todas as tarefas completas"
```

### Usar `xargs -P`

```bash
# Sequencial
cat files.txt | xargs -I {} process {}

# Paralelo (4 concorrentes)
cat files.txt | xargs -P 4 -I {} process {}
```

---

## 17.5 Evitar Subshells

```bash
# Lento: subshell por iteração
for f in *.txt; do
    content=$(cat "$f")
    echo "$content" | wc -l
done

# Rápido: subshell único
while IFS= read -r f; do
    wc -l "$f"
done < <(ls *.txt)
```

---

## 17.6 Referência Rápida

| Otimização | Lento | Rápido |
|------------|-------|--------|
| Ler arquivo | `$(cat file)` | `$(<file)` ou `while read` |
| Caminho | `$(basename $f)` | `${f##*/}` |
| Matemática | `$(expr $a + $b)` | `$((a + b))` |
| Paralelo | sequencial | `&` + `wait` ou `xargs -P` |

---

## 17.7 Exercícios

1. Usar `time` para medir quanto tempo um loop que processa 1000 arquivos leva
2. Converter um script sequencial para processamento paralelo
3. Comparar desempenho de `$(cat file)` vs `while read`
4. Usar `xargs -P` para acelerar processamento em lote de imagens