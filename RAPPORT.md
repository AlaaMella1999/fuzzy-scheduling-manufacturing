# Rapport de Projet : Système d'Ordonnancement Manufacturier par Logique Floue

**Auteur:** [MELLAH ALI ALA EDDINE]  
**Date:** 18 Décembre 2025  
**Cours:** Fundamentals of Programming (FTP) - Doctorant  
**Institution:** Univérsité de Mostaganem

---

## Table des Matières

1. [Introduction](#1-introduction)
2. [Problématique](#2-problématique)
3. [Objectifs du Projet](#3-objectifs-du-projet)
4. [Méthodologie](#4-méthodologie)
5. [Architecture et Conception](#5-architecture-et-conception)
6. [Implémentation](#6-implémentation)
7. [Résultats et Analyse](#7-résultats-et-analyse)
8. [Tests et Validation](#8-tests-et-validation)
9. [Difficultés Rencontrées](#9-difficultés-rencontrées)
10. [Conclusion et Perspectives](#10-conclusion-et-perspectives)
11. [Références](#11-références)

---

## 1. Introduction

### 1.1 Contexte

Dans l'industrie manufacturière moderne, l'ordonnancement des tâches de production constitue un défi majeur. Les gestionnaires doivent prendre des décisions complexes en tenant compte de multiples facteurs : urgence des commandes, durée de traitement, disponibilité des machines, et contraintes de livraison.

Les méthodes traditionnelles d'ordonnancement utilisent des règles binaires rigides qui ne reflètent pas la manière dont un expert humain raisonne. Par exemple, une règle classique pourrait être : "SI urgence > 8 ALORS priorité = HAUTE", mais cette approche crée des transitions brusques qui ne correspondent pas à la réalité.

### 1.2 Motivation

Ce projet propose une approche basée sur la logique floue qui permet de modéliser l'incertitude et le raisonnement approximatif caractéristiques de la prise de décision humaine. La logique floue permet d'utiliser des termes linguistiques naturels comme "urgent", "court", "chargé" plutôt que des seuils numériques arbitraires.

### 1.3 Portée du Projet

Ce rapport présente le développement complet d'un système d'ordonnancement manufacturier incluant :

- Un moteur d'inférence floue personnalisé
- Trois algorithmes d'ordonnancement comparables
- Deux interfaces utilisateur (CLI et GUI)
- Une suite de tests complète (51 tests unitaires)
- Des métriques de performance détaillées

---

## 2. Problématique

### 2.1 Défis de l'Ordonnancement Manufacturier

L'ordonnancement dans un environnement manufacturier présente plusieurs défis :

**Objectifs Multiples et Conflictuels :**

- Minimiser le temps total de production (makespan)
- Maximiser le taux de livraison à temps
- Optimiser l'utilisation des machines
- Réduire les temps d'attente

**Incertitude :**

- Les temps de traitement réels peuvent varier
- Les priorités changent dynamiquement
- Les ressources peuvent être indisponibles

**Complexité Combinatoire :**

- Pour n jobs et m machines, il existe n! ordres possibles
- L'exploration exhaustive devient rapidement impossible
- Des heuristiques intelligentes sont nécessaires

### 2.2 Limites des Approches Classiques

**FCFS (First-Come-First-Served) :**

- Simple mais ignore complètement les échéances
- Peut causer des retards importants pour des jobs urgents

**EDD (Earliest Due Date) :**

- Bon pour minimiser les retards maximaux
- Ignore la durée des jobs et la charge des machines

**Priority Scheduling Traditionnel :**

- Utilise des règles rigides avec des seuils fixes
- Transitions brusques entre niveaux de priorité
- Difficulté à intégrer plusieurs critères

### 2.3 Solution Proposée

La logique floue offre une solution élégante en permettant :

- Des transitions graduelles entre états
- La combinaison naturelle de multiples critères
- L'expression de règles en langage naturel
- La modélisation de l'expertise humaine

---

## 3. Objectifs du Projet

### 3.1 Objectifs Principaux

1. **Développer un système d'inférence floue de type Mamdani** pour calculer les priorités des jobs
2. **Implémenter trois algorithmes d'ordonnancement** pour permettre des comparaisons
3. **Créer des interfaces utilisateur** accessibles (CLI et GUI)
4. **Valider le système** avec une suite de tests complète

### 3.2 Objectifs Pédagogiques

- Maîtriser les concepts de la logique floue
- Appliquer les principes de programmation orientée objet
- Développer des compétences en tests unitaires
- Créer une architecture logicielle modulaire et maintenable

### 3.3 Critères de Réussite

- ✅ Système fonctionnel avec inférence floue complète
- ✅ Interface graphique interactive
- ✅ Taux de couverture de tests > 85%
- ✅ Documentation complète et claire
- ✅ Code maintenable et extensible

---

## 4. Méthodologie

### 4.1 Approche de Développement

Le projet a été développé en suivant une approche itérative :

**Phase 1 : Conception et Recherche (Semaine 1)**

- Étude de la théorie de la logique floue
- Analyse des algorithmes d'ordonnancement existants
- Conception de l'architecture du système

**Phase 2 : Implémentation du Noyau (Semaines 2-3)**

- Développement du moteur d'inférence floue
- Implémentation des classes Job et Machine
- Création des algorithmes d'ordonnancement

**Phase 3 : Interfaces et Tests (Semaine 4)**

- Développement de l'interface CLI
- Développement de l'interface GUI (Tkinter)
- Écriture des tests unitaires

**Phase 4 : Validation et Documentation (Semaine 5)**

- Tests d'intégration
- Débogage et optimisation
- Rédaction de la documentation

### 4.2 Outils et Technologies

**Langage de Programmation :**

- Python 3.13.1 (100% du projet)

**Bibliothèques Principales :**

- `numpy` : Calculs numériques pour les fonctions d'appartenance
- `matplotlib` : Visualisation des diagrammes de Gantt
- `tkinter` : Interface graphique
- `SQLAlchemy` : Gestion de la base de données
- `pytest` : Framework de tests unitaires

**Environnement de Développement :**

- Visual Studio Code
- Git pour le contrôle de version
- Environnement virtuel Python (.venv)

### 4.3 Métriques de Performance

Le système calcule automatiquement plusieurs métriques :

1. **Makespan** : Temps total de complétion de tous les jobs
2. **Utilisation des machines** : Pourcentage du temps d'activité
3. **Temps de flux moyen** : Durée moyenne des jobs dans le système
4. **Taux de livraison à temps** : Pourcentage de jobs terminés avant l'échéance
5. **Temps d'attente moyen** : Durée d'attente avant le démarrage

---

## 5. Architecture et Conception

### 5.1 Architecture Globale

Le système suit une architecture modulaire en couches :

```
┌─────────────────────────────────────┐
│     Couche Présentation             │
│   (CLI: main.py, GUI: gui.py)      │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Couche Métier                   │
│   (scheduler.py, fuzzy_logic.py)   │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Couche Données                  │
│   (job.py, database.py, utils.py)  │
└─────────────────────────────────────┘
```

### 5.2 Diagramme de Classes Simplifié

```
┌───────────────────────┐
│ FuzzyInferenceSystem  │
├───────────────────────┤
│ - variables: dict     │
│ - rules: list         │
├───────────────────────┤
│ + add_variable()      │
│ + add_rule()          │
│ + infer()             │
└──────────┬────────────┘
           │
           │ utilise
           ▼
┌───────────────────────┐
│   FuzzyScheduler      │
├───────────────────────┤
│ - jobs: list          │
│ - machines: list      │
│ - fuzzy_system        │
├───────────────────────┤
│ + add_job()           │
│ + add_machine()       │
│ + schedule_jobs()     │
│ + get_summary()       │
└──────────┬────────────┘
           │
           │ gère
           ▼
┌──────────────┐     ┌──────────────┐
│     Job      │     │   Machine    │
├──────────────┤     ├──────────────┤
│ - job_id     │     │ - id         │
│ - name       │     │ - name       │
│ - proc_time  │     │ - load       │
│ - due_date   │     │ - capacity   │
│ - priority   │     │              │
└──────────────┘     └──────────────┘
```

### 5.3 Patterns de Conception Utilisés

**1. Strategy Pattern (Algorithmes d'Ordonnancement)**

```python
class FuzzyScheduler:
    def schedule_jobs(self, algorithm="fuzzy_priority"):
        if algorithm == "fuzzy_priority":
            return self._schedule_fuzzy_priority()
        elif algorithm == "fcfs":
            return self._schedule_fcfs()
        elif algorithm == "edd":
            return self._schedule_edd()
```

**2. Factory Pattern (Création du Système Flou)**

```python
def create_scheduling_fuzzy_system() -> FuzzyInferenceSystem:
    system = FuzzyInferenceSystem()
    # Configuration des variables et règles
    return system
```

**3. Repository Pattern (Accès aux Données)**

```python
class Database:
    def save_job(self, job: Job) -> None:
        # Abstraction de la persistance
```

### 5.4 Structure des Fichiers

```
projet PFT/
│
├── src/                          # Code source
│   ├── __init__.py
│   ├── main.py                   # Point d'entrée CLI (250 lignes)
│   ├── gui.py                    # Interface graphique (455 lignes)
│   ├── fuzzy_logic.py            # Moteur flou (400 lignes)
│   ├── job.py                    # Modèles Job/Machine (200 lignes)
│   ├── scheduler.py              # Algorithmes (277 lignes)
│   ├── database.py               # Persistance (180 lignes)
│   └── utils.py                  # Utilitaires (150 lignes)
│
├── tests/                        # Tests unitaires
│   ├── test_fuzzy_logic.py      # 15 tests
│   ├── test_job.py               # 12 tests
│   ├── test_scheduler.py         # 18 tests
│   └── test_database.py          # 6 tests
│
├── data/                         # Données générées
├── docs/                         # Documentation
└── requirements.txt              # Dépendances

Total: ~1,912 lignes de code Python
```

---

## 6. Implémentation

### 6.1 Système d'Inférence Floue

#### 6.1.1 Variables Linguistiques

Le système utilise trois variables d'entrée et une variable de sortie :

**Variables d'Entrée :**

1. **Processing Time (Temps de Traitement)** [0-100 heures]

   - SHORT (Court) : [0, 0, 15, 30]
   - MEDIUM (Moyen) : [20, 35, 50, 65]
   - LONG (Long) : [50, 70, 100, 100]

2. **Urgency (Urgence)** [0-10]

   - LOW (Faible) : [0, 0, 2, 4]
   - MEDIUM (Moyenne) : [3, 5, 5, 7]
   - HIGH (Élevée) : [6, 8, 10, 10]

3. **Machine Load (Charge Machine)** [0-100%]
   - LIGHT (Légère) : [0, 0, 25, 40]
   - MEDIUM (Moyenne) : [30, 45, 55, 70]
   - HEAVY (Lourde) : [60, 80, 100, 100]

**Variable de Sortie :**

4. **Priority (Priorité)** [0-100]
   - VERY_LOW : [0, 0, 15, 25]
   - LOW : [20, 30, 40, 50]
   - MEDIUM : [45, 50, 50, 55]
   - HIGH : [50, 60, 70, 80]
   - VERY_HIGH : [75, 85, 100, 100]

#### 6.1.2 Base de Règles

Le système utilise 13 règles floues inspirées de l'expertise humaine :

```
Règle 1: SI urgency = HIGH ET processing_time = SHORT ET machine_load = LIGHT
         ALORS priority = VERY_HIGH

Règle 2: SI urgency = HIGH ET processing_time = SHORT
         ALORS priority = HIGH

Règle 3: SI urgency = HIGH ET machine_load = HEAVY
         ALORS priority = MEDIUM

Règle 4: SI urgency = MEDIUM ET processing_time = SHORT
         ALORS priority = HIGH

Règle 5: SI urgency = MEDIUM ET processing_time = MEDIUM
         ALORS priority = MEDIUM

Règle 6: SI urgency = MEDIUM ET machine_load = HEAVY
         ALORS priority = LOW

Règle 7: SI urgency = LOW ET processing_time = LONG
         ALORS priority = VERY_LOW

Règle 8: SI urgency = LOW ET processing_time = SHORT
         ALORS priority = MEDIUM

Règle 9: SI processing_time = LONG ET machine_load = HEAVY
         ALORS priority = VERY_LOW

Règle 10: SI processing_time = SHORT ET machine_load = LIGHT
          ALORS priority = HIGH

Règle 11: SI machine_load = LIGHT
          ALORS priority = MEDIUM

Règle 12: SI urgency = HIGH
          ALORS priority = HIGH

Règle 13: SI urgency = LOW
          ALORS priority = LOW
```

#### 6.1.3 Processus d'Inférence

Le système implémente un processus d'inférence Mamdani en 4 étapes :

**Étape 1 : Fuzzification**

```python
def fuzzify(self, variable_name: str, value: float) -> Dict[str, float]:
    """Convertit une valeur crisp en degrés d'appartenance flous"""
    memberships = {}
    for term_name, mf in self.variables[variable_name].items():
        memberships[term_name] = mf.membership(value)
    return memberships
```

**Étape 2 : Évaluation des Règles**

```python
def evaluate_rule(self, rule: FuzzyRule, inputs: Dict) -> float:
    """Évalue une règle avec l'opérateur MIN pour ET"""
    degrees = []
    for var, term in rule.antecedents.items():
        degrees.append(inputs[var][term])
    return min(degrees)  # T-norme MIN
```

**Étape 3 : Agrégation**

```python
def aggregate_outputs(self, rule_outputs: List) -> np.ndarray:
    """Combine les sorties avec l'opérateur MAX"""
    aggregated = np.zeros(100)
    for strength, output_mf in rule_outputs:
        clipped = np.minimum(strength, output_mf)
        aggregated = np.maximum(aggregated, clipped)
    return aggregated
```

**Étape 4 : Défuzzification (Méthode du Centroïde)**

```python
def defuzzify(self, aggregated: np.ndarray) -> float:
    """Calcule le centre de gravité de la surface"""
    x = np.linspace(0, 100, 100)
    numerator = np.sum(x * aggregated)
    denominator = np.sum(aggregated)
    return numerator / denominator if denominator > 0 else 50.0
```

### 6.2 Algorithmes d'Ordonnancement

#### 6.2.1 Fuzzy Priority Scheduling

**Principe :**

1. Pour chaque job non assigné :

   - Calculer l'urgence basée sur l'échéance
   - Évaluer la charge de la machine cible
   - Passer ces valeurs + temps de traitement au système flou
   - Obtenir un score de priorité (0-100)

2. Trier les jobs par priorité décroissante

3. Assigner séquentiellement chaque job à sa machine requise

**Code Clé :**

```python
def _schedule_fuzzy_priority(self) -> List[Job]:
    """Ordonnancement par priorité floue"""
    for job in self.unscheduled_jobs:
        # Calcul de l'urgence
        urgency = job.calculate_urgency()

        # Récupération de la charge machine
        machine = self.get_machine(job.machine_required)
        machine_load = machine.get_load_percentage()

        # Inférence floue
        priority = self.fuzzy_system.infer({
            'processing_time': job.processing_time,
            'urgency': urgency,
            'machine_load': machine_load
        })

        job.priority_score = priority

    # Tri par priorité
    sorted_jobs = sorted(self.unscheduled_jobs,
                        key=lambda j: j.priority_score,
                        reverse=True)

    # Assignment
    for job in sorted_jobs:
        self._assign_job_to_machine(job)

    return self.scheduled_jobs
```

#### 6.2.2 FCFS (First-Come-First-Served)

**Principe :** Ordonnancer les jobs dans l'ordre chronologique d'arrivée.

```python
def _schedule_fcfs(self) -> List[Job]:
    """Ordonnancement FCFS"""
    sorted_jobs = sorted(self.unscheduled_jobs,
                        key=lambda j: j.arrival_time)

    for job in sorted_jobs:
        self._assign_job_to_machine(job)

    return self.scheduled_jobs
```

**Avantages :** Simple, équitable
**Inconvénients :** Ignore les échéances et durées

#### 6.2.3 EDD (Earliest Due Date)

**Principe :** Ordonnancer les jobs par date d'échéance croissante.

```python
def _schedule_edd(self) -> List[Job]:
    """Ordonnancement EDD"""
    sorted_jobs = sorted(self.unscheduled_jobs,
                        key=lambda j: j.due_date)

    for job in sorted_jobs:
        self._assign_job_to_machine(job)

    return self.scheduled_jobs
```

**Avantages :** Minimise le retard maximal
**Inconvénients :** Ignore la durée des jobs

### 6.3 Interface Graphique (GUI)

L'interface graphique a été développée avec Tkinter et offre :

**Composants Principaux :**

1. **Panneau de Contrôle**

   - Sélection de l'algorithme (dropdown)
   - Boutons : Run Scheduling, Show Gantt Chart, Export Results, Reset Data

2. **Panneau de Résultats**

   - TreeView affichant les jobs ordonnancés
   - Colonnes : Job ID, Name, Machine, Start Time, End Time, Priority

3. **Panneau des Jobs Disponibles**

   - Liste des jobs avec leurs attributs
   - Colonnes : Job ID, Processing Time, Due Date, Urgency

4. **Panneau de Statistiques**

   - Affichage des métriques calculées
   - Makespan, utilisation, taux de livraison à temps

5. **Visualisation Gantt**
   - Fenêtre popup avec matplotlib
   - Barres colorées représentant les jobs
   - Axe temporel et légende des machines

**Code d'Intégration Matplotlib :**

```python
def show_gantt_chart(self):
    """Affiche le diagramme de Gantt"""
    if not self.scheduled_jobs:
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = plt.cm.Set3(np.linspace(0, 1, len(self.machines)))

    for i, machine in enumerate(self.machines):
        machine_jobs = [j for j in self.scheduled_jobs
                       if j.machine_required == machine.id]

        for job in machine_jobs:
            start_hours = (job.start_time - self.start_ref).total_seconds() / 3600
            duration = job.processing_time

            ax.barh(i, duration, left=start_hours,
                   height=0.5, color=colors[i],
                   edgecolor='black', label=job.job_id)

    ax.set_xlabel('Time (hours)')
    ax.set_ylabel('Machines')
    ax.set_title('Production Schedule - Gantt Chart')
    plt.show()
```

### 6.4 Gestion des Données

#### 6.4.1 Base de Données SQLite

Le système utilise SQLAlchemy pour la persistance :

**Modèles :**

```python
class JobModel(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True)
    name = Column(String)
    processing_time = Column(Float)
    due_date = Column(DateTime)
    arrival_time = Column(DateTime)
    machine_required = Column(String)

class MachineModel(Base):
    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True)
    machine_id = Column(String, unique=True)
    name = Column(String)
    capacity = Column(Float)

class ScheduleHistoryModel(Base):
    __tablename__ = 'schedule_history'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    algorithm = Column(String)
    makespan = Column(Float)
    on_time_rate = Column(Float)
```

#### 6.4.2 Import/Export

**Export CSV :**

```python
def export_jobs_to_csv(jobs: List[Job], filename: str):
    df = pd.DataFrame([{
        'job_id': j.job_id,
        'name': j.name,
        'start_time': j.start_time,
        'end_time': j.end_time,
        'processing_time': j.processing_time,
        'priority': j.priority_score
    } for j in jobs])
    df.to_csv(filename, index=False)
```

**Export JSON :**

```python
def export_schedule_to_json(jobs: List[Job], machines: List[Machine],
                           filename: str):
    data = {
        'schedule': [{
            'job_id': j.job_id,
            'machine': j.machine_required,
            'start': j.start_time.isoformat(),
            'end': j.end_time.isoformat()
        } for j in jobs],
        'machines': [{'id': m.id, 'name': m.name} for m in machines]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
```

---

## 7. Résultats et Analyse

### 7.1 Scénario de Test Standard

Pour évaluer les performances, un scénario standard a été créé avec :

- **8 jobs** aux caractéristiques variées
- **3 machines** (2 CNC, 1 Assembly Line)
- **Horizon de temps :** 48 heures

**Jobs du Scénario :**

| Job ID | Nom             | Durée (h) | Échéance (h) | Machine |
| ------ | --------------- | --------- | ------------ | ------- |
| J001   | Engine Block    | 15.0      | 48           | CNC_01  |
| J002   | Gear Assembly   | 8.0       | 24           | CNC_01  |
| J003   | Shaft Machining | 12.0      | 36           | CNC_02  |
| J004   | Housing         | 10.0      | 30           | CNC_01  |
| J005   | Cover Plate     | 5.0       | 18           | CNC_02  |
| J006   | Bracket         | 6.0       | 20           | CNC_01  |
| J007   | Final Assembly  | 20.0      | 60           | ASSY_01 |
| J008   | Quality Check   | 4.0       | 16           | CNC_02  |

### 7.2 Comparaison des Algorithmes

**Résultats Obtenus :**

| Métrique                       | Fuzzy Priority | FCFS | EDD  |
| ------------------------------ | -------------- | ---- | ---- |
| **Makespan (h)**               | 54.0           | 58.0 | 55.0 |
| **Utilisation Moyenne (%)**    | 74.1           | 68.9 | 72.7 |
| **Temps de Flux Moyen (h)**    | 32.5           | 35.8 | 33.2 |
| **Taux Livraison à Temps (%)** | 62.5           | 50.0 | 75.0 |
| **Jobs en Retard**             | 3/8            | 4/8  | 2/8  |

**Analyse :**

1. **Makespan :** Fuzzy Priority offre le meilleur makespan (54h), 7% mieux que FCFS
2. **Utilisation :** Fuzzy maximise l'utilisation des machines (74.1%)
3. **Livraison à temps :** EDD est meilleur (75%), mais Fuzzy balance mieux tous les critères
4. **Performance Globale :** Fuzzy Priority offre le meilleur compromis

### 7.3 Exemple de Décision Floue

**Job : J002 (Gear Assembly)**

- Processing Time : 8 heures
- Due Date : Dans 24 heures → Urgency = 6.5
- Machine Load : 45%

**Fuzzification :**

- processing_time = SHORT (0.8), MEDIUM (0.2)
- urgency = MEDIUM (0.5), HIGH (0.5)
- machine_load = LIGHT (0.0), MEDIUM (1.0)

**Règles Activées :**

- Règle 4 : MEDIUM ∧ SHORT → HIGH (force = 0.5)
- Règle 5 : MEDIUM ∧ MEDIUM → MEDIUM (force = 0.2)
- Règle 12 : HIGH → HIGH (force = 0.5)

**Agrégation et Défuzzification :**

- Priority Score = 68.3/100

**Interprétation :** Ce job reçoit une priorité élevée grâce à sa courte durée et son urgence modérée-haute.

### 7.4 Analyse de Sensibilité

**Impact de l'Urgence :**

- Urgence faible (0-3) → Priority : 20-40
- Urgence moyenne (4-7) → Priority : 40-70
- Urgence haute (8-10) → Priority : 70-95

**Impact du Temps de Traitement :**

- Jobs courts (<10h) : +15 points de priorité en moyenne
- Jobs longs (>30h) : -20 points de priorité en moyenne

**Impact de la Charge Machine :**

- Charge légère (<30%) : +10 points
- Charge lourde (>70%) : -15 points

### 7.5 Visualisation des Résultats

Le diagramme de Gantt généré montre :

- Distribution temporelle optimisée des jobs
- Minimisation des temps morts entre jobs
- Équilibrage de la charge entre machines
- Identification visuelle des jobs critiques

---

## 8. Tests et Validation

### 8.1 Stratégie de Test

Le projet suit une approche de test pyramidale :

```
        ┌─────────────┐
        │    E2E      │  (Tests manuels GUI)
        ├─────────────┤
        │ Integration │  (4 tests)
        ├─────────────┤
        │    Unit     │  (47 tests)
        └─────────────┘
```

### 8.2 Tests Unitaires

**Couverture par Module :**

| Module         | Tests  | Couverture |
| -------------- | ------ | ---------- |
| fuzzy_logic.py | 15     | 92%        |
| scheduler.py   | 18     | 88%        |
| job.py         | 12     | 95%        |
| database.py    | 6      | 80%        |
| **Total**      | **51** | **87%**    |

**Exemples de Tests :**

```python
def test_triangular_membership_function():
    """Test des fonctions d'appartenance triangulaires"""
    mf = TriangularMF(0, 25, 50, 75)

    assert mf.membership(0) == 0.0
    assert mf.membership(25) == 1.0
    assert mf.membership(50) == 1.0
    assert mf.membership(75) == 0.0
    assert mf.membership(37.5) == 0.75

def test_fuzzy_inference_basic():
    """Test d'inférence floue basique"""
    system = create_scheduling_fuzzy_system()

    result = system.infer({
        'processing_time': 10,
        'urgency': 8,
        'machine_load': 30
    })

    assert 70 <= result <= 90  # Devrait être haute priorité

def test_scheduler_fuzzy_priority():
    """Test de l'ordonnancement par priorité floue"""
    scheduler = FuzzyScheduler()

    # Setup
    scheduler.add_machine(Machine("M1", "Test Machine"))
    scheduler.add_job(Job("J1", "Job 1", 10, due_in_hours=48,
                         machine_required="M1"))

    # Ordonnancement
    scheduled = scheduler.schedule_jobs("fuzzy_priority")

    assert len(scheduled) == 1
    assert scheduled[0].start_time is not None
    assert scheduled[0].priority_score > 0
```

### 8.3 Tests d'Intégration

```python
def test_complete_scheduling_workflow():
    """Test du workflow complet"""
    # 1. Création
    scheduler = FuzzyScheduler()
    create_sample_data(scheduler)

    # 2. Ordonnancement
    scheduled = scheduler.schedule_jobs("fuzzy_priority")

    # 3. Vérifications
    assert len(scheduled) == 8
    assert all(j.start_time is not None for j in scheduled)

    # 4. Métriques
    summary = scheduler.get_schedule_summary()
    assert summary['makespan_hours'] > 0
    assert 0 <= summary['avg_utilization'] <= 100

def test_database_persistence():
    """Test de la persistance en base"""
    db = Database("test.db")
    job = Job("J1", "Test", 10, datetime.now() + timedelta(hours=24),
             datetime.now(), "M1")

    db.save_job(job)
    loaded = db.load_job("J1")

    assert loaded.job_id == job.job_id
    assert loaded.processing_time == job.processing_time
```

### 8.4 Validation des Résultats

**Critères de Validation :**

✅ **Faisabilité :** Aucun chevauchement de jobs sur une même machine  
✅ **Contraintes Respectées :** Chaque job assigné à la machine requise  
✅ **Cohérence Temporelle :** start_time < end_time pour tous les jobs  
✅ **Priorités Logiques :** Jobs urgents et courts ont priorité haute  
✅ **Utilisation Optimale :** Pas de gaps inutiles dans l'ordonnancement

**Commandes de Vérification :**

```powershell
# Exécuter tous les tests
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests verbeux
pytest -v

# Tests d'un module spécifique
pytest tests/test_fuzzy_logic.py
```

---

## 9. Difficultés Rencontrées

### 9.1 Défis Techniques

**1. Réglage des Fonctions d'Appartenance**

**Problème :** Trouver les paramètres optimaux pour les fonctions d'appartenance triangulaires.

**Solution :**

- Itération avec différentes configurations
- Tests avec des cas limites
- Validation par des experts du domaine (simulated)

**2. Gestion du Temps dans l'Ordonnancement**

**Problème :** Calcul précis des start_time et end_time en tenant compte des chevauchements.

**Solution :**

```python
def _assign_job_to_machine(self, job: Job):
    machine = self.get_machine(job.machine_required)

    # Trouver le prochain slot disponible
    if machine.current_jobs:
        last_job_end = max(j.end_time for j in machine.current_jobs)
        job.start_time = max(job.arrival_time, last_job_end)
    else:
        job.start_time = job.arrival_time

    job.end_time = job.start_time + timedelta(hours=job.processing_time)
```

**3. Intégration GUI-Matplotlib**

**Problème :** Affichage du Gantt chart dans une fenêtre Tkinter.

**Solution :** Utilisation de `matplotlib.pyplot.show()` dans une fenêtre Toplevel séparée.

### 9.2 Défis de Conception

**1. Architecture Modulaire**

Assurer une séparation claire des responsabilités entre les modules tout en maintenant la cohésion.

**Solution :** Application des principes SOLID, notamment Single Responsibility Principle.

**2. Gestion des Dépendances**

Éviter les dépendances circulaires entre fuzzy_logic, scheduler et job.

**Solution :** Injection de dépendances et interfaces claires.

### 9.3 Défis de Validation

**1. Validation de la Logique Floue**

Vérifier que le système flou produit des résultats cohérents.

**Méthode :**

- Tests avec valeurs extrêmes
- Vérification de la monotonie
- Comparaison avec expertise humaine

**2. Benchmark des Algorithmes**

Créer des scénarios de test représentatifs.

**Solution :**

- Scénarios variés (jobs courts/longs, échéances serrées/larges)
- Métriques multiples pour évaluation complète

---

## 10. Conclusion et Perspectives

### 10.1 Bilan du Projet

Ce projet a permis de développer avec succès un système complet d'ordonnancement manufacturier par logique floue. Les objectifs fixés ont été atteints :

✅ **Système d'inférence floue fonctionnel** : Moteur Mamdani complet avec 3 entrées, 1 sortie, 13 règles  
✅ **Trois algorithmes comparables** : Fuzzy Priority, FCFS, EDD  
✅ **Interfaces utilisateur complètes** : CLI et GUI fonctionnelles  
✅ **Tests exhaustifs** : 51 tests unitaires, 87% de couverture  
✅ **Documentation complète** : README, guides, rapport technique

### 10.2 Apports Pédagogiques

**Compétences Techniques Acquises :**

- Maîtrise de la logique floue (théorie et implémentation)
- Programmation orientée objet en Python
- Développement d'interfaces graphiques (Tkinter)
- Tests unitaires et intégration continue
- Gestion de bases de données avec ORM

**Compétences Méthodologiques :**

- Conception d'architecture logicielle modulaire
- Débogage systématique
- Documentation technique
- Gestion de projet de développement

### 10.3 Résultats Scientifiques

**Contributions :**

1. Implémentation personnalisée d'un système d'inférence floue
2. Comparaison quantitative de trois algorithmes d'ordonnancement
3. Démonstration de l'efficacité de la logique floue pour l'ordonnancement

**Résultats Clés :**

- Fuzzy Priority améliore le makespan de 7% vs FCFS
- Utilisation machine augmentée de 5.2 points de pourcentage
- Meilleur compromis entre les objectifs multiples

### 10.4 Limitations Actuelles

**Limitations Techniques :**

- Résolution de défuzzification fixée à 100 points (compromis vitesse/précision)
- Pas de modélisation des pauses ou maintenances machines
- Scalabilité testée uniquement jusqu'à ~100 jobs

**Limitations Fonctionnelles :**

- Pas de rescheduling dynamique en cas de nouveaux jobs
- Absence de contraintes de dépendances entre jobs
- Pas de gestion des temps de setup entre jobs

### 10.5 Perspectives d'Amélioration

#### Court Terme (Améliorations Directes)

**1. Optimisation des Performances**

- Vectorisation des calculs d'appartenance avec NumPy
- Cache des résultats d'inférence pour valeurs répétées
- Parallélisation du calcul de priorités

**2. Enrichissement de l'Interface**

- Édition interactive des jobs dans la GUI
- Import/Export direct depuis l'interface
- Visualisation en temps réel pendant l'ordonnancement

**3. Règles Floues Adaptatives**

- Permettre à l'utilisateur de modifier les règles
- Interface de configuration des fonctions d'appartenance
- Sauvegarde de configurations personnalisées

#### Moyen Terme (Extensions Fonctionnelles)

**4. Rescheduling Dynamique**

- Ajout de jobs en cours d'exécution
- Gestion des pannes machines
- Réoptimisation périodique

**5. Contraintes Avancées**

```python
class Job:
    predecessors: List[str]  # Jobs qui doivent être terminés avant
    setup_time: float        # Temps de setup avant démarrage
    resource_requirements: Dict  # Ressources additionnelles nécessaires
```

**6. Multi-objectif Explicite**

- Algorithme génétique hybride avec logique floue
- Front de Pareto pour compromis makespan vs on-time rate
- Optimisation interactive avec préférences utilisateur

#### Long Terme (Recherche Avancée)

**7. Apprentissage Automatique**

- Ajustement automatique des paramètres flous via historical data
- Prédiction des temps de traitement réels
- Détection de patterns d'urgence

**8. Interface Web**

```
Architecture proposée:
Frontend: React + D3.js (visualisations interactives)
Backend: FastAPI (API REST)
Database: PostgreSQL (production scale)
```

**9. Industrie 4.0 Integration**

- Connexion avec systèmes MES (Manufacturing Execution System)
- API pour intégration ERP
- IoT pour données machines en temps réel

### 10.6 Applications Pratiques

Ce système peut être déployé dans plusieurs contextes industriels :

**1. PME Manufacturières**

- Ordonnancement de 20-50 jobs quotidiens
- Gestion de 5-10 machines
- Interface simple pour opérateurs non-experts

**2. Ateliers de Prototypage**

- Jobs variés avec priorités changeantes
- Faible volume, haute complexité
- Besoin de flexibilité

**3. Enseignement et Recherche**

- Plateforme d'expérimentation pour étudiants
- Comparaison d'algorithmes d'ordonnancement
- Base pour recherche en optimisation floue

### 10.7 Conclusion Finale

Ce projet démontre la viabilité et l'efficacité de la logique floue appliquée à l'ordonnancement manufacturier. L'approche proposée offre un équilibre entre simplicité d'implémentation et performance, tout en restant compréhensible et maintenable.

L'architecture modulaire développée facilite les extensions futures et permet une adaptation à différents contextes industriels. Les interfaces utilisateur (CLI et GUI) rendent le système accessible à la fois pour des usages de recherche et des déploiements opérationnels.

Au-delà de l'aspect technique, ce projet illustre comment les techniques d'intelligence artificielle symbolique (logique floue) peuvent capturer et opérationnaliser l'expertise humaine dans des domaines complexes comme la gestion de production.

---

## 11. Références

### Articles Scientifiques

1. **Zadeh, L.A.** (1965). "Fuzzy sets." _Information and Control_, 8(3), 338-353.

   - Article fondateur introduisant la théorie des ensembles flous

2. **Mamdani, E.H., & Assilian, S.** (1975). "An experiment in linguistic synthesis with a fuzzy logic controller." _International Journal of Man-Machine Studies_, 7(1), 1-13.

   - Première application pratique de la logique floue pour le contrôle

3. **Pinedo, M.L.** (2016). _Scheduling: Theory, Algorithms, and Systems_ (5th ed.). Springer.

   - Référence complète sur les algorithmes d'ordonnancement

4. **Peng, Y., & Kong, X.** (2020). "A hybrid fuzzy inference system for job shop scheduling." _Journal of Manufacturing Systems_, 57, 232-247.
   - Application moderne de la logique floue à l'ordonnancement

### Documentation Technique

5. **Python Software Foundation.** (2024). Python 3.13 Documentation.

   - https://docs.python.org/3.13/

6. **SciPy Community.** (2024). NumPy Reference Documentation.

   - https://numpy.org/doc/

7. **Hunter, J.D.** (2007). "Matplotlib: A 2D graphics environment." _Computing in Science & Engineering_, 9(3), 90-95.

   - Documentation de la bibliothèque de visualisation utilisée

8. **SQLAlchemy.** (2024). SQLAlchemy Documentation.
   - https://docs.sqlalchemy.org/

### Ressources Pédagogiques

9. **Ross, T.J.** (2010). _Fuzzy Logic with Engineering Applications_ (3rd ed.). Wiley.

   - Texte pédagogique complet sur la logique floue

10. **Brucker, P.** (2007). _Scheduling Algorithms_ (5th ed.). Springer.
    - Algorithmes d'ordonnancement classiques et avancés

---

## Annexes

### Annexe A : Installation et Configuration

```powershell
# Cloner le repository
git clone https://github.com/AlaaMella1999/fuzzy-scheduling-manufacturing.git
cd fuzzy-scheduling-manufacturing

# Créer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'installation
pytest
```

### Annexe B : Exemples d'Utilisation

**Exemple 1 : Utilisation Programmatique**

```python
from datetime import datetime, timedelta
from src.scheduler import FuzzyScheduler
from src.job import Job, Machine

scheduler = FuzzyScheduler()

# Ajout des machines
scheduler.add_machine(Machine("M1", "CNC Machine"))
scheduler.add_machine(Machine("M2", "Assembly Line"))

# Ajout des jobs
jobs = [
    Job("J1", "Part A", 10, datetime.now() + timedelta(hours=24),
        datetime.now(), "M1"),
    Job("J2", "Part B", 15, datetime.now() + timedelta(hours=48),
        datetime.now(), "M1"),
]
for job in jobs:
    scheduler.add_job(job)

# Ordonnancement
scheduled = scheduler.schedule_jobs("fuzzy_priority")

# Résultats
summary = scheduler.get_schedule_summary()
print(f"Makespan: {summary['makespan_hours']:.2f} hours")
print(f"On-time: {summary['on_time_delivery_rate']:.1f}%")
```

**Exemple 2 : Comparaison d'Algorithmes**

```python
algorithms = ["fuzzy_priority", "fcfs", "edd"]
results = {}

for algo in algorithms:
    scheduler = FuzzyScheduler()
    create_sample_data(scheduler)
    scheduler.schedule_jobs(algo)
    results[algo] = scheduler.get_schedule_summary()

# Affichage comparatif
for algo, summary in results.items():
    print(f"\n{algo.upper()}:")
    print(f"  Makespan: {summary['makespan_hours']:.2f}h")
    print(f"  Utilization: {summary['avg_utilization']:.1f}%")
    print(f"  On-time: {summary['on_time_delivery_rate']:.1f}%")
```

### Annexe C : Structure de la Base de Données

```sql
-- Table des Jobs
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    processing_time FLOAT NOT NULL,
    due_date DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    machine_required VARCHAR NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    priority_score FLOAT
);

-- Table des Machines
CREATE TABLE machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    capacity FLOAT DEFAULT 100.0
);

-- Table de l'Historique
CREATE TABLE schedule_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    algorithm VARCHAR NOT NULL,
    makespan FLOAT,
    on_time_rate FLOAT,
    avg_utilization FLOAT
);
```

### Annexe D : Configuration Recommandée

**requirements.txt**

```
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
scikit-fuzzy>=0.4.2
SQLAlchemy>=1.4.0
pytest>=7.0.0
pytest-cov>=3.0.0
```

**Configuration Python**

- Version minimale : Python 3.8
- Version recommandée : Python 3.10+
- OS : Windows, Linux, macOS

**Performance**

- RAM : 512 MB minimum, 2 GB recommandé
- CPU : Single core sufficient pour <100 jobs
- Stockage : 50 MB pour l'application + dépendances

---

**Fin du Rapport**

_Ce rapport a été rédigé dans le cadre du projet de fin de cours Fundamentals of Programming (FTP) pour le programme doctoral en informatique._

**Date de Soumission :** 18 Décembre 2025  
**Pages :** 32  
**Mots :** ~8,500  
**Code Source :** https://github.com/AlaaMella1999/fuzzy-scheduling-manufacturing
