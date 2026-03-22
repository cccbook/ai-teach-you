# 17. Optimisation des Performances

---

## 17.1 Pourquoi les Performances Shell Importent

Les scripts Shell sont souvent utilisés pour :
- Le traitement par lots d'un grand nombre de fichiers
- Les tâches d'automatisation
- Les pipelines CI/CD

Un script lent peut retarder l'ensemble du processus de plusieurs heures. Optimiser les scripts Shell peut améliorer considérablement l'efficacité.

---

## 17.2 Éviter les Commandes Externes

```bash
# Lent : commandes externes
for f in *.txt; do
    name=$(basename "$f")
    echo "$name"
done

# Rapide : commandes internes du shell
for f in *.txt; do
    echo "${f##*/}"
done
```

### Interne vs Externe

| Lent | Rapide | Description |
|------|--------|-------------|
| `$(cat fichier)` | `$(<fichier)` | Lecture directe |
| `$(basename $f)` | `${f##*/}` | Expansion de paramètre |
| `$(expr $a + $b)` | `$((a + b))` | Arithmétique |
| `$(echo $var)` | `"$var"` | Utilisation directe |

---

## 17.3 Utiliser `while read` au lieu de `for`

```bash
# Lent : for + substitution de commande
for line in $(cat fichier.txt); do
    process "$line"
done

# Rapide : while read
while IFS= read -r line; do
    process "$line"
done < fichier.txt
```

---

## 17.4 Traitement Parallèle

### Utiliser `&` et `wait`

```bash
#!/bin/bash

task1 &
task2 &
task3 &

wait

echo "Toutes les tâches terminées"
```

### Utiliser `xargs -P`

```bash
# Séquentiel
cat fichiers.txt | xargs -I {} process {}

# Parallèle (4 simultanés)
cat fichiers.txt | xargs -P 4 -I {} process {}
```

---

## 17.5 Éviter les Sous-shells

```bash
# Lent : sous-shell par itération
for f in *.txt; do
    content=$(cat "$f")
    echo "$content" | wc -l
done

# Rapide : sous-shell unique
while IFS= read -r f; do
    wc -l "$f"
done < <(ls *.txt)
```

---

## 17.6 Référence Rapide

| Optimisation | Lent | Rapide |
|--------------|------|--------|
| Lire fichier | `$(cat fichier)` | `$(<fichier)` ou `while read` |
| Chemin | `$(basename $f)` | `${f##*/}` |
| Maths | `$(expr $a + $b)` | `$((a + b))` |
| Parallèle | séquentiel | `&` + `wait` ou `xargs -P` |

---

## 17.7 Exercices

1. Utiliser `time` pour mesurer le temps d'une boucle traitant 1000 fichiers
2. Convertir un script séquentiel en traitement parallèle
3. Comparer les performances de `$(cat fichier)` vs `while read`
4. Utiliser `xargs -P` pour accélérer le traitement par lots d'images
