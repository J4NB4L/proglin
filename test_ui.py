from tabulate import tabulate
from colorama import init, Fore, Style, Back
import os
import time
from typing import Dict, List, Tuple

# Initialiser colorama
init(autoreset=True)

class SimplexInterface:
    """Interface moderne pour la méthode du simplexe"""
    
    def __init__(self):
        self.clear_screen()
        self.show_welcome()
    
    def clear_screen(self):
        """Nettoie l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Affiche l'écran de bienvenue"""
        self.clear_screen()
        print(Fore.CYAN + "="*80)
        print(Fore.CYAN + " "*20 + "🎯 MÉTHODE DU SIMPLEXE 🎯")
        print(Fore.CYAN + "="*80)
        print(Fore.WHITE + "\n" + " "*15 + "Optimisation Linéaire Interactive")
        print(Fore.YELLOW + " "*20 + "Version 2.0 - Interface Améliorée\n")
        print(Fore.CYAN + "="*80)
        time.sleep(2)
    
    def show_menu(self):
        """Affiche le menu principal"""
        self.clear_screen()
        print(Fore.BLUE + "\n╔═══════════════════════════════════════════════════════╗")
        print(Fore.BLUE + "║" + Fore.WHITE + "                  MENU PRINCIPAL                       " + Fore.BLUE + "║")
        print(Fore.BLUE + "╠═══════════════════════════════════════════════════════╣")
        print(Fore.BLUE + "║" + Fore.GREEN + "  1. " + Fore.WHITE + "📝 Nouveau problème                              " + Fore.BLUE + "║")
        print(Fore.BLUE + "║" + Fore.GREEN + "  2. " + Fore.WHITE + "📊 Charger un exemple                            " + Fore.BLUE + "║")
        print(Fore.BLUE + "║" + Fore.GREEN + "  3. " + Fore.WHITE + "📚 Aide et tutoriel                              " + Fore.BLUE + "║")
        print(Fore.BLUE + "║" + Fore.GREEN + "  4. " + Fore.WHITE + "🚪 Quitter                                       " + Fore.BLUE + "║")
        print(Fore.BLUE + "╚═══════════════════════════════════════════════════════╝\n")
        
    def get_menu_choice(self):
        """Obtient le choix du menu"""
        while True:
            choice = input(Fore.YELLOW + "Votre choix (1-4): " + Fore.WHITE)
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            print(Fore.RED + "❌ Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
    
    def show_problem_type_menu(self):
        """Menu pour choisir le type de problème"""
        print(Fore.CYAN + "\n🎯 Type de problème:")
        print(Fore.WHITE + "  1. Maximisation")
        print(Fore.WHITE + "  2. Minimisation")
        
        while True:
            choice = input(Fore.YELLOW + "\nVotre choix (1 ou 2): " + Fore.WHITE)
            if choice in ['1', '2']:
                return choice == '1'  # True pour Max, False pour Min
            print(Fore.RED + "❌ Choix invalide.")


class ImprovedSimplexInput:
    """Classe améliorée pour la saisie des données du simplexe"""
    
    def __init__(self):
        self.interface = SimplexInterface()
        
    def get_problem_dimensions(self) -> Tuple[int, int]:
        """Obtient les dimensions du problème avec validation améliorée"""
        print(Fore.CYAN + "\n📐 DIMENSIONS DU PROBLÈME")
        print(Fore.CYAN + "━" * 40)
        
        # Nombre de variables
        while True:
            try:
                n_vars = input(Fore.GREEN + "\n📊 Nombre de variables de décision: " + Fore.WHITE)
                n_vars = int(n_vars)
                if n_vars <= 0:
                    print(Fore.RED + "❌ Le nombre doit être positif.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "❌ Veuillez entrer un nombre entier.")
        
        # Nombre de contraintes
        while True:
            try:
                n_constraints = input(Fore.GREEN + "\n🔗 Nombre de contraintes: " + Fore.WHITE)
                n_constraints = int(n_constraints)
                if n_constraints <= 0:
                    print(Fore.RED + "❌ Le nombre doit être positif.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "❌ Veuillez entrer un nombre entier.")
        
        print(Fore.YELLOW + f"\n✅ Problème de dimension {n_vars}x{n_constraints} créé!")
        return n_vars, n_constraints
    
    def get_objective_function(self, n_vars: int, is_max: bool) -> List[float]:
        """Saisie de la fonction objectif avec aide visuelle"""
        obj_type = "MAXIMISATION" if is_max else "MINIMISATION"
        print(Fore.CYAN + f"\n🎯 FONCTION OBJECTIF ({obj_type})")
        print(Fore.CYAN + "━" * 50)
        
        # Affichage de la forme générale
        var_names = [f"x{chr(0x2081+i)}" for i in range(n_vars)]
        formula = " + ".join([f"c{chr(0x2081+i)}{var_names[i]}" for i in range(n_vars)])
        print(Fore.WHITE + f"\nForme: {'Max' if is_max else 'Min'} Z = {formula}")
        print(Fore.YELLOW + "\nEntrez les coefficients:")
        
        coefficients = [0]  # Premier élément pour Z
        
        for i in range(n_vars):
            while True:
                try:
                    prompt = f"{Fore.GREEN}  c{chr(0x2081+i)} = {Fore.WHITE}"
                    coeff = float(input(prompt))
                    coefficients.append(coeff)
                    break
                except ValueError:
                    print(Fore.RED + "  ❌ Veuillez entrer un nombre valide.")
        
        # Afficher la fonction objectif complète
        print(Fore.CYAN + "\n✅ Fonction objectif:")
        actual_formula = " + ".join([f"{coefficients[i+1]}{var_names[i]}" 
                                    for i in range(n_vars)])
        print(Fore.WHITE + f"   {'Max' if is_max else 'Min'} Z = {actual_formula}")
        
        return coefficients
    
    def get_constraints(self, n_vars: int, n_constraints: int) -> Dict:
        """Saisie des contraintes avec interface améliorée"""
        print(Fore.CYAN + "\n🔗 SAISIE DES CONTRAINTES")
        print(Fore.CYAN + "━" * 50)
        
        equations = {}
        constraint_data = []
        var_names = [f"x{chr(0x2081+i)}" for i in range(n_vars)]
        
        for j in range(n_constraints):
            print(Fore.YELLOW + f"\n📋 Contrainte {j+1}:")
            
            # Afficher le format
            formula = " + ".join([f"a{chr(0x2081+i)}{chr(0x2081+j)}{var_names[i]}" 
                                 for i in range(n_vars)])
            print(Fore.WHITE + f"   {formula} ≤ b{chr(0x2081+j)}")
            
            key_eq = f"equation_{j+1}"
            equations[key_eq] = []
            
            # Saisir d'abord b (membre de droite)
            while True:
                try:
                    b_value = float(input(Fore.GREEN + f"   b{chr(0x2081+j)} = " + Fore.WHITE))
                    if b_value < 0:
                        print(Fore.YELLOW + "   ⚠️  Valeur négative détectée. Êtes-vous sûr? (o/n): ", end="")
                        if input().lower() != 'o':
                            continue
                    equations[key_eq].append(b_value)
                    break
                except ValueError:
                    print(Fore.RED + "   ❌ Veuillez entrer un nombre valide.")
            
            # Saisir les coefficients
            coeffs = []
            print(Fore.YELLOW + "   Coefficients:")
            for i in range(n_vars):
                while True:
                    try:
                        coeff = float(input(Fore.GREEN + f"   a{chr(0x2081+i)}{chr(0x2081+j)} = " + Fore.WHITE))
                        coeffs.append(coeff)
                        equations[key_eq].append(coeff)
                        break
                    except ValueError:
                        print(Fore.RED + "   ❌ Veuillez entrer un nombre valide.")
            
            # Stocker pour l'affichage
            constraint_data.append([f"Contrainte {j+1}"] + coeffs + [b_value])
            
            # Afficher la contrainte complète
            actual_formula = " + ".join([f"{coeffs[i]}{var_names[i]}" for i in range(n_vars)])
            print(Fore.CYAN + f"   ✅ {actual_formula} ≤ {b_value}")
        
        return equations, constraint_data
    
    def display_problem_summary(self, variables: Dict, constraint_data: List):
        """Affiche un résumé du problème saisi"""
        print(Fore.CYAN + "\n" + "="*70)
        print(Fore.CYAN + " "*20 + "📊 RÉSUMÉ DU PROBLÈME")
        print(Fore.CYAN + "="*70)
        
        n_vars = variables["nombres_variables_base"]
        var_names = [f"x{chr(0x2081+i)}" for i in range(n_vars)]
        
        # Fonction objectif
        print(Fore.YELLOW + "\n🎯 Fonction Objectif:")
        obj_coeffs = variables["tab_optimisation"][1:]
        obj_formula = " + ".join([f"{obj_coeffs[i]}{var_names[i]}" for i in range(n_vars)])
        print(Fore.WHITE + f"   Max Z = {obj_formula}")
        
        # Contraintes sous forme de tableau
        print(Fore.YELLOW + "\n🔗 Contraintes:")
        headers = [""] + var_names + ["≤", "b"]
        
        # Préparer les données du tableau
        table_data = []
        for i, constraint_row in enumerate(constraint_data):
            row = [constraint_row[0]]  # Nom de la contrainte
            row.extend(constraint_row[1:-1])  # Coefficients
            row.append("≤")
            row.append(constraint_row[-1])  # Valeur b
            table_data.append(row)
        
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid", floatfmt=".2f"))
        
        # Conditions de non-négativité
        print(Fore.YELLOW + "\n📐 Conditions de non-négativité:")
        print(Fore.WHITE + f"   {', '.join(var_names)} ≥ 0")
        
        input(Fore.GREEN + "\n✅ Appuyez sur Entrée pour continuer...")


class ImprovedSimplexDisplay:
    """Classe pour l'affichage amélioré des tableaux du simplexe"""
    
    @staticmethod
    def display_iteration_header(iteration: int):
        """Affiche l'en-tête d'une itération"""
        if iteration == 0:
            print(Fore.BLUE + "\n" + "╔" + "═"*60 + "╗")
            print(Fore.BLUE + "║" + Fore.WHITE + " "*20 + "TABLEAU INITIAL" + " "*25 + Fore.BLUE + "║")
            print(Fore.BLUE + "╚" + "═"*60 + "╝")
        else:
            print(Fore.BLUE + "\n" + "╔" + "═"*60 + "╗")
            print(Fore.BLUE + "║" + Fore.WHITE + f" "*20 + f"ITÉRATION {iteration}" + " "*28 + Fore.BLUE + "║")
            print(Fore.BLUE + "╚" + "═"*60 + "╝")
    
    @staticmethod
    def display_tableau(variables: Dict, iteration: int = 0, pivot_info: Dict = None):
        """Affiche le tableau du simplexe avec mise en forme améliorée"""
        equations = variables["equations"]
        tab_optimisation = variables["tab_optimisation"]
        n_vars = variables["nombres_variables_base"]
        n_slack = variables["nb_equations"]
        
        # Headers
        headers = ["VB", "Cte"] + [f"x{i+1}" for i in range(n_vars)] + [f"s{i+1}" for i in range(n_slack)]
        
        # Préparer les données
        rows = []
        
        # Ligne Z
        z_row = ["Z"] + tab_optimisation
        rows.append(z_row)
        
        # Lignes des contraintes
        for i, (key, eq) in enumerate(equations.items()):
            base_var = f"s{i+1}"  # Par défaut
            rows.append([base_var] + eq)
        
        # Colorier le pivot si disponible
        if pivot_info:
            pivot_row = pivot_info.get('row', -1)
            pivot_col = pivot_info.get('col', -1)
            
            if pivot_row >= 0 and pivot_col >= 0:
                # Marquer la cellule pivot
                rows[pivot_row + 1][pivot_col + 1] = (
                    Back.YELLOW + Fore.BLACK + 
                    f"{rows[pivot_row + 1][pivot_col + 1]:.3f}" + 
                    Style.RESET_ALL
                )
        
        print("\n" + tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".3f"))
    
    @staticmethod
    def display_pivot_selection(entering_var: str, leaving_var: str, pivot_value: float):
        """Affiche les informations de sélection du pivot"""
        print(Fore.YELLOW + "\n🎯 Sélection du pivot:")
        print(Fore.GREEN + f"   → Variable entrante: {Fore.WHITE}{entering_var}")
        print(Fore.RED + f"   → Variable sortante: {Fore.WHITE}{leaving_var}")
        print(Fore.CYAN + f"   → Valeur du pivot: {Fore.WHITE}{pivot_value:.3f}")
    
    @staticmethod
    def display_solution(variables: Dict, optimal_value: float):
        """Affiche la solution optimale de manière claire"""
        print(Fore.GREEN + "\n" + "╔" + "═"*60 + "╗")
        print(Fore.GREEN + "║" + Fore.WHITE + " "*18 + "SOLUTION OPTIMALE" + " "*25 + Fore.GREEN + "║")
        print(Fore.GREEN + "╚" + "═"*60 + "╝")
        
        n_vars = variables["nombres_variables_base"]
        
        print(Fore.YELLOW + "\n📊 Valeur optimale de Z: " + Fore.WHITE + f"{optimal_value:.3f}")
        print(Fore.YELLOW + "\n📈 Variables de décision:")
        
        # Extraire les valeurs des variables
        var_values = [0] * n_vars
        for j in range(1, n_vars + 1):
            ones_count = 0
            one_position = -1
            for i, eq in enumerate(variables["equations"].values()):
                if abs(eq[j] - 1.0) < 1e-10:
                    ones_count += 1
                    one_position = i
                elif abs(eq[j]) > 1e-10:
                    ones_count = 0
                    break
            
            if ones_count == 1:
                var_values[j-1] = list(variables["equations"].values())[one_position][0]
        
        for i in range(n_vars):
            print(f"   {Fore.CYAN}x{i+1} = {Fore.WHITE}{var_values[i]:.3f}")
        
        # Afficher les variables d'écart
        print(Fore.YELLOW + "\n📉 Variables d'écart:")
        slack_values = []
        for i in range(variables["nb_equations"]):
            col_idx = n_vars + i + 1
            ones_count = 0
            one_position = -1
            for j, eq in enumerate(variables["equations"].values()):
                if col_idx < len(eq):
                    if abs(eq[col_idx] - 1.0) < 1e-10:
                        ones_count += 1
                        one_position = j
                    elif abs(eq[col_idx]) > 1e-10:
                        ones_count = 0
                        break
            
            if ones_count == 1:
                value = list(variables["equations"].values())[one_position][0]
            else:
                value = 0
            slack_values.append(value)
            print(f"   {Fore.CYAN}s{i+1} = {Fore.WHITE}{value:.3f}")
        
        print(Fore.GREEN + "\n✨ Optimisation terminée avec succès!")


def main():
    """Fonction principale avec l'interface améliorée"""
    interface = SimplexInterface()
    input_handler = ImprovedSimplexInput()
    
    while True:
        interface.show_menu()
        choice = interface.get_menu_choice()
        
        if choice == 1:
            # Nouveau problème
            is_max = interface.show_problem_type_menu()
            n_vars, n_constraints = input_handler.get_problem_dimensions()
            
            # Créer la structure variables
            variables = {
                "nombres_variables_base": n_vars,
                "nb_equations": n_constraints
            }
            
            # Fonction objectif
            tab_optimisation = input_handler.get_objective_function(n_vars, is_max)
            variables["tab_optimisation"] = tab_optimisation
            
            # Contraintes
            equations, constraint_data = input_handler.get_constraints(n_vars, n_constraints)
            variables["equations"] = equations
            
            # Afficher le résumé
            input_handler.display_problem_summary(variables, constraint_data)
            
            # Lancer la résolution
            print(Fore.CYAN + "\n🚀 Lancement de la méthode du simplexe...")
            time.sleep(1)
            
            # Ici, vous pouvez intégrer votre classe SimplexMethodTab
            # simplex = SimplexMethodTab(variables)
            # simplex.run()
            
            input(Fore.YELLOW + "\n📌 Appuyez sur Entrée pour retourner au menu...")
            
        elif choice == 2:
            # Charger un exemple
            print(Fore.CYAN + "\n📊 EXEMPLES DISPONIBLES:")
            print(Fore.WHITE + "1. Problème de production (2 variables, 3 contraintes)")
            print(Fore.WHITE + "2. Problème de transport (3 variables, 4 contraintes)")
            print(Fore.WHITE + "3. Problème d'allocation (4 variables, 5 contraintes)")
            
            example_choice = input(Fore.YELLOW + "\nChoisir un exemple (1-3): " + Fore.WHITE)
            
            if example_choice == "1":
                # Exemple du cours
                variables = {
                    "tab_optimisation": [0, 3, 5],
                    "nombres_variables_base": 2,
                    "equations": {
                        "equation_1": [4, 1, 0],
                        "equation_2": [12, 0, 2],
                        "equation_3": [18, 3, 2]
                    },
                    "nb_equations": 3
                }
                print(Fore.GREEN + "\n✅ Exemple chargé: Problème de production")
                input(Fore.YELLOW + "\nAppuyez sur Entrée pour continuer...")
                
        elif choice == 3:
            # Aide
            interface.clear_screen()
            print(Fore.CYAN + "📚 AIDE ET TUTORIEL")
            print(Fore.CYAN + "="*60)
            print(Fore.WHITE + """
La méthode du simplexe est un algorithme pour résoudre des problèmes
de programmation linéaire. Voici les étapes:

1. FORMULATION: Définir la fonction objectif et les contraintes
2. TABLEAU INITIAL: Convertir en forme standard avec variables d'écart
3. ITÉRATIONS: Améliorer la solution à chaque étape
4. SOLUTION: Obtenir la valeur optimale

CONSEILS:
• Assurez-vous que toutes les contraintes sont de type ≤
• Les valeurs b doivent être positives
• Vérifiez la cohérence de vos données
            """)
            input(Fore.YELLOW + "\nAppuyez sur Entrée pour continuer...")
            
        elif choice == 4:
            # Quitter
            print(Fore.CYAN + "\n👋 Merci d'avoir utilisé le solveur Simplexe!")
            print(Fore.YELLOW + "À bientôt! 🎯\n")
            break


if __name__ == "__main__":
    main()