# Solveur de Programmation Linéaire Avancé

Bienvenue dans le Solveur de Programmation Linéaire Avancé. Ce projet universitaire est une application de bureau complète, conçue pour résoudre les problèmes de programmation linéaire (PL) en utilisant diverses méthodes. Il offre à la fois une interface en ligne de commande (CLI) interactive et une interface utilisateur graphique (GUI) moderne et riche en fonctionnalités pour une expérience utilisateur optimale.

<!-- Insérer ici une capture d'écran ou un GIF de l'application en action -->
<!-- Exemple : <p align="center"><img src="demo.gif" alt="Démo du Solveur Simplexe"></p> -->

## Fonctionnalités Clés

Ce solveur se distingue par un ensemble de fonctionnalités avancées :

*   **Interface Utilisateur Graphique (GUI) Moderne :**
    *   Développée avec **CustomTkinter** pour un design élégant et personnalisable (thèmes clair/sombre).
    *   Navigation intuitive avec barre de navigation, barre latérale et onglets.
    *   **Tableau de Bord (Dashboard)** : Visualisation des statistiques d'utilisation.
    *   **Définition de Problèmes Facilitée :** Champs de saisie dynamiques et validation.
    *   **Visualisations Interactives :**
        *   Région réalisable (pour problèmes à 2 variables) avec **Matplotlib**.
        *   Graphiques 3D (pour problèmes à 3 variables) avec **Plotly**.
        *   Animation du processus de résolution (concept).
    *   **Exportation de Rapports :** Génération de rapports PDF professionnels avec **ReportLab**.
    *   Gestion de Fichiers : Historique des problèmes, import/export (JSON, CSV, Excel - conceptuellement).
    *   Personnalisation : Thèmes de couleurs, taille de police (concept).
*   **Interface en Ligne de Commande (CLI) :**
    *   Menu interactif coloré (`colorama`, `tabulate`) pour une utilisation alternative.
    *   Fonctionnalités similaires à la GUI pour la définition et la résolution de problèmes.
*   **Méthodes de Résolution Implémentées :**
    *   **Simplexe Standard (Méthode Tabulaire)** : Pour les problèmes de maximisation avec contraintes `≤`.
    *   **Méthode du Grand M** : Pour gérer les contraintes d'égalité (`=`) et de supériorité (`≥`).
    *   **Méthode Duale** : Construction et résolution du problème dual, analyse primal-dual.
*   **Gestion des Problèmes :**
    *   Création interactive de nouveaux problèmes.
    *   Sauvegarde et chargement de problèmes depuis des fichiers JSON.
    *   Historique des problèmes résolus.
    *   Exemples prédéfinis pour une prise en main rapide.
*   **Lanceur Premium :**
    *   Un écran de démarrage (`main.py`) avec animations pour une première impression soignée avant le lancement de la GUI principale.
*   **Packaging :**
    *   Scripts de configuration pour **PyInstaller** (`SimplexSolver.spec`) et **cx_Freeze** (`setup.py`) pour créer des exécutables.

## Composants du Projet

Le projet est structuré en plusieurs modules Python, chacun ayant un rôle spécifique :

*   `main.py`: Lanceur "Premium" de l'application avec un écran de démarrage animé, qui ensuite lance l'interface graphique principale.
*   `gui.py`: Cœur de l'interface utilisateur graphique (GUI). Utilise CustomTkinter, Matplotlib, Plotly et ReportLab pour offrir une expérience riche et interactive.
*   `complete_example.py`: Fournit une interface en ligne de commande (CLI) complète et interactive pour définir, résoudre et gérer les problèmes de PL.
*   `tab_method.py`: Implémentation de la méthode du Simplexe standard (tabulaire).
*   `grand_M_method.py`: Implémentation de la méthode du Grand M.
*   `dual_method.py`: Implémentation de la construction du problème dual et de l'analyse primal-dual.
*   `enhanced_variables.py`: Fonctions améliorées pour la saisie des variables, l'affichage des tableaux simplexe en console (avec `tabulate`, `colorama`), et la gestion de l'historique des problèmes.
*   `variables.py`: Fonctions de base (potentiellement une version initiale) pour la saisie et l'affichage des variables et tableaux.
*   `SimplexSolver.spec`: Fichier de configuration pour PyInstaller, permettant de packager l'application en un exécutable.
*   `setup.py`: Script de configuration pour cx_Freeze, une autre option pour créer un exécutable.
*   `.gitignore`: Spécifie les fichiers et dossiers à ignorer par Git.
*   `icon.ico`: Icône utilisée pour l'application et l'exécutable.

## Technologies Utilisées

*   **Langage :** Python 3.x
*   **Interface Graphique (GUI) :**
    *   Tkinter (bibliothèque standard Python)
    *   CustomTkinter (pour un look moderne)
*   **Visualisation de Données :**
    *   Matplotlib (graphiques 2D)
    *   Plotly (graphiques 3D interactifs)
*   **Manipulation de Données :**
    *   NumPy (pour les calculs numériques, implicitement via Matplotlib/Plotly)
    *   Pandas (potentiellement pour la gestion de données tabulaires, importé dans `gui.py`)
*   **Interface Console (CLI) :**
    *   Colorama (texte coloré)
    *   Tabulate (affichage de tableaux en console)
*   **Exportation :**
    *   ReportLab (génération de PDF)
*   **Packaging :**
    *   PyInstaller
    *   cx_Freeze

## Installation et Utilisation

### Option 1 : Exécutable Pré-compilé (Windows)

Un exécutable pour Windows est disponible au téléchargement. Cela vous permet d'utiliser l'application sans avoir à installer Python ou les dépendances manuellement.

*   **Télécharger l'exécutable :** [SimplexSolver.exe via Google Drive](https://drive.google.com/file/d/1_pgSaU6TG14vFB8ZcEdVEToY079U3rLY/view?usp=sharing)
*   Après le téléchargement, vous pouvez simplement exécuter le fichier `SimplexSolver.exe`.

### Option 2 : Depuis le Code Source

1.  **Prérequis :**
    *   Python 3.8 ou supérieur.
    *   `pip` (gestionnaire de paquets Python).

2.  **Cloner le Dépôt (si applicable) ou Télécharger les Fichiers Source :**
    ```bash
    # Si c'est un dépôt Git
    git clone <url-du-depot>
    cd <nom-du-dossier-du-projet>
    ```

3.  **Créer un Environnement Virtuel (Recommandé) :**
    ```bash
    python -m venv venv
    # Sous Windows
    .\venv\Scripts\activate
    # Sous macOS/Linux
    source venv/bin/activate
    ```

4.  **Installer les Dépendances :**
    Les dépendances principales sont listées dans `SimplexSolver.spec` et `setup.py`. Vous pouvez les installer manuellement ou créer un fichier `requirements.txt`.
    ```bash
    pip install customtkinter matplotlib numpy colorama tabulate pandas plotly reportlab seaborn Pillow
    ```
    *(Note: `seaborn` et `Pillow` sont listés comme dépendances cachées ou pour des fonctionnalités spécifiques dans le `.spec`)*

### Lancement de l'Application (depuis le code source)

*   **Interface Graphique (GUI) :**
    Pour démarrer l'application avec son interface graphique moderne et son lanceur premium :
    ```bash
    python main.py
    ```

*   **Interface en Ligne de Commande (CLI) :**
    Pour utiliser la version console interactive :
    ```bash
    python complete_example.py
    ```
    Suivez les instructions affichées dans le terminal pour définir et résoudre votre problème.

## Création de l'Exécutable (depuis le code source)

Si vous souhaitez recompiler l'exécutable :

### Avec PyInstaller

Utilisez le fichier `.spec` fourni :

```bash
pyinstaller SimplexSolver.spec
```