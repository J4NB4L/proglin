from tabulate import tabulate
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
init()

def tab_var(nombres_variables_base: int, nb_equations: int) -> dict:
    """
    This function returns a list of tab variables.
    :param nombres_variables_base: number of variables
    :param nb_equations: l'equation a combien d'equations principales
    :return: a dictionary with the list of variables and the number of variables
    """
    print(Fore.CYAN + "=" * 60)
    print(f"Configuration du problème avec {nombres_variables_base} variables et {nb_equations} contraintes")
    print("=" * 60 + Style.RESET_ALL)
    
    tab_optimisation = [0] 
    
    print(Fore.GREEN + "\n[1] FONCTION OBJECTIF (maximisation)" + Style.RESET_ALL)
    print(f"veuillez remplir la fonction optimisation : Max Z = {" + ".join([f"{chr(945 +i)}x{chr(0x2081+i)}" for i in range(nombres_variables_base)])}")

    for i in range(nombres_variables_base):
        while True:
            try:
                coeff = float(input(f"ecart_{chr(945+i)} : {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                tab_optimisation.append(coeff)
                break
            except ValueError:
                print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
    
    equations = {}
    
    print(Fore.GREEN + "\n[2] CONTRAINTES" + Style.RESET_ALL)
    
    data_table = []
    header = ["Contrainte"] + [f"x{chr(0x2081+i)}" for i in range(nombres_variables_base)] + ["b"]
    
    for j in range(nb_equations):
        print(f"\nveuillez completer l'equation {j+1} :{" + ".join([f"{chr(945 +i)}{chr(0x2081+j)}x{chr(0x2081+i)}" for i in range(nombres_variables_base)])}{chr(62)}b{chr(0x2081+j)}")
        
        key_eq = "equation_"+str(j+1)
        equations[key_eq] = []
        
        while True:
            try:
                b_value = float(input(f"b{chr(0x2081+j)} = {Fore.YELLOW}"))
                print(Style.RESET_ALL, end="")
                equations[key_eq].append(b_value)
                break
            except ValueError:
                print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
        
        coeffs = []
        for k in range(nombres_variables_base):
            while True:
                try:
                    coeff = float(input(f"{chr(945 +k)}{chr(0x2081+j)} = {Fore.YELLOW}"))
                    print(Style.RESET_ALL, end="")
                    coeffs.append(coeff)
                    equations[key_eq].append(coeff)
                    break
                except ValueError:
                    print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
        
        data_table.append([f"Contrainte {j+1}"] + coeffs + [b_value])
    
    obj_row = ["Fonction objectif"] + tab_optimisation[1:] + [tab_optimisation[0]]
    
    print(Fore.CYAN + "\n" + "=" * 60)
    print("RÉCAPITULATIF DU PROBLÈME")
    print("=" * 60 + Style.RESET_ALL)
    
    print("\n" + tabulate([obj_row] + data_table, headers=header, tablefmt="grid", floatfmt=".2f"))
    
    variables = {
        "tab_optimisation": tab_optimisation,
        "nombres_variables_base": nombres_variables_base,
        "equations": equations,
        "nb_equations": nb_equations
    }
    
    return variables

def display_simplex_tableau(variables, iteration=0):
    """
    Fonction pour afficher le tableau du simplexe de manière esthétique.
    """
    equations = variables["equations"]
    tab_optimisation = variables["tab_optimisation"]
    
    print(Fore.CYAN + "\n" + "=" * 60)
    print(f"TABLEAU DU SIMPLEXE - ITÉRATION {iteration}")
    print("=" * 60 + Style.RESET_ALL)
    
    nb_vars = variables["nombres_variables_base"]
    nb_slack = variables["nb_equations"]
    
    headers = ["Base", "Cst"] + [f"x{chr(0x2081+i)}" for i in range(nb_vars)] + [f"s{chr(0x2081+i)}" for i in range(nb_slack)]
    
    rows = []
    
    obj_row = ["Z"] + tab_optimisation
    rows.append(obj_row)
    
    for i, (key, eq) in enumerate(equations.items()):
        base_var = f"s{chr(0x2081+i)}"  # Par défaut, variable d'écart
        rows.append([base_var] + eq)
    
    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".3f"))

def update_simplex_display(simplex_obj):
    """
    Fonction à utiliser pendant l'exécution de l'algorithme du simplexe
    pour mettre à jour l'affichage à chaque itération.
    """
    iteration = simplex_obj.current_iteration
    display_simplex_tableau(simplex_obj.variables, iteration)

if __name__ == "__main__":
    print(Fore.MAGENTA + "MÉTHODE DU SIMPLEXE - INTERFACE DE SAISIE" + Style.RESET_ALL)
    
    while True:
        try:
            nombres_variables_base = int(input("\nNombre de variables de décision : "))
            if nombres_variables_base <= 0:
                print(Fore.RED + "Le nombre doit être positif." + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier." + Style.RESET_ALL)
    
    while True:
        try:
            nb_equations = int(input("Nombre de contraintes : "))
            if nb_equations <= 0:
                print(Fore.RED + "Le nombre doit être positif." + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier." + Style.RESET_ALL)
    
    variables = tab_var(nombres_variables_base, nb_equations)
    
    display_simplex_tableau(variables)
