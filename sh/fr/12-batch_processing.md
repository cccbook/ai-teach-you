# 12. Traitement par Lots de Fichiers

---

## 12.1 Renommage par Lots

### Remplacement Simple d'Extension

```bash
# Changer tous les .txt en .md
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

### Ajouter un Prefixe

```bash
# Ajouter le prefixe thumb_ a toutes les images
for f in *.jpg *.png *.gif; do
    [[ -f "$f" ]] || continue
    mv "$f" "thumb_$f"
done
```

### Supprimer les Espaces

```bash
# Remplacer les espaces dans les noms de fichiers par des underscores
for f in *\ *; do
    [[ -f "$f" ]] || continue
    mv "$f" "${f// /_}"
done
```

### Ajouter des Nombres

```bash
# Numeroter les fichiers 001, 002, 003...
i=1
for f in *.jpg; do
    [[ -f "$f" ]] || continue
    mv "$f" "$(printf '%03d.jpg' $i)"
    ((i++))
done
```

---

## 12.2 Traitement d'Images par Lots

```bash
#!/bin/bash
set -euo pipefail

TAILLE=${1:-800}

for img in *.jpg *.png; do
    [[ -f "$img" ]] || continue
    
    echo "Traitement : $img"
    
    if command -v convert &>/dev/null; then
        # Creer une miniature
        convert "$img" -resize "${TAILLE}x${TAILLE}>" "thumb_$img"
        
        # Creer une grande version
        convert "$img" -resize 1920x1080 "large_$img"
        
        echo "Fait : thumb_$img, large_$img"
    fi
done
```

---

## 12.3 Recherche et Remplacement par Lots

```bash
#!/bin/bash

# Remplacer "foo" par "bar" dans tous les fichiers .txt
for f in *.txt; do
    [[ -f "$f" ]] || continue
    sed -i.bak 's/foo/bar/g' "$f"
done
```

---

## 12.4 Compression par Lots

```bash
#!/bin/bash

# Compresser chaque fichier
for f in *.txt; do
    [[ -f "$f" ]] || continue
    gzip "$f"
done

# Decompresser tous
gunzip *.gz
```

---

## 12.5 Telechargement par Lots

```bash
#!/bin/bash
set -euo pipefail

while read -r url; do
    nomfichier=$(basename "$url")
    echo "Telechargement : $url"
    curl -L -o "$nomfichier" "$url"
done < urls.txt
```

---

## 12.6 Reference Rapide

| Tache | Commande |
|------|---------|
| Changer d'extension | `mv "$f" "${f%.old}.new"` |
| Ajouter un prefixe | `mv "$f" "prefixe_$f"` |
| Supprimer les espaces | `mv "$f" "${f// /_}"` |
| Ajouter des nombres | `mv "$f" "$(printf '%03d' $i)"` |
| Remplacement par lots | `for f in *.txt; do sed -i 's/a/b/g' "$f"; done` |
| Compression par lots | `for f in *.txt; do gzip "$f"; done` |
| Telechargement par lots | `while read url; do curl -LO "$url"; done < urls.txt` |

---

## 12.7 Exercices

1. Renommer par lots 10 fichiers de `.txt` en `.md`
2. Ajouter le prefixe `thumb_` a toutes les images et creer des miniatures
3. Remplacer `ancien-site.com` par `nouveau-site.com` dans tous les fichiers `.html`
4. Creer un script de nettoyage qui supprime tous les fichiers `__pycache__`, `.pyc` et `.log`
