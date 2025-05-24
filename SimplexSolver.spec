# SimplexSolver.spec
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Liste des modules à inclure
added_files = [
    ('tab_method.py', '.'),
    ('variables.py', '.'),
    ('grand_M_method.py', '.'),
    ('dual_method.py', '.'),
    ('enhanced_variables.py', '.'),
    ('gui.py', '.'),
    # Ajoutez d'autres fichiers nécessaires
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        # Tkinter et CustomTkinter
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.font',
        'customtkinter',

        # Matplotlib
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.patches',
        'matplotlib.animation',
        
        # Plotly - IMPORTANT pour résoudre l'erreur
        'plotly',
        'plotly.graph_objects',
        'plotly.graph_objs',
        'plotly.graph_objs._scatter',
        'plotly.graph_objs._bar',
        'plotly.graph_objs._line',
        'plotly.express',
        'plotly.subplots',
        'plotly.offline',
        'plotly.io',
        'plotly.validators',
        'plotly.colors',
        
        # Data processing
        'numpy',
        'pandas',
        'seaborn',
        
        # System et utilitaires
        'json',
        'os',
        'sys',
        'io',
        'base64',
        'datetime',
        'threading',
        'copy',
        'math',
        'time',
        'random',
        'webbrowser',
        'typing',
        
        # Image processing
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        
        # PDF generation
        'reportlab',
        'reportlab.lib',
        'reportlab.lib.colors',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        
        # Console formatting
        'colorama',
        'tabulate'
    ]+ collect_submodules('plotly'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pysqlite2',
        'MySQLdb', 
        'psycopg2'
    ],
    collect_all=['plotly'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SimplexSolver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False pour cacher la console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' 
)