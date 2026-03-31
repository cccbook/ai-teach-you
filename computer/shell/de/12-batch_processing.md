# 12. Stapelverarbeitung von Dateien

---

## 12.1 Stapel-Umbenennung

### Einfacher Ersetzen der Erweiterung

```bash
# Alle .txt in .md ändern
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

### Präfix hinzufügen

```bash
# thumb_ Präfix zu allen Bildern hinzufügen
for f in *.jpg *.png *.gif; do
    [[ -f "$f" ]] || continue
    mv "$f" "thumb_$f"
done
```

### Leerzeichen entfernen

```bash
# Leerzeichen in Dateinamen durch Unterstriche ersetzen
for f in *\ *; do
    [[ -f "$f" ]] || continue
    mv "$f" "${f// /_}"
done
```

### Nummern hinzufügen

```bash
# Dateien nummerieren 001, 002, 003...
i=1
for f in *.jpg; do
    [[ -f "$f" ]] || continue
    mv "$f" "$(printf '%03d.jpg' $i)"
    ((i++))
done
```

---

## 12.2 Stapel-Bildverarbeitung

```bash
#!/bin/bash
set -euo pipefail

SIZE=${1:-800}

for img in *.jpg *.png; do
    [[ -f "$img" ]] || continue
    
    echo "Verarbeite: $img"
    
    if command -v convert &>/dev/null; then
        # Thumbnail erstellen
        convert "$img" -resize "${SIZE}x${SIZE}>" "thumb_$img"
        
        # Große Version erstellen
        convert "$img" -resize 1920x1080 "large_$img"
        
        echo "✓ Fertig: thumb_$img, large_$img"
    fi
done
```

---

## 12.3 Stapel-Suchen und Ersetzen

```bash
#!/bin/bash

# "foo" durch "bar" in allen .txt Dateien ersetzen
for f in *.txt; do
    [[ -f "$f" ]] || continue
    sed -i.bak 's/foo/bar/g' "$f"
done
```

---

## 12.4 Stapel-Komprimierung

```bash
#!/bin/bash

# Jede Datei komprimieren
for f in *.txt; do
    [[ -f "$f" ]] || continue
    gzip "$f"
done

# Alle dekomprimieren
gunzip *.gz
```

---

## 12.5 Stapel-Download

```bash
#!/bin/bash
set -euo pipefail

while read -r url; do
    filename=$(basename "$url")
    echo "Lade herunter: $url"
    curl -L -o "$filename" "$url"
done < urls.txt
```

---

## 12.6 Kurzreferenz

| Aufgabe | Befehl |
|---------|--------|
| Erweiterung ändern | `mv "$f" "${f%.old}.new"` |
| Präfix hinzufügen | `mv "$f" "praefix_$f"` |
| Leerzeichen entfernen | `mv "$f" "${f// /_}"` |
| Nummern hinzufügen | `mv "$f" "$(printf '%03d' $i)"` |
| Stapel ersetzen | `for f in *.txt; do sed -i 's/a/b/g' "$f"; done` |
| Stapel komprimieren | `for f in *.txt; do gzip "$f"; done` |
| Stapel download | `while read url; do curl -LO "$url"; done < urls.txt` |

---

## 12.7 Übungen

1. 10 Dateien stapelweise von `.txt` in `.md` umbenennen
2. `thumb_` Präfix zu allen Bildern hinzufügen und Thumbnails erstellen
3. `altes-site.com` durch `neues-site.com` in allen `.html` Dateien ersetzen
4. Ein Bereinigungsskript erstellen, das alle `__pycache__`, `.pyc` und `.log` Dateien löscht
