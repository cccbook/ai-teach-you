# 13. Tests Automatises

---

## 13.1 Pourquoi Utiliser Shell pour les Tests

- Execution rapide de verifications simples
- Tester les commandes systeme et les scripts
- Tests d'integration dans CI/CD
- Tests de regression des scripts existants

---

## 13.2 Framework de Test de Base

```bash
#!/bin/bash
set -euo pipefail

TESTS_EXECUTES=0
TESTS_REUSSIS=0
TESTS_ECHOUES=0

test() {
    local nom=$1
    local commande=$2
    local attendu=$3
    
    ((TESTS_EXECUTES++))
    
    local actuel
    actuel=$(eval "$commande" 2>/dev/null)
    
    if [[ "$actuel" == "$attendu" ]]; then
        echo "OK $nom"
        ((TESTS_REUSSIS++))
    else
        echo "Echec $nom"
        echo "  Attendu : $attendu"
        echo "  Actuel : $actuel"
        ((TESTS_ECHOUES++))
    fi
}

test "Addition" "echo \$((1 + 1))" "2"
test "Chaine egale" "echo bonjour" "bonjour"

echo ""
echo "Resultats : $TESTS_REUSSIS/$TESTS_EXECUTES reussis"
[[ $TESTS_ECHOUES -eq 0 ]] || exit 1
```

---

## 13.3 Tester Fichiers et Repertoires

```bash
#!/bin/bash

test_fichier_existe() {
    local fichier=$1
    [[ -f "$fichier" ]] || { echo "Echec : Fichier non trouve : $fichier"; return 1; }
}

test_repertoire_existe() {
    local repertoire=$1
    [[ -d "$repertoire" ]] || { echo "Echec : Repertoire non trouve : $repertoire"; return 1; }
}

test_fichier_contient() {
    local fichier=$1
    local motif=$2
    grep -q "$motif" "$fichier" || { echo "Echec : Fichier manquant : $motif"; return 1; }
}
```

---

## 13.4 Tester la Sortie des Commandes

```bash
#!/bin/bash

test_succes() {
    local nom=$1
    shift
    if "$@"; then
        echo "OK $nom"
    else
        echo "Echec $nom (code de sortie : $?)"
        return 1
    fi
}

test_echec() {
    local nom=$1
    shift
    if ! "$@" 2>/dev/null; then
        echo "OK $nom (echec correct)"
    else
        echo "Echec $nom (devrait echouer mais a reussi)"
        return 1
    fi
}

test_sortie() {
    local nom=$1
    local attendu=$2
    shift 2
    
    local sortie=$("$@" 2>/dev/null)
    if [[ "$sortie" == *"$attendu"* ]]; then
        echo "OK $nom"
    else
        echo "Echec $nom"
        return 1
    fi
}
```

---

## 13.5 Script de Tests Compatible CI

```bash
cat > scripts/test.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ROUGE='\033[0;31m'
VERT='\033[0;32m'
NC='\033[0m'

ECHEC=0

executer_test() {
    local nom=$1
    local cmd=$2
    
    echo -n "Test : $nom ... "
    if eval "$cmd" &>/dev/null; then
        echo -e "${VERT}OK${NC}"
    else
        echo -e "${ROUGE}Echec${NC}"
        ((ECHEC++))
    fi
}

executer_test "Script init existe" "[[ -x scripts/init-project.sh ]]"
executer_test "Script build existe" "[[ -f scripts/build.sh ]]"
executer_test "Script deploy existe" "[[ -f scripts/deploy.sh ]]"

echo ""
if [[ $ECHEC -eq 0 ]]; then
    echo -e "${VERT}Tous les tests ont reussi${NC}"
    exit 0
else
    echo -e "${ROUGE}$ECHEC tests ont echoue${NC}"
    exit 1
fi
EOF

chmod +x scripts/test.sh
```

---

## 13.6 Exercices

1. Ecrire un framework de test avec les fonctions `test_eq`, `test_contient`, `test_succes`
2. Ecrire 5 cas de test pour un de vos scripts
3. Creer un script de tests compatible CI produisant un format TAP
4. Tester un script de traitement par lots pour s'assurer qu'il traite tous les fichiers correctement
