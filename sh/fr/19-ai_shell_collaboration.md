# 19. Mode de Collaboration IA + Shell

---

## 19.1 Nouvelle Forme de Collaboration Humain-Machine

Programmation traditionnelle :
- Les humains tapent au clavier
- Les humains utilisent la souris pour manipuler l'IDE
- Les humains exécutent et testent

Programmation à l'ère de l'IA :
- Les humains décrivent les besoins
- L'IA génère des commandes Shell et des scripts
- Les humains examinent et exécutent
- Les humains et l'IA déboguent ensemble

---

## 19.2 Décrire les Besoins à l'IA

### Bonnes Descriptions

```bash
# Tâche claire
"Trouver tous les fichiers .log de plus de 100 Mo dans /var/log"

# Inclure le format de sortie attendu
"Lister tous les fichiers .py, en montrant : nombre_lignes nom_fichier par ligne"

# Préciser les contraintes
"Compresser tous les fichiers .txt, mais exclure ceux contenant 'test'"
```

### Mauvaises Descriptions

```bash
# Trop vague
"aide-moi à traiter les logs"

# Irréaliste
"aide-moi à écrire un système d'exploitation"
```

---

## 19.3 Motifs de Commandes Shell Générées par l'IA

### Motif 1 : Commande Unique

```bash
# Humain demande : trouver les 10 fichiers Python avec le plus de lignes
find . -name "*.py" -exec wc -l {} + | sort -rn | head -10
```

### Motif 2 : Script Shell

```bash
# Humain demande : traiter des images par lots
cat > process_images.sh << 'EOF'
#!/bin/bash
for img in *.jpg; do
    convert "$img" -resize 800x600 "thumb_$img"
done
EOF
```

---

## 19.4 Développement Itératif

### Tour 1 : Générer la Version Initiale

```bash
# Humain : écrire un script de sauvegarde
# L'IA génère une version initiale, puis l'humain teste et signale des problèmes :

# Humain : bien, mais il faut un mode --dry-run
```

### Tour 2 : Ajouter des Fonctionnalités

```bash
# Humain : ajouter aussi la gestion d'erreurs et la journalisation
```

### Tour 3 : Déboguer

```bash
# Humain : j'ai une erreur 'Permission denied' après exécution
# L'IA : corrige le problème...
```

---

## 19.5 Faire Aider par l'IA pour Déboguer

```bash
# Humain : j'ai une erreur après avoir exécuté cette commande
$ ./deploy.sh
# Sortie : /bin/bash^M: bad interpreter: No such file or directory

# L'IA : c'est un problème de fin de ligne Windows. Exécutez :
sed -i 's/\r$//' deploy.sh
```

---

## 19.6 Outils de Collaboration Recommandés

### Multiplexeur de Terminal

```bash
# tmux : diviser les fenêtres
tmux new -s masession
# Ctrl+b %  # division verticale
# Ctrl+b "  # division horizontale
```

---

## 19.7 Exercices

1. Décrire une tâche complexe et faire générer des commandes Shell par l'IA
2. Faire examiner un script existant par l'IA pour des problèmes de sécurité
3. Utiliser l'itération pour faire écrire un outil pratique par l'IA
4. Faire expliquer par l'IA du code Shell que vous ne comprenez pas
