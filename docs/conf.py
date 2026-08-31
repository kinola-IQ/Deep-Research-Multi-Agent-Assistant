# docs/conf.py

# -- Project information -----------------------------------------------------
project = "Deep-Research-Multi-Agent-Assistant"
author = "kinola-iq"
release = "0.1"
version = release

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",      # auto-generate docs from docstrings
    "sphinx.ext.napoleon",     # support for Google/NumPy style docstrings
    "sphinx.ext.viewcode",     # add links to source code
    "sphinx.ext.todo",         # support TODOs
    "sphinx.ext.githubpages",  # publish on GitHub Pages if needed
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for LaTeX output ------------------------------------------------
latex_engine = "pdflatex"
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
        \usepackage{amsmath,amssymb}
        \setcounter{tocdepth}{2}
    """,
}
latex_documents = [
    ("index", "Deep-Research-Multi-Agent-Assistant.tex",
     "Deep-Research-Multi-Agent-Assistant Documentation",
     author, "manual"),
]

# -- Options for EPUB output -------------------------------------------------
epub_title = project
epub_author = author
epub_language = "en"
epub_identifier = "https://readthedocs.org/projects/deep-research-multi-agent-assistant/"
epub_publisher = author
epub_copyright = "2026, " + author
epub_show_urls = "footnote"

# -- Options for manual page output ------------------------------------------
man_pages = [
    ("index", "deep-research-multi-agent-assistant",
     "Deep-Research-Multi-Agent-Assistant Documentation",
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    ("index", "Deep-Research-Multi-Agent-Assistant",
     "Deep-Research-Multi-Agent-Assistant Documentation",
     author, "Deep-Research-Multi-Agent-Assistant",
     "Multi-agent assistant project documentation.",
     "Miscellaneous"),
]

# -- Extension configuration -------------------------------------------------
todo_include_todos = True


# running doc generator automatically
# docs/conf.py
import os
import sys
import subprocess

# Add your project root to sys.path
sys.path.insert(0, os.path.abspath('../src'))

def run_apidoc(_):
    """Run sphinx-apidoc automatically before build."""
    src_dir = os.path.abspath('../src')
    apidoc_dir = os.path.abspath('api')
    subprocess.call([
        'sphinx-apidoc',
        '-o', apidoc_dir,
        src_dir,
        '--force',
        '--module-first'
    ])

def setup(app):
    app.connect('builder-inited', run_apidoc)
