# 13. Automatisierte Tests

---

## 13.1 Warum Shell für Tests verwenden

- Schnelle Ausführung einfacher Verifikationen
- Testen von Systembefehlen und Skripten
- Integrationstests in CI/CD
- Regressionstests bestehender Skripte

---

## 13.2 Grundlegendes Test-Framework

```bash
#!/bin/bash
set -euo pipefail

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

test() {
    local name=$1
    local command=$2
    local expected=$3
    
    ((TESTS_RUN++))
    
    local actual
    actual=$(eval "$command" 2>/dev/null)
    
    if [[ "$actual" == "$expected" ]]; then
        echo "✓ $name"
        ((TESTS_PASSED++))
    else
        echo "✗ $name"
        echo "  Erwartet: $expected"
        echo "  Tatsaechlich: $actual"
        ((TESTS_FAILED++))
    fi
}

test "Addition" "echo \$((1 + 1))" "2"
test "Zeichenkette gleich" "echo hallo" "hallo"

echo ""
echo "Ergebnisse: $TESTS_PASSED/$TESTS_RUN bestanden"
[[ $TESTS_FAILED -eq 0 ]] || exit 1
```

---

## 13.3 Testen von Dateien und Verzeichnissen

```bash
#!/bin/bash

test_datei_existiert() {
    local datei=$1
    [[ -f "$datei" ]] || { echo "✗ Datei nicht gefunden: $datei"; return 1; }
}

test_verzeichnis_existiert() {
    local verzeichnis=$1
    [[ -d "$verzeichnis" ]] || { echo "✗ Verzeichnis nicht gefunden: $verzeichnis"; return 1; }
}

test_datei_enthält() {
    local datei=$1
    local muster=$2
    grep -q "$muster" "$datei" || { echo "✗ Datei enthält nicht: $muster"; return 1; }
}
```

---

## 13.4 Testen von Befehlsausgaben

```bash
#!/bin/bash

test_erfolg() {
    local name=$1
    shift
    if "$@"; then
        echo "✓ $name"
    else
        echo "✗ $name (Exit-Code: $?)"
        return 1
    fi
}

test_fehler() {
    local name=$1
    shift
    if ! "$@" 2>/dev/null; then
        echo "✓ $name (korrekt fehlgeschlagen)"
    else
        echo "✗ $name (sollte fehlschlagen, war aber erfolgreich)"
        return 1
    fi
}

test_ausgabe() {
    local name=$1
    local expected=$2
    shift 2
    
    local output=$("$@" 2>/dev/null)
    if [[ "$output" == *"$expected"* ]]; then
        echo "✓ $name"
    else
        echo "✗ $name"
        return 1
    fi
}
```

---

## 13.5 CI-freundliches Testskript

```bash
cat > scripts/test.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ROT='\033[0;31m'
GRUEN='\033[0;32m'
NC='\033[0m'

FAILED=0

run_test() {
    local name=$1
    local cmd=$2
    
    echo -n "Test: $name ... "
    if eval "$cmd" &>/dev/null; then
        echo -e "${GRUEN}✓${NC}"
    else
        echo -e "${ROT}✗${NC}"
        ((FAILED++))
    fi
}

run_test "Init-Skript existiert" "[[ -x scripts/init-project.sh ]]"
run_test "Build-Skript existiert" "[[ -f scripts/build.sh ]]"
run_test "Deploy-Skript existiert" "[[ -f scripts/deploy.sh ]]"

echo ""
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GRUEN}✅ Alle Tests bestanden${NC}"
    exit 0
else
    echo -e "${ROT}❌ $FAILED Tests fehlgeschlagen${NC}"
    exit 1
fi
EOF

chmod +x scripts/test.sh
```

---

## 13.6 Übungen

1. Schreibe ein Test-Framework mit `test_eq`, `test_enthält`, `test_erfolg` Funktionen
2. Schreibe 5 Testfälle für eines deiner Skripte
3. Erstelle ein CI-freundliches Testskript, das TAP-Format ausgibt
4. Teste ein Stapelverarbeitungsskript, um sicherzustellen, dass es alle Dateien korrekt bearbeitet
