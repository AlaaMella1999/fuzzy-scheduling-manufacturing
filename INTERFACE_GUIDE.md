# 🖥️ GUIDE D'UTILISATION - INTERFACE GRAPHIQUE

## 🚀 LANCEMENT DE L'INTERFACE GRAPHIQUE

### Méthode 1: Commande simple

```powershell
# Activer l'environnement
.\.venv\Scripts\Activate.ps1

# Lancer l'interface graphique
python -m src.gui
```

### Méthode 2: Depuis Python

```powershell
python src/gui.py
```

---

## 📸 APERÇU DE L'INTERFACE

```
┌─────────────────────────────────────────────────────────────────────┐
│              🏭 Fuzzy Manufacturing Scheduler                       │
├──────────────────────┬──────────────────────────────────────────────┤
│   CONTROL PANEL      │         SCHEDULING RESULTS                   │
│                      │                                              │
│ Algorithm:           │  Job ID │ Name    │ Priority │ Machine │... │
│ ○ Fuzzy Priority     │  J001   │ Engine  │ 75.50    │ M1      │... │
│ ○ FCFS               │  J002   │ Gear    │ 68.20    │ M3      │... │
│ ○ EDD                │  ...    │ ...     │ ...      │ ...     │... │
│                      │                                              │
│ [🚀 Run Scheduling]  │                                              │
│ [📊 Show Gantt Chart]│                                              │
│ [💾 Export Results]  │                                              │
│ [🔄 Reset Data]      │                                              │
│                      │                                              │
│ Statistics:          │                                              │
│ ┌──────────────────┐ │                                              │
│ │ Total Jobs: 8    │ │                                              │
│ │ Makespan: 32h    │ │                                              │
│ │ On-Time: 62.5%   │ │                                              │
│ │ M1: 80%          │ │                                              │
│ │ M2: 65%          │ │                                              │
│ └──────────────────┘ │                                              │
├──────────────────────┴──────────────────────────────────────────────┤
│                     AVAILABLE JOBS                                  │
│ Job ID │ Name              │ Processing │ Due Date    │ Machine │   │
│ J001   │ Engine Machining  │ 15.0h      │ 2025-12-15  │ M1      │   │
│ J002   │ Gear Assembly     │ 8.0h       │ 2025-12-14  │ M3      │   │
│ ...    │ ...               │ ...        │ ...         │ ...     │   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 UTILISATION ÉTAPE PAR ÉTAPE

### 1️⃣ Démarrage

1. Ouvrir PowerShell dans VS Code (`Ctrl + \``)
2. Activer l'environnement: `.\.venv\Scripts\Activate.ps1`
3. Lancer: `python -m src.gui`

### 2️⃣ Voir les données

- La section "Available Jobs" montre les 8 tâches par défaut
- Chaque tâche a: ID, nom, durée, échéance, machine requise

### 3️⃣ Choisir l'algorithme

Sélectionner un algorithme:

- **Fuzzy Priority** (recommandé) - Logique floue
- **FCFS** - First Come First Served
- **EDD** - Earliest Due Date

### 4️⃣ Lancer l'ordonnancement

1. Cliquer sur **🚀 Run Scheduling**
2. Les résultats apparaissent dans le tableau
3. Les statistiques se mettent à jour automatiquement

### 5️⃣ Visualiser le planning

1. Cliquer sur **📊 Show Gantt Chart**
2. Une nouvelle fenêtre s'ouvre avec le diagramme de Gantt
3. Voir visuellement comment les tâches sont réparties sur les machines

### 6️⃣ Exporter les résultats

1. Cliquer sur **💾 Export Results**
2. Fichiers créés:
   - `data/scheduled_jobs_gui.csv` (format Excel)
   - `data/schedule_gui.json` (format JSON)

### 7️⃣ Recommencer

- Cliquer sur **🔄 Reset Data** pour recharger les données initiales

---

## 📊 FONCTIONNALITÉS

### ✅ Panel de contrôle

- **Sélection d'algorithme**: 3 algorithmes disponibles
- **Boutons d'action**: 4 actions principales
- **Statistiques en temps réel**:
  - Nombre total de tâches
  - Makespan (durée totale)
  - Taux de livraison à temps
  - Utilisation des machines

### ✅ Résultats d'ordonnancement

- **Tableau complet** avec:
  - Job ID
  - Nom de la tâche
  - Score de priorité
  - Machine assignée
  - Heure de début
  - Heure de fin
  - Statut (✅ On Time / ⚠️ Late)

### ✅ Liste des tâches

- **Vue d'ensemble** de toutes les tâches disponibles
- **Tri automatique** par Job ID
- **Scroll** pour voir toutes les tâches

### ✅ Diagramme de Gantt

- **Visualisation graphique** du planning
- **Couleurs différentes** par tâche
- **Axe temporel** en heures
- **Séparation par machine**

---

## 🎬 DÉMONSTRATION DEVANT LE PROF

### Scénario recommandé (3 minutes):

**1. Lancement (30 sec)**

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.gui
```

> "Voici l'interface graphique que j'ai développée en Python avec Tkinter"

**2. Présentation de l'interface (30 sec)**

> "On a 8 tâches à ordonnancer sur 3 machines. Je peux choisir entre 3 algorithmes différents."

**3. Exécution avec Fuzzy (30 sec)**

- Sélectionner "Fuzzy Priority"
- Cliquer "Run Scheduling"
  > "L'algorithme de logique floue calcule une priorité pour chaque tâche et les ordonnance de façon optimale. Résultat: 62.5% des tâches livrées à temps."

**4. Diagramme de Gantt (30 sec)**

- Cliquer "Show Gantt Chart"
  > "Ce diagramme montre visuellement comment les tâches sont réparties dans le temps sur chaque machine."

**5. Comparaison d'algorithmes (30 sec)**

- Fermer le Gantt
- Sélectionner "FCFS"
- Cliquer "Run Scheduling"
  > "Avec l'algorithme FCFS, les résultats sont différents. On peut comparer les performances."

**6. Export (30 sec)**

- Cliquer "Export Results"
  > "Les résultats sont exportés automatiquement en CSV et JSON pour une utilisation externe."

---

## 🎨 CARACTÉRISTIQUES TECHNIQUES

### Architecture

- **100% Python** - Aucun HTML/CSS/JavaScript
- **Tkinter** - Bibliothèque GUI standard Python
- **Matplotlib** - Pour les graphiques Gantt
- **Intégration complète** - Utilise tous les modules existants

### Composants

- **4 panels principaux**:

  1. Control Panel (contrôles et algorithmes)
  2. Results Panel (tableau des résultats)
  3. Jobs Panel (liste des tâches)
  4. Status Bar (barre d'état)

- **Fenêtre secondaire**:
  - Gantt Chart (diagramme de planification)

### Code

- **~450 lignes** de code Python pur
- **Classes OOP** - Architecture orientée objet
- **Intégration parfaite** - Réutilise scheduler, fuzzy_logic, utils
- **Gestion d'erreurs** - Messages d'erreur clairs

---

## 🔧 RÉSOLUTION DE PROBLÈMES

### ❌ Erreur: "No module named 'tkinter'"

**Solution:** Tkinter devrait être inclus avec Python, mais si ce n'est pas le cas:

```powershell
# Réinstaller Python en incluant tkinter
# Ou utiliser:
pip install tk
```

### ❌ Erreur: "No module named 'matplotlib'"

**Solution:**

```powershell
pip install matplotlib
```

### ❌ La fenêtre ne s'affiche pas

**Solution:** Vérifier que l'environnement graphique fonctionne:

```powershell
python -c "import tkinter; tkinter.Tk()"
```

### ❌ Graphique Gantt ne s'affiche pas

**Solution:** Installer matplotlib si manquant:

```powershell
pip install matplotlib
```

---

## 💡 AVANTAGES DE L'INTERFACE GRAPHIQUE

### Pour votre projet FTP:

✅ **Professionnel** - Interface moderne et intuitive
✅ **100% Python** - Respecte les exigences du projet
✅ **Visuel** - Diagrammes et tableaux pour mieux comprendre
✅ **Comparaison facile** - Tester plusieurs algorithmes rapidement
✅ **Export automatique** - Résultats sauvegardés en un clic

### Pour la démonstration:

✅ **Impressionnant** - Beaucoup plus visuel que la CLI
✅ **Interactif** - Le prof peut tester en temps réel
✅ **Pédagogique** - Facile de montrer les différences entre algorithmes
✅ **Complet** - Montre toutes les compétences (GUI + algorithmes)

---

## 📝 POINTS À MENTIONNER AU PROF

> "J'ai développé deux interfaces pour l'application:"
>
> **1. Interface en ligne de commande (CLI)**
>
> - Pour les utilisations en production/scripts
> - Export automatique vers fichiers
>
> **2. Interface graphique (GUI) avec Tkinter**
>
> - Pour la visualisation et l'analyse
> - Diagrammes de Gantt interactifs
> - Comparaison facile entre algorithmes
>
> "Les deux interfaces utilisent exactement le même code métier (scheduler, fuzzy_logic),
> ce qui montre une bonne séparation des responsabilités et une architecture modulaire."

---

## 🎯 COMMANDES MÉMO

```powershell
# 1. LANCER L'INTERFACE GRAPHIQUE
.\.venv\Scripts\Activate.ps1
python -m src.gui

# 2. LANCER LA VERSION CLI (pour comparer)
python -m src.main --no-db

# 3. LANCER LES TESTS
pytest
```

---

## ✅ CHECKLIST AVANT DÉMONSTRATION

- [ ] Environnement virtuel activé
- [ ] `python -m src.gui` fonctionne
- [ ] Interface graphique s'affiche correctement
- [ ] Bouton "Run Scheduling" fonctionne
- [ ] Gantt Chart s'affiche
- [ ] Export crée les fichiers dans `data/`
- [ ] Tous les algorithmes fonctionnent
- [ ] Version CLI fonctionne aussi (pour comparaison)

---

**VOTRE PROJET EST MAINTENANT COMPLET AVEC UNE BELLE INTERFACE ! 🎨**
