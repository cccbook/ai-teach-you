# 3. Dateioperationen

---

## 3.1 Das mentale Modell der KI vom Dateisystem

Bevor wir uns in jeden Befehl vertiefen, verstehen Sie, wie die KI das Dateisystem sieht.

Menschliche Ingenieure sehen das Dateisystem typischerweise **visuell** - wie Windows Explorer oder macOS Finder, verstehen durch Icons und Ordnerformen.

Die Sicht der KI ist völlig anders:

```
Pfad           = absoluter Speicherort /home/user/project/src/main.py
relativ        = vom aktuellen Standort nach unten gehen
Knoten         = jede Datei oder jedes Verzeichnis ist ein "Knoten"
Attribute      = Berechtigungen, Größe, Zeitstempel, Eigentümer
Typ            = reguläre Datei(-), Verzeichnis(d), Link(l), Gerät(b/c)
```

Wenn die KI `ls -la` ausführt, sieht sie:

```
drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
-rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
-rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
-rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json
```

Die KI kann sofort daraus lesen:
- Welche sind Verzeichnisse (`d`)
- Welche sind versteckte Dateien (beginnend mit `.`)
- Wer hat welche Berechtigungen
- Dateigrößen (bestimmen, ob große Dateien)
- Letzte Änderungszeit

---

## 3.2 `ls`: Der am häufigsten verwendete erste Befehl der KI

Fast vor jeder Operation führt die KI `ls` aus, um den aktuellen Zustand zu bestätigen.

### Die häufigsten `ls`-Kombinationen der KI

```bash
# Grundlegendes Auflisten
ls

# Versteckte Dateien anzeigen (sehr wichtig!)
ls -a

# Lange Auflistung (detaillierte Info)
ls -l

# Lange Auflistung + versteckte Dateien (am häufigsten)
ls -la

# Nach Änderungszeit sortieren (neueste zuerst)
ls -lt

# Nach Änderungszeit sortieren (älteste zuerst)
ls -ltr

# Menschenlesbare Größen (K, M, G)
ls -lh

# Nur Verzeichnisse anzeigen
ls -d */

# Rekursiv alle Dateien anzeigen
ls -R

# Inode-Nummern anzeigen (nützlich für Hardlinks)
ls -li
```

### Der tatsächliche Workflow der KI

```bash
cd ~/project && ls -la

# Ergebnis:
# drwxr-xr-x  5 ai  staff  170 Mar 22 10:30 .
# drwxr-xr-x  3 ai  staff  102 Mar 22 09:00 ..
# -rw-r--r--  1 ai  staff  4096 Mar 22 10:30 .env
# -rw-r--r--  1 ai  staff  8192 Mar 22 10:31 README.md
# drwxr-xr-x  3 ai  staff   96 Mar 22 10:30 src
# drwxr-xr-x  2 ai  staff   64 Mar 22 10:30 tests
# -rw-r--r--  1 ai  staff  2048 Mar 22 10:32 package.json

# Analyse der KI: Es gibt eine .env-Datei, src- und tests-Verzeichnisse, package.json
# Das ist ein Node.js-Projekt
```

---

## 3.3 `cd`: Das Verzeichnis, das die KI nie vergisst

### Die `cd`-Gewohnheiten der KI

```bash
# Ins Home-Verzeichnis gehen
cd ~

# Ins vorherige Verzeichnis gehen (sehr nützlich!)
cd -

# Ins übergeordnete Verzeichnis gehen
cd ..

# In Unterverzeichnis gehen
cd src

# Tiefe Pfade navigieren (Verdienst der Tab-Vervollständigung)
cd ~/project/backend/api/v2/routes
```

### Das `cd` + `&&`-Muster der KI

Dies ist eines der häufigsten Muster der KI:

```bash
# Zuerst cd, nächsten Befehl nur ausführen nach Bestätigung des Erfolgs
cd ~/project && ls -la
```

### Häufige Fehler

```bash
# Fehler: Verzeichnis existiert nicht bestätigen
cd nonexistent
# Ausgabe: bash: cd: nonexistent: No such file or directory

# Ansatz der KI: Zuerst prüfen
[ -d "nonexistent" ] && cd nonexistent || echo "Verzeichnis existiert nicht"
```

---

## 3.4 `mkdir`: Die Kunst, Verzeichnisse zu erstellen

### Grundlegende Verwendung

```bash
# Einzelnes Verzeichnis erstellen
mkdir myproject

# Mehrere Verzeichnisse erstellen
mkdir src tests docs

# Verschachtelte Verzeichnisse erstellen (-p ist der Schlüssel!)
mkdir -p project/src/components project/tests
```

### Warum die KI fast immer `-p` verwendet

Das `-p` (parents)-Flag bedeutet:
1. Wenn das Verzeichnis existiert, **kein Fehler**
2. Wenn das übergeordnete Verzeichnis nicht existiert, **automatisch erstellen**

### Das typische Projekterstellungsmuster der KI

```bash
# Eine Standard-Projektstruktur erstellen
mkdir -p project/{src,tests,docs,scripts,config}
```

---

## 3.5 `rm`: Die Kunst des Löschens

**Warnung**: Dies ist einer der gefährlichsten Befehle in Shell.

### Grundlegende Verwendung

```bash
# Datei löschen
rm file.txt

# Verzeichnis löschen (braucht -r)
rm -r directory/

# Verzeichnis und alles löschen (gefährlich!)
rm -rf directory/
```

### Die Gefahr von `rm -rf`

```bash
# Niemals als root ausführen!
# rm -rf /

# Wenn Sie versehentlich ein zusätzliches Leerzeichen hinzufügen:
rm -rf * 
# (Leerzeichen) = rm -rf löscht alles im aktuellen Verzeichnis
```

---

## 3.6 `cp`: Dateien und Verzeichnisse kopieren

### Grundlegende Verwendung

```bash
# Datei kopieren
cp source.txt destination.txt

# Verzeichnis kopieren (braucht -r)
cp -r source_directory/ destination_directory/

# Fortschritt beim Kopieren anzeigen (-v verbose)
cp -v large_file.iso /backup/

# Interaktiver Modus (vor Überschreiben fragen)
cp -i *.py src/
```

### Die Kraft von Wildcards

```bash
# Alle .txt-Dateien kopieren
cp *.txt backup/

# Alle Bilddateien kopieren
cp *.{jpg,png,gif,webp} images/
```

---

## 3.7 `mv`: Verschieben und Umbenennen

### Grundlegende Verwendung

```bash
# Datei verschieben
mv file.txt backup/

# Verschieben und umbenennen
mv oldname.txt newname.txt

# Stapelweise umbenennen
for f in *.txt; do
    mv "$f" "${f%.txt}.md"
done
```

---

## 3.8 Schnellreferenz

| Befehl | Grundlegende Verwendung | Häufige Flags | KI-Hinweis |
|--------|------------------------|---------------|------------|
| `ls` | `ls [Pfad]` | `-l` lang, `-a` versteckt, `-h` menschlich | `ls -la` ist immer gut |
| `cd` | `cd [Pfad]` | `-` vorheriges, `..` übergeordnetes | `cd xxx &&` ist gute Gewohnheit |
| `mkdir` | `mkdir [Verz]` | `-p` verschachtelt | fast immer `-p` verwenden |
| `rm` | `rm [Datei]` | `-r` rekursiv, `-f` erzwingen | auf `rm -rf /*` achten |
| `cp` | `cp [Qu] [Zi]` | `-r` Verzeichnis, `-i` fragen, `-p` erhalten | `-i` zur Sicherheit verwenden |
| `mv` | `mv [Qu] [Zi]` | `-i` fragen, `-n` nicht überschreiben | das ist Umbenennen |

---

## 3.9 Übungen

1. Verwenden Sie `mkdir -p`, um ein dreistufig verschachteltes Verzeichnis zu erstellen, bestätigen Sie dann mit `tree` oder `find`
2. Kopieren Sie eine große Datei mit `cp -v` und sehen Sie die Ausgabe
3. Benennen Sie 10 `.txt`-Dateien stapelweise mit `mv` zu `.md` um
4. Löschen Sie eine Testdatei mit `rm -i`, um die Eingabeaufforderung zu erleben
