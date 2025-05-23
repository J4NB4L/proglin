#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de styles modernes et effets visuels pour tkinter
Améliore considérablement l'apparence des applications tkinter
"""

import tkinter as tk
from tkinter import ttk
import math
import colorsys
from typing import Callable, Tuple, Optional

class ModernTheme:
    """Thème moderne avec palettes de couleurs"""
    
    # Thème sombre par défaut
    DARK = {
        'bg_primary': '#0a0e27',
        'bg_secondary': '#1a1f3a',
        'bg_tertiary': '#252b48',
        'bg_card': '#2d3454',
        'bg_hover': '#3d4464',
        
        'text_primary': '#ffffff',
        'text_secondary': '#b0b9c6',
        'text_disabled': '#6c7293',
        
        'accent': '#00d4ff',
        'accent_hover': '#00a8cc',
        'accent_light': '#66e5ff',
        
        'success': '#00ff88',
        'warning': '#ffa500',
        'danger': '#ff4757',
        'info': '#5f78ff',
        
        'border': '#3d4464',
        'shadow': '#000000'
    }
    
    # Thème clair
    LIGHT = {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f5f7fa',
        'bg_tertiary': '#e9ecef',
        'bg_card': '#ffffff',
        'bg_hover': '#f8f9fa',
        
        'text_primary': '#2c3e50',
        'text_secondary': '#6c757d',
        'text_disabled': '#adb5bd',
        
        'accent': '#007bff',
        'accent_hover': '#0056b3',
        'accent_light': '#80bdff',
        
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        
        'border': '#dee2e6',
        'shadow': 'rgba(0,0,0,0.1)'
    }
    
    @classmethod
    def get_theme(cls, theme_name='dark'):
        """Retourne le thème demandé"""
        return cls.DARK if theme_name == 'dark' else cls.LIGHT


class ModernButton(tk.Frame):
    """Bouton moderne avec animations et effets"""
    
    def __init__(self, parent, text="Button", command=None, 
                 style="primary", width=150, height=40, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.text = text
        self.command = command
        self.style = style
        self.width = width
        self.height = height
        self.theme = ModernTheme.DARK
        
        # État du bouton
        self.is_hovered = False
        self.is_pressed = False
        
        # Créer le canvas
        self.canvas = tk.Canvas(self, width=width, height=height,
                               highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Dessiner le bouton
        self.draw_button()
        
        # Lier les événements
        self.bind_events()
    
    def draw_button(self):
        """Dessine le bouton avec style"""
        self.canvas.delete("all")
        
        # Couleurs selon le style
        if self.style == "primary":
            bg_color = self.theme['accent']
            hover_color = self.theme['accent_hover']
        elif self.style == "success":
            bg_color = self.theme['success']
            hover_color = '#00cc66'
        elif self.style == "danger":
            bg_color = self.theme['danger']
            hover_color = '#cc3545'
        else:
            bg_color = self.theme['bg_tertiary']
            hover_color = self.theme['bg_hover']
        
        # Couleur actuelle
        current_color = hover_color if self.is_hovered else bg_color
        
        # Ombre
        if not self.is_pressed:
            for i in range(3):
                self.canvas.create_rectangle(i+2, i+2, self.width-i, self.height-i,
                                           fill='#00000020', outline='')
        
        # Rectangle principal avec coins arrondis
        self.main_rect = self.create_rounded_rectangle(
            0, 0, self.width-3, self.height-3,
            radius=8, fill=current_color, outline=''
        )
        
        # Texte
        text_y = self.height // 2 + (2 if self.is_pressed else 0)
        self.text_item = self.canvas.create_text(
            self.width // 2, text_y,
            text=self.text,
            font=('Arial', 12, 'bold'),
            fill='white'
        )
        
        # Effet de brillance
        if self.is_hovered and not self.is_pressed:
            self.canvas.create_rectangle(
                10, 5, self.width-13, 15,
                fill='#ffffff30', outline=''
            )
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Crée un rectangle avec coins arrondis"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y2 - radius),
                     (x1 + radius, y2), (x2 - radius, y2),
                     (x2, y2 - radius), (x2, y1 + radius),
                     (x2 - radius, y1), (x1 + radius, y1)]:
            points.extend([x, y])
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def bind_events(self):
        """Lie les événements d'interaction"""
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
    
    def on_enter(self, event):
        """Effet au survol"""
        self.is_hovered = True
        self.draw_button()
        self.animate_hover()
    
    def on_leave(self, event):
        """Effet quand la souris quitte"""
        self.is_hovered = False
        self.draw_button()
    
    def on_press(self, event):
        """Effet au clic"""
        self.is_pressed = True
        self.draw_button()
    
    def on_release(self, event):
        """Effet au relâchement"""
        self.is_pressed = False
        self.draw_button()
        
        if self.command and self.is_hovered:
            self.animate_click()
            self.after(150, self.command)
    
    def animate_hover(self):
        """Animation au survol"""
        # Effet de pulsation subtile
        def pulse(scale=1.0, growing=True):
            if not self.is_hovered:
                return
            
            new_scale = scale + 0.01 if growing else scale - 0.01
            
            if new_scale > 1.05:
                growing = False
            elif new_scale < 1.0:
                growing = True
            
            # Redimensionner légèrement
            self.canvas.scale("all", self.width/2, self.height/2, new_scale, new_scale)
            
            self.after(50, lambda: pulse(new_scale, growing))
        
        pulse()
    
    def animate_click(self):
        """Animation au clic"""
        # Effet d'onde
        circle = self.canvas.create_oval(
            self.width/2 - 5, self.height/2 - 5,
            self.width/2 + 5, self.height/2 + 5,
            outline=self.theme['accent_light'], width=2
        )
        
        def expand(size=10):
            if size < max(self.width, self.height):
                self.canvas.coords(circle,
                    self.width/2 - size, self.height/2 - size,
                    self.width/2 + size, self.height/2 + size
                )
                
                # Fade out
                opacity = int(255 * (1 - size/max(self.width, self.height)))
                color = f'#{opacity:02x}d4ff'
                self.canvas.itemconfig(circle, outline=color)
                
                self.after(20, lambda: expand(size + 5))
            else:
                self.canvas.delete(circle)
        
        expand()


class ModernEntry(tk.Frame):
    """Champ de saisie moderne avec animations"""
    
    def __init__(self, parent, placeholder="", width=250, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.placeholder = placeholder
        self.width = width
        self.theme = ModernTheme.DARK
        
        # Créer le frame conteneur
        self.configure(bg=self.theme['bg_tertiary'])
        
        # Ligne de focus animée
        self.focus_line = tk.Frame(self, height=2, bg=self.theme['border'])
        self.focus_line.pack(side='bottom', fill='x')
        
        # Entry widget
        self.entry = tk.Entry(self,
                             font=('Arial', 11),
                             bg=self.theme['bg_tertiary'],
                             fg=self.theme['text_primary'],
                             bd=0,
                             insertbackground=self.theme['accent'])
        self.entry.pack(fill='both', expand=True, padx=10, pady=8)
        
        # Placeholder
        self.show_placeholder()
        
        # Événements
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyRelease>', self.on_key_release)
    
    def show_placeholder(self):
        """Affiche le placeholder"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.theme['text_disabled'])
    
    def hide_placeholder(self):
        """Cache le placeholder"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, 'end')
            self.entry.config(fg=self.theme['text_primary'])
    
    def on_focus_in(self, event):
        """Animation à la prise de focus"""
        self.hide_placeholder()
        self.animate_focus_line(True)
    
    def on_focus_out(self, event):
        """Animation à la perte de focus"""
        self.show_placeholder()
        self.animate_focus_line(False)
    
    def on_key_release(self, event):
        """Validation en temps réel"""
        # Peut être étendu pour la validation
        pass
    
    def animate_focus_line(self, focused):
        """Anime la ligne de focus"""
        target_color = self.theme['accent'] if focused else self.theme['border']
        target_height = 3 if focused else 2
        
        def transition(step=0):
            if step <= 10:
                # Interpolation de couleur
                if focused:
                    # Animation d'expansion du centre
                    progress = step / 10
                    self.focus_line.config(height=target_height)
                    
                    # Créer un gradient (simulation)
                    color = self.theme['accent'] if step > 5 else self.theme['border']
                    self.focus_line.config(bg=color)
                else:
                    self.focus_line.config(bg=target_color, height=target_height)
                
                self.after(20, lambda: transition(step + 1))
        
        transition()
    
    def get(self):
        """Retourne la valeur (sans placeholder)"""
        value = self.entry.get()
        return "" if value == self.placeholder else value
    
    def set(self, value):
        """Définit la valeur"""
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)
        self.entry.config(fg=self.theme['text_primary'])


class AnimatedProgressBar(tk.Canvas):
    """Barre de progression animée moderne"""
    
    def __init__(self, parent, width=400, height=8, **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bd=0, **kwargs)
        
        self.width = width
        self.height = height
        self.theme = ModernTheme.DARK
        self.progress = 0
        self.is_indeterminate = False
        
        # Fond
        self.create_rectangle(0, 0, width, height,
                            fill=self.theme['bg_secondary'], outline='')
        
        # Barre de progression
        self.progress_bar = self.create_rectangle(0, 0, 0, height,
                                                fill=self.theme['accent'], outline='')
        
        # Particules
        self.particles = []
    
    def set_progress(self, value):
        """Définit la progression (0-100)"""
        self.progress = max(0, min(100, value))
        self.animate_progress()
    
    def animate_progress(self):
        """Anime la barre vers la nouvelle valeur"""
        current_width = self.coords(self.progress_bar)[2]
        target_width = (self.progress / 100) * self.width
        
        def move(step=0):
            if step <= 20:
                # Easing function
                t = step / 20
                t = t * t * (3.0 - 2.0 * t)  # smoothstep
                
                new_width = current_width + (target_width - current_width) * t
                self.coords(self.progress_bar, 0, 0, new_width, self.height)
                
                # Ajouter des particules
                if step % 4 == 0 and self.progress > 0:
                    self.add_particle(new_width)
                
                self.after(20, lambda: move(step + 1))
        
        move()
    
    def add_particle(self, x):
        """Ajoute une particule brillante"""
        particle = self.create_oval(x-2, self.height//2-2,
                                   x+2, self.height//2+2,
                                   fill=self.theme['accent_light'], outline='')
        self.particles.append(particle)
        
        # Animer la particule
        def animate_particle(p=particle, offset=0):
            if p in self.particles:
                # Mouvement et fade
                self.move(p, 2, 0)
                offset += 2
                
                if offset < 50:
                    # Fade out
                    opacity = int(255 * (1 - offset/50))
                    color = f'#{opacity:02x}d4ff'
                    self.itemconfig(p, fill=color)
                    
                    self.after(30, lambda: animate_particle(p, offset))
                else:
                    self.delete(p)
                    self.particles.remove(p)
        
        animate_particle()
    
    def start_indeterminate(self):
        """Démarre l'animation indéterminée"""
        self.is_indeterminate = True
        self.animate_indeterminate()
    
    def stop_indeterminate(self):
        """Arrête l'animation indéterminée"""
        self.is_indeterminate = False
    
    def animate_indeterminate(self):
        """Animation de progression indéterminée"""
        if not self.is_indeterminate:
            return
        
        # Créer une onde qui traverse la barre
        wave_width = 100
        
        def move_wave(pos=0):
            if not self.is_indeterminate:
                return
            
            # Effacer l'ancienne onde
            self.coords(self.progress_bar, pos, 0, pos + wave_width, self.height)
            
            # Gradient (simulation)
            for i in range(5):
                opacity = int(255 * (1 - i/5))
                color = f'#{opacity:02x}d4ff'
                
                rect = self.create_rectangle(
                    pos + i*20, 0, pos + (i+1)*20, self.height,
                    fill=color, outline=''
                )
                self.after(50, lambda r=rect: self.delete(r))
            
            # Continuer le mouvement
            new_pos = pos + 5
            if new_pos > self.width:
                new_pos = -wave_width
            
            self.after(20, lambda: move_wave(new_pos))
        
        move_wave()


class FloatingCard(tk.Toplevel):
    """Carte flottante avec ombre et animations"""
    
    def __init__(self, parent, title="", content="", width=300, height=200):
        super().__init__(parent)
        
        self.title_text = title
        self.content_text = content
        self.theme = ModernTheme.DARK
        
        # Configuration de la fenêtre
        self.overrideredirect(True)  # Sans bordure
        self.geometry(f"{width}x{height}")
        self.configure(bg=self.theme['shadow'])
        
        # Transparence (Windows)
        self.attributes('-alpha', 0.0)
        
        # Frame principal avec ombre
        self.main_frame = tk.Frame(self, bg=self.theme['bg_card'])
        self.main_frame.place(x=5, y=5, width=width-10, height=height-10)
        
        # En-tête
        header = tk.Frame(self.main_frame, bg=self.theme['accent'], height=40)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Titre
        tk.Label(header, text=title, font=('Arial', 12, 'bold'),
                bg=self.theme['accent'], fg='white').pack(side='left', padx=15, pady=10)
        
        # Bouton fermer
        close_btn = tk.Label(header, text="✕", font=('Arial', 14),
                           bg=self.theme['accent'], fg='white', cursor='hand2')
        close_btn.pack(side='right', padx=15)
        close_btn.bind('<Button-1>', lambda e: self.close_animated())
        
        # Contenu
        content_frame = tk.Frame(self.main_frame, bg=self.theme['bg_card'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        tk.Label(content_frame, text=content, font=('Arial', 10),
                bg=self.theme['bg_card'], fg=self.theme['text_primary'],
                justify='left', wraplength=width-40).pack()
        
        # Positionner près du parent
        self.position_near_parent(parent)
        
        # Animation d'ouverture
        self.open_animated()
    
    def position_near_parent(self, parent):
        """Positionne la carte près du widget parent"""
        parent.update_idletasks()
        x = parent.winfo_rootx() + parent.winfo_width() + 10
        y = parent.winfo_rooty()
        self.geometry(f"+{x}+{y}")
    
    def open_animated(self):
        """Animation d'ouverture avec fade in"""
        def fade_in(alpha=0.0):
            if alpha < 0.95:
                self.attributes('-alpha', alpha)
                self.after(20, lambda: fade_in(alpha + 0.05))
        
        fade_in()
    
    def close_animated(self):
        """Animation de fermeture avec fade out"""
        def fade_out(alpha=0.95):
            if alpha > 0.0:
                self.attributes('-alpha', alpha)
                self.after(20, lambda: fade_out(alpha - 0.05))
            else:
                self.destroy()
        
        fade_out()


class ModernTooltip:
    """Tooltip moderne avec animations"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        
        self.widget.bind('<Enter>', self.on_enter)
        self.widget.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event):
        """Affiche le tooltip après un délai"""
        self.show_timer = self.widget.after(500, self.show_tooltip)
    
    def on_leave(self, event):
        """Cache le tooltip"""
        if hasattr(self, 'show_timer'):
            self.widget.after_cancel(self.show_timer)
        
        if self.tooltip:
            self.tooltip.close_animated()
            self.tooltip = None
    
    def show_tooltip(self):
        """Affiche le tooltip animé"""
        if not self.tooltip:
            self.tooltip = FloatingCard(self.widget, "Info", self.text, 250, 100)


# Fonction utilitaire pour appliquer le thème moderne à toute l'application
def apply_modern_theme(root, theme_name='dark'):
    """Applique le thème moderne à toute l'application"""
    theme = ModernTheme.get_theme(theme_name)
    
    # Configuration de base
    root.configure(bg=theme['bg_primary'])
    
    # Style ttk
    style = ttk.Style()
    style.theme_use('clam')
    
    # Personnaliser tous les widgets ttk
    style.configure('TLabel', background=theme['bg_primary'], 
                   foreground=theme['text_primary'])
    style.configure('TFrame', background=theme['bg_primary'])
    style.configure('TButton', background=theme['accent'],
                   foreground='white', borderwidth=0)
    style.map('TButton', background=[('active', theme['accent_hover'])])
    
    # Ajouter des méthodes d'animation au root
    root.theme = theme
    
    return theme


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer une fenêtre de démonstration
    demo = tk.Tk()
    demo.title("Démonstration des styles modernes")
    demo.geometry("600x500")
    
    # Appliquer le thème
    theme = apply_modern_theme(demo, 'dark')
    
    # Frame principal
    main_frame = tk.Frame(demo, bg=theme['bg_primary'])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Titre
    tk.Label(main_frame, text="Composants Modernes", 
            font=('Arial', 20, 'bold'),
            bg=theme['bg_primary'], 
            fg=theme['text_primary']).pack(pady=(0, 20))
    
    # Boutons
    btn_frame = tk.Frame(main_frame, bg=theme['bg_primary'])
    btn_frame.pack(pady=10)
    
    ModernButton(btn_frame, "Primary", style="primary").pack(side='left', padx=5)
    ModernButton(btn_frame, "Success", style="success").pack(side='left', padx=5)
    ModernButton(btn_frame, "Danger", style="danger").pack(side='left', padx=5)
    
    # Entries
    ModernEntry(main_frame, placeholder="Entrez votre nom").pack(pady=10)
    ModernEntry(main_frame, placeholder="Email").pack(pady=10)
    
    # Progress bar
    progress = AnimatedProgressBar(main_frame)
    progress.pack(pady=20)
    
    # Animer la progression
    def animate_demo():
        import random
        progress.set_progress(random.randint(20, 80))
        demo.after(2000, animate_demo)
    
    animate_demo()
    
    # Tooltip
    label_with_tooltip = tk.Label(main_frame, text="Survolez-moi pour voir le tooltip",
                                 bg=theme['bg_secondary'], fg=theme['text_primary'],
                                 padx=20, pady=10)
    label_with_tooltip.pack(pady=20)
    
    ModernTooltip(label_with_tooltip, "Ceci est un tooltip moderne avec animations!")
    
    demo.mainloop()