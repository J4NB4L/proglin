import tab_method


variables = {
    "tab_optimisation": [0, 45, 55],
    "nombres_variables_base": 2,
    "equations": {
        "equation_1": [120, 6,4],
        "equation_2": [180,  3,10],
    },
    "nb_equations": 2
}
simplex = tab_method.SimplexMethodTab(variables)
simplex.run()