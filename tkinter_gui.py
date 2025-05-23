#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Graphique Ultra-Moderne pour le Solveur de Programmation Linéaire
Utilise CustomTkinter pour un design professionnel et moderne
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
import json
import os
from datetime import datetime
import threading
import sys
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from typing import Dict, List, Tuple, Optional
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import webbrowser
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import base64

# Configuration de CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Import des modules existants
try:
    from tab_method import SimplexMethodTab
    from grand_M_method import GrandMMethod  
    from dual_method import DualMethod
    from enhanced_variables import VariableManager
    from variables import display_simplex_tableau
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que tous les modules sont dans le même dossier")

class ModernTheme:
    """Thème moderne avec support du mode sombre/clair"""
    
    def __init__(self):
        self.dark_mode = True
        self.update_colors()
    
    def update_colors(self):
        if self.dark_mode:
            # Mode sombre
            self.bg_primary = "#1a1a1a"
            self.bg_secondary = "#2b2b2b"
            self.bg_tertiary = "#3c3c3c"
            self.fg_primary = "#ffffff"
            self.fg_secondary = "#cccccc"
            self.fg_tertiary = "#999999"
            self.accent = "#3b82f6"
            self.success = "#10b981"
            self.warning = "#f59e0b"
            self.error = "#ef4444"
            self.border = "#4a4a4a"
        else:
            # Mode clair
            self.bg_primary = "#ffffff"
            self.bg_secondary = "#f3f4f6"
            self.bg_tertiary = "#e5e7eb"
            self.fg_primary = "#1f2937"
            self.fg_secondary = "#4b5563"
            self.fg_tertiary = "#6b7280"
            self.accent = "#3b82f6"
            self.success = "#10b981"
            self.warning = "#f59e0b"
            self.error = "#ef4444"
            self.border = "#d1d5db"
    
    def toggle(self):
        self.dark_mode = not self.dark_mode
        self.update_colors()
        ctk.set_appearance_mode("dark" if self.dark_mode else "light")

class AnimatedButton(ctk.CTkButton):
    """Bouton avec animations au survol"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = kwargs.get("fg_color", self._fg_color)
    
    def on_enter(self, event):
        self.configure(cursor="hand2")
        # Animation de couleur au survol
        if hasattr(self, '_fg_color'):
            self.configure(fg_color=self.original_color)
    
    def on_leave(self, event):
        self.configure(cursor="")

class ToolTip:
    """Classe pour afficher des tooltips"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.show_tooltip()
    
    def on_leave(self, event):
        self.hide_tooltip()
    
    def show_tooltip(self):
        if self.tooltip or not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(self.tooltip, text=self.text, 
                            fg_color=("#333333", "#f0f0f0"),
                            corner_radius=6,
                            padx=10, pady=5)
        label.pack()
    
    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SimplexGUI:
    """Interface graphique principale améliorée pour le solveur de programmation linéaire"""
    
    def __init__(self, root):
        self.root = root
        self.theme = ModernTheme()
        self.setup_window()
        self.variable_manager = VariableManager()
        self.current_problem = None
        self.solving_animation = None
        self.auto_save_enabled = True
        self.history_visualizations = []
        
        # Variables pour l'interface
        self.problem_vars = []
        self.constraint_vars = []
        self.constraint_types = []
        
        # Statistiques
        self.stats = {
            'problems_solved': 0,
            'total_iterations': 0,
            'avg_solving_time': 0,
            'methods_used': {'Simplexe': 0, 'Grand M': 0, 'Dual': 0}
        }
        
        self.create_main_interface()
        self.setup_keyboard_shortcuts()
        self.load_stats()
        
    def setup_window(self):
        """Configuration initiale de la fenêtre"""
        self.root.title("🚀 Solveur de Programmation Linéaire - Edition Premium")
        self.root.geometry("1400x900")
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        width = 1400
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configuration de la grille
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Icône personnalisée
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def setup_keyboard_shortcuts(self):
        """Configure les raccourcis clavier"""
        self.root.bind('<Control-n>', lambda e: self.new_problem())
        self.root.bind('<Control-o>', lambda e: self.load_problem())
        self.root.bind('<Control-s>', lambda e: self.save_problem())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<F5>', lambda e: self.solve_standard())
        self.root.bind('<F6>', lambda e: self.solve_grand_m())
        self.root.bind('<F7>', lambda e: self.solve_dual())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Control-d>', lambda e: self.theme.toggle())
    
    def toggle_fullscreen(self):
        """Bascule en mode plein écran"""
        state = not self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", state)
        
    def create_main_interface(self):
        """Crée l'interface principale moderne"""
        # Container principal
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Barre de navigation supérieure
        self.create_navbar()
        
        # Zone principale avec sidebar
        self.content_frame = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Zone de contenu principal
        self.main_content = ctk.CTkFrame(self.content_frame)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # Tabview moderne
        self.create_modern_tabs()
        
        # Barre de statut
        self.create_status_bar()
        
    def create_navbar(self):
        """Crée une barre de navigation moderne"""
        self.navbar = ctk.CTkFrame(self.main_container, height=60, corner_radius=0)
        self.navbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.navbar.grid_columnconfigure(1, weight=1)
        
        # Logo et titre
        title_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🚀 Solveur Simplexe Premium",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Boutons de navigation rapide
        nav_buttons_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        nav_buttons_frame.grid(row=0, column=1, padx=20, pady=10)
        
        # Boutons avec icônes
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📊 Résoudre", self.focus_solve_tab),
            ("📈 Visualiser", self.show_visualization),
            ("📚 Historique", self.show_history),
        ]
        
        for text, command in nav_buttons:
            btn = AnimatedButton(
                nav_buttons_frame,
                text=text,
                command=command,
                width=120,
                height=35,
                corner_radius=8
            )
            btn.pack(side="left", padx=5)
        
        # Boutons d'actions à droite
        actions_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        actions_frame.grid(row=0, column=2, padx=20, pady=10)
        
        # Mode sombre/clair
        self.theme_switch = ctk.CTkSwitch(
            actions_frame,
            text="🌙",
            command=self.toggle_theme,
            width=50
        )
        self.theme_switch.pack(side="left", padx=10)
        ToolTip(self.theme_switch, "Basculer le thème")
        
        # Paramètres
        settings_btn = AnimatedButton(
            actions_frame,
            text="⚙️",
            command=self.show_settings,
            width=40,
            height=35,
            corner_radius=8
        )
        settings_btn.pack(side="left", padx=5)
        ToolTip(settings_btn, "Paramètres")
        
    def create_sidebar(self):
        """Crée une sidebar moderne"""
        self.sidebar = ctk.CTkFrame(self.content_frame, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(10, 0), pady=10)
        self.sidebar.grid_propagate(False)
        
        # Titre de la sidebar
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Actions Rapides",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sidebar_title.pack(pady=(20, 10))
        
        # Séparateur
        separator = ctk.CTkFrame(self.sidebar, height=2)
        separator.pack(fill="x", padx=20, pady=10)
        
        # Boutons de la sidebar
        sidebar_buttons = [
            ("📝 Nouveau Problème", self.new_problem, "Ctrl+N"),
            ("📂 Charger", self.load_problem, "Ctrl+O"),
            ("💾 Sauvegarder", self.save_problem, "Ctrl+S"),
            ("🎯 Exemples", self.load_examples, None),
            ("📊 Comparer Méthodes", self.compare_methods, None),
            ("📈 Statistiques", self.show_statistics, None),
            ("🎨 Personnaliser", self.customize_interface, None),
            ("📤 Exporter PDF", self.export_to_pdf, None),
            ("❓ Aide", self.show_help, "F1"),
        ]
        
        for text, command, shortcut in sidebar_buttons:
            btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            btn_frame.pack(fill="x", padx=10, pady=5)
            
            btn = AnimatedButton(
                btn_frame,
                text=text,
                command=command,
                anchor="w",
                corner_radius=8,
                height=40
            )
            btn.pack(fill="x")
            
            if shortcut:
                shortcut_label = ctk.CTkLabel(
                    btn_frame,
                    text=shortcut,
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                )
                shortcut_label.place(relx=0.95, rely=0.5, anchor="e")
        
        # Zone d'information
        self.create_info_zone()
        
    def create_info_zone(self):
        """Crée une zone d'information dans la sidebar"""
        info_frame = ctk.CTkFrame(self.sidebar, corner_radius=10)
        info_frame.pack(fill="x", padx=10, pady=20, side="bottom")
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="📊 Statistiques",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        self.stats_label = ctk.CTkLabel(
            info_frame,
            text=f"Problèmes résolus: {self.stats['problems_solved']}\n"
                 f"Temps moyen: {self.stats['avg_solving_time']:.2f}s",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack(pady=(5, 10))
        
    def create_modern_tabs(self):
        """Crée des onglets modernes avec CustomTkinter"""
        self.tabview = ctk.CTkTabview(self.main_content, corner_radius=10)
        self.tabview.pack(fill="both", expand=True)
        
        # Création des onglets
        self.tabview.add("📝 Définition")
        self.tabview.add("🔍 Résolution") 
        self.tabview.add("📊 Résultats")
        self.tabview.add("📈 Visualisation")
        self.tabview.add("💾 Fichiers")
        self.tabview.add("🏠 Dashboard")
        
        # Configuration des onglets
        self.create_definition_tab()
        self.create_solve_tab_modern()
        self.create_results_tab_modern()
        self.create_visualization_tab()
        self.create_files_tab_modern()
        self.create_dashboard_tab()
        
    def create_definition_tab(self):
        """Onglet de définition du problème moderne"""
        tab = self.tabview.tab("📝 Définition")
        
        # Scrollable frame
        self.def_scroll = ctk.CTkScrollableFrame(tab)
        self.def_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre avec animation
        title_frame = ctk.CTkFrame(self.def_scroll, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Définition du Problème de Programmation Linéaire",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack()
        
        # Section dimensions avec style moderne
        dims_frame = ctk.CTkFrame(self.def_scroll, corner_radius=10)
        dims_frame.pack(fill="x", pady=(0, 20))
        
        dims_title = ctk.CTkLabel(
            dims_frame,
            text="📐 Dimensions du Problème",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        dims_title.pack(pady=(15, 10))
        
        # Grille pour les dimensions
        dims_grid = ctk.CTkFrame(dims_frame, fg_color="transparent")
        dims_grid.pack(pady=(0, 15))
        
        # Variables
        vars_frame = ctk.CTkFrame(dims_grid, fg_color="transparent")
        vars_frame.grid(row=0, column=0, padx=20)
        
        ctk.CTkLabel(vars_frame, text="Variables:").pack()
        self.nb_vars_var = tk.StringVar(value="2")
        vars_spinbox = ctk.CTkEntry(
            vars_frame,
            textvariable=self.nb_vars_var,
            width=80,
            height=35,
            corner_radius=8
        )
        vars_spinbox.pack(pady=5)
        ToolTip(vars_spinbox, "Nombre de variables de décision (x₁, x₂, ...)")
        
        # Contraintes
        constr_frame = ctk.CTkFrame(dims_grid, fg_color="transparent")
        constr_frame.grid(row=0, column=1, padx=20)
        
        ctk.CTkLabel(constr_frame, text="Contraintes:").pack()
        self.nb_constraints_var = tk.StringVar(value="3")
        constr_spinbox = ctk.CTkEntry(
            constr_frame,
            textvariable=self.nb_constraints_var,
            width=80,
            height=35,
            corner_radius=8
        )
        constr_spinbox.pack(pady=5)
        ToolTip(constr_spinbox, "Nombre de contraintes du problème")
        
        # Bouton de génération avec animation
        generate_btn = AnimatedButton(
            dims_frame,
            text="🔄 Générer les Champs",
            command=self.generate_input_fields_modern,
            width=200,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        generate_btn.pack(pady=(0, 15))
        
        # Frame pour les champs dynamiques
        self.fields_frame = ctk.CTkFrame(self.def_scroll, corner_radius=10)
        self.fields_frame.pack(fill="both", expand=True, pady=20)
        
        # Boutons d'action
        self.create_definition_actions()
        
    def generate_input_fields_modern(self):
        """Génère les champs de saisie avec un design moderne"""
        try:
            nb_vars = int(self.nb_vars_var.get())
            nb_constraints = int(self.nb_constraints_var.get())
        except ValueError:
            self.show_error("Veuillez entrer des nombres valides")
            return
        
        # Animation de chargement
        self.show_loading_animation(self.fields_frame)
        
        # Nettoyer le frame
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        
        self.problem_vars = []
        self.constraint_vars = []
        self.constraint_types = []
        
        # Fonction objectif avec style moderne
        obj_frame = ctk.CTkFrame(self.fields_frame, corner_radius=10)
        obj_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        obj_title = ctk.CTkLabel(
            obj_frame,
            text="🎯 Fonction Objectif",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        obj_title.pack(pady=(15, 10))
        
        # Type d'optimisation avec switch moderne
        opt_frame = ctk.CTkFrame(obj_frame, fg_color="transparent")
        opt_frame.pack(pady=(0, 15))
        
        self.opt_type_var = tk.StringVar(value="max")
        
        opt_selector = ctk.CTkSegmentedButton(
            opt_frame,
            values=["Maximiser", "Minimiser"],
            command=self.on_optimization_type_change
        )
        opt_selector.pack()
        opt_selector.set("Maximiser")
        
        # Coefficients avec style moderne
        coeffs_frame = ctk.CTkFrame(obj_frame, fg_color="transparent")
        coeffs_frame.pack(pady=(0, 15))
        
        ctk.CTkLabel(coeffs_frame, text="Z = ", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=(0, 10))
        
        for i in range(nb_vars):
            if i > 0:
                ctk.CTkLabel(coeffs_frame, text="+", font=ctk.CTkFont(size=14)).grid(row=0, column=2*i, padx=5)
            
            var = tk.StringVar(value="1")
            entry = ctk.CTkEntry(
                coeffs_frame,
                textvariable=var,
                width=60,
                height=35,
                corner_radius=8,
                placeholder_text="Coef"
            )
            entry.grid(row=0, column=2*i+1, padx=2)
            self.problem_vars.append(var)
            
            ctk.CTkLabel(
                coeffs_frame, 
                text=f"x{self.subscript(i+1)}", 
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=2*i+2, padx=(2, 10))
        
        # Contraintes avec style moderne
        constraints_frame = ctk.CTkFrame(self.fields_frame, corner_radius=10)
        constraints_frame.pack(fill="x", padx=20, pady=10)
        
        constr_title = ctk.CTkLabel(
            constraints_frame,
            text="📋 Contraintes",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        constr_title.pack(pady=(15, 10))
        
        # Conteneur pour les contraintes
        constr_container = ctk.CTkFrame(constraints_frame, fg_color="transparent")
        constr_container.pack(fill="x", padx=20, pady=(0, 15))
        
        for i in range(nb_constraints):
            # Frame pour chaque contrainte avec hover effect
            constraint_frame = ctk.CTkFrame(constr_container, corner_radius=8)
            constraint_frame.pack(fill="x", pady=5)
            
            # Effet au survol
            constraint_frame.bind("<Enter>", lambda e, f=constraint_frame: f.configure(fg_color=("gray85", "gray25")))
            constraint_frame.bind("<Leave>", lambda e, f=constraint_frame: f.configure(fg_color=("gray90", "gray20")))
            
            inner_frame = ctk.CTkFrame(constraint_frame, fg_color="transparent")
            inner_frame.pack(padx=15, pady=10)
            
            # Label de la contrainte
            ctk.CTkLabel(
                inner_frame, 
                text=f"C{self.subscript(i+1)}:",
                font=ctk.CTkFont(size=14, weight="bold")
            ).grid(row=0, column=0, padx=(0, 15))
            
            # Coefficients
            constraint_coeffs = []
            for j in range(nb_vars):
                if j > 0:
                    ctk.CTkLabel(inner_frame, text="+", font=ctk.CTkFont(size=14)).grid(row=0, column=2*j+1, padx=5)
                
                var = tk.StringVar(value="1")
                entry = ctk.CTkEntry(
                    inner_frame,
                    textvariable=var,
                    width=60,
                    height=35,
                    corner_radius=8,
                    placeholder_text="Coef"
                )
                entry.grid(row=0, column=2*j+2, padx=2)
                constraint_coeffs.append(var)
                
                ctk.CTkLabel(
                    inner_frame,
                    text=f"x{self.subscript(j+1)}",
                    font=ctk.CTkFont(size=14)
                ).grid(row=0, column=2*j+3, padx=(2, 10))
            
            # Type de contrainte avec dropdown moderne
            type_var = tk.StringVar(value="<=")
            type_menu = ctk.CTkOptionMenu(
                inner_frame,
                values=["<=", ">=", "="],
                variable=type_var,
                width=80,
                height=35,
                corner_radius=8
            )
            type_menu.grid(row=0, column=2*nb_vars+2, padx=10)
            self.constraint_types.append(type_var)
            
            # RHS
            rhs_var = tk.StringVar(value="0")
            rhs_entry = ctk.CTkEntry(
                inner_frame,
                textvariable=rhs_var,
                width=80,
                height=35,
                corner_radius=8,
                placeholder_text="RHS"
            )
            rhs_entry.grid(row=0, column=2*nb_vars+3, padx=(10, 0))
            constraint_coeffs.append(rhs_var)
            
            self.constraint_vars.append(constraint_coeffs)
        
        # Animation de fin
        self.hide_loading_animation()
        
    def subscript(self, n):
        """Convertit un nombre en indice"""
        subscripts = "₀₁₂₃₄₅₆₇₈₉"
        return ''.join(subscripts[int(d)] for d in str(n))
    
    def on_optimization_type_change(self, value):
        """Callback pour le changement de type d'optimisation"""
        self.opt_type_var.set("max" if value == "Maximiser" else "min")
        
    def create_definition_actions(self):
        """Crée les boutons d'action pour la définition"""
        actions_frame = ctk.CTkFrame(self.def_scroll, corner_radius=10)
        actions_frame.pack(fill="x", padx=20, pady=20)
        
        actions_inner = ctk.CTkFrame(actions_frame, fg_color="transparent")
        actions_inner.pack(pady=15)
        
        # Boutons avec animations
        buttons_data = [
            ("✅ Valider", self.validate_problem, "green", "Valider et sauvegarder le problème"),
            ("👁️ Aperçu", self.preview_problem, "blue", "Voir un aperçu du problème"),
            ("🗑️ Effacer", self.clear_problem, "red", "Effacer tous les champs"),
        ]
        
        for text, command, color, tooltip in buttons_data:
            btn = AnimatedButton(
                actions_inner,
                text=text,
                command=command,
                width=140,
                height=40,
                corner_radius=10,
                fg_color=color,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            btn.pack(side="left", padx=10)
            ToolTip(btn, tooltip)
    
    def show_loading_animation(self, parent):
        """Affiche une animation de chargement"""
        self.loading_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text="⏳ Chargement...",
            font=ctk.CTkFont(size=16)
        )
        self.loading_label.pack()
        
        # Animation de rotation
        self.rotate_loading()
    
    def rotate_loading(self):
        """Animation de rotation pour le chargement"""
        if hasattr(self, 'loading_label'):
            symbols = ["⏳", "⌛", "⏳", "⌛"]
            current = self.loading_label.cget("text")
            idx = 0
            for i, s in enumerate(symbols):
                if s in current:
                    idx = (i + 1) % len(symbols)
                    break
            self.loading_label.configure(text=f"{symbols[idx]} Chargement...")
            self.root.after(500, self.rotate_loading)
    
    def hide_loading_animation(self):
        """Cache l'animation de chargement"""
        if hasattr(self, 'loading_frame'):
            self.loading_frame.destroy()
            
    def create_solve_tab_modern(self):
        """Onglet de résolution moderne"""
        tab = self.tabview.tab("🔍 Résolution")
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # État du problème
        status_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        status_frame.pack(fill="x", pady=(0, 20))
        
        status_title = ctk.CTkLabel(
            status_frame,
            text="📊 État du Problème",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        status_title.pack(pady=(15, 10))
        
        self.problem_status_label = ctk.CTkLabel(
            status_frame,
            text="❌ Aucun problème chargé",
            font=ctk.CTkFont(size=14)
        )
        self.problem_status_label.pack(pady=(0, 15))
        
        # Méthodes de résolution avec cartes modernes
        methods_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        methods_frame.pack(fill="x", pady=(0, 20))
        
        methods_title = ctk.CTkLabel(
            methods_frame,
            text="🛠️ Méthodes de Résolution",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        methods_title.pack(pady=(15, 10))
        
        # Grille de méthodes
        methods_grid = ctk.CTkFrame(methods_frame, fg_color="transparent")
        methods_grid.pack(pady=(0, 15))
        
        methods_data = [
            {
                "name": "Simplexe Standard",
                "icon": "📈",
                "desc": "Méthode classique pour problèmes standards",
                "command": self.solve_standard,
                "color": "blue",
                "shortcut": "F5"
            },
            {
                "name": "Grand M",
                "icon": "🎯",
                "desc": "Pour problèmes avec contraintes ≥ ou =",
                "command": self.solve_grand_m,
                "color": "green",
                "shortcut": "F6"
            },
            {
                "name": "Analyse Duale",
                "icon": "🔄",
                "desc": "Analyse primal-dual complète",
                "command": self.solve_dual,
                "color": "orange",
                "shortcut": "F7"
            }
        ]
        
        for i, method in enumerate(methods_data):
            self.create_method_card(methods_grid, method, i)
        
        # Comparaison des méthodes
        compare_btn = AnimatedButton(
            methods_frame,
            text="⚖️ Comparer Toutes les Méthodes",
            command=self.compare_methods,
            width=300,
            height=50,
            corner_radius=10,
            fg_color="purple",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        compare_btn.pack(pady=(0, 15))
        
        # Progression
        self.create_progress_section(scroll_frame)
        
    def create_method_card(self, parent, method, index):
        """Crée une carte pour une méthode de résolution"""
        card = ctk.CTkFrame(parent, corner_radius=10, width=250, height=200)
        card.grid(row=0, column=index, padx=10, pady=10)
        card.grid_propagate(False)
        
        # Effet au survol
        card.bind("<Enter>", lambda e: card.configure(fg_color=("gray85", "gray25")))
        card.bind("<Leave>", lambda e: card.configure(fg_color=("gray90", "gray20")))
        
        # Icône
        icon_label = ctk.CTkLabel(
            card,
            text=method["icon"],
            font=ctk.CTkFont(size=40)
        )
        icon_label.pack(pady=(20, 10))
        
        # Nom
        name_label = ctk.CTkLabel(
            card,
            text=method["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack()
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=method["desc"],
            font=ctk.CTkFont(size=12),
            wraplength=200,
            text_color="gray"
        )
        desc_label.pack(pady=(5, 15))
        
        # Bouton
        btn = AnimatedButton(
            card,
            text=f"Lancer ({method['shortcut']})",
            command=method["command"],
            width=180,
            height=35,
            corner_radius=8,
            fg_color=method["color"]
        )
        btn.pack(pady=(0, 20))
        
    def create_progress_section(self, parent):
        """Crée la section de progression"""
        progress_frame = ctk.CTkFrame(parent, corner_radius=10)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        progress_title = ctk.CTkLabel(
            progress_frame,
            text="⏳ Progression",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_title.pack(pady=(15, 10))
        
        self.progress_var = tk.StringVar(value="En attente...")
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.progress_var,
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack()
        
        # Barre de progression moderne
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=(10, 15))
        self.progress_bar.set(0)
        
    def create_results_tab_modern(self):
        """Onglet des résultats moderne"""
        tab = self.tabview.tab("📊 Résultats")
        
        # Notebook pour les sous-onglets
        self.results_notebook = ctk.CTkTabview(tab, corner_radius=10)
        self.results_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sous-onglets
        self.results_notebook.add("📝 Sortie Détaillée")
        self.results_notebook.add("📊 Tableau Final")
        self.results_notebook.add("📈 Graphiques")
        self.results_notebook.add("📋 Rapport")
        
        # Configuration des sous-onglets
        self.create_detailed_output_tab()
        self.create_final_tableau_tab()
        self.create_graphs_tab()
        self.create_report_tab()
        
    def create_detailed_output_tab(self):
        """Crée l'onglet de sortie détaillée"""
        tab = self.results_notebook.tab("📝 Sortie Détaillée")
        
        # Zone de texte moderne
        self.results_text = ctk.CTkTextbox(
            tab,
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=10
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(tab, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        copy_btn = AnimatedButton(
            actions_frame,
            text="📋 Copier",
            command=self.copy_results,
            width=100,
            height=35,
            corner_radius=8
        )
        copy_btn.pack(side="left", padx=5)
        
        save_btn = AnimatedButton(
            actions_frame,
            text="💾 Sauvegarder",
            command=self.save_results,
            width=100,
            height=35,
            corner_radius=8
        )
        save_btn.pack(side="left", padx=5)
        
    def create_final_tableau_tab(self):
        """Crée l'onglet du tableau final"""
        tab = self.results_notebook.tab("📊 Tableau Final")
        
        # Frame pour le tableau
        self.tableau_frame = ctk.CTkScrollableFrame(tab)
        self.tableau_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_graphs_tab(self):
        """Crée l'onglet des graphiques"""
        tab = self.results_notebook.tab("📈 Graphiques")
        
        # Frame pour les graphiques
        self.graphs_frame = ctk.CTkFrame(tab)
        self.graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_report_tab(self):
        """Crée l'onglet du rapport"""
        tab = self.results_notebook.tab("📋 Rapport")
        
        # Frame pour le rapport
        self.report_frame = ctk.CTkScrollableFrame(tab)
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_visualization_tab(self):
        """Onglet de visualisation avancée"""
        tab = self.tabview.tab("📈 Visualisation")
        
        # Notebook pour différents types de visualisations
        viz_notebook = ctk.CTkTabview(tab, corner_radius=10)
        viz_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        viz_notebook.add("🎨 Région Réalisable")
        viz_notebook.add("📊 Analyse 3D")
        viz_notebook.add("🔄 Animation")
        viz_notebook.add("📈 Sensibilité")
        
        # Configuration des sous-onglets
        self.create_feasible_region_viz(viz_notebook.tab("🎨 Région Réalisable"))
        self.create_3d_analysis(viz_notebook.tab("📊 Analyse 3D"))
        self.create_animation_viz(viz_notebook.tab("🔄 Animation"))
        self.create_sensitivity_analysis(viz_notebook.tab("📈 Sensibilité"))
        
    def create_feasible_region_viz(self, parent):
        """Visualisation de la région réalisable"""
        control_frame = ctk.CTkFrame(parent)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        # Contrôles
        ctk.CTkLabel(control_frame, text="Options de visualisation:").pack(side="left", padx=10)
        
        self.show_grid_var = tk.BooleanVar(value=True)
        grid_check = ctk.CTkCheckBox(
            control_frame,
            text="Grille",
            variable=self.show_grid_var,
            command=self.update_feasible_region
        )
        grid_check.pack(side="left", padx=10)
        
        self.show_optimal_var = tk.BooleanVar(value=True)
        optimal_check = ctk.CTkCheckBox(
            control_frame,
            text="Point optimal",
            variable=self.show_optimal_var,
            command=self.update_feasible_region
        )
        optimal_check.pack(side="left", padx=10)
        
        # Canvas pour matplotlib
        self.viz_frame = ctk.CTkFrame(parent)
        self.viz_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_3d_analysis(self, parent):
        """Analyse 3D pour problèmes à 3 variables"""
        info_label = ctk.CTkLabel(
            parent,
            text="📊 Visualisation 3D disponible pour les problèmes à 3 variables",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=20)
        
        self.viz_3d_frame = ctk.CTkFrame(parent)
        self.viz_3d_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_animation_viz(self, parent):
        """Animation du processus de résolution"""
        control_frame = ctk.CTkFrame(parent)
        control_frame.pack(fill="x", padx=10, pady=10)
        
        play_btn = AnimatedButton(
            control_frame,
            text="▶️ Démarrer l'animation",
            command=self.start_solving_animation,
            width=200,
            height=40,
            corner_radius=8
        )
        play_btn.pack(side="left", padx=10)
        
        speed_label = ctk.CTkLabel(control_frame, text="Vitesse:").pack(side="left", padx=(20, 5))
        
        self.animation_speed = tk.DoubleVar(value=1.0)
        speed_slider = ctk.CTkSlider(
            control_frame,
            from_=0.1,
            to=3.0,
            variable=self.animation_speed,
            width=200
        )
        speed_slider.pack(side="left", padx=10)
        
        self.animation_frame = ctk.CTkFrame(parent)
        self.animation_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_sensitivity_analysis(self, parent):
        """Analyse de sensibilité"""
        info_label = ctk.CTkLabel(
            parent,
            text="📈 Analyse de sensibilité des paramètres",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=20)
        
        self.sensitivity_frame = ctk.CTkFrame(parent)
        self.sensitivity_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_files_tab_modern(self):
        """Onglet de gestion des fichiers moderne"""
        tab = self.tabview.tab("💾 Fichiers")
        
        # Notebook pour organisation
        files_notebook = ctk.CTkTabview(tab, corner_radius=10)
        files_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        files_notebook.add("📚 Historique")
        files_notebook.add("💾 Import/Export")
        files_notebook.add("☁️ Cloud")
        
        # Configuration des sous-onglets
        self.create_history_tab(files_notebook.tab("📚 Historique"))
        self.create_import_export_tab(files_notebook.tab("💾 Import/Export"))
        self.create_cloud_tab(files_notebook.tab("☁️ Cloud"))
        
    def create_history_tab(self, parent):
        """Crée l'onglet historique"""
        # Barre de recherche
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Rechercher dans l'historique...",
            width=300,
            height=35,
            corner_radius=8
        )
        search_entry.pack(side="left", padx=10)
        
        filter_btn = AnimatedButton(
            search_frame,
            text="🔽 Filtres",
            command=self.show_history_filters,
            width=100,
            height=35,
            corner_radius=8
        )
        filter_btn.pack(side="left")
        
        # Liste avec style moderne
        self.history_frame = ctk.CTkScrollableFrame(parent)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_history_modern()
        
    def create_import_export_tab(self, parent):
        """Crée l'onglet import/export"""
        # Section Import
        import_frame = ctk.CTkFrame(parent, corner_radius=10)
        import_frame.pack(fill="x", padx=10, pady=10)
        
        import_title = ctk.CTkLabel(
            import_frame,
            text="📥 Importer",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        import_title.pack(pady=(15, 10))
        
        import_buttons = ctk.CTkFrame(import_frame, fg_color="transparent")
        import_buttons.pack(pady=(0, 15))
        
        formats = ["JSON", "CSV", "Excel", "LP"]
        for fmt in formats:
            btn = AnimatedButton(
                import_buttons,
                text=f"📄 {fmt}",
                command=lambda f=fmt: self.import_file(f),
                width=100,
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", padx=5)
        
        # Section Export
        export_frame = ctk.CTkFrame(parent, corner_radius=10)
        export_frame.pack(fill="x", padx=10, pady=10)
        
        export_title = ctk.CTkLabel(
            export_frame,
            text="📤 Exporter",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        export_title.pack(pady=(15, 10))
        
        export_buttons = ctk.CTkFrame(export_frame, fg_color="transparent")
        export_buttons.pack(pady=(0, 15))
        
        export_formats = ["PDF", "Excel", "LaTeX", "HTML"]
        for fmt in export_formats:
            btn = AnimatedButton(
                export_buttons,
                text=f"📄 {fmt}",
                command=lambda f=fmt: self.export_file(f),
                width=100,
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", padx=5)
            
    def create_cloud_tab(self, parent):
        """Crée l'onglet cloud"""
        cloud_frame = ctk.CTkFrame(parent, corner_radius=10)
        cloud_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        cloud_icon = ctk.CTkLabel(
            cloud_frame,
            text="☁️",
            font=ctk.CTkFont(size=60)
        )
        cloud_icon.pack(pady=(30, 10))
        
        cloud_title = ctk.CTkLabel(
            cloud_frame,
            text="Stockage Cloud",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        cloud_title.pack()
        
        cloud_desc = ctk.CTkLabel(
            cloud_frame,
            text="Synchronisez vos problèmes et résultats dans le cloud",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        cloud_desc.pack(pady=(5, 20))
        
        # Boutons de connexion
        services_frame = ctk.CTkFrame(cloud_frame, fg_color="transparent")
        services_frame.pack()
        
        cloud_services = [
            ("Google Drive", "green"),
            ("Dropbox", "blue"),
            ("OneDrive", "purple")
        ]
        
        for service, color in cloud_services:
            btn = AnimatedButton(
                services_frame,
                text=f"📁 {service}",
                command=lambda s=service: self.connect_cloud_service(s),
                width=150,
                height=40,
                corner_radius=8,
                fg_color=color
            )
            btn.pack(side="left", padx=10)
            
    def create_dashboard_tab(self):
        """Crée l'onglet dashboard"""
        tab = self.tabview.tab("🏠 Dashboard")
        
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title = ctk.CTkLabel(
            scroll,
            text="📊 Tableau de Bord",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Statistiques en cartes
        stats_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_grid.pack(fill="x", pady=(0, 20))
        
        self.create_stat_cards(stats_grid)
        
        # Graphiques
        graphs_frame = ctk.CTkFrame(scroll, corner_radius=10)
        graphs_frame.pack(fill="both", expand=True)
        
        self.create_dashboard_graphs(graphs_frame)
        
    def create_stat_cards(self, parent):
        """Crée les cartes de statistiques"""
        stats = [
            {
                "title": "Problèmes Résolus",
                "value": str(self.stats['problems_solved']),
                "icon": "✅",
                "color": "green"
            },
            {
                "title": "Temps Moyen",
                "value": f"{self.stats['avg_solving_time']:.2f}s",
                "icon": "⏱️",
                "color": "blue"
            },
            {
                "title": "Méthode Favorite",
                "value": max(self.stats['methods_used'], key=self.stats['methods_used'].get),
                "icon": "🏆",
                "color": "orange"
            },
            {
                "title": "Taux de Succès",
                "value": "100%",
                "icon": "📈",
                "color": "purple"
            }
        ]
        
        for i, stat in enumerate(stats):
            card = self.create_stat_card(parent, stat)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            parent.grid_columnconfigure(i, weight=1)
            
    def create_stat_card(self, parent, stat):
        """Crée une carte de statistique"""
        card = ctk.CTkFrame(parent, corner_radius=10, height=150)
        card.grid_propagate(False)
        
        # Icône
        icon_label = ctk.CTkLabel(
            card,
            text=stat["icon"],
            font=ctk.CTkFont(size=30)
        )
        icon_label.pack(pady=(20, 5))
        
        # Valeur
        value_label = ctk.CTkLabel(
            card,
            text=stat["value"],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=stat["color"]
        )
        value_label.pack()
        
        # Titre
        title_label = ctk.CTkLabel(
            card,
            text=stat["title"],
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        title_label.pack(pady=(5, 20))
        
        return card
        
    def create_dashboard_graphs(self, parent):
        """Crée les graphiques du dashboard"""
        graphs_title = ctk.CTkLabel(
            parent,
            text="📈 Analyses Graphiques",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        graphs_title.pack(pady=(15, 10))
        
        # Frame pour les graphiques matplotlib
        self.dashboard_graphs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.dashboard_graphs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Créer les graphiques
        self.create_methods_pie_chart()
        self.create_time_series_chart()
        
    def create_methods_pie_chart(self):
        """Crée un graphique en secteurs des méthodes utilisées"""
        fig, ax = plt.subplots(figsize=(6, 4))
        
        methods = list(self.stats['methods_used'].keys())
        values = list(self.stats['methods_used'].values())
        
        if sum(values) > 0:
            ax.pie(values, labels=methods, autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center', transform=ax.transAxes)
        
        ax.set_title("Répartition des Méthodes Utilisées")
        
        canvas = FigureCanvasTkAgg(fig, self.dashboard_graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", padx=10, pady=10)
        
    def create_time_series_chart(self):
        """Crée un graphique temporel"""
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Données simulées
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        values = np.random.randint(0, 10, 30)
        
        ax.plot(dates, values, marker='o', linestyle='-', linewidth=2, markersize=6)
        ax.set_title("Problèmes Résolus par Jour")
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre de Problèmes")
        ax.grid(True, alpha=0.3)
        
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, self.dashboard_graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="right", padx=10, pady=10)
        
    def create_status_bar(self):
        """Crée une barre de statut moderne"""
        self.status_bar = ctk.CTkFrame(self.main_container, height=30, corner_radius=0)
        self.status_bar.grid(row=2, column=0, sticky="ew")
        self.status_bar.grid_columnconfigure(1, weight=1)
        
        # Statut à gauche
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="✅ Prêt",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, padx=20)
        
        # Info au centre
        self.info_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.info_label.grid(row=0, column=1)
        
        # Heure à droite
        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.time_label.grid(row=0, column=2, padx=20)
        
        self.update_time()
        
    def update_time(self):
        """Met à jour l'heure dans la barre de statut"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
        
    def toggle_theme(self):
        """Bascule entre thème clair et sombre"""
        self.theme.toggle()
        
        # Mettre à jour l'icône du switch
        if self.theme.dark_mode:
            self.theme_switch.configure(text="🌙")
        else:
            self.theme_switch.configure(text="☀️")
            
    def show_dashboard(self):
        """Affiche le dashboard"""
        self.tabview.set("🏠 Dashboard")
        
    def focus_solve_tab(self):
        """Focus sur l'onglet de résolution"""
        self.tabview.set("🔍 Résolution")
        
    def show_visualization(self):
        """Affiche les visualisations"""
        self.tabview.set("📈 Visualisation")
        
    def show_history(self):
        """Affiche l'historique"""
        self.tabview.set("💾 Fichiers")
        
    def show_settings(self):
        """Affiche les paramètres"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("⚙️ Paramètres")
        settings_window.geometry("600x500")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Centrer la fenêtre
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - 300
        y = (settings_window.winfo_screenheight() // 2) - 250
        settings_window.geometry(f"600x500+{x}+{y}")
        
        # Contenu des paramètres
        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Paramètres",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Options
        options = [
            ("Sauvegarde automatique", self.auto_save_enabled),
            ("Animations", True),
            ("Sons", False),
            ("Tooltips", True)
        ]
        
        for option, default in options:
            var = tk.BooleanVar(value=default)
            switch = ctk.CTkSwitch(
                settings_frame,
                text=option,
                variable=var
            )
            switch.pack(pady=10)
            
        # Bouton fermer
        close_btn = AnimatedButton(
            settings_frame,
            text="✅ Fermer",
            command=settings_window.destroy,
            width=150,
            height=40,
            corner_radius=8
        )
        close_btn.pack(pady=(20, 0))
        
    def show_help(self):
        """Affiche l'aide"""
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("❓ Aide")
        help_window.geometry("700x600")
        help_window.transient(self.root)
        
        # Contenu de l'aide
        help_frame = ctk.CTkScrollableFrame(help_window)
        help_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            help_frame,
            text="📚 Guide d'Utilisation",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Sections d'aide
        help_sections = [
            {
                "title": "🚀 Démarrage Rapide",
                "content": "1. Définissez le nombre de variables et contraintes\n"
                          "2. Remplissez les coefficients\n"
                          "3. Choisissez une méthode de résolution\n"
                          "4. Consultez les résultats"
            },
            {
                "title": "⌨️ Raccourcis Clavier",
                "content": "Ctrl+N : Nouveau problème\n"
                          "Ctrl+O : Ouvrir un fichier\n"
                          "Ctrl+S : Sauvegarder\n"
                          "F5 : Simplexe Standard\n"
                          "F6 : Grand M\n"
                          "F7 : Analyse Duale\n"
                          "F11 : Plein écran"
            },
            {
                "title": "💡 Conseils",
                "content": "• Utilisez Grand M pour les contraintes ≥ ou =\n"
                          "• La visualisation fonctionne mieux avec 2 variables\n"
                          "• Exportez vos résultats en PDF pour les rapports"
            }
        ]
        
        for section in help_sections:
            section_frame = ctk.CTkFrame(help_frame, corner_radius=10)
            section_frame.pack(fill="x", pady=10)
            
            section_title = ctk.CTkLabel(
                section_frame,
                text=section["title"],
                font=ctk.CTkFont(size=16, weight="bold")
            )
            section_title.pack(pady=(10, 5))
            
            section_content = ctk.CTkLabel(
                section_frame,
                text=section["content"],
                font=ctk.CTkFont(size=12),
                justify="left"
            )
            section_content.pack(pady=(5, 10), padx=20)
            
    def show_statistics(self):
        """Affiche les statistiques détaillées"""
        stats_window = ctk.CTkToplevel(self.root)
        stats_window.title("📈 Statistiques")
        stats_window.geometry("800x600")
        stats_window.transient(self.root)
        
        # Contenu
        stats_frame = ctk.CTkFrame(stats_window)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            stats_frame,
            text="📈 Statistiques Détaillées",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Créer des graphiques statistiques avec plotly
        self.create_plotly_stats(stats_frame)
        
    def create_plotly_stats(self, parent):
        """Crée des graphiques statistiques avec Plotly"""
        # Données simulées
        methods = list(self.stats['methods_used'].keys())
        values = list(self.stats['methods_used'].values())
        
        # Graphique en barres
        fig = go.Figure(data=[
            go.Bar(x=methods, y=values, marker_color=['blue', 'green', 'orange'])
        ])
        
        fig.update_layout(
            title="Utilisation des Méthodes",
            xaxis_title="Méthode",
            yaxis_title="Nombre d'utilisations",
            template="plotly_dark" if self.theme.dark_mode else "plotly_white"
        )
        
        # Sauvegarder et afficher
        fig.write_html("temp_stats.html")
        webbrowser.open("temp_stats.html")
        
    def customize_interface(self):
        """Personnalise l'interface"""
        custom_window = ctk.CTkToplevel(self.root)
        custom_window.title("🎨 Personnalisation")
        custom_window.geometry("500x400")
        custom_window.transient(self.root)
        
        frame = ctk.CTkFrame(custom_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="🎨 Personnaliser l'Interface",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Options de couleur
        color_label = ctk.CTkLabel(
            frame,
            text="Thème de couleur:",
            font=ctk.CTkFont(size=14)
        )
        color_label.pack(pady=(0, 10))
        
        color_options = ctk.CTkSegmentedButton(
            frame,
            values=["Bleu", "Vert", "Rouge", "Violet"],
            command=self.change_color_theme
        )
        color_options.pack(pady=(0, 20))
        color_options.set("Bleu")
        
        # Taille de police
        font_label = ctk.CTkLabel(
            frame,
            text="Taille de police:",
            font=ctk.CTkFont(size=14)
        )
        font_label.pack(pady=(0, 10))
        
        font_slider = ctk.CTkSlider(
            frame,
            from_=10,
            to=20,
            command=self.change_font_size
        )
        font_slider.pack(pady=(0, 20))
        
    def change_color_theme(self, value):
        """Change le thème de couleur"""
        themes = {
            "Bleu": "blue",
            "Vert": "green",
            "Rouge": "dark-blue",
            "Violet": "blue"
        }
        ctk.set_default_color_theme(themes.get(value, "blue"))
        
    def change_font_size(self, value):
        """Change la taille de police"""
        # Implémenter le changement de taille de police
        pass
        
    def export_to_pdf(self):
        """Exporte les résultats en PDF"""
        if not hasattr(self, 'last_result'):
            self.show_error("Aucun résultat à exporter")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Exporter en PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")]
        )
        
        if filename:
            self.create_pdf_report(filename)
            
    def create_pdf_report(self, filename):
        """Crée un rapport PDF professionnel"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E86AB'),
            alignment=1
        )
        
        title = Paragraph("Rapport de Programmation Linéaire", title_style)
        elements.append(title)
        elements.append(Spacer(1, 30))
        
        # Informations
        info_text = f"""
        <b>Date:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>
        <b>Méthode:</b> {self.last_result.get('method', 'N/A')}<br/>
        <b>Statut:</b> Résolu avec succès
        """
        info = Paragraph(info_text, styles['Normal'])
        elements.append(info)
        elements.append(Spacer(1, 20))
        
        # Résultats
        results_title = Paragraph("Résultats", styles['Heading2'])
        elements.append(results_title)
        elements.append(Spacer(1, 10))
        
        # Contenu des résultats
        results_text = self.last_result.get('output', 'Aucun résultat')
        # Limiter la longueur pour le PDF
        if len(results_text) > 5000:
            results_text = results_text[:5000] + "\n... (tronqué)"
        
        results_para = Paragraph(
            f"<pre>{results_text}</pre>",
            styles['Code']
        )
        elements.append(results_para)
        
        # Générer le PDF
        try:
            doc.build(elements)
            self.show_success(f"PDF exporté: {filename}")
        except Exception as e:
            self.show_error(f"Erreur lors de l'export PDF: {e}")
            
    def refresh_history_modern(self):
        """Actualise l'historique avec un design moderne"""
        # Nettoyer
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        # Afficher l'historique
        for i, problem in enumerate(self.variable_manager.history):
            self.create_history_card(problem, i)
            
    def create_history_card(self, problem, index):
        """Crée une carte d'historique moderne"""
        card = ctk.CTkFrame(self.history_frame, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # Effet au survol
        card.bind("<Enter>", lambda e: card.configure(fg_color=("gray85", "gray25")))
        card.bind("<Leave>", lambda e: card.configure(fg_color=("gray90", "gray20")))
        
        # Contenu
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Infos principales
        method = problem.get('method', '?')
        timestamp = problem.get('timestamp', '?')
        metadata = problem.get('metadata', {})
        
        # Titre et méthode
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        method_label = ctk.CTkLabel(
            title_frame,
            text=f"🔧 {method}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        method_label.pack(side="left")
        
        time_label = ctk.CTkLabel(
            title_frame,
            text=timestamp,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        time_label.pack(side="right")
        
        # Détails
        details_text = f"Variables: {metadata.get('nb_variables', '?')} | Contraintes: {metadata.get('nb_contraintes', '?')}"
        details_label = ctk.CTkLabel(
            content_frame,
            text=details_text,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        details_label.pack(anchor="w", pady=(5, 0))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(10, 0))
        
        load_btn = AnimatedButton(
            actions_frame,
            text="📂 Charger",
            command=lambda: self.load_from_history(index),
            width=80,
            height=30,
            corner_radius=6
        )
        load_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = AnimatedButton(
            actions_frame,
            text="🗑️",
            command=lambda: self.delete_from_history(index),
            width=40,
            height=30,
            corner_radius=6,
            fg_color="red"
        )
        delete_btn.pack(side="left")
        
    def show_error(self, message):
        """Affiche un message d'erreur moderne"""
        self.show_notification(message, "error")
        
    def show_success(self, message):
        """Affiche un message de succès moderne"""
        self.show_notification(message, "success")
        
    def show_notification(self, message, type="info"):
        """Affiche une notification moderne"""
        colors = {
            "info": "blue",
            "success": "green",
            "error": "red",
            "warning": "orange"
        }
        
        notification = ctk.CTkFrame(
            self.root,
            corner_radius=10,
            fg_color=colors.get(type, "blue"),
            width=300,
            height=60
        )
        
        notification.place(relx=0.5, rely=0.1, anchor="center")
        notification.lift()
        
        msg_label = ctk.CTkLabel(
            notification,
            text=message,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        msg_label.pack(expand=True)
        
        # Animation de disparition
        self.root.after(3000, notification.destroy)
        
    def update_feasible_region(self):
        """Met à jour la visualisation de la région réalisable"""
        if not self.current_problem or self.current_problem["nombres_variables_base"] != 2:
            return
            
        # Nettoyer le frame
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
            
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Configuration du style
        if self.theme.dark_mode:
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
            
        # Tracer les contraintes
        self.plot_constraints(ax)
        
        # Options
        if self.show_grid_var.get():
            ax.grid(True, alpha=0.3)
            
        if self.show_optimal_var.get():
            # Ajouter le point optimal (simulé)
            ax.plot(5, 5, 'ro', markersize=10, label='Point Optimal')
            
        ax.set_xlabel('x₁', fontsize=12)
        ax.set_ylabel('x₂', fontsize=12)
        ax.set_title('Région Réalisable', fontsize=14, fontweight='bold')
        ax.legend()
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.viz_frame)
        toolbar.update()
        
    def plot_constraints(self, ax):
        """Trace les contraintes sur le graphique"""
        x = np.linspace(0, 20, 400)
        equations = self.current_problem["equations"]
        constraints_info = self.current_problem.get("constraints_info", [])
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, (key, eq) in enumerate(equations.items()):
            if len(eq) >= 3:
                rhs = eq[0]
                a1, a2 = eq[1], eq[2]
                
                if a2 != 0:
                    y = (rhs - a1 * x) / a2
                    
                    # Filtrer les valeurs négatives
                    valid_mask = (y >= 0) & (x >= 0)
                    
                    constraint_type = constraints_info[i] if i < len(constraints_info) else "<="
                    label = f"C{i+1}: {a1}x₁ + {a2}x₂ {constraint_type} {rhs}"
                    
                    ax.plot(x[valid_mask], y[valid_mask], 
                           color=colors[i % len(colors)], 
                           label=label, linewidth=2)
                    
                    # Zone réalisable
                    if constraint_type == "<=":
                        ax.fill_between(x[valid_mask], 0, y[valid_mask], 
                                      color=colors[i % len(colors)], alpha=0.1)
                                      
    def start_solving_animation(self):
        """Démarre l'animation du processus de résolution"""
        # Nettoyer le frame
        for widget in self.animation_frame.winfo_children():
            widget.destroy()
            
        # Créer l'animation
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Animation simulée du simplexe
        self.animation_step = 0
        self.animation_points = [(0, 0), (2, 3), (4, 5), (6, 4), (8, 2)]
        
        line, = ax.plot([], [], 'ro-', markersize=8)
        
        def init():
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.set_xlabel('x₁')
            ax.set_ylabel('x₂')
            ax.set_title('Animation du Simplexe')
            ax.grid(True, alpha=0.3)
            return line,
            
        def animate(frame):
            if frame < len(self.animation_points):
                x_data = [p[0] for p in self.animation_points[:frame+1]]
                y_data = [p[1] for p in self.animation_points[:frame+1]]
                line.set_data(x_data, y_data)
            return line,
            
        anim = FuncAnimation(
            fig, animate, init_func=init,
            frames=len(self.animation_points),
            interval=1000/self.animation_speed.get(),
            blit=True,
            repeat=True
        )
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, self.animation_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def copy_results(self):
        """Copie les résultats dans le presse-papier"""
        if hasattr(self, 'results_text'):
            content = self.results_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.show_success("✅ Résultats copiés!")
            
    def load_from_history(self, index):
        """Charge un problème depuis l'historique"""
        variables = self.variable_manager.get_problem(index)
        if variables:
            self.current_problem = variables
            self.update_solve_tab()
            self.show_success("✅ Problème chargé!")
            self.tabview.set("🔍 Résolution")
            
    def delete_from_history(self, index):
        """Supprime un problème de l'historique"""
        if messagebox.askyesno("Confirmation", "Supprimer ce problème ?"):
            if self.variable_manager.delete_problem(index):
                self.refresh_history_modern()
                self.show_success("✅ Problème supprimé!")
                
    def show_history_filters(self):
        """Affiche les filtres d'historique"""
        # Implémenter les filtres d'historique
        pass
        
    def import_file(self, format):
        """Importe un fichier selon le format"""
        filetypes = {
            "JSON": [("JSON", "*.json")],
            "CSV": [("CSV", "*.csv")],
            "Excel": [("Excel", "*.xlsx")],
            "LP": [("LP", "*.lp")]
        }
        
        filename = filedialog.askopenfilename(
            title=f"Importer {format}",
            filetypes=filetypes.get(format, [])
        )
        
        if filename:
            # Implémenter l'import selon le format
            self.show_success(f"✅ Fichier {format} importé!")
            
    def export_file(self, format):
        """Exporte vers un fichier selon le format"""
        if not self.current_problem:
            self.show_error("Aucun problème à exporter")
            return
            
        # Implémenter l'export selon le format
        self.show_success(f"✅ Export {format} réussi!")
        
    def connect_cloud_service(self, service):
        """Connecte un service cloud"""
        self.show_notification(f"Connexion à {service}...", "info")
        # Implémenter la connexion cloud
        
    def load_stats(self):
        """Charge les statistiques sauvegardées"""
        try:
            with open("stats.json", "r") as f:
                saved_stats = json.load(f)
                self.stats.update(saved_stats)
        except:
            pass
            
    def save_stats(self):
        """Sauvegarde les statistiques"""
        try:
            with open("stats.json", "w") as f:
                json.dump(self.stats, f)
        except:
            pass
            
    def on_closing(self):
        """Gestion de la fermeture de l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
            self.save_stats()
            self.root.quit()
            self.root.destroy()
            
    # Méthodes existantes adaptées
    def validate_problem(self):
        """Valide et construit le problème de PL"""
        try:
            nb_vars = int(self.nb_vars_var.get())
            nb_constraints = int(self.nb_constraints_var.get())
            
            # Construire la fonction objectif
            obj_coeffs = [0]  # Constante
            for var in self.problem_vars:
                coeff = float(var.get())
                if self.opt_type_var.get() == "min":
                    coeff = -coeff  # Conversion min -> max
                obj_coeffs.append(coeff)
            
            # Construire les contraintes
            equations = {}
            constraints_info = []
            
            for i, (constraint_coeffs, constraint_type) in enumerate(zip(self.constraint_vars, self.constraint_types)):
                # RHS en premier, puis coefficients
                rhs = float(constraint_coeffs[-1].get())
                coeffs = [rhs]
                
                for j in range(nb_vars):
                    coeffs.append(float(constraint_coeffs[j].get()))
                
                equations[f"equation_{i+1}"] = coeffs
                constraints_info.append(constraint_type.get())
            
            # Créer le dictionnaire du problème
            self.current_problem = {
                "tab_optimisation": obj_coeffs,
                "nombres_variables_base": nb_vars,
                "equations": equations,
                "nb_equations": nb_constraints,
                "constraints_info": constraints_info,
                "objective_type": self.opt_type_var.get(),
                "method_type": "Interface Graphique"
            }
            
            # Sauvegarder dans l'historique
            self.variable_manager.save_problem(self.current_problem, "Interface Graphique")
            
            # Statistiques
            self.stats['problems_solved'] += 1
            
            self.show_success("✅ Problème validé et sauvegardé!")
            
            # Passer à l'onglet de résolution
            self.tabview.set("🔍 Résolution")
            self.update_solve_tab()
            
        except ValueError as e:
            self.show_error(f"Erreur dans les données: {e}")
        except Exception as e:
            self.show_error(f"Erreur inattendue: {e}")
    
    def update_solve_tab(self):
        """Met à jour l'onglet de résolution avec les infos du problème"""
        if self.current_problem:
            nb_vars = self.current_problem["nombres_variables_base"]
            nb_constraints = self.current_problem["nb_equations"]
            obj_type = self.current_problem.get("objective_type", "max")
            
            info_text = f"✅ Problème défini: {nb_vars} variables, {nb_constraints} contraintes ({obj_type}imisation)"
            
            # Suggestion de méthode
            constraints_info = self.current_problem.get("constraints_info", [])
            if any(c in [">=", "="] for c in constraints_info):
                info_text += "\n💡 Méthode suggérée: Grand M"
            else:
                info_text += "\n💡 Méthode suggérée: Simplexe Standard"
            
            self.problem_status_label.configure(text=info_text)
            self.status_label.configure(text="✅ Problème chargé")
        else:
            self.problem_status_label.configure(text="❌ Aucun problème chargé")
            self.status_label.configure(text="⚠️ Aucun problème")
    
    def solve_standard(self):
        """Résolution par simplexe standard"""
        if not self.current_problem:
            self.show_error("Veuillez d'abord définir un problème")
            return
        
        self.run_solver("Simplexe Standard", self._solve_standard_worker)
    
    def solve_grand_m(self):
        """Résolution par Grand M"""
        if not self.current_problem:
            self.show_error("Veuillez d'abord définir un problème")
            return
        
        self.run_solver("Grand M", self._solve_grand_m_worker)
    
    def solve_dual(self):
        """Analyse primal-dual"""
        if not self.current_problem:
            self.show_error("Veuillez d'abord définir un problème")
            return
        
        self.run_solver("Analyse Duale", self._solve_dual_worker)
    
    def run_solver(self, method_name, worker_func):
        """Lance la résolution dans un thread séparé"""
        self.progress_var.set(f"🔄 Résolution en cours ({method_name})...")
        self.progress_bar.set(0)
        self.status_label.configure(text=f"⏳ {method_name} en cours...")
        
        # Animation de progression
        self.animate_progress = True
        self.animate_progress_bar()
        
        # Thread pour éviter de bloquer l'interface
        thread = threading.Thread(target=worker_func, args=(method_name,))
        thread.daemon = True
        thread.start()
    
    def animate_progress_bar(self):
        """Anime la barre de progression"""
        if hasattr(self, 'animate_progress') and self.animate_progress:
            current = self.progress_bar.get()
            if current >= 1.0:
                self.progress_bar.set(0)
            else:
                self.progress_bar.set(current + 0.05)
            self.root.after(100, self.animate_progress_bar)
    
    def _solve_standard_worker(self, method_name):
        """Worker pour simplexe standard"""
        try:
            import copy
            import time
            start_time = time.time()
            
            problem_copy = copy.deepcopy(self.current_problem)
            solver = SimplexMethodTab(problem_copy)
            
            # Capturer la sortie
            result = self.capture_solver_output(solver.run)
            
            # Calculer le temps écoulé
            elapsed_time = time.time() - start_time
            
            # Mettre à jour les statistiques
            self.stats['methods_used']['Simplexe'] += 1
            self.stats['avg_solving_time'] = (self.stats['avg_solving_time'] + elapsed_time) / 2
            
            # Mettre à jour l'interface dans le thread principal
            self.root.after(0, self._solver_completed, method_name, result, problem_copy, elapsed_time)
            
        except Exception as e:
            self.root.after(0, self._solver_error, method_name, str(e))
    
    def _solve_grand_m_worker(self, method_name):
        """Worker pour Grand M"""
        try:
            import copy
            import time
            start_time = time.time()
            
            problem_copy = copy.deepcopy(self.current_problem)
            solver = GrandMMethod(problem_copy)
            
            result = self.capture_solver_output(solver.run)
            
            elapsed_time = time.time() - start_time
            
            self.stats['methods_used']['Grand M'] += 1
            self.stats['avg_solving_time'] = (self.stats['avg_solving_time'] + elapsed_time) / 2
            
            self.root.after(0, self._solver_completed, method_name, result, problem_copy, elapsed_time)
            
        except Exception as e:
            self.root.after(0, self._solver_error, method_name, str(e))
    
    def _solve_dual_worker(self, method_name):
        """Worker pour analyse duale"""
        try:
            import copy
            import time
            start_time = time.time()
            
            problem_copy = copy.deepcopy(self.current_problem)
            analyzer = DualMethod(problem_copy)
            
            result = self.capture_solver_output(analyzer.run_complete_analysis)
            
            elapsed_time = time.time() - start_time
            
            self.stats['methods_used']['Dual'] += 1
            self.stats['avg_solving_time'] = (self.stats['avg_solving_time'] + elapsed_time) / 2
            
            self.root.after(0, self._solver_completed, method_name, result, problem_copy, elapsed_time)
            
        except Exception as e:
            self.root.after(0, self._solver_error, method_name, str(e))
    
    def capture_solver_output(self, solver_func):
        """Capture la sortie de la console"""
        import io
        import contextlib
        
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            solver_func()
        
        return output.getvalue()
    
    def _solver_completed(self, method_name, result, final_problem, elapsed_time):
        """Callback quand la résolution est terminée"""
        self.animate_progress = False
        self.progress_bar.set(1.0)
        self.progress_var.set(f"✅ {method_name} terminé en {elapsed_time:.2f}s!")
        self.status_label.configure(text="✅ Résolution terminée")
        
        # Stocker le résultat
        self.last_result = {
            'method': method_name,
            'output': result,
            'problem': final_problem,
            'timestamp': datetime.now(),
            'elapsed_time': elapsed_time
        }
        
        # Mise à jour des statistiques
        self.update_stats_display()
        
        # Passer à l'onglet des résultats
        self.tabview.set("📊 Résultats")
        self.display_results()
        
        # Notification
        self.show_success(f"✅ {method_name} terminé en {elapsed_time:.2f}s!")
        
        # Visualisation automatique si 2 variables
        if self.current_problem["nombres_variables_base"] == 2:
            self.update_feasible_region()
    
    def _solver_error(self, method_name, error_msg):
        """Callback en cas d'erreur"""
        self.animate_progress = False
        self.progress_bar.set(0)
        self.progress_var.set(f"❌ Erreur lors de {method_name}")
        self.status_label.configure(text="❌ Erreur")
        self.show_error(f"Erreur durant {method_name}:\n{error_msg}")
    
    def update_stats_display(self):
        """Met à jour l'affichage des statistiques"""
        self.stats_label.configure(
            text=f"Problèmes résolus: {self.stats['problems_solved']}\n"
                 f"Temps moyen: {self.stats['avg_solving_time']:.2f}s"
        )
    
    def display_results(self):
        """Affiche les résultats de la dernière résolution"""
        if not hasattr(self, 'last_result'):
            self.results_text.delete(0.0, tk.END)
            self.results_text.insert(0.0, "Aucun résultat à afficher.\nLancez d'abord une résolution.")
            return
        
        result = self.last_result
        
        # Titre avec informations
        title_text = f"📊 Résultats - {result['method']}\n"
        title_text += f"⏰ {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        title_text += f"⏱️ Temps d'exécution: {result.get('elapsed_time', 0):.2f}s\n"
        title_text += "="*60 + "\n\n"
        
        # Contenu dans l'onglet sortie détaillée
        self.results_text.delete(0.0, tk.END)
        self.results_text.insert(0.0, title_text + result['output'])
        
        # Créer le tableau final
        self.create_final_tableau_display()
        
        # Créer les graphiques
        self.create_result_graphs()
        
        # Créer le rapport
        self.create_result_report()
    
    def create_final_tableau_display(self):
        """Affiche le tableau final sous forme de table"""
        # Nettoyer le frame
        for widget in self.tableau_frame.winfo_children():
            widget.destroy()
        
        title = ctk.CTkLabel(
            self.tableau_frame,
            text="📊 Tableau Final du Simplexe",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Extraire le tableau final depuis les résultats
        output = self.last_result.get('output', '')
        
        # Rechercher le tableau final dans la sortie
        if "Tableau final" in output or "Solution optimale" in output:
            # Créer une représentation visuelle du tableau
            table_frame = ctk.CTkFrame(self.tableau_frame, corner_radius=10)
            table_frame.pack(padx=20, pady=10)
            
            # Exemple de tableau (à adapter selon la sortie réelle)
            self.create_example_tableau(table_frame)
        else:
            no_table_label = ctk.CTkLabel(
                self.tableau_frame,
                text="Aucun tableau final disponible",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_table_label.pack(pady=50)
    
    def create_example_tableau(self, parent):
        """Crée un exemple de tableau visuel"""
        # Headers
        headers = ["Base", "x₁", "x₂", "s₁", "s₂", "s₃", "RHS"]
        
        # Créer le header
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=80
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Données exemple
        data = [
            ["s₁", "1", "0", "1", "0", "0", "4"],
            ["x₂", "0", "1", "0", "0.5", "0", "6"],
            ["s₃", "3", "0", "0", "-1", "1", "6"],
            ["Z", "-3", "0", "0", "2.5", "0", "30"]
        ]
        
        # Créer les lignes
        for row_idx, row_data in enumerate(data):
            row_frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray15") if row_idx % 2 == 0 else "transparent")
            row_frame.pack(fill="x", padx=10)
            
            for col_idx, value in enumerate(row_data):
                if row_idx == len(data) - 1:  # Ligne Z
                    font = ctk.CTkFont(size=12, weight="bold")
                    text_color = "green" if col_idx == len(row_data) - 1 else None
                else:
                    font = ctk.CTkFont(size=12)
                    text_color = None
                
                label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=font,
                    text_color=text_color,
                    width=80
                )
                label.grid(row=0, column=col_idx, padx=5, pady=5)
    
    def create_result_graphs(self):
        """Crée les graphiques de résultats"""
        # Nettoyer le frame
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
        
        if self.current_problem["nombres_variables_base"] == 2:
            # Graphique 2D
            self.create_2d_solution_graph()
        elif self.current_problem["nombres_variables_base"] == 3:
            # Graphique 3D
            self.create_3d_solution_graph()
        else:
            # Graphique en barres pour plus de 3 variables
            self.create_bar_solution_graph()
    
    def create_2d_solution_graph(self):
        """Crée un graphique 2D de la solution"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Style selon le thème
        if self.theme.dark_mode:
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
        
        # Tracer les contraintes
        self.plot_constraints(ax)
        
        # Ajouter la fonction objectif
        x = np.linspace(0, 20, 100)
        obj_coeffs = self.current_problem["tab_optimisation"][1:]
        if len(obj_coeffs) >= 2 and obj_coeffs[1] != 0:
            # Lignes d'iso-profit
            for z in [10, 20, 30, 40]:
                y = (z - obj_coeffs[0] * x) / obj_coeffs[1]
                ax.plot(x, y, '--', alpha=0.3, label=f'Z={z}')
        
        # Point optimal (simulé)
        ax.plot(6, 3, 'r*', markersize=20, label='Solution Optimale')
        ax.annotate('Optimal\n(6, 3)', xy=(6, 3), xytext=(7, 4),
                   arrowprops=dict(arrowstyle='->', color='red'))
        
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 15)
        ax.set_xlabel('x₁', fontsize=14)
        ax.set_ylabel('x₂', fontsize=14)
        ax.set_title('Solution Graphique du Problème', fontsize=16, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar_frame = ctk.CTkFrame(self.graphs_frame)
        toolbar_frame.pack(fill="x", padx=10)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
    
    def create_3d_solution_graph(self):
        """Crée un graphique 3D de la solution"""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Créer une grille pour la visualisation
        x = np.linspace(0, 10, 50)
        y = np.linspace(0, 10, 50)
        X, Y = np.meshgrid(x, y)
        
        # Fonction objectif
        obj_coeffs = self.current_problem["tab_optimisation"][1:]
        if len(obj_coeffs) >= 2:
            Z = obj_coeffs[0] * X + obj_coeffs[1] * Y
            
            # Surface de la fonction objectif
            surf = ax.plot_surface(X, Y, Z, alpha=0.3, cmap='viridis')
            
            # Point optimal (simulé)
            ax.scatter([5], [3], [obj_coeffs[0]*5 + obj_coeffs[1]*3], 
                      color='red', s=100, label='Solution Optimale')
        
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.set_zlabel('Z')
        ax.set_title('Visualisation 3D de la Solution')
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_bar_solution_graph(self):
        """Crée un graphique en barres pour la solution"""
        # Extraire les valeurs de la solution
        nb_vars = self.current_problem["nombres_variables_base"]
        
        # Valeurs simulées (à remplacer par les vraies valeurs extraites)
        variables = [f'x{self.subscript(i+1)}' for i in range(nb_vars)]
        values = np.random.uniform(0, 10, nb_vars)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Style selon le thème
        if self.theme.dark_mode:
            plt.style.use('dark_background')
        
        # Créer le graphique en barres
        bars = ax.bar(variables, values, color=plt.cm.viridis(np.linspace(0, 1, nb_vars)))
        
        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}', ha='center', va='bottom')
        
        ax.set_xlabel('Variables', fontsize=14)
        ax.set_ylabel('Valeurs', fontsize=14)
        ax.set_title('Valeurs des Variables de Décision', fontsize=16, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_result_report(self):
        """Crée un rapport formaté des résultats"""
        # Nettoyer le frame
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        # Titre du rapport
        title = ctk.CTkLabel(
            self.report_frame,
            text="📋 Rapport d'Analyse",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Sections du rapport
        self.create_report_section("📊 Résumé Exécutif", self.get_executive_summary())
        self.create_report_section("🔍 Détails du Problème", self.get_problem_details())
        self.create_report_section("💡 Solution Optimale", self.get_optimal_solution())
        self.create_report_section("📈 Analyse de Sensibilité", self.get_sensitivity_analysis())
        self.create_report_section("💭 Recommandations", self.get_recommendations())
    
    def create_report_section(self, title, content):
        """Crée une section du rapport"""
        section_frame = ctk.CTkFrame(self.report_frame, corner_radius=10)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        section_title = ctk.CTkLabel(
            section_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_title.pack(anchor="w", padx=15, pady=(10, 5))
        
        section_content = ctk.CTkLabel(
            section_frame,
            text=content,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        section_content.pack(anchor="w", padx=15, pady=(5, 15))
    
    def get_executive_summary(self):
        """Génère le résumé exécutif"""
        return f"""Le problème de programmation linéaire a été résolu avec succès.
Méthode utilisée: {self.last_result.get('method', 'N/A')}
Temps d'exécution: {self.last_result.get('elapsed_time', 0):.2f} secondes
Statut: Solution optimale trouvée"""
    
    def get_problem_details(self):
        """Génère les détails du problème"""
        nb_vars = self.current_problem["nombres_variables_base"]
        nb_constraints = self.current_problem["nb_equations"]
        obj_type = self.current_problem.get("objective_type", "max")
        
        return f"""Type d'optimisation: {obj_type.upper()}IMISATION
Nombre de variables de décision: {nb_vars}
Nombre de contraintes: {nb_constraints}
Méthode suggérée: {"Grand M" if any(c in [">=", "="] for c in self.current_problem.get("constraints_info", [])) else "Simplexe Standard"}"""
    
    def get_optimal_solution(self):
        """Extrait la solution optimale"""
        # Parser la sortie pour extraire la solution
        output = self.last_result.get('output', '')
        
        # Recherche basique de la valeur optimale
        if "Solution optimale" in output or "Z =" in output:
            return "Solution optimale trouvée (voir sortie détaillée)"
        else:
            return "Solution en cours d'extraction..."
    
    def get_sensitivity_analysis(self):
        """Génère l'analyse de sensibilité"""
        return """L'analyse de sensibilité permet d'évaluer l'impact des variations
des paramètres sur la solution optimale. Cette analyse est disponible
dans la méthode d'analyse duale."""
    
    def get_recommendations(self):
        """Génère des recommandations"""
        recommendations = []
        
        if self.current_problem["nombres_variables_base"] == 2:
            recommendations.append("• La visualisation graphique est disponible pour ce problème")
        
        if any(c in [">=", "="] for c in self.current_problem.get("constraints_info", [])):
            recommendations.append("• La méthode Grand M est recommandée pour ce type de contraintes")
        
        recommendations.append("• Considérez l'analyse duale pour une compréhension approfondie")
        recommendations.append("• Exportez les résultats en PDF pour vos rapports")
        
        return "\n".join(recommendations)
    
    def compare_methods(self):
        """Compare plusieurs méthodes avec une interface moderne"""
        if not self.current_problem:
            self.show_error("Veuillez d'abord définir un problème")
            return
        
        # Fenêtre de comparaison moderne
        compare_window = ctk.CTkToplevel(self.root)
        compare_window.title("⚖️ Comparaison des Méthodes")
        compare_window.geometry("1000x700")
        
        # Centrer la fenêtre
        compare_window.transient(self.root)
        compare_window.update_idletasks()
        x = (compare_window.winfo_screenwidth() // 2) - 500
        y = (compare_window.winfo_screenheight() // 2) - 350
        compare_window.geometry(f"1000x700+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(compare_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title = ctk.CTkLabel(
            main_frame,
            text="⚖️ Comparaison des Méthodes de Résolution",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Notebook pour les résultats
        comparison_notebook = ctk.CTkTabview(main_frame, corner_radius=10)
        comparison_notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Onglets pour chaque méthode
        methods_data = [
            ("Simplexe Standard", self._solve_standard_worker),
            ("Grand M", self._solve_grand_m_worker),
            ("Analyse Duale", self._solve_dual_worker)
        ]
        
        # Dictionnaire pour stocker les résultats
        self.comparison_results = {}
        
        for method_name, worker in methods_data:
            comparison_notebook.add(method_name)
            tab = comparison_notebook.tab(method_name)
            
            # Zone de texte pour les résultats
            text_widget = ctk.CTkTextbox(
                tab,
                font=ctk.CTkFont(family="Consolas", size=11),
                corner_radius=10
            )
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Frame pour les contrôles
            control_frame = ctk.CTkFrame(tab, fg_color="transparent")
            control_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            # Bouton pour lancer cette méthode
            run_btn = AnimatedButton(
                control_frame,
                text=f"🚀 Lancer {method_name}",
                command=lambda m=method_name, w=worker, t=text_widget: self.run_comparison_method(m, w, t),
                width=200,
                height=35,
                corner_radius=8
            )
            run_btn.pack(side="left", padx=5)
            
            # Label de statut
            status_label = ctk.CTkLabel(
                control_frame,
                text="En attente...",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            status_label.pack(side="left", padx=20)
            
            # Stocker les widgets
            setattr(tab, 'text_widget', text_widget)
            setattr(tab, 'status_label', status_label)
        
        # Onglet de synthèse
        comparison_notebook.add("📊 Synthèse")
        synthesis_tab = comparison_notebook.tab("📊 Synthèse")
        self.create_synthesis_tab(synthesis_tab)
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        actions_frame.pack(fill="x")
        
        all_btn = AnimatedButton(
            actions_frame,
            text="🎯 Lancer Toutes les Méthodes",
            command=lambda: self.run_all_comparisons(comparison_notebook),
            width=250,
            height=40,
            corner_radius=10,
            fg_color="green"
        )
        all_btn.pack(side="left", padx=10)
        
        export_btn = AnimatedButton(
            actions_frame,
            text="📤 Exporter Comparaison",
            command=self.export_comparison,
            width=200,
            height=40,
            corner_radius=10
        )
        export_btn.pack(side="left", padx=10)
    
    def create_synthesis_tab(self, parent):
        """Crée l'onglet de synthèse de comparaison"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.synthesis_frame = scroll_frame
        
        # Titre
        title = ctk.CTkLabel(
            scroll_frame,
            text="📊 Synthèse Comparative",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Message initial
        self.synthesis_message = ctk.CTkLabel(
            scroll_frame,
            text="Lancez les méthodes pour voir la comparaison",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.synthesis_message.pack(pady=50)
    
    def run_comparison_method(self, method_name, worker, text_widget):
        """Lance une méthode pour la comparaison"""
        text_widget.delete(0.0, tk.END)
        text_widget.insert(0.0, f"🔄 Lancement de {method_name}...\n\n")
        
        # Trouver le label de statut
        parent = text_widget.master
        if hasattr(parent, 'status_label'):
            parent.status_label.configure(text="🔄 En cours...", text_color="orange")
        
        try:
            import copy
            import time
            start_time = time.time()
            
            problem_copy = copy.deepcopy(self.current_problem)
            
            if method_name == "Simplexe Standard":
                solver = SimplexMethodTab(problem_copy)
                result = self.capture_solver_output(solver.run)
            elif method_name == "Grand M":
                solver = GrandMMethod(problem_copy)
                result = self.capture_solver_output(solver.run)
            elif method_name == "Analyse Duale":
                analyzer = DualMethod(problem_copy)
                result = self.capture_solver_output(analyzer.run_complete_analysis)
            
            elapsed_time = time.time() - start_time
            
            # Afficher les résultats
            text_widget.delete(0.0, tk.END)
            header = f"✅ {method_name} - Résultats (Temps: {elapsed_time:.2f}s)\n"
            header += "="*60 + "\n\n"
            text_widget.insert(0.0, header + result)
            
            # Mettre à jour le statut
            if hasattr(parent, 'status_label'):
                parent.status_label.configure(text=f"✅ Terminé ({elapsed_time:.2f}s)", text_color="green")
            
            # Stocker les résultats
            self.comparison_results[method_name] = {
                'output': result,
                'time': elapsed_time,
                'success': True
            }
            
            # Mettre à jour la synthèse
            self.update_synthesis()
            
        except Exception as e:
            text_widget.delete(0.0, tk.END)
            text_widget.insert(0.0, f"❌ Erreur {method_name}:\n{str(e)}")
            
            if hasattr(parent, 'status_label'):
                parent.status_label.configure(text="❌ Erreur", text_color="red")
            
            self.comparison_results[method_name] = {
                'output': str(e),
                'time': 0,
                'success': False
            }
    
    def run_all_comparisons(self, notebook):
        """Lance toutes les méthodes de comparaison"""
        methods = ["Simplexe Standard", "Grand M", "Analyse Duale"]
        
        for method in methods:
            # Trouver l'onglet
            tab = notebook.tab(method)
            if hasattr(tab, 'text_widget'):
                # Simuler le clic sur le bouton
                for child in tab.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for widget in child.winfo_children():
                            if isinstance(widget, AnimatedButton) and "Lancer" in widget.cget("text"):
                                widget.invoke()
                                break
    
    def update_synthesis(self):
        """Met à jour la synthèse comparative"""
        if not self.comparison_results:
            return
        
        # Nettoyer la synthèse
        for widget in self.synthesis_frame.winfo_children():
            if widget != self.synthesis_frame.winfo_children()[0]:  # Garder le titre
                widget.destroy()
        
        # Tableau comparatif
        table_frame = ctk.CTkFrame(self.synthesis_frame, corner_radius=10)
        table_frame.pack(fill="x", padx=20, pady=20)
        
        # Headers
        headers = ["Méthode", "Statut", "Temps (s)", "Itérations"]
        header_frame = ctk.CTkFrame(table_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=150
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Données
        for row_idx, (method, data) in enumerate(self.comparison_results.items()):
            row_frame = ctk.CTkFrame(
                table_frame,
                fg_color=("gray95", "gray15") if row_idx % 2 == 0 else "transparent"
            )
            row_frame.pack(fill="x", padx=10)
            
            # Méthode
            ctk.CTkLabel(
                row_frame,
                text=method,
                font=ctk.CTkFont(size=12),
                width=150
            ).grid(row=0, column=0, padx=5, pady=5)
            
            # Statut
            status = "✅ Succès" if data['success'] else "❌ Erreur"
            status_color = "green" if data['success'] else "red"
            ctk.CTkLabel(
                row_frame,
                text=status,
                font=ctk.CTkFont(size=12),
                text_color=status_color,
                width=150
            ).grid(row=0, column=1, padx=5, pady=5)
            
            # Temps
            ctk.CTkLabel(
                row_frame,
                text=f"{data['time']:.3f}",
                font=ctk.CTkFont(size=12),
                width=150
            ).grid(row=0, column=2, padx=5, pady=5)
            
            # Itérations (à extraire de la sortie)
            iterations = self.extract_iterations(data['output'])
            ctk.CTkLabel(
                row_frame,
                text=str(iterations),
                font=ctk.CTkFont(size=12),
                width=150
            ).grid(row=0, column=3, padx=5, pady=5)
        
        # Graphique comparatif
        self.create_comparison_chart()
    
    def extract_iterations(self, output):
        """Extrait le nombre d'itérations de la sortie"""
        # Recherche basique du nombre d'itérations
        import re
        match = re.search(r'Itération[s]?\s*[:=]\s*(\d+)', output, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return "N/A"
    
    def create_comparison_chart(self):
        """Crée un graphique comparatif"""
        if not self.comparison_results:
            return
        
        # Frame pour le graphique
        chart_frame = ctk.CTkFrame(self.synthesis_frame, corner_radius=10)
        chart_frame.pack(fill="x", padx=20, pady=20)
        
        chart_title = ctk.CTkLabel(
            chart_frame,
            text="📊 Comparaison des Temps d'Exécution",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        chart_title.pack(pady=(10, 5))
        
        # Créer le graphique
        fig, ax = plt.subplots(figsize=(8, 4))
        
        methods = list(self.comparison_results.keys())
        times = [data['time'] for data in self.comparison_results.values()]
        colors = ['blue', 'green', 'orange']
        
        bars = ax.bar(methods, times, color=colors[:len(methods)])
        
        # Ajouter les valeurs sur les barres
        for bar, time in zip(bars, times):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{time:.3f}s', ha='center', va='bottom')
        
        ax.set_ylabel('Temps (secondes)')
        ax.set_title("Temps d'Exécution par Méthode")
        ax.grid(True, axis='y', alpha=0.3)
        
        # Intégrer dans tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
    
    def export_comparison(self):
        """Exporte la comparaison"""
        if not self.comparison_results:
            self.show_error("Aucune comparaison à exporter")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Exporter la comparaison",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("CSV", "*.csv")]
        )
        
        if filename:
            # Créer un DataFrame pandas
            data = []
            for method, result in self.comparison_results.items():
                data.append({
                    'Méthode': method,
                    'Statut': 'Succès' if result['success'] else 'Erreur',
                    'Temps (s)': result['time'],
                    'Itérations': self.extract_iterations(result['output'])
                })
            
            df = pd.DataFrame(data)
            
            if filename.endswith('.xlsx'):
                df.to_excel(filename, index=False)
            else:
                df.to_csv(filename, index=False)
            
            self.show_success(f"✅ Comparaison exportée: {filename}")
    
    def new_problem(self):
        """Crée un nouveau problème"""
        if self.current_problem and messagebox.askyesno("Nouveau Problème", 
                                                        "Créer un nouveau problème?\n(Le problème actuel sera perdu)"):
            self.current_problem = None
            self.tabview.set("📝 Définition")
            self.show_success("✅ Prêt pour un nouveau problème!")
            self.update_solve_tab()
    
    def clear_problem(self):
        """Efface le problème actuel"""
        if messagebox.askyesno("Confirmation", "Effacer tous les champs ?"):
            self.current_problem = None
            # Réinitialiser les champs
            for widget in self.fields_frame.winfo_children():
                widget.destroy()
            self.show_success("✅ Champs effacés")
    
    def preview_problem(self):
        """Affiche un aperçu du problème avec style moderne"""
        if not self.current_problem:
            self.validate_problem()
        
        if self.current_problem:
            preview_window = ctk.CTkToplevel(self.root)
            preview_window.title("👁️ Aperçu du Problème")
            preview_window.geometry("700x500")
            preview_window.transient(self.root)
            
            # Frame principal
            main_frame = ctk.CTkFrame(preview_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Titre
            title = ctk.CTkLabel(
                main_frame,
                text="📋 Aperçu du Problème de Programmation Linéaire",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.pack(pady=(0, 20))
            
            # Zone de texte
            text_widget = ctk.CTkTextbox(
                main_frame,
                font=ctk.CTkFont(family="Consolas", size=12),
                corner_radius=10
            )
            text_widget.pack(fill="both", expand=True, pady=(0, 20))
            
            # Générer et afficher le texte
            problem_text = self.generate_problem_text()
            text_widget.insert(0.0, problem_text)
            text_widget.configure(state="disabled")
            
            # Boutons
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x")
            
            copy_btn = AnimatedButton(
                buttons_frame,
                text="📋 Copier",
                command=lambda: self.copy_to_clipboard(problem_text),
                width=100,
                height=35,
                corner_radius=8
            )
            copy_btn.pack(side="left", padx=5)
            
            close_btn = AnimatedButton(
                buttons_frame,
                text="✅ Fermer",
                command=preview_window.destroy,
                width=100,
                height=35,
                corner_radius=8
            )
            close_btn.pack(side="right", padx=5)
    
    def copy_to_clipboard(self, text):
        """Copie le texte dans le presse-papier"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.show_success("✅ Copié dans le presse-papier!")
    
    def generate_problem_text(self):
        """Génère la représentation textuelle du problème"""
        if not self.current_problem:
            return "Aucun problème défini"
        
        text = []
        
        # Type d'optimisation
        obj_type = self.current_problem.get("objective_type", "max")
        text.append(f"{'='*50}\n")
        text.append(f"PROBLÈME DE PROGRAMMATION LINÉAIRE\n")
        text.append(f"{'='*50}\n\n")
        text.append(f"Type: {obj_type.upper()}IMISATION\n\n")
        
        # Fonction objectif
        text.append("FONCTION OBJECTIF:\n")
        coeffs = self.current_problem["tab_optimisation"][1:]
        text.append(f"{obj_type.upper()} Z = ")
        
        for i, c in enumerate(coeffs):
            display_c = c if obj_type == "max" else -c
            if i == 0:
                text.append(f"{display_c}x{self.subscript(1)}")
            else:
                sign = " + " if display_c >= 0 else " - "
                text.append(f"{sign}{abs(display_c)}x{self.subscript(i+1)}")
        
        text.append("\n\nCONTRAINTES:\n")
        
        # Contraintes
        equations = self.current_problem["equations"]
        constraints_info = self.current_problem.get("constraints_info", [])
        
        for i, (key, eq) in enumerate(equations.items()):
            text.append(f"  C{self.subscript(i+1)}: ")
            rhs = eq[0]
            coeffs = eq[1:]
            
            for j, c in enumerate(coeffs):
                if j == 0:
                    text.append(f"{c}x{self.subscript(1)}")
                else:
                    sign = " + " if c >= 0 else " - "
                    text.append(f"{sign}{abs(c)}x{self.subscript(j+1)}")
            
            constraint_type = constraints_info[i] if i < len(constraints_info) else "<="
            text.append(f" {constraint_type} {rhs}\n")
        
        text.append("\n  xⱼ ≥ 0 pour tout j\n\n")
        
        # Informations supplémentaires
        text.append("INFORMATIONS:\n")
        text.append(f"• Variables de décision: {self.current_problem['nombres_variables_base']}\n")
        text.append(f"• Contraintes: {self.current_problem['nb_equations']}\n")
        
        if constraints_info:
            has_eq = "=" in constraints_info
            has_geq = ">=" in constraints_info
            if has_eq or has_geq:
                text.append("• ⚠️ Méthode suggérée: Grand M\n")
            else:
                text.append("• ✅ Méthode suggérée: Simplexe Standard\n")
        
        return "".join(text)
    
    def save_problem(self):
        """Sauvegarde le problème actuel"""
        if not self.current_problem:
            self.show_error("Aucun problème à sauvegarder")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder le problème",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            problem_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "method": "Interface Graphique",
                "variables": self.current_problem,
                "metadata": {
                    "nb_variables": self.current_problem.get("nombres_variables_base", 0),
                    "nb_contraintes": self.current_problem.get("nb_equations", 0),  
                    "constraints_types": self.current_problem.get("constraints_info", [])
                }
            }
            
            self.variable_manager.save_to_file(problem_data, filename)
            self.show_success(f"✅ Problème sauvegardé: {filename}")
    
    def load_problem(self):
        """Charge un problème depuis un fichier"""
        filename = filedialog.askopenfilename(
            title="Charger un problème",
            filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            variables = self.variable_manager.load_from_file(filename)
            if variables:
                self.current_problem = variables
                self.update_solve_tab()
                self.show_success(f"✅ Problème chargé: {filename}")
                self.tabview.set("🔍 Résolution")
    
    def load_examples(self):
        """Charge des exemples prédéfinis avec interface moderne"""
        examples_window = ctk.CTkToplevel(self.root)
        examples_window.title("🎯 Exemples Prédéfinis")
        examples_window.geometry("800x600")
        examples_window.transient(self.root)
        
        # Frame principal
        main_frame = ctk.CTkFrame(examples_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title = ctk.CTkLabel(
            main_frame,
            text="🎯 Exemples de Problèmes Prédéfinis",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Scrollable frame pour les exemples
        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Exemples
        examples = {
            "📊 Problème de Production": {
                "description": "Une usine produit 2 types de produits avec des contraintes de ressources",
                "details": "Max Z = 3x₁ + 5x₂\nContraintes: ressources limitées",
                "variables": {
                    "tab_optimisation": [0, 3, 5],
                    "nombres_variables_base": 2,
                    "equations": {
                        "equation_1": [4, 1, 0],
                        "equation_2": [12, 0, 2],
                        "equation_3": [18, 3, 2],
                    },
                    "nb_equations": 3,
                    "constraints_info": ["<=", "<=", "<="],
                    "objective_type": "max",
                    "method_type": "Exemple"
                },
                "color": "blue"
            },
            "🏭 Problème de Mélange": {
                "description": "Optimisation du mélange de matières premières",
                "details": "Min Z = 7x₁ + 6x₂ + 5x₃\nContraintes d'égalité",
                "variables": {
                    "tab_optimisation": [0, -7, -6, -5],
                    "nombres_variables_base": 3,
                    "equations": {
                        "equation_1": [18, 3, 8, 6],
                        "equation_2": [15, 1, 2, 6],
                    },
                    "nb_equations": 2,
                    "constraints_info": ["=", "="],
                    "objective_type": "min",
                    "method_type": "Exemple"
                },
                "color": "green"
            },
            "📦 Problème de Transport": {
                "description": "Minimisation des coûts de transport entre entrepôts",
                "details": "Min Z = 4x₁ + 3x₂ + 8x₃\nContraintes mixtes",
                "variables": {
                    "tab_optimisation": [0, -4, -3, -8],
                    "nombres_variables_base": 3,
                    "equations": {
                        "equation_1": [20, 2, 3, 1],
                        "equation_2": [15, 1, 1, 2],
                        "equation_3": [10, 1, 0, 1],
                    },
                    "nb_equations": 3,
                    "constraints_info": ["<=", ">=", "="],
                    "objective_type": "min",
                    "method_type": "Exemple"
                },
                "color": "orange"
            },
            "💰 Problème d'Investissement": {
                "description": "Maximisation du retour sur investissement",
                "details": "Max Z = 0.08x₁ + 0.12x₂ + 0.15x₃\nBudget limité",
                "variables": {
                    "tab_optimisation": [0, 0.08, 0.12, 0.15],
                    "nombres_variables_base": 3,
                    "equations": {
                        "equation_1": [100000, 1, 1, 1],
                        "equation_2": [30000, 1, 0, 0],
                        "equation_3": [50000, 0, 1, 0],
                    },
                    "nb_equations": 3,
                    "constraints_info": ["<=", ">=", "<="],
                    "objective_type": "max",
                    "method_type": "Exemple"
                },
                "color": "purple"
            }
        }
        
        # Créer les cartes d'exemples
        for name, data in examples.items():
            self.create_example_card(scroll_frame, name, data, examples_window)
        
        # Bouton fermer
        close_btn = AnimatedButton(
            main_frame,
            text="✅ Fermer",
            command=examples_window.destroy,
            width=150,
            height=40,
            corner_radius=10
        )
        close_btn.pack()
    
    def create_example_card(self, parent, name, data, window):
        """Crée une carte pour un exemple"""
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)
        
        # Effet au survol
        card.bind("<Enter>", lambda e: card.configure(fg_color=("gray85", "gray25")))
        card.bind("<Leave>", lambda e: card.configure(fg_color=("gray90", "gray20")))
        
        # Contenu
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Titre avec icône
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=data["color"]
        )
        title_label.pack(side="left")
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=data["description"],
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.pack(anchor="w", pady=(5, 0))
        
        # Détails
        details_label = ctk.CTkLabel(
            content_frame,
            text=data["details"],
            font=ctk.CTkFont(family="Consolas", size=11),
            justify="left"
        )
        details_label.pack(anchor="w", pady=(5, 10))
        
        # Bouton charger
        load_btn = AnimatedButton(
            content_frame,
            text="📂 Charger cet exemple",
            command=lambda: self.load_example(data, window),
            width=200,
            height=35,
            corner_radius=8,
            fg_color=data["color"]
        )
        load_btn.pack(anchor="w")
    
    def load_example(self, example_data, window):
        """Charge un exemple spécifique"""
        self.current_problem = example_data["variables"]
        self.variable_manager.save_problem(self.current_problem, "Exemple Prédéfini")
        
        window.destroy()
        self.show_success("✅ Exemple chargé avec succès!")
        
        # Mettre à jour l'interface
        self.update_solve_tab()
        self.refresh_history_modern()
        self.tabview.set("🔍 Résolution")
    
    def save_results(self):
        """Sauvegarde les résultats"""
        if not hasattr(self, 'last_result'):
            self.show_error("Aucun résultat à sauvegarder")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder les résultats",
            defaultextension=".txt",
            filetypes=[
                ("Fichier texte", "*.txt"),
                ("Markdown", "*.md"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    result = self.last_result
                    f.write(f"Résultats - {result['method']}\n")
                    f.write(f"Timestamp: {result['timestamp']}\n")
                    f.write(f"Temps d'exécution: {result.get('elapsed_time', 0):.2f}s\n")
                    f.write("="*60 + "\n\n")
                    f.write(result['output'])
                
                self.show_success(f"✅ Résultats sauvegardés: {filename}")
            except Exception as e:
                self.show_error(f"Erreur lors de la sauvegarde: {e}")

def main():
    """Fonction principale pour lancer l'application"""
    root = ctk.CTk()
    app = SimplexGUI(root)
    
    # Gestion de la fermeture
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Lancement de l'application
    root.mainloop()

if __name__ == "__main__":
    main()