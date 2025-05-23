from variables import display_simplex_tableau
from tab_method import SimplexMethodTab
import copy

class DualMethod:
    def __init__(self, primal_variables: dict):
        self.primal_variables = primal_variables
        self.dual_variables = None
        self.construct_dual()
        
    def construct_dual(self):
        """Construit le problème dual à partir du problème primal"""
        print(f"\n{'='*60}")
        print("CONSTRUCTION DU PROBLÈME DUAL")
        print(f"{'='*60}")
        
        # Extraire les données du problème primal
        primal_c = self.primal_variables["tab_optimisation"][1:]  # Coefficients fonction objectif
        primal_equations = list(self.primal_variables["equations"].values())
        primal_b = [eq[0] for eq in primal_equations]  # Membres de droite
        
        # Matrice des contraintes A (sans les membres de droite)
        primal_A = []
        for eq in primal_equations:
            primal_A.append(eq[1:self.primal_variables["nombres_variables_base"] + 1])
        
        self.display_primal_problem(primal_c, primal_A, primal_b)
        
        # Construction du dual
        # Nombre de variables duales = nombre de contraintes primales
        dual_n = len(primal_equations)
        
        # Coefficients de la fonction objectif du dual = membres de droite du primal
        dual_c = primal_b.copy()
        
        # Contraintes du dual: A^T * y >= c (du primal)
        dual_equations = {}
        dual_b = primal_c.copy()
        
        # Transposition de la matrice A
        dual_A = []
        for j in range(len(primal_A[0])):  # Pour chaque variable primale
            dual_constraint = []
            dual_constraint.append(dual_b[j])  # Membre de droite
            for i in range(len(primal_A)):     # Pour chaque contrainte primale
                dual_constraint.append(primal_A[i][j])
            dual_A.append(dual_constraint)
            dual_equations[f"equation_{j+1}"] = dual_constraint
        
        # Le dual est un problème de minimisation, on le convertit en maximisation
        # Min f(y) = -Max(-f(y))
        dual_tab_optimisation = [0] + [-c for c in dual_c]
        
        self.dual_variables = {
            "tab_optimisation": dual_tab_optimisation,
            "nombres_variables_base": dual_n,
            "equations": dual_equations,
            "nb_equations": len(dual_equations),
            "constraints_info": [">="] * len(dual_equations)  # Toutes les contraintes sont >=
        }
        
        self.display_dual_problem(dual_c, dual_A, dual_b)
        
    def display_primal_problem(self, c, A, b):
        """Affiche le problème primal"""
        print("\nPROBLÈME PRIMAL:")
        print("Max Z =", end="")
        for i, coeff in enumerate(c):
            if i == 0:
                print(f" {coeff}x{i+1}", end="")
            else:
                print(f" + {coeff}x{i+1}" if coeff >= 0 else f" - {abs(coeff)}x{i+1}", end="")
        print()
        
        print("Sujet à:")
        for i, (constraint, rhs) in enumerate(zip(A, b)):
            print("  ", end="")
            for j, coeff in enumerate(constraint):
                if j == 0:
                    print(f"{coeff}x{j+1}", end="")
                else:
                    print(f" + {coeff}x{j+1}" if coeff >= 0 else f" - {abs(coeff)}x{j+1}", end="")
            print(f" ≤ {rhs}")
        
        print("  x_i ≥ 0 pour tout i")
    
    def display_dual_problem(self, c, A, b):
        """Affiche le problème dual"""
        print("\nPROBLÈME DUAL:")
        print("Min W =", end="")
        for i, coeff in enumerate(c):
            if i == 0:
                print(f" {coeff}y{i+1}", end="")
            else:
                print(f" + {coeff}y{i+1}" if coeff >= 0 else f" - {abs(coeff)}y{i+1}", end="")
        print()
        
        print("Sujet à:")
        for i, constraint in enumerate(A):
            print("  ", end="")
            rhs = constraint[0]
            coeffs = constraint[1:]
            for j, coeff in enumerate(coeffs):
                if j == 0:
                    print(f"{coeff}y{j+1}", end="")
                else:
                    print(f" + {coeff}y{j+1}" if coeff >= 0 else f" - {abs(coeff)}y{j+1}", end="")
            print(f" ≥ {rhs}")
        
        print("  y_i ≥ 0 pour tout i")
        
        print("\nÉquivalent en maximisation:")
        print("Max W' = -W =", end="")
        for i, coeff in enumerate(c):
            if i == 0:
                print(f" {-coeff}y{i+1}", end="")
            else:
                print(f" + {-coeff}y{i+1}" if -coeff >= 0 else f" - {abs(-coeff)}y{i+1}", end="")
        print()
    
    def solve_dual(self):
        """Résout le problème dual"""
        print(f"\n{'='*60}")
        print("RÉSOLUTION DU PROBLÈME DUAL")
        print(f"{'='*60}")
        
        # Pour résoudre les contraintes >=, on les convertit en <=
        # a1*y1 + a2*y2 + ... >= b devient -a1*y1 - a2*y2 - ... <= -b
        converted_equations = {}
        for key, equation in self.dual_variables["equations"].items():
            converted_eq = [-equation[0]]  # -b
            converted_eq.extend([-x for x in equation[1:]])  # -coefficients
            converted_equations[key] = converted_eq
        
        dual_for_simplex = {
            "tab_optimisation": self.dual_variables["tab_optimisation"],
            "nombres_variables_base": self.dual_variables["nombres_variables_base"],
            "equations": converted_equations,
            "nb_equations": self.dual_variables["nb_equations"]
        }
        
        print("Résolution du dual par la méthode du simplexe:")
        simplex_dual = SimplexMethodTab(dual_for_simplex)
        simplex_dual.run()
        
        return dual_for_simplex
    
    def solve_primal(self):
        """Résout le problème primal pour comparaison"""
        print(f"\n{'='*60}")
        print("RÉSOLUTION DU PROBLÈME PRIMAL")
        print(f"{'='*60}")
        
        print("Résolution du primal par la méthode du simplexe:")
        simplex_primal = SimplexMethodTab(copy.deepcopy(self.primal_variables))
        simplex_primal.run()
        
        return self.primal_variables
    
    def compare_solutions(self, primal_result, dual_result):
        """Compare les solutions primale et duale"""
        print(f"\n{'='*60}")
        print("COMPARAISON DES SOLUTIONS")
        print(f"{'='*60}")
        
        primal_z = primal_result["tab_optimisation"][0]
        dual_w = -dual_result["tab_optimisation"][0]  # Rappel: on a maximisé -W
        
        print(f"Valeur optimale du primal (Z): {primal_z:.6f}")
        print(f"Valeur optimale du dual (W): {dual_w:.6f}")
        print(f"Différence |Z - W|: {abs(primal_z - dual_w):.10f}")
        
        if abs(primal_z - dual_w) < 1e-6:
            print("✅ Théorème de dualité forte vérifié: Z* = W*")
        else:
            print("❌ Problème dans les calculs - les valeurs devraient être égales")
        
        # Extraction des solutions
        print("\nSOLUTION PRIMALE:")
        primal_equations = list(primal_result["equations"].values())
        for j in range(1, self.primal_variables["nombres_variables_base"] + 1):
            value = 0
            for i, eq in enumerate(primal_equations):
                if j < len(eq) and abs(eq[j] - 1.0) < 1e-10:
                    others_zero = all(abs(other_eq[j]) < 1e-10 for k, other_eq in enumerate(primal_equations) if k != i)
                    if others_zero:
                        value = eq[0]
            print(f"  x{j} = {value:.6f}")
        
        print("\nSOLUTION DUALE:")
        dual_equations = list(dual_result["equations"].values())
        for j in range(1, self.dual_variables["nombres_variables_base"] + 1):
            value = 0
            for i, eq in enumerate(dual_equations):
                if j < len(eq) and abs(eq[j] - 1.0) < 1e-10:
                    others_zero = all(abs(other_eq[j]) < 1e-10 for k, other_eq in enumerate(dual_equations) if k != i)
                    if others_zero:
                        value = eq[0]
            print(f"  y{j} = {value:.6f}")
    
    def run_complete_analysis(self):
        """Exécute l'analyse complète primal-dual"""
        print(f"\n{'='*80}")
        print("ANALYSE COMPLÈTE PRIMAL-DUAL")
        print(f"{'='*80}")
        
        # Résolution des deux problèmes
        primal_result = self.solve_primal()
        dual_result = self.solve_dual()
        
        # Comparaison
        self.compare_solutions(primal_result, dual_result)
        
        # Analyse économique
        self.economic_interpretation()
    
    def economic_interpretation(self):
        """Fournit une interprétation économique"""
        print(f"\n{'='*60}")
        print("INTERPRÉTATION ÉCONOMIQUE")
        print(f"{'='*60}")
        
        print("PROBLÈME PRIMAL:")
        print("- Variables x_j: niveaux d'activité")
        print("- Coefficients c_j: profits unitaires")
        print("- Contraintes: limitations de ressources")
        print("- Objectif: maximiser le profit total")
        
        print("\nPROBLÈME DUAL:")
        print("- Variables y_i: prix implicites (valeurs marginales) des ressources")
        print("- Coefficients b_i: quantités de ressources disponibles") 
        print("- Contraintes: la valeur des ressources utilisées ≥ profit de l'activité")
        print("- Objectif: minimiser la valeur totale des ressources")
        
        print("\nTHÉORÈME DE DUALITÉ:")
        print("- Si les deux problèmes ont une solution optimale, alors Z* = W*")
        print("- Les prix optimaux du dual indiquent la valeur marginale de chaque ressource")
        print("- Une ressource avec prix dual nul n'est pas entièrement utilisée")


# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple classique
    # Max Z = 3x1 + 5x2
    # x1 ≤ 4
    # 2x2 ≤ 12
    # 3x1 + 2x2 ≤ 18
    # x1, x2 ≥ 0
    
    variables_primal = {
        "tab_optimisation": [0, 3, 5],
        "nombres_variables_base": 2,
        "equations": {
            "equation_1": [4, 1, 0],
            "equation_2": [12, 0, 2],
            "equation_3": [18, 3, 2],
        },
        "nb_equations": 3
    }
    
    dual_analyzer = DualMethod(variables_primal)
    dual_analyzer.run_complete_analysis()