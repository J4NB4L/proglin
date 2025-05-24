# setup.py
from cx_Freeze import setup, Executable
import sys

# Dépendances
build_exe_options = {
    "packages": ["tkinter", "matplotlib", "numpy", "colorama", "tabulate"],
    "include_files": [
        "tab_method.py",
        "variables.py",
        "grand_M_method.py",
        "dual_method.py",
        "enhanced_variables.py",
        "gui.py"
    ],
    "excludes": ["test", "unittest"],
}

# Base pour Windows GUI
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SimplexSolver",
    version="2.0",
    description="Solveur de Programmation Linéaire",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            icon="icon.ico",
            target_name="SimplexSolver_1.exe"
        )
    ]
)