from variables import display_simplex_tableau

class SimplexMethodTab:
    def __init__(self, variables:dict):
        self.variables = variables
        self.n = variables["nombres_variables_base"]
        
    def run(self):
        self.add_ecart_variables()
        self.variables["tab_optimisation"] = [-x for x in self.variables["tab_optimisation"]]
        iteration = 0
        while self.can_iterate():
            iteration += 1
            print(f"\n===== Itération {iteration} =====")
            col = self.find_pivot_column()
            pivot = self.row_pivot(col)
            print(f"colonne pivot : {col}")
            print(f"ligne pivot : {pivot}")
            self.new_tableau(pivot, col)
            display_simplex_tableau(self.variables, iteration)
        self.display_results()
        
    def find_pivot_column(self):
        min_val = min(self.variables["tab_optimisation"][1:])
        if min_val >= 0:
            return -1 
        return self.variables["tab_optimisation"][1:].index(min_val) + 1
    
    def new_tableau(self, pivot:int, col:int)->None:
        equations = list(self.variables["equations"].values())
        tab_optimisation = self.variables["tab_optimisation"].copy()
        equations[pivot] = [x / equations[pivot][col] for x in equations[pivot]]
        for i in range(len(equations)):
            if i != pivot:
                equations[i] = [x - (equations[i][col] * equations[pivot][j]) for j, x in enumerate(equations[i])]
        tab_optimisation = [x - (tab_optimisation[col] * equations[pivot][j])  for j, x in enumerate(tab_optimisation)]
        self.variables["tab_optimisation"] = tab_optimisation
        for k, equation in enumerate(equations):
            self.variables["equations"][list(self.variables["equations"].keys())[k]] = equation
        return None
    
    def maximum(self, table:list)->int:
        abs_tab = [abs(x) for x in table]
        return abs_tab.index(max(abs_tab))
    
    def row_pivot(self,col):
        temp = []
        for row in self.variables["equations"].values():
            if row[col] > 0:
                temp.append(row[0] / row[col])
            else:
                temp.append(float('inf'))

        return temp.index(min(temp))
    
    def add_ecart_variables(self)->None:
        equations = list(self.variables["equations"].values())
        for _ in range(len(equations)):
            self.variables["tab_optimisation"].append(0)
            
        for i, equation in enumerate(equations):
            init_len = len(equations[i])
            for k in range(len(equations[i]), self.variables["nombres_variables_base"] + self.variables["nb_equations"]+1):
                if len(equations[i]) == init_len+i:
                    equations[i].append(1)
                else:
                    equations[i].append(0)
        for k, equation in enumerate(equations):
            self.variables["equations"][list(self.variables["equations"].keys())[k]] = equation
        return
    
    def can_iterate(self)->bool:
        for value in self.variables["tab_optimisation"][1:]:
            if value < 0:
                return True
        return False
    
    def ajout_variables_ecart(self):
        if(self.n >=len(self.variables['equations'])):
            # je dois completer les equations par les variables
            pass
        pass
    
    
    
    def display_results(self):
        print("\n===== Solution Optimale =====")
        z_opt = self.variables["tab_optimisation"][0]
        print(f"Valeur optimale: {z_opt}")
        
        var_values = [0] * (self.variables["nombres_variables_base"])
        # On cherche les colonnes qui ont exactement un '1' et le reste des '0'
        for j in range(1, self.variables["nombres_variables_base"] + 1):
            ones_count = 0
            one_position = -1
            for i, eq in enumerate(self.variables["equations"].values()):
                if abs(eq[j] - 1.0) < 1e-10:
                    ones_count += 1
                    one_position = i
                elif abs(eq[j]) > 1e-10:
                    ones_count = 0
                    break
            
            if ones_count == 1:
                var_values[j-1] = list(self.variables["equations"].values())[one_position][0]
        for i, val in enumerate(var_values):
            print(f"x{i+1} = {val}")
        
if __name__ == "__main__":
    variables = {
        "tab_optimisation": [0, 45, 55],
        "nombres_variables_base": 2,
        "equations": {
            "equation_1": [120, 6,4],
            "equation_2": [180,  3,10],
        },
        "nb_equations": 2
    }
    simplex = SimplexMethodTab(variables)
    simplex.run()