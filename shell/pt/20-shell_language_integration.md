# 20. Conectando Shell com Outras Linguagens

---

## 20.1 Que Tarefas Devem Usar Shell

Tarefas que Shell excelsa:
- Operações de arquivo
- Administração de sistemas
- Fluxos de automação
- Composição de pipeline
- Protótipos rápidos

Tarefas mais adequadas para outras linguagens:
- Processamento de dados complexos (Python, AWK)
- Programação web (JavaScript, Go)
- Computação numérica (Python, R, Julia)
- Programação de sistemas (C, Rust)

---

## 20.2 Shell Chama Python

### Invocação Simples

```bash
#!/bin/bash

# Chamar script Python
python3 process_data.py input.csv

# Passar argumentos
python3 script.py arg1 arg2

# Obter saída
result=$(python3 -c "print('hello from python')")
echo "$result"
```

### Embedar Python no Shell

```bash
#!/bin/bash

python3 << 'PYEOF'
import csv

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    total = sum(int(row['amount']) for row in reader)
    print(f"Total: {total}")
PYEOF
```

---

## 20.3 Python Chama Shell

### Usando `subprocess`

```python
import subprocess

# Executar comando simples
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Executar comando complexo
result = subprocess.run(
    'find . -name "*.py" | wc -l',
    shell=True,
    capture_output=True,
    text=True
)
```

---

## 20.4 Shell Chama JavaScript/Node.js

```bash
#!/bin/bash

# Executar comando Node.js
node -e "console.log('hello from node')"

# Executar script Node.js
node process-json.js data.json
```

---

## 20.5 Ferramentas de Ponte

### `jq`: Processamento JSON

```bash
# Parsear JSON
echo '{"name": "Alice", "age": 25}' | jq '.name'

# Ler de arquivo
jq '.users[] | select(.age > 18)' data.json
```

### `yq`: Processamento YAML

```bash
# Parsear YAML
yq '.database.host' config.yaml

# Converter YAML para JSON
yq -o=json config.yaml
```

---

## 20.6 Referência Rápida

| Ponte | Sintaxe |
|--------|--------|
| Shell→Python | `python3 script.py` ou `python3 << PYEOF` |
| Python→Shell | `subprocess.run(['ls'])` |
| Shell→Node | `node script.js` ou `node << JSEOF` |
| Parse JSON | `jq '.key' file.json` |
| Parse YAML | `yq '.key' file.yaml` |
| Orquestrar | `make` |

---

## 20.7 Exercícios

1. Usar Shell para chamar Python para processar um arquivo CSV
2. Usar `subprocess` do Python para executar comandos Shell
3. Usar `jq` para parsear uma resposta de API JSON
4. Usar Makefile para orquestrar tarefas Shell, Python e Node.js