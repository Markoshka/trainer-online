import os
import sys

sys.path.insert(0, os.path.abspath('../../backend'))

project = 'Trainer Online'
copyright = '2026, Markoshka'
author = 'Markoshka'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

autodoc_mock_imports = [
    'fastapi', 'pydantic', 'jose', 'passlib', 'uvicorn',
]

templates_path = ['_templates']
exclude_patterns = []
language = 'ru'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
