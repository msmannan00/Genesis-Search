# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Orion Platform Documentation'
author = 'Your Name'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = ['myst_parser']  # Enable Markdown support

# Add paths for templates and static files
templates_path = ['_templates']
exclude_patterns = []

# The suffixes of source filenames
source_suffix = ['.rst', '.md']

# The master toctree document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'  # Use Read the Docs theme
html_static_path = ['_static']

# -- Additional options ------------------------------------------------------

# Allow Sphinx to parse Markdown files
myst_heading_anchors = 3  # Adds anchor links to headings
