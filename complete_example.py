#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple complet d'utilisation des méthodes de programmation linéaire
Inclut: Simplexe Standard, Grand M, Dual, et système d'enregistrement
"""

import sys
import os
from enhanced_variables import interactive_problem_builder, VariableManager, enhanced_display_simplex_tableau
from tab_method import SimplexMethodTab
from grand_M_method import GrandMMethod
from dual_method import DualMethod
from colorama import init, Fore, Style

init()

class LinearProgrammingSolver:
    def __init__(self):
        self.variable_manager = VariableManager()
        self.current_problem = None
        self.current_method = None
    
    def main_menu(self):
        """Menu principal de l'application"""
        while True:
            print(f"\n{Fore.MAGENTA}{'='*80}")
            print("🔬 SOLVEUR DE PROGRAMMATION LINÉAIRE")
            print(f"{'='*80}{Style.RESET_ALL}")
            
            options = {
                "1": "📝 Créer un nouveau problème",
                "2": "📂 Charger un problème existant", 
                "3": "🔍 Résoudre le problème actuel",
                "4": "🔄 Analyser Primal-Dual",
                "5": "📊 Historique des problèmes",
                "6": "💾 Sauvegarder le problème actuel",
                "7": "❌ Quitter"
            }
            
            for key, desc in options.items():
                print(f"  {key}. {desc}")
            
            if self.current_problem:
                method = self.current_problem.get("method_type", "Inconnu")
                vars_count = self.current_problem.get("nombres_variables_base", 0)
                constraints_count = self.current_problem.get("nb_equations", 0)
                print(f"\n📌 Problème actuel: {method} ({vars_count} vars, {constraints_count} contraintes)")
            
            choice = input(f"\n{Fore.YELLOW}Votre choix: {Style.RESET_ALL}")
            
            if choice == "1":
                self.create_new_problem()
            elif choice == "2":
                self.load_problem()
            elif choice == "3":
                self.solve_current_problem()
            elif choice == "4":
                self.dual_analysis()
            elif choice == "5":
                self.show_history()
            elif choice == "6":
                self.save_current_problem()
            elif choice == "7":
                print("👋 Au revoir!")
                break
            else:
                print(f"{Fore.RED}❌ Choix invalide{Style.RESET_ALL}")
    
    def create_new_problem(self):
        """Crée un nouveau problème"""
        print(f"\n{Fore.CYAN}📝 CRÉATION D'UN NOUVEAU PROBLÈME{Style.RESET_ALL}")
        
        try:
            variables, method = interactive_problem_builder()
            if variables:
                self.current_problem = variables
                self.current_method = method
                
                # Sauvegarde automatique dans l'historique
                index = self.variable_manager.save_problem(variables, method)
                print(f"✅ Problème créé et sauvegardé (index: {index})")
                
                # Affichage du problème
                enhanced_display_simplex_tableau(variables, 0, method)
            else:
                print(f"{Fore.RED}❌ Création annulée{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Erreur lors de la création: {e}{Style.RESET_ALL}")
    
    def load_problem(self):
        """Charge un problème existant"""
        print(f"\n{Fore.CYAN}📂 CHARGEMENT D'UN PROBLÈME{Style.RESET_ALL}")
        
        print("Options de chargement:")
        print("1. Depuis un fichier")
        print("2. Depuis l'historique")
        print("3. Exemples prédéfinis")
        
        choice = input("Votre choix (1-3): ")
        
        if choice == "1":
            filename = input("Nom du fichier: ")
            variables = self.variable_manager.load_from_file(filename)
            if variables:
                self.current_problem = variables
                self.current_method = variables.get("method_type", "Chargé")
                enhanced_display_simplex_tableau(variables, 0, self.current_method)
        
        elif choice == "2":
            self.variable_manager.list_history()
            if self.variable_manager.history:
                try:
                    index = int(input("Index du problème à charger: "))
                    variables = self.variable_manager.get_problem(index)
                    if variables:
                        self.current_problem = variables
                        self.current_method = self.variable_manager.history[index]["method"]
                        print(f"✅ Problème {index} chargé")
                        enhanced_display_simplex_tableau(variables, 0, self.current_method)
                    else:
                        print(f"{Fore.RED}❌ Index invalide{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}❌ Index invalide{Style.RESET_ALL}")
        
        elif choice == "3":
            self.load_predefined_examples()
        else:
            print(f"{Fore.RED}❌ Choix invalide{Style.RESET_ALL}")
    
    def load_predefined_examples(self):
        """Charge des exemples prédéfinis"""
        examples = {
            "1": {
                "name": "Exemple Standard (3x₁ + 5x₂)",
                "variables": {
                    "tab_optimisation": [0, 3, 5],
                    "nombres_variables_base": 2,
                    "equations": {
                        "equation_1": [4, 1, 0],
                        "equation_2": [12, 0, 2],
                        "equation_3": [18, 3, 2],
                    },
                    "nb_equations": 3,
                    "method_type": "Simplexe Standard"
                }
            },
            "2": {
                "name": "Exemple Grand M (avec contrainte d'égalité)",
                "variables": {
                    "tab_optimisation": [0, 3, 5],
                    "nombres_variables_base": 2,
                    "equations": {
                        "equation_1": [4, 1, 0],
                        "equation_2": [12, 0, 2],
                        "equation_3": [18, 3, 2],
                    },
                    "nb_equations": 3,
                    "constraints_info": ["<=", "<=", "="],
                    "method_type": "Grand M"
                }
            },
            "3": {
                "name": "Problème de minimisation",
                "variables": {
                    "tab_optimisation": [0, -7, -6, -5],  # Min devient Max avec -
                    "nombres_variables_base": 3,
                    "equations": {
                        "equation_1": [18, 3, 8, 6],
                        "equation_2": [15, 1, 2, 6],
                    },
                    "nb_equations": 2,
                    "constraints_info": ["=", "="],
                    "method_type": "Grand M",
                    "objective_type": "min"
                }
            }
        }
        
        print("\nExemples disponibles:")
        for key, example in examples.items():
            print(f"  {key}. {example['name']}")
        
        choice = input("Choisir un exemple (1-3): ")
        if choice in examples:
            self.current_problem = examples[choice]["variables"]
            self.current_method = examples[choice]["variables"]["method_type"]
            print(f"✅ {examples[choice]['name']} chargé")
            enhanced_display_simplex_tableau(self.current_problem, 0, self.current_method)
        else:
            print(f"{Fore.RED}❌ Exemple invalide{Style.RESET_ALL}")
    
    def solve_current_problem(self):
        """Résout le problème actuel"""
        if not self.current_problem:
            print(f"{Fore.RED}❌ Aucun problème à résoudre. Créez ou chargez un problème d'abord.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🔍 RÉSOLUTION DU PROBLÈME{Style.RESET_ALL}")
        
        # Déterminer la méthode appropriée
        constraints_info = self.current_problem.get("constraints_info", [])
        has_equality = "=" in constraints_info
        has_greater_equal = ">=" in constraints_info
        
        print("Méthodes de résolution disponibles:")
        methods = ["1. Simplexe Standard"]
        
        if has_equality or has_greater_equal:
            methods.extend(["2. Grand M", "3. Deux Phases (non implémenté)"])
        
        for method in methods:
            print(f"  {method}")
        
        # Suggestion automatique
        if has_equality or has_greater_equal:
            suggested = "2"
            print(f"\n💡 Méthode suggérée: Grand M (contraintes d'égalité ou ≥ détectées)")
        else:
            suggested = "1"
            print(f"\n💡 Méthode suggérée: Simplexe Standard")
        
        choice = input(f"Votre choix [{suggested}]: ") or suggested
        
        try:
            if choice == "1":
                self.solve_with_standard_simplex()
            elif choice == "2":
                self.solve_with_grand_m()
            elif choice == "3":
                print(f"{Fore.YELLOW}⚠️ Méthode des deux phases non encore implémentée{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Choix invalide{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Erreur lors de la résolution: {e}{Style.RESET_ALL}")
    
    def solve_with_standard_simplex(self):
        """Résout avec la méthode du simplexe standard"""
        print(f"\n{Fore.GREEN}🚀 Résolution par Simplexe Standard{Style.RESET_ALL}")
        
        # Copie pour éviter de modifier l'original
        import copy
        problem_copy = copy.deepcopy(self.current_problem)
        
        solver = SimplexMethodTab(problem_copy)
        solver.run()
    
    def solve_with_grand_m(self):
        """Résout avec la méthode du Grand M"""
        print(f"\n{Fore.GREEN}🚀 Résolution par Grand M{Style.RESET_ALL}")
        
        # Copie pour éviter de modifier l'original
        import copy
        problem_copy = copy.deepcopy(self.current_problem)
        
        solver = GrandMMethod(problem_copy)
        solver.run()
    
    def dual_analysis(self):
        """Effectue une analyse primal-dual"""
        if not self.current_problem:
            print(f"{Fore.RED}❌ Aucun problème pour l'analyse duale.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🔄 ANALYSE PRIMAL-DUAL{Style.RESET_ALL}")
        
        # Vérifier si le problème est compatible avec l'analyse duale
        constraints_info = self.current_problem.get("constraints_info", [])
        if any(c in [">=", "="] for c in constraints_info):
            print(f"{Fore.YELLOW}⚠️ Le problème contient des contraintes ≥ ou =.")
            print("L'analyse duale sera effectuée après conversion en forme standard.{Style.RESET_ALL}")
        
        try:
            import copy
            problem_copy = copy.deepcopy(self.current_problem)
            
            dual_analyzer = DualMethod(problem_copy)
            dual_analyzer.run_complete_analysis()
        except Exception as e:
            print(f"{Fore.RED}❌ Erreur lors de l'analyse duale: {e}{Style.RESET_ALL}")
    
    def show_history(self):
        """Affiche l'historique des problèmes"""
        print(f"\n{Fore.CYAN}📊 HISTORIQUE DES PROBLÈMES{Style.RESET_ALL}")
        self.variable_manager.list_history()
    
    def save_current_problem(self):
        """Sauvegarde le problème actuel"""
        if not self.current_problem:
            print(f"{Fore.RED}❌ Aucun problème à sauvegarder.{Style.RESET_ALL}")
            return
        
        filename = input("Nom du fichier de sauvegarde: ")
        if filename:
            self.variable_manager.save_to_file({
                "timestamp": "Manual save",
                "method": self.current_method or "Inconnu",
                "variables": self.current_problem,
                "metadata": {
                    "nb_variables": self.current_problem.get("nombres_variables_base", 0),
                    "nb_contraintes": self.current_problem.get("nb_equations", 0),
                    "constraints_types": self.current_problem.get("constraints_info", [])
                }
            }, filename)

def demo_complete():
    """Démonstration complète des fonctionnalités"""
    print(f"{Fore.MAGENTA}{'='*80}")
    print("🎯 DÉMONSTRATION COMPLÈTE DU SOLVEUR")
    print(f"{'='*80}{Style.RESET_ALL}")
    
    # Exemple 1: Problème standard
    print(f"\n{Fore.CYAN}📋 EXEMPLE 1: Problème Standard{Style.RESET_ALL}")
    variables_std = {
        "tab_optimisation": [0, 3, 5],
        "nombres_variables_base": 2,
        "equations": {
            "equation_1": [4, 1, 0],
            "equation_2": [12, 0, 2],
            "equation_3": [18, 3, 2],
        },
        "nb_equations": 3,
        "method_type": "Simplexe Standard"
    }
    
    print("Max Z = 3x₁ + 5x₂")
    print("  x₁ ≤ 4")
    print("  2x₂ ≤ 12")  
    print("  3x₁ + 2x₂ ≤ 18")
    
    solver_std = SimplexMethodTab(variables_std)
    solver_std.run()
    
    # Exemple 2: Grand M
    print(f"\n{Fore.CYAN}📋 EXEMPLE 2: Méthode du Grand M{Style.RESET_ALL}")
    variables_gm = {
        "tab_optimisation": [0, 3, 5],
        "nombres_variables_base": 2,
        "equations": {
            "equation_1": [4, 1, 0],
            "equation_2": [12, 0, 2],
            "equation_3": [18, 3, 2],
        },
        "nb_equations": 3,
        "constraints_info": ["<=", "<=", "="],
        "method_type": "Grand M"
    }
    
    print("Max Z = 3x₁ + 5x₂")
    print("  x₁ ≤ 4")
    print("  2x₂ ≤ 12")
    print("  3x₁ + 2x₂ = 18")
    
    solver_gm = GrandMMethod(variables_gm)
    solver_gm.run()
    
    # Exemple 3: Analyse duale
    print(f"\n{Fore.CYAN}📋 EXEMPLE 3: Analyse Primal-Dual{Style.RESET_ALL}")
    dual_analyzer = DualMethod(variables_std)
    dual_analyzer.run_complete_analysis()

if __name__ == "__main__":
    print("Choisir le mode d'exécution:")
    print("1. Interface interactive")
    print("2. Démonstration complète")
    
    choice = input("Votre choix (1-2): ")
    
    if choice == "1":
        app = LinearProgrammingSolver()
        app.main_menu()
    elif choice == "2":
        demo_complete()
    else:
        print("Choix invalide, lancement de l'interface interactive par défaut...")
        app = LinearProgrammingSolver()
        app.main_menu()