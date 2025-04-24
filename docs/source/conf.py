# Configuration file for the Sphinx documentation builder.

import os
import sys

# Añade el path raíz del proyecto para que 'app' sea importable
sys.path.insert(0, os.path.abspath('../..'))

project = 'Traductor-inador'
copyright = '2025, Mictla'
author = 'Mictla'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = [
    '**/__pycache__',
    '**/.venv',
    '**/assets'
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'collapse_navigation': False,  # Esto evita que se colapse el sidebar.
}

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

napoleon_google_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# 🔽 Esto evita que se muestre 'app.' delante del nombre del módulo
add_module_names = False

# 🔽 Esto evita que se muestre el nombre completo en la firma
autodoc_strip_signature_backslash = True

# 🔽 Esto ayuda a ocultar el prefijo 'app.' en títulos y módulos en general
modindex_common_prefix = ['app.']
