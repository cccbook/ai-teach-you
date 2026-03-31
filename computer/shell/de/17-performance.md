# 17. Leistungsoptimierung

---

## 17.1 Warum Shell-Performance wichtig ist

Shell-Skripte werden oft verwendet für:
- Stapelverarbeitung großer Dateimengen
- Automatisierungsaufgaben
- CI/CD-Pipelines

Ein langsames Skript kann den gesamten Prozess um Stunden verzögern. Die Optimierung von Shell-Skripten kann die Effizienz erheblich verbessern.

---

## 17.2 Externe Befehle vermeiden

```bash
# Langsam: externe Befehle
for f in *.txt; do
    name=$(basename "$f")
    echo "$name"
done

# Schnell: Shell-Builtins
for f in *.txt; do
    echo "${f##*/}"
done
```

### Builtin vs. Extern

| Langsam | Schnell | Beschreibung |
|---------|---------|-------------|
| `$(cat datei)` | `$(<datei)` | Direktes Lesen |
| `$(basename $f)` | `${f##*/}` | Parametererweiterung |
| `$(expr $a + $b)` | `$((a + b))` | Arithmetik |
| `$(echo $var)` | `"$var"` | Direkte Verwendung |

---

## 17.3 `while read` statt `for` verwenden

```bash
# Langsam: for + Kommando-Substitution
for line in $(cat datei.txt); do
    process "$line"
done

# Schnell: while read
while IFS= read -r line; do
    process "$line"
done < datei.txt
```

---

## 17.4 Parallelverarbeitung

### `&` und `wait` verwenden

```bash
#!/bin/bash

task1 &
task2 &
task3 &

wait

echo "Alle Aufgaben abgeschlossen"
```

### `xargs -P` verwenden

```bash
# Sequenziell
cat dateien.txt | xargs -I {} process {}

# Parallel (4 gleichzeitig)
cat dateien.txt | xargs -P 4 -I {} process {}
```

---

## 17.5 Subshells vermeiden

```bash
# Langsam: Subshell pro Iteration
for f in *.txt; do
    content=$(cat "$f")
    echo "$content" | wc -l
done

# Schnell: einzelne Subshell
while IFS= read -r f; do
    wc -l "$f"
done < <(ls *.txt)
```

---

## 17.6 Kurzreferenz

| Optimierung | Langsam | Schnell |
|-------------|---------|---------|
| Datei lesen | `$(cat datei)` | `$(<datei)` oder `while read` |
| Pfad | `$(basename $f)` | `${f##*/}` |
| Mathe | `$(expr $a + $b)` | `$((a + b))` |
| Parallel | sequenziell | `&` + `wait` oder `xargs -P` |

---

## 17.7 Übungen

1. Verwende `time`, um zu messen, wie lange ein Loop mit 1000 Dateien dauert
2. Wandle ein sequenzielles Skript in Parallelverarbeitung um
3. Vergleiche die Leistung von `$(cat datei)` vs. `while read`
4. Verwende `xargs -P`, um die Stapelverarbeitung von Bildern zu beschleunigen
