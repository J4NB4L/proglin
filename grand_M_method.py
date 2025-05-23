from variables import display_simplex_tableau
import copy
from fractions import Fraction

class GrandMMethod:
    def __init__(self, variables: dict):
        self.variables = variables
        self.n = variables["nombres_variables_base"]
        self.M = 1000  # Valeur de M (très grande)
        self.artificial_vars = []
        self.iteration = 0
        
    def run(self):
        """Exécute la méthode du Grand M"""
        print(f"\n{'='*60}")
        print("MÉTHODE DU GRAND M")
        print(f"{'='*60}")
        
        # Ajout des variables d'écart et artificielles
        self.add_slack_and_artificial_variables()
        
        # Modification de la fonction objectif
        self.modify_objective_function()
        
        # Rendre le tableau propre
        self.make_tableau_proper()
        
        # Affichage du tableau initial
        print("\nTableau initial après introduction des variables artificielles:")
        display_simplex_tableau(self.variables, 0)
        
        # Itérations du simplexe
        while self.can_iterate():
            self.iteration += 1
            print(f"\n{'='*20} Itération {self.iteration} {'='*20}")
            
            col = self.find_pivot_column()
            if col == -1:
                break
                
            pivot_row = self.find_pivot_row(col)
            if pivot_row == -1:
                print("Solution illimitée!")
                return
                
            print(f"Colonne pivot : {col}")
            print(f"Ligne pivot : {pivot_row}")
            
            self.pivot_operation(pivot_row, col)
            display_simplex_tableau(self.variables, self.iteration)
        
        self.analyze_final_solution()
    
    def add_slack_and_artificial_variables(self):
        """Ajoute les variables d'écart et artificielles selon le type de contrainte"""
        constraints_info = self.variables.get("constraints_info", [])
        equations = list(self.variables["equations"].values())
        
        # Si pas d'info sur les contraintes, on assume toutes ≤
        if not constraints_info:
            constraints_info = ["<="] * len(equations)
        
        slack_count = 0
        artificial_count = 0
        
        # Modification de la fonction objectif pour inclure les nouvelles variables
        original_vars = len(self.variables["tab_optimisation"])
        
        for i, constraint_type in enumerate(constraints_info):
            if constraint_type == "<=":
                # Variable d'écart
                self.variables["tab_optimisation"].append(0)
                slack_count += 1
            elif constraint_type == ">=":
                # Variable d'écart (négative) + variable artificielle
                self.variables["tab_optimisation"].append(0)  # Variable d'écart
                self.variables["tab_optimisation"].append(-self.M)  # Variable artificielle
                self.artificial_vars.append(original_vars + slack_count + artificial_count + 1)
                slack_count += 1
                artificial_count += 1
            elif constraint_type == "=":
                # Variable artificielle seulement
                self.variables["tab_optimisation"].append(-self.M)
                self.artificial_vars.append(original_vars + slack_count + artificial_count)
                artificial_count += 1
        
        # Modification des équations
        total_new_vars = slack_count + artificial_count
        for i, constraint_type in enumerate(constraints_info):
            current_length = len(equations[i])
            target_length = original_vars + total_new_vars
            
            # Ajouter des zéros pour toutes les nouvelles variables
            while len(equations[i]) < target_length:
                equations[i].append(0)
            
            # Placer les coefficients appropriés
            var_index = original_vars - 1  # -1 car on compte à partir de 0
            
            if constraint_type == "<=":
                var_index += 1
                equations[i][var_index] = 1  # Variable d'écart
            elif constraint_type == ">=":
                var_index += 1
                equations[i][var_index] = -1  # Variable d'écart (négative)
                var_index += 1
                equations[i][var_index] = 1   # Variable artificielle
            elif constraint_type == "=":
                var_index += 1
                equations[i][var_index] = 1   # Variable artificielle
        
        # Mise à jour des équations dans variables
        for k, equation in enumerate(equations):
            self.variables["equations"][list(self.variables["equations"].keys())[k]] = equation
    
    def modify_objective_function(self):
        """Modifie la fonction objectif en ajoutant -M pour les variables artificielles"""
        # La fonction objectif est déjà modifiée dans add_slack_and_artificial_variables
        # On inverse le signe pour la maximisation
        self.variables["tab_optimisation"] = [-x for x in self.variables["tab_optimisation"]]
    
    def make_tableau_proper(self):
        """Rend le tableau propre en éliminant les variables artificielles de la fonction objectif"""
        equations = list(self.variables["equations"].values())
        tab_optimisation = self.variables["tab_optimisation"].copy()
        
        for var_index in self.artificial_vars:
            # Trouver la ligne où cette variable artificielle est de base
            for i, equation in enumerate(equations):
                if var_index < len(equation) and equation[var_index] == 1:
                    # Éliminer cette variable de la fonction objectif
                    coeff = tab_optimisation[var_index]
                    for j in range(len(tab_optimisation)):
                        if j < len(equation):
                            tab_optimisation[j] -= coeff * equation[j]
                    break
        
        self.variables["tab_optimisation"] = tab_optimisation
    
    def find_pivot_column(self):
        """Trouve la colonne pivot (coefficient le plus négatif)"""
        min_val = min(self.variables["tab_optimisation"][1:])
        if min_val >= 0:
            return -1
        return self.variables["tab_optimisation"][1:].index(min_val) + 1
    
    def find_pivot_row(self, col):
        """Trouve la ligne pivot selon la règle du minimum des rapports"""
        equations = list(self.variables["equations"].values())
        min_ratio = float('inf')
        pivot_row = -1
        
        for i, equation in enumerate(equations):
            if col < len(equation) and equation[col] > 0:
                ratio = equation[0] / equation[col]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i
        
        return pivot_row
    
    def pivot_operation(self, pivot_row, pivot_col):
        """Effectue l'opération de pivotage"""
        equations = list(self.variables["equations"].values())
        tab_optimisation = self.variables["tab_optimisation"].copy()
        
        # Normaliser la ligne pivot
        pivot_element = equations[pivot_row][pivot_col]
        equations[pivot_row] = [x / pivot_element for x in equations[pivot_row]]
        
        # Éliminer la variable pivot des autres lignes
        for i in range(len(equations)):
            if i != pivot_row and pivot_col < len(equations[i]):
                factor = equations[i][pivot_col]
                for j in range(len(equations[i])):
                    equations[i][j] -= factor * equations[pivot_row][j]
        
        # Éliminer de la fonction objectif
        factor = tab_optimisation[pivot_col]
        for j in range(len(tab_optimisation)):
            if j < len(equations[pivot_row]):
                tab_optimisation[j] -= factor * equations[pivot_row][j]
        
        # Mise à jour
        self.variables["tab_optimisation"] = tab_optimisation
        for k, equation in enumerate(equations):
            self.variables["equations"][list(self.variables["equations"].keys())[k]] = equation
    
    def can_iterate(self):
        """Vérifie s'il faut continuer les itérations"""
        return any(x < -1e-10 for x in self.variables["tab_optimisation"][1:])
    
    def analyze_final_solution(self):
        """Analyse la solution finale"""
        print(f"\n{'='*60}")
        print("ANALYSE DE LA SOLUTION FINALE")
        print(f"{'='*60}")
        
        # Vérifier si les variables artificielles sont nulles
        artificial_in_solution = False
        equations = list(self.variables["equations"].values())
        
        for var_index in self.artificial_vars:
            # Chercher si cette variable artificielle est en base avec valeur non nulle
            for i, equation in enumerate(equations):
                if var_index < len(equation):
                    # Vérifier si c'est une variable de base
                    is_basic = abs(equation[var_index] - 1.0) < 1e-10
                    others_zero = all(abs(eq[var_index]) < 1e-10 for j, eq in enumerate(equations) if j != i)
                    
                    if is_basic and others_zero and abs(equation[0]) > 1e-10:
                        artificial_in_solution = True
                        print(f"⚠️  Variable artificielle x{var_index+1} = {equation[0]:.6f}")
        
        if artificial_in_solution:
            print("\n❌ PROBLÈME NON RÉALISABLE")
            print("Au moins une variable artificielle est non nulle dans la solution optimale.")
        else:
            print("\n✅ SOLUTION OPTIMALE TROUVÉE")
            z_opt = self.variables["tab_optimisation"][0]
            print(f"Valeur optimale: Z = {z_opt:.6f}")
            
            # Extraction de la solution
            var_values = [0] * self.variables["nombres_variables_base"]
            for j in range(1, self.variables["nombres_variables_base"] + 1):
                for i, eq in enumerate(equations):
                    if j < len(eq) and abs(eq[j] - 1.0) < 1e-10:
                        # Vérifier que c'est bien une variable de base
                        others_zero = all(abs(other_eq[j]) < 1e-10 for k, other_eq in enumerate(equations) if k != i)
                        if others_zero:
                            var_values[j-1] = eq[0]
            
            print("\nVariables de décision:")
            for i, val in enumerate(var_values):
                print(f"  x{i+1} = {val:.6f}")


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple du cours: 
    # Max Z = 3x1 + 5x2
    # x1 ≤ 4
    # 2x2 ≤ 12  
    # 3x1 + 2x2 = 18
    # x1, x2 ≥ 0
    
    variables_grand_m = {
        "tab_optimisation": [0, 3, 5],  # [constante, coeff_x1, coeff_x2]
        "nombres_variables_base": 2,
        "equations": {
            "equation_1": [4, 1, 0],    # x1 ≤ 4
            "equation_2": [12, 0, 2],   # 2x2 ≤ 12
            "equation_3": [18, 3, 2],   # 3x1 + 2x2 = 18
        },
        "nb_equations": 3,
        "constraints_info": ["<=", "<=", "="]  # Types de contraintes
    }
    
    print("Résolution par la méthode du Grand M:")
    grand_m = GrandMMethod(variables_grand_m)
    grand_m.run()