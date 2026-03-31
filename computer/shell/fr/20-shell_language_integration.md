# 20. Connecter Shell avec Autres Langages

---

## 20.1 Quelles Tâches Utiliser avec Shell ?

Tâches où Shell excelle :
- Opérations sur les fichiers
- Administration système
- Flux de travail d'automatisation
- Composition de pipelines
- Prototypage rapide

Tâches mieux adaptées à d'autres langages :
- Traitement de données complexe (Python, AWK)
- Programmation web (JavaScript, Go)
- Calcul numérique (Python, R, Julia)
- Programmation système (C, Rust)

---

## 20.2 Shell Appelle Python

### Invocation Simple

```bash
#!/bin/bash

# Appeler un script Python
python3 process_data.py input.csv

# Passer des arguments
python3 script.py arg1 arg2

# Obtenir la sortie
result=$(python3 -c "print('bonjour depuis python')")
echo "$result"
```

### Intégrer Python dans Shell

```bash
#!/bin/bash

python3 << 'PYEOF'
import csv

with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    total = sum(int(row['amount']) for row in reader)
    print(f"Total : {total}")
PYEOF
```

---

## 20.3 Python Appelle Shell

### Utiliser `subprocess`

```python
import subprocess

# Exécuter une commande simple
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Exécuter une commande complexe
result = subprocess.run(
    'find . -name "*.py" | wc -l',
    shell=True,
    capture_output=True,
    text=True
)
```

---

## 20.4 Shell Appelle JavaScript/Node.js

```bash
#!/bin/bash

# Exécuter une commande Node.js
node -e "console.log('bonjour depuis node')"

# Exécuter un script Node.js
node process-json.js data.json
```

---

## 20.5 Outils de Pont

### `jq` : Traitement JSON

```bash
# Parser JSON
echo '{"name": "Alice", "age": 25}' | jq '.name'

# Lire depuis un fichier
jq '.users[] | select(.age > 18)' data.json
```

### `yq` : Traitement YAML

```bash
# Parser YAML
yq '.database.host' config.yaml

# Convertir YAML en JSON
yq -o=json config.yaml
```

---

## 20.6 Référence Rapide

| Pont | Syntaxe |
|------|---------|
| Shell→Python | `python3 script.py` ou `python3 << PYEOF` |
| Python→Shell | `subprocess.run(['ls'])` |
| Shell→Node | `node script.js` ou `node << JSEOF` |
| Parser JSON | `jq '.key' fichier.json` |
| Parser YAML | `yq '.key' fichier.yaml` |
| Orchestrer | `make` |

---

## 20.7 Exercices

1. Utiliser Shell pour appeler Python et traiter un fichier CSV
2. Utiliser `subprocess` de Python pour exécuter des commandes Shell
3. Utiliser `jq` pour parser une réponse API JSON
4. Utiliser un Makefile pour orchestrer des tâches Shell, Python et Node.js
