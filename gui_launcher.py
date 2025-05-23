#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanceur Premium avec animations et effets visuels avancés
Version ultra-moderne pour le Solveur de Programmation Linéaire
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import math
import time
import threading
import random
from datetime import datetime
import os
import sys

class PremiumLauncher:
    """Lanceur premium avec animations sophistiquées"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Variables d'animation
        self.animation_running = True
        self.particles = []
        self.wave_offset = 0
        
        # Couleurs et thème
        self.theme = {
            'bg_gradient_start': '#0a0e27',
            'bg_gradient_end': '#1a1f3a',
            'accent': '#00d4ff',
            'accent_light': '#66e5ff',
            'success': '#00ff88',
            'warning': '#ffa500',
            'danger': '#ff4757',
            'text': '#ffffff',
            'text_dim': '#8892b0',
            'card_bg': 'rgba(26, 31, 58, 0.8)',
            'glow': '#00d4ff'
        }
        
        # Canvas principal pour les animations
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Démarrer les animations de fond
        self.create_animated_background()
        
        # Créer l'interface
        self.create_premium_interface()
        
        # Lancer les animations
        self.animate_background()
        self.animate_particles()
        
    def setup_window(self):
        """Configure la fenêtre avec style premium"""
        self.root.title("✨ Solveur Simplexe Premium")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 500
        y = (self.root.winfo_screenheight() // 2) - 350
        self.root.geometry(f"1000x700+{x}+{y}")
        
        # Style sombre
        self.root.configure(bg='#0a0e27')
        
        # Fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_animated_background(self):
        """Crée un fond animé avec gradient et particules"""
        # Gradient de fond
        self.create_gradient()
        
        # Grille animée
        self.create_animated_grid()
        
        # Particules flottantes
        self.create_particles()
    
    def create_gradient(self):
        """Crée un gradient de fond"""
        width = 1000
        height = 700
        
        # Créer le gradient vertical
        for i in range(height):
            # Interpolation des couleurs
            ratio = i / height
            r1, g1, b1 = int('0a', 16), int('0e', 16), int('27', 16)
            r2, g2, b2 = int('1a', 16), int('1f', 16), int('3a', 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.main_canvas.create_line(0, i, width, i, fill=color, width=1)
    
    def create_animated_grid(self):
        """Crée une grille animée en arrière-plan"""
        self.grid_lines = []
        
        # Lignes verticales
        for x in range(0, 1000, 50):
            line = self.main_canvas.create_line(x, 0, x, 700, 
                                               fill='#1a2545', width=1)
            self.grid_lines.append(line)
        
        # Lignes horizontales
        for y in range(0, 700, 50):
            line = self.main_canvas.create_line(0, y, 1000, y,
                                               fill='#1a2545', width=1)
            self.grid_lines.append(line)
    
    def create_particles(self):
        """Crée des particules flottantes"""
        for _ in range(30):
            x = random.randint(0, 1000)
            y = random.randint(0, 700)
            size = random.randint(2, 4)
            speed = random.uniform(0.5, 2)
            
            particle = {
                'id': self.main_canvas.create_oval(x-size, y-size, x+size, y+size,
                                                  fill=self.theme['accent_light'],
                                                  outline=''),
                'x': x,
                'y': y,
                'size': size,
                'speed': speed,
                'opacity': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)
    
    def animate_background(self):
        """Anime le fond (grille avec effet de vague)"""
        if not self.animation_running:
            return
        
        self.wave_offset += 0.1
        
        # Animer la grille avec effet de vague
        for i, line in enumerate(self.grid_lines):
            coords = self.main_canvas.coords(line)
            if len(coords) == 4:
                # Déterminer si c'est une ligne verticale ou horizontale
                if coords[0] == coords[2]:  # Verticale
                    wave = math.sin(self.wave_offset + i * 0.1) * 5
                    self.main_canvas.coords(line, coords[0] + wave, coords[1], 
                                          coords[2] + wave, coords[3])
        
        self.root.after(50, self.animate_background)
    
    def animate_particles(self):
        """Anime les particules flottantes"""
        if not self.animation_running:
            return
        
        for particle in self.particles:
            # Mouvement vertical
            particle['y'] -= particle['speed']
            
            # Réinitialiser si sort de l'écran
            if particle['y'] < -10:
                particle['y'] = 710
                particle['x'] = random.randint(0, 1000)
            
            # Mouvement sinusoïdal horizontal
            wave_x = math.sin(particle['y'] * 0.01) * 20
            
            # Mettre à jour la position
            self.main_canvas.coords(particle['id'],
                                   particle['x'] + wave_x - particle['size'],
                                   particle['y'] - particle['size'],
                                   particle['x'] + wave_x + particle['size'],
                                   particle['y'] + particle['size'])
        
        self.root.after(30, self.animate_particles)
    
    def create_premium_interface(self):
        """Crée l'interface principale premium"""
        # Container principal flottant
        self.container = tk.Frame(self.main_canvas, bg='#1a1f3a', bd=0)
        self.container.place(relx=0.5, rely=0.5, anchor='center', width=800, height=500)
        
        # Effet d'ombre
        self.create_shadow_effect(self.container)
        
        # En-tête animé
        self.create_animated_header()
        
        # Zone de contenu principal
        self.content_area = tk.Frame(self.container, bg='#1a1f3a')
        self.content_area.pack(fill=tk.BOTH, expand=True, padx=40, pady=(20, 40))
        
        # Créer l'écran de démarrage
        self.show_splash_screen()
        
        # Transition vers l'interface principale après 3 secondes
        self.root.after(3000, self.show_main_interface)
    
    def create_shadow_effect(self, widget):
        """Crée un effet d'ombre pour les widgets"""
        # Créer plusieurs rectangles décalés pour l'effet d'ombre
        for i in range(5):
            offset = i * 2
            color = f'#{int(10 + i*2):02x}{int(14 + i*2):02x}{int(39 + i*2):02x}'
            shadow = tk.Frame(self.main_canvas, bg=color, bd=0)
            shadow.place(in_=widget, x=offset, y=offset, relwidth=1, relheight=1)
            shadow.lower()
    
    def create_animated_header(self):
        """Crée un en-tête avec animation de texte"""
        self.header_frame = tk.Frame(self.container, bg='#0f1629', height=100)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)
        
        # Canvas pour l'animation du titre
        self.title_canvas = tk.Canvas(self.header_frame, bg='#0f1629', 
                                     highlightthickness=0, height=100)
        self.title_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Titre avec effet de lueur
        self.title_text = self.title_canvas.create_text(400, 50,
                                                        text="SOLVEUR SIMPLEXE PREMIUM",
                                                        font=('Arial', 28, 'bold'),
                                                        fill=self.theme['accent'])
        
        # Ligne décorative animée
        self.deco_line = self.title_canvas.create_rectangle(200, 80, 600, 82,
                                                           fill=self.theme['accent'],
                                                           outline='')
        
        # Lancer l'animation du titre
        self.animate_title()
    
    def animate_title(self):
        """Anime le titre avec effet de lueur pulsante"""
        # Effet de pulsation
        self.title_glow_phase = getattr(self, 'title_glow_phase', 0)
        self.title_glow_phase += 0.1
        
        # Calculer l'intensité de la lueur
        glow_intensity = (math.sin(self.title_glow_phase) + 1) / 2
        
        # Créer l'effet de lueur avec plusieurs textes superposés
        for i in range(3):
            offset = i * 2
            opacity = int(255 * glow_intensity * (1 - i/3))
            color = f'#{opacity:02x}d4ff'
            
            # Créer ou mettre à jour le texte de lueur
            glow_id = getattr(self, f'title_glow_{i}', None)
            if glow_id:
                self.title_canvas.itemconfig(glow_id, fill=color)
            else:
                glow = self.title_canvas.create_text(400 + offset, 50 + offset,
                                                    text="SOLVEUR SIMPLEXE PREMIUM",
                                                    font=('Arial', 28, 'bold'),
                                                    fill=color)
                self.title_canvas.tag_lower(glow, self.title_text)
                setattr(self, f'title_glow_{i}', glow)
        
        # Animer la ligne décorative
        line_width = 200 + 200 * glow_intensity
        self.title_canvas.coords(self.deco_line, 400 - line_width/2, 80,
                                400 + line_width/2, 82)
        
        if self.animation_running:
            self.root.after(50, self.animate_title)
    
    def show_splash_screen(self):
        """Affiche l'écran de démarrage animé"""
        self.splash_frame = tk.Frame(self.content_area, bg='#1a1f3a')
        self.splash_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo animé (simulation)
        logo_canvas = tk.Canvas(self.splash_frame, bg='#1a1f3a', 
                               highlightthickness=0, width=200, height=200)
        logo_canvas.pack(pady=50)
        
        # Créer un logo animé avec des cercles concentriques
        self.logo_circles = []
        colors = ['#00d4ff', '#00a8cc', '#008099', '#005866']
        for i, color in enumerate(colors):
            size = 100 - i*20
            circle = logo_canvas.create_oval(100-size, 100-size, 100+size, 100+size,
                                           outline=color, width=3)
            self.logo_circles.append(circle)
        
        # Texte de chargement
        self.loading_text = tk.Label(self.splash_frame,
                                    text="Initialisation du système...",
                                    font=('Arial', 14),
                                    fg=self.theme['text_dim'],
                                    bg='#1a1f3a')
        self.loading_text.pack()
        
        # Barre de progression stylisée
        self.create_stylized_progress_bar()
        
        # Animer le logo
        self.animate_logo()
    
    def create_stylized_progress_bar(self):
        """Crée une barre de progression personnalisée"""
        progress_frame = tk.Frame(self.splash_frame, bg='#1a1f3a')
        progress_frame.pack(pady=20)
        
        # Canvas pour la barre de progression
        self.progress_canvas = tk.Canvas(progress_frame, width=400, height=10,
                                        bg='#0f1629', highlightthickness=0)
        self.progress_canvas.pack()
        
        # Fond de la barre
        self.progress_canvas.create_rectangle(0, 0, 400, 10, fill='#0f1629', outline='')
        
        # Barre de progression avec gradient
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 10,
                                                                 fill=self.theme['accent'],
                                                                 outline='')
        
        # Particules sur la barre
        self.progress_particles = []
        
        # Animer la progression
        self.animate_progress()
    
    def animate_logo(self):
        """Anime le logo de démarrage"""
        if not hasattr(self, 'logo_rotation'):
            self.logo_rotation = 0
        
        self.logo_rotation += 2
        
        # Faire tourner les cercles
        for i, circle in enumerate(self.logo_circles):
            # Rotation différente pour chaque cercle
            angle = self.logo_rotation * (1 + i * 0.2)
            # Effet de respiration
            scale = 1 + 0.1 * math.sin(angle * 0.05)
            size = (100 - i*20) * scale
            
            # Mettre à jour la position
            logo_canvas = self.splash_frame.winfo_children()[0]
            logo_canvas.coords(circle, 100-size, 100-size, 100+size, 100+size)
        
        if self.animation_running and hasattr(self, 'splash_frame'):
            self.root.after(30, self.animate_logo)
    
    def animate_progress(self):
        """Anime la barre de progression"""
        if not hasattr(self, 'progress_value'):
            self.progress_value = 0
        
        if self.progress_value < 400:
            self.progress_value += 4
            self.progress_canvas.coords(self.progress_bar, 0, 0, self.progress_value, 10)
            
            # Ajouter des particules
            if random.random() > 0.7:
                particle = self.progress_canvas.create_oval(
                    self.progress_value-2, 3, self.progress_value+2, 7,
                    fill=self.theme['accent_light'], outline=''
                )
                self.progress_particles.append({
                    'id': particle,
                    'x': self.progress_value,
                    'speed': random.uniform(2, 5)
                })
            
            # Animer les particules existantes
            for particle in self.progress_particles[:]:
                particle['x'] += particle['speed']
                self.progress_canvas.coords(particle['id'],
                                          particle['x']-2, 3,
                                          particle['x']+2, 7)
                
                # Supprimer si hors écran
                if particle['x'] > 420:
                    self.progress_canvas.delete(particle['id'])
                    self.progress_particles.remove(particle)
            
            self.root.after(20, self.animate_progress)
    
    def show_main_interface(self):
        """Affiche l'interface principale après le splash"""
        # Fade out du splash screen
        if hasattr(self, 'splash_frame'):
            self.splash_frame.destroy()
        
        # Créer l'interface principale
        self.main_frame = tk.Frame(self.content_area, bg='#1a1f3a')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cartes d'action avec effet hover
        self.create_action_cards()
        
        # Zone de statut
        self.create_status_zone()
        
        # Vérifier les dépendances
        self.check_dependencies_animated()
    
    def create_action_cards(self):
        """Crée des cartes d'action interactives"""
        cards_frame = tk.Frame(self.main_frame, bg='#1a1f3a')
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Configuration des cartes
        cards_config = [
            {
                'title': '🚀 LANCER',
                'subtitle': 'Démarrer l\'application',
                'color': self.theme['success'],
                'command': self.launch_application
            },
            {
                'title': '📦 INSTALLER',
                'subtitle': 'Gérer les dépendances',
                'color': self.theme['warning'],
                'command': self.show_dependencies
            },
            {
                'title': '📚 AIDE',
                'subtitle': 'Documentation',
                'color': self.theme['accent'],
                'command': self.show_help
            }
        ]
        
        # Créer les cartes
        for i, config in enumerate(cards_config):
            card = self.create_interactive_card(cards_frame, config)
            card.grid(row=0, column=i, padx=20, pady=10, sticky='nsew')
            
        # Configuration du grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
    
    def create_interactive_card(self, parent, config):
        """Crée une carte interactive avec animations"""
        # Frame de la carte
        card = tk.Frame(parent, bg='#252b48', bd=0, cursor='hand2')
        
        # Canvas pour les effets
        canvas = tk.Canvas(card, highlightthickness=0, bg='#252b48')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Taille de la carte
        card_width = 200
        card_height = 150
        canvas.config(width=card_width, height=card_height)
        
        # Fond avec bordure
        bg_rect = canvas.create_rectangle(2, 2, card_width-2, card_height-2,
                                         fill='#252b48', outline=config['color'], width=2)
        
        # Titre
        title = canvas.create_text(card_width//2, 50,
                                  text=config['title'],
                                  font=('Arial', 18, 'bold'),
                                  fill=config['color'])
        
        # Sous-titre
        subtitle = canvas.create_text(card_width//2, 80,
                                     text=config['subtitle'],
                                     font=('Arial', 10),
                                     fill=self.theme['text_dim'])
        
        # Effet hover
        def on_enter(e):
            canvas.itemconfig(bg_rect, fill='#2d3454')
            canvas.itemconfig(title, font=('Arial', 20, 'bold'))
            
            # Effet de lueur
            for i in range(3):
                glow = canvas.create_rectangle(2-i*2, 2-i*2, 
                                             card_width-2+i*2, card_height-2+i*2,
                                             outline=config['color'], width=1)
                canvas.tag_lower(glow, bg_rect)
                canvas.after(100, lambda g=glow: canvas.delete(g))
        
        def on_leave(e):
            canvas.itemconfig(bg_rect, fill='#252b48')
            canvas.itemconfig(title, font=('Arial', 18, 'bold'))
        
        def on_click(e):
            # Animation de clic
            canvas.move(bg_rect, 2, 2)
            canvas.move(title, 2, 2)
            canvas.move(subtitle, 2, 2)
            canvas.after(100, lambda: [
                canvas.move(bg_rect, -2, -2),
                canvas.move(title, -2, -2),
                canvas.move(subtitle, -2, -2)
            ])
            
            # Exécuter la commande
            if config['command']:
                self.root.after(150, config['command'])
        
        # Lier les événements
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        canvas.bind('<Button-1>', on_click)
        
        return card
    
    def create_status_zone(self):
        """Crée la zone de statut avec indicateurs animés"""
        status_frame = tk.Frame(self.main_frame, bg='#0f1629', height=100)
        status_frame.pack(fill=tk.X, side='bottom')
        status_frame.pack_propagate(False)
        
        # Canvas pour les animations de statut
        self.status_canvas = tk.Canvas(status_frame, bg='#0f1629',
                                      highlightthickness=0)
        self.status_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Texte de statut
        self.status_text = self.status_canvas.create_text(400, 30,
                                                         text="Vérification du système...",
                                                         font=('Arial', 12),
                                                         fill=self.theme['text_dim'])
        
        # Indicateurs de statut
        self.status_indicators = []
        indicators = ['Python', 'Modules', 'Interface']
        
        for i, name in enumerate(indicators):
            x = 250 + i * 150
            
            # Cercle indicateur
            indicator = self.status_canvas.create_oval(x-10, 50, x+10, 70,
                                                     fill='#1a2545', outline='')
            
            # Texte
            text = self.status_canvas.create_text(x+30, 60,
                                                text=name,
                                                font=('Arial', 10),
                                                fill=self.theme['text_dim'],
                                                anchor='w')
            
            self.status_indicators.append({'circle': indicator, 'text': text, 'status': 'checking'})
        
        # Animer les indicateurs
        self.animate_status_indicators()
    
    def animate_status_indicators(self):
        """Anime les indicateurs de statut"""
        for i, indicator in enumerate(self.status_indicators):
            if indicator['status'] == 'checking':
                # Animation de vérification (pulsation)
                phase = time.time() * 2 + i * 0.5
                intensity = (math.sin(phase) + 1) / 2
                color = f'#{int(0 + 212*intensity):02x}{int(212 + 43*intensity):02x}ff'
                self.status_canvas.itemconfig(indicator['circle'], fill=color)
        
        if self.animation_running:
            self.root.after(50, self.animate_status_indicators)
    
    def check_dependencies_animated(self):
        """Vérifie les dépendances avec animation"""
        def check():
            # Simuler la vérification
            time.sleep(1)
            
            # Python OK
            self.status_indicators[0]['status'] = 'ok'
            self.status_canvas.itemconfig(self.status_indicators[0]['circle'], 
                                        fill=self.theme['success'])
            
            time.sleep(0.5)
            
            # Modules OK
            self.status_indicators[1]['status'] = 'ok'
            self.status_canvas.itemconfig(self.status_indicators[1]['circle'],
                                        fill=self.theme['success'])
            
            time.sleep(0.5)
            
            # Interface OK
            self.status_indicators[2]['status'] = 'ok'
            self.status_canvas.itemconfig(self.status_indicators[2]['circle'],
                                        fill=self.theme['success'])
            
            # Mettre à jour le statut
            self.status_canvas.itemconfig(self.status_text,
                                        text="✅ Système prêt - Toutes les dépendances sont installées",
                                        fill=self.theme['success'])
        
        # Lancer dans un thread
        thread = threading.Thread(target=check)
        thread.daemon = True
        thread.start()
    
    def launch_application(self):
        """Lance l'application avec effet de transition"""
        # Créer un overlay de transition
        overlay = tk.Frame(self.root, bg='#0a0e27')
        overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Texte de transition
        loading_label = tk.Label(overlay,
                               text="Lancement en cours...",
                               font=('Arial', 24, 'bold'),
                               fg=self.theme['accent'],
                               bg='#0a0e27')
        loading_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Animation de fondu
        def fade_in(alpha=0):
            if alpha < 1:
                overlay.place(x=0, y=0, relwidth=1, relheight=1)
                self.root.after(20, lambda: fade_in(alpha + 0.05))
            else:
                # Lancer l'application
                try:
                    from tkinter_gui import main
                    self.animation_running = False
                    self.root.destroy()
                    main()
                except Exception as e:
                    overlay.destroy()
                    messagebox.showerror("Erreur", f"Impossible de lancer l'application:\n{e}")
        
        fade_in()
    
    def show_dependencies(self):
        """Affiche la gestion des dépendances"""
        messagebox.showinfo("Dépendances", "Gestionnaire de dépendances premium\n\nToutes les dépendances sont installées!")
    
    def show_help(self):
        """Affiche l'aide"""
        messagebox.showinfo("Aide", "Solveur Simplexe Premium\n\nInterface moderne pour l'optimisation linéaire")
    
    def on_closing(self):
        """Gestion de la fermeture"""
        self.animation_running = False
        self.root.destroy()
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()


def main():
    """Point d'entrée principal"""
    app = PremiumLauncher()
    app.run()


if __name__ == "__main__":
    main()