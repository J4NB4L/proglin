from tabulate import tabulate
from colorama import init, Fore, Style
import json
import os
from datetime import datetime

# Initialiser colorama
init()

class VariableManager:
    def __init__(self):
        self.history = []
        self.current_problem = None
        
    def save_problem(self, variables, method_name, filename=None):
        """Sauvegarde un problème avec métadonnées"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        problem_data = {
            "timestamp": timestamp,
            "method": method_name,
            "variables": variables,
            "metadata": {
                "nb_variables": variables.get("nombres_variables_base", 0),
                "nb_contraintes": variables.get("nb_equations", 0),
                "constraints_types": variables.get("constraints_info", [])
            }
        }
        
        self.history.append(problem_data)
        
        if filename:
            self.save_to_file(problem_data, filename)
        
        return len(self.history) - 1  # Retourne l'index
    
    def save_to_file(self, problem_data, filename):
        """Sauvegarde dans un fichier JSON"""
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(problem_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Problème sauvegardé dans {filename}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
    
    def load_from_file(self, filename):
        """Charge un problème depuis un fichier JSON"""
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                problem_data = json.load(f)
            
            self.history.append(problem_data)
            print(f"✅ Problème chargé depuis {filename}")
            return problem_data["variables"]
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return None
    
    def list_history(self):
        """Affiche l'historique des problèmes"""
        if not self.history:
            print("Aucun problème dans l'historique.")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print("HISTORIQUE DES PROBLÈMES")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        for i, problem in enumerate(self.history):
            print(f"\n{Fore.YELLOW}[{i}] {problem['method']}{Style.RESET_ALL}")
            print(f"  📅 {problem['timestamp']}")
            print(f"  📊 {problem['metadata']['nb_variables']} variables, {problem['metadata']['nb_contraintes']} contraintes")
            if problem['metadata']['constraints_types']:
                print(f"  🔗 Contraintes: {', '.join(problem['metadata']['constraints_types'])}")
    
    def get_problem(self, index):
        """Récupère un problème par son index"""
        if 0 <= index < len(self.history):
            return self.history[index]["variables"]
        return None

def enhanced_tab_var(nombres_variables_base: int, nb_equations: int, method_type="Simplexe Standard") -> dict:
    """Version améliorée de tab_var avec plus d'options"""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"CONFIGURATION - {method_type.upper()}")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"📈 {nombres_variables_base} variables de décision")
    print(f"📋 {nb_equations} contraintes")
    
    # Fonction objectif
    tab_optimisation = [0]
    print(f"\n{Fore.GREEN}[1] FONCTION OBJECTIF{Style.RESET_ALL}")
    
    # Choix min/max
    obj_type = input("Type d'optimisation (max/min) [max]: ").lower() or "max"
    
    print(f"Fonction à {obj_type}imiser: Z = ", end="")
    for i in range(nombres_variables_base):
        if i > 0:
            print(" + ", end="")
        print(f"c{i+1}x{i+1}", end="")
    print()
    
    coefficients = []
    for i in range(nombres_variables_base):
        while True:
            try:
                coeff = float(input(f"c{i+1} = {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                coefficients.append(coeff)
                tab_optimisation.append(coeff)
                break
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
    
    # Contraintes
    print(f"\n{Fore.GREEN}[2] CONTRAINTES{Style.RESET_ALL}")
    equations = {}
    constraints_info = []
    
    # Options pour les contraintes
    if method_type in ["Grand M", "Deux Phases"]:
        print("Types de contraintes disponibles: ≤ (<=), ≥ (>=), = (=)")
    
    data_table = []
    headers = ["Contrainte"] + [f"x{i+1}" for i in range(nombres_variables_base)] + ["Type", "b"]
    
    for j in range(nb_equations):
        print(f"\n{Fore.BLUE}Contrainte {j+1}:{Style.RESET_ALL}")
        
        equation = []
        # Membre de droite
        while True:
            try:
                b_value = float(input(f"Membre de droite b{j+1} = {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                equation.append(b_value)
                break
            except ValueError:
                print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
        
        # Coefficients
        coeffs = []
        for k in range(nombres_variables_base):
            while True:
                try:
                    coeff = float(input(f"a{j+1}{k+1} (coeff. de x{k+1}) = {Fore.YELLOW}"))
                    print(Style.RESET_ALL, end="")
                    coeffs.append(coeff)
                    equation.append(coeff)
                    break
                except ValueError:
                    print(f"{Fore.RED}Veuillez entrer un nombre valide.{Style.RESET_ALL}")
        
        # Type de contrainte
        if method_type in ["Grand M", "Deux Phases"]:
            while True:
                constraint_type = input("Type de contrainte (<=, >=, =) [<=]: ") or "<="
                if constraint_type in ["<=", ">=", "="]:
                    constraints_info.append(constraint_type)
                    break
                print(f"{Fore.RED}Type invalide. Utilisez <=, >= ou ={Style.RESET_ALL}")
        else:
            constraint_type = "<="
            constraints_info.append(constraint_type)
        
        equations[f"equation_{j+1}"] = equation
        data_table.append([f"C{j+1}"] + coeffs + [constraint_type, b_value])
    
    # Récapitulatif
    print(f"\n{Fore.CYAN}{'='*70}")
    print("RÉCAPITULATIF DU PROBLÈME")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    obj_row = [f"{obj_type.title()}imiser Z"] + coefficients + ["", tab_optimisation[0]]
    
    print(f"\n{tabulate([obj_row] + data_table, headers=headers, tablefmt='grid', floatfmt='.3f')}")
    
    # Confirmation
    while True:
        confirm = input(f"\n{Fore.YELLOW}Confirmer ce problème ? (o/n) [o]: {Style.RESET_ALL}") or "o"
        if confirm.lower() in ['o', 'oui', 'y', 'yes']:
            break
        elif confirm.lower() in ['n', 'non', 'no']:
            print("❌ Annulation...")
            return None
        
    # Ajustement pour minimisation
    if obj_type == "min":
        tab_optimisation = [tab_optimisation[0]] + [-x for x in tab_optimisation[1:]]
    
    variables = {
        "tab_optimisation": tab_optimisation,
        "nombres_variables_base": nombres_variables_base,
        "equations": equations,
        "nb_equations": nb_equations,
        "constraints_info": constraints_info,
        "objective_type": obj_type,
        "method_type": method_type
    }
    
    # Proposition de sauvegarde
    save = input(f"{Fore.GREEN}Sauvegarder ce problème ? (o/n) [n]: {Style.RESET_ALL}") or "n"
    if save.lower() in ['o', 'oui', 'y', 'yes']:
        filename = input("Nom du fichier [auto]: ") or f"probleme_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        manager = VariableManager()
        manager.save_to_file({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": method_type,
            "variables": variables,
            "metadata": {
                "nb_variables": nombres_variables_base,
                "nb_contraintes": nb_equations,
                "constraints_types": constraints_info
            }
        }, filename)
    
    return variables

def enhanced_display_simplex_tableau(variables, iteration=0, method_name="Simplexe"):
    """Version améliorée de l'affichage du tableau"""
    equations = variables["equations"]
    tab_optimisation = variables["tab_optimisation"]
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"TABLEAU {method_name.upper()} - ITÉRATION {iteration}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    # Information sur le type d'objectif
    obj_type = variables.get("objective_type", "max")
    print(f"🎯 Objectif: {obj_type}imisation")
    
    # Calcul du nombre de variables totales
    nb_vars_base = variables["nombres_variables_base"]
    total_vars = len(tab_optimisation) - 1
    nb_slack_artificial = total_vars - nb_vars_base
    
    # En-têtes dynamiques
    headers = ["Base", "Cst"]
    headers.extend([f"x{i+1}" for i in range(nb_vars_base)])
    
    # Variables d'écart et artificielles
    if nb_slack_artificial > 0:
        constraints_info = variables.get("constraints_info", [])
        var_index = nb_vars_base + 1
        
        for i, constraint_type in enumerate(constraints_info):
            if constraint_type == "<=":
                headers.append(f"s{i+1}")
                var_index += 1
            elif constraint_type == ">=":
                headers.append(f"s{i+1}")
                headers.append(f"a{i+1}")
                var_index += 2
            elif constraint_type == "=":
                headers.append(f"a{i+1}")
                var_index += 1
    
    # Construction des lignes
    rows = []
    
    # Ligne de la fonction objectif
    obj_row = [f"Z ({obj_type})"] + tab_optimisation
    # Compléter avec des zéros si nécessaire
    while len(obj_row) < len(headers):
        obj_row.append(0)
    rows.append(obj_row)
    
    # Lignes des contraintes
    base_vars = []
    for i, (key, eq) in enumerate(equations.items()):
        # Déterminer la variable de base pour cette ligne
        base_var = f"s{i+1}"  # Par défaut
        
        # Chercher la variable de base réelle
        for j in range(1, len(eq)):
            if abs(eq[j] - 1.0) < 1e-10:
                # Vérifier que c'est bien une variable de base
                others_zero = True
                for other_key, other_eq in equations.items():
                    if other_key != key and j < len(other_eq) and abs(other_eq[j]) > 1e-10:
                        others_zero = False
                        break
                if others_zero:
                    if j <= nb_vars_base:
                        base_var = f"x{j}"
                    else:
                        # Variable d'écart ou artificielle
                        base_var = headers[j+1] if j+1 < len(headers) else f"var{j}"
                    break
        
        base_vars.append(base_var)
        row = [base_var] + eq
        # Compléter avec des zéros si nécessaire
        while len(row) < len(headers):
            row.append(0)
        rows.append(row)
    
    # Affichage du tableau
    print(f"\n{tabulate(rows, headers=headers, tablefmt='grid', floatfmt='.3f')}")
    
    # Informations supplémentaires
    if iteration > 0:
        z_value = tab_optimisation[0]
        print(f"\n📊 Valeur actuelle de Z: {z_value:.6f}")
        
        # Variables de base actuelles
        print(f"🔧 Variables de base: {', '.join(base_vars)}")
    
    return {"base_variables": base_vars, "z_value": tab_optimisation[0]}

def interactive_problem_builder():
    """Interface interactive pour construire un problème"""
    print(f"{Fore.MAGENTA}{'='*70}")
    print("CONSTRUCTEUR INTERACTIF DE PROBLÈMES")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    print("🚀 Méthodes disponibles:")
    methods = {
        "1": ("Simplexe Standard", "tab_var"),
        "2": ("Grand M", "enhanced_tab_var"),
        "3": ("Deux Phases", "enhanced_tab_var"),
        "4": ("Charger depuis fichier", "load_file")
    }
    
    for key, (name, _) in methods.items():
        print(f"  {key}. {name}")
    
    while True:
        choice = input(f"\n{Fore.YELLOW}Choisissez une méthode (1-4): {Style.RESET_ALL}")
        if choice in methods:
            method_name, method_type = methods[choice]
            break
        print(f"{Fore.RED}Choix invalide{Style.RESET_ALL}")
    
    if method_type == "load_file":
        filename = input("Nom du fichier à charger: ")
        manager = VariableManager()
        variables = manager.load_from_file(filename)
        return variables, "Fichier chargé"
    
    # Saisie des dimensions
    while True:
        try:
            nb_vars = int(input(f"\n{Fore.CYAN}Nombre de variables de décision: {Style.RESET_ALL}"))
            if nb_vars > 0:
                break
            print(f"{Fore.RED}Le nombre doit être positif{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un nombre entier{Style.RESET_ALL}")
    
    while True:
        try:
            nb_constraints = int(input(f"{Fore.CYAN}Nombre de contraintes: {Style.RESET_ALL}"))
            if nb_constraints > 0:
                break
            print(f"{Fore.RED}Le nombre doit être positif{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Veuillez entrer un nombre entier{Style.RESET_ALL}")
    
    # Construction du problème
    variables = enhanced_tab_var(nb_vars, nb_constraints, method_name)
    
    return variables, method_name

# Mise à jour de la fonction display_simplex_tableau existante
def display_simplex_tableau(variables, iteration=0):
    """Wrapper pour maintenir la compatibilité"""
    method_name = variables.get("method_type", "Simplexe")
    return enhanced_display_simplex_tableau(variables, iteration, method_name)

if __name__ == "__main__":
    # Test du système amélioré
    print("Test du système d'enregistrement amélioré")
    
    # Interface interactive
    variables, method = interactive_problem_builder()
    
    if variables:
        print("\n✅ Problème construit avec succès!")
        display_simplex_tableau(variables, 0)