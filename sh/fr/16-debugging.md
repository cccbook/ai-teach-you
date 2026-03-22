# 16. Techniques de Débogage

---

## 16.1 L'État d'Esprit de Débogage de l'IA

Quand les humains rencontrent des erreurs : panique, recherche en ligne, copier-coller
Quand l'IA rencontre des erreurs : analyser le message, déduire la cause, exécuter le correctif

Flux de débogage de l'IA :
```
Observer la sortie d'erreur → Comprendre le type d'erreur → Localiser le problème → Corriger → Vérifier
```

---

## 16.2 `bash -x` : Tracer l'Exécution

Débogage le plus simple : ajouter le flag `-x`

```bash
bash -x script.sh
```

Affiche chaque ligne exécutée avec le préfixe `+` :

```bash
+ mkdir -p test
+ cd test
+ echo 'Bonjour'
Bonjour
```

### Déboguer Seulement une Section

```bash
#!/bin/bash

echo "Ceci ne s'affichera pas"
set -x
# Le débogage commence ici
name="Alice"
echo "Bonjour, $name"
set +x
# Le débogage se termine ici
echo "Ceci ne s'affichera pas"
```

---

## 16.3 Erreurs Courantes et Correctifs

### Erreur 1 : Permission Refusée

```bash
# Erreur
./script.sh
# Sortie : Permission denied

# Correctif
chmod +x script.sh
./script.sh
```

### Erreur 2 : Commande Non Trouvée

```bash
# Erreur
python script.py
# Sortie : command not found: python

# Correctif : utiliser le chemin complet
/usr/bin/python3 script.py
```

### Erreur 3 : Variable Non Définie

```bash
#!/bin/bash
set -u

echo $undefined_var
# Sortie : bash: undefined_var: unbound variable

# Correctif : donner une valeur par défaut
echo ${undefined_var:-defaut}
```

---

## 16.4 Débogage avec `echo`

Quand `-x` ne suffit pas, ajouter `echo` manuellement :

```bash
#!/bin/bash

echo "DEBUG : Entrée dans la fonction"
echo "DEBUG : Paramètre = $@"

process() {
    echo "DEBUG : Dans process"
    local result=$(expensive_command)
    echo "DEBUG : resultat = $result"
}
```

---

## 16.5 Référence Rapide

| Commande | Description |
|----------|-------------|
| `bash -n script.sh` | Vérifier la syntaxe uniquement |
| `bash -x script.sh` | Tracer l'exécution |
| `set -x` | Activer le mode débogage |
| `set +x` | Désactiver le mode débogage |
| `trap 'echo cmd' DEBUG` | Tracer chaque commande |

---

## 16.6 Exercices

1. Exécuter un script avec `bash -x` et observer le format de sortie
2. Utiliser `set -x` dans un script pour déboguer seulement une fonction spécifique
3. Trouver une commande qui échoue, analyser le message d'erreur et le corriger
4. Créer une gestion d'erreurs élégante avec `trap`
