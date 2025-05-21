nombres_variables_base = 3
tab_optimisation = []
# print(f"""veuillez completer la fonction optimisation :
#         Z = {" + ".join([f"{chr(945 +i)}x{chr(0x2081+i)}" for i in range(nombres_variables_base)])}""")

# for i in range(nombres_variables_base):
#     tab_optimisation.append(temp := input(f"ecart_{chr(945+i)} : "));

equations = {};
nb_equations = 1
# for j in range(nb_equations):
#     print(f"veuillez completer l'equation{j+1} :{" + ".join([f"{chr(945 +j)}{chr(0x2081+i)}x{chr(0x2081+i)}" for i in range(nombres_variables_base)])}");
#     key_eq = "equation_"+str(j+1)
#     equations[key_eq] = []
#     for k in range(nombres_variables_base):
#         temp = int(input(f"{chr(945 +k)}{chr(0x2081+j)} = "))
#         equations[key_eq].append(temp)
# print(equations)


test = [-253,2, 5, 57, -84]
def maximum(table:list)->int:
    abs_tab = [abs(x) for x in table]
    return abs_tab.index(max(abs_tab))




print(test[1:])
print(test[-(len(test)-1):])