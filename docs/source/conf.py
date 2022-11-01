# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'Micron DLA SDK'
copyright = '2022, Micron Technology, Inc'
author = 'MDLA Team'
release = '2022.1'

import sphinx_rtd_theme

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_rtd_theme',
              'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []
latex_engine = 'pdflatex'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_logo = 'images/micron.png'
html_theme_options = {
    'logo_only': True
}
html_static_path = ['_static']
html_css_files = ['css/colors.css']
