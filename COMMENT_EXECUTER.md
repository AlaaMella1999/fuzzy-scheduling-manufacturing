# 🚀 COMMENT EXÉCUTER LE PROJET

## ⚡ DÉMARRAGE RAPIDE (3 commandes)

### 1. Ouvrir PowerShell dans VS Code

```
Appuyez sur: Ctrl + `
```

### 2. Activer l'environnement virtuel

```powershell
.\.venv\Scripts\Activate.ps1
```

✅ Vous devez voir `(.venv)` avant votre ligne de commande

### 3. Lancer l'application

```powershell
python -m src.main --no-db
```

---

## 📋 COMMANDES PRINCIPALES

### ✅ Exécution normale (avec tous les exports)

```powershell
python -m src.main --no-db
```

**Ce qui se passe:**

- Crée 8 tâches et 3 machines
- Ordonnance avec logique floue
- Affiche les résultats
- Exporte vers CSV, JSON et TXT dans `data/`

### ✅ Comparer différents algorithmes

#### Algorithme Fuzzy (logique floue - par défaut)

```powershell
python -m src.main --algorithm fuzzy --no-db
```

#### Algorithme FCFS (First Come First Served)

```powershell
python -m src.main --algorithm fcfs --no-db
```

#### Algorithme EDD (Earliest Due Date)

```powershell
python -m src.main --algorithm edd --no-db
```

### ✅ Exécuter les tests

```powershell
pytest
```

Résultat: `51 passed in 2.83s`

### ✅ Tests avec détails

```powershell
pytest -v
```

### ✅ Tests avec couverture de code

```powershell
pytest --cov=src
```

---

## 📁 VOIR LES RÉSULTATS

### Lister les fichiers générés

```powershell
ls data/
```

### Voir le rapport texte

```powershell
cat data/schedule_report.txt
```

### Voir le CSV

```powershell
cat data/scheduled_jobs.csv
```

### Voir le JSON

```powershell
cat data/schedule.json
```

---

## 🔧 RÉSOLUTION DE PROBLÈMES

### ❌ Problème: "cannot be loaded because running scripts is disabled"

**Solution:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Puis réessayez d'activer l'environnement.

### ❌ Problème: "UNIQUE constraint failed"

**Solution:** Supprimer la base de données existante

```powershell
Remove-Item data/scheduling.db -Force
python -m src.main --no-db
```

### ❌ Problème: "No module named 'src'"

**Solution:** Vérifier que vous êtes dans le bon dossier

```powershell
cd "c:\Users\CATECH\OneDrive\Bureau\projet PFT"
.\.venv\Scripts\Activate.ps1
python -m src.main --no-db
```

### ❌ Problème: L'environnement virtuel ne s'active pas

**Solution:** Utiliser Python directement

```powershell
.\.venv\Scripts\python.exe -m src.main --no-db
```

---

## 🎯 SCÉNARIO DE DÉMONSTRATION DEVANT LE PROF

### **Étape 1: Ouvrir le terminal** (10 secondes)

```
Ctrl + `
```

### **Étape 2: Activer l'environnement** (5 secondes)

```powershell
.\.venv\Scripts\Activate.ps1
```

### **Étape 3: Lancer la démo principale** (30 secondes)

```powershell
python -m src.main --no-db
```

**Expliquer pendant l'exécution:**

- "8 tâches créées avec différentes durées et échéances"
- "L'algorithme calcule une priorité avec logique floue"
- "Résultat: ordonnancement optimal avec 62.5% de tâches à temps"

### **Étape 4: Montrer les fichiers générés** (20 secondes)

```powershell
ls data/
cat data/schedule_report.txt
```

### **Étape 5: Comparer avec un autre algorithme** (30 secondes)

```powershell
python -m src.main --algorithm fcfs --no-db
```

**Dire:** "Avec FCFS (First Come First Served), les résultats sont différents"

### **Étape 6: Montrer les tests** (20 secondes)

```powershell
pytest
```

**Dire:** "51 tests unitaires qui valident toutes les fonctionnalités"

### **Étape 7: Montrer le code** (60 secondes)

```powershell
code src/fuzzy_logic.py
```

**Montrer:**

- Les classes (ligne 10-50)
- Le système d'inférence (ligne 200-250)

**TOTAL: 3 minutes de démonstration !**

---

## 📊 OPTIONS DISPONIBLES

### Aide complète

```powershell
python -m src.main --help
```

### Toutes les options

```
Options:
  --algorithm {fuzzy,fcfs,edd}   Algorithme d'ordonnancement (défaut: fuzzy)
  --no-db                         Ne pas sauvegarder en base de données
  --no-export                     Ne pas exporter les fichiers
```

### Exemples combinés

```powershell
# Fuzzy sans base de données ni export
python -m src.main --algorithm fuzzy --no-db --no-export

# EDD avec export mais sans base
python -m src.main --algorithm edd --no-db

# FCFS avec tout
python -m src.main --algorithm fcfs --no-db
```

---

## 📦 VÉRIFIER L'INSTALLATION

### Vérifier Python

```powershell
python --version
```

Devrait afficher: `Python 3.13.1` ou similaire

### Vérifier les packages installés

```powershell
pip list
```

Devrait inclure:

- numpy
- pandas
- matplotlib
- scikit-fuzzy
- SQLAlchemy
- pytest

### Réinstaller les dépendances si nécessaire

```powershell
pip install -r requirements.txt
```

---

## 🎓 STRUCTURE DU PROJET

```
projet PFT/
├── src/                    ← Code source
│   ├── fuzzy_logic.py     ← Logique floue
│   ├── job.py             ← Modèles Job/Machine
│   ├── scheduler.py       ← Algorithmes d'ordonnancement
│   ├── database.py        ← Gestion base de données
│   ├── utils.py           ← Fonctions utilitaires
│   └── main.py            ← Point d'entrée
├── tests/                  ← Tests unitaires (51 tests)
├── data/                   ← Fichiers générés (CSV, JSON, TXT)
├── docs/                   ← Documentation technique
├── examples/               ← Exemples d'utilisation
└── requirements.txt        ← Dépendances Python
```

---

## ✅ CHECKLIST AVANT DÉMONSTRATION

- [ ] Terminal PowerShell ouvert dans VS Code
- [ ] Dans le bon dossier (`projet PFT`)
- [ ] Environnement virtuel activé (`.venv`)
- [ ] Commande de test fonctionne: `python -m src.main --no-db`
- [ ] Tests passent: `pytest`
- [ ] Fichiers dans `data/` sont générés
- [ ] Code source ouvert dans VS Code

---

## 💡 COMMANDES MÉMO (à imprimer)

```powershell
# 1. ACTIVER L'ENVIRONNEMENT
.\.venv\Scripts\Activate.ps1

# 2. DÉMO PRINCIPALE
python -m src.main --no-db

# 3. TESTS
pytest

# 4. AUTRES ALGORITHMES
python -m src.main --algorithm fcfs --no-db
python -m src.main --algorithm edd --no-db

# 5. VOIR LES RÉSULTATS
ls data/
cat data/schedule_report.txt

# 6. NETTOYER
Remove-Item data/scheduling.db -Force
```

---

## 🎯 EN RÉSUMÉ

### Pour exécuter normalement:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.main --no-db
```

### Pour la démonstration:

1. Activer environnement
2. Lancer `python -m src.main --no-db`
3. Montrer les résultats
4. Lancer `pytest`
5. Montrer le code

**C'EST TOUT ! 🚀**
