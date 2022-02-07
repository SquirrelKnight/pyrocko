# -*- coding: utf-8 -*-
#
# Pyrocko documentation build configuration file, created by sphinx-quickstart
# on Tue Jan 25 22:08:33 2011.
#
# This file is execfile()d with the current directory set to its containing
# dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out serve
# to show the default.

import sys
import os
from datetime import datetime as dt
from pyrocko import version as pyrocko_version
import sphinx_sleekcat_theme


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('extensions'))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.imgmath',  # 'sphinx.ext.jsmath',
  'sphinx.ext.viewcode',
  'sphinx.ext.intersphinx',
  'sphinx.ext.autosummary'
]

intersphinx_mapping = {'numpy': ('https://docs.scipy.org/doc/numpy/',
                                 None),
                       'scipy': ('https://docs.scipy.org/doc/scipy/reference/',
                                 None),
                       'matplotlib': ('https://matplotlib.org/', None),
                       'python': ('https://docs.python.org/3.8', None),
                       'obspy': ('https://docs.obspy.org/', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'
imgmath_image_format = 'svg'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Pyrocko'
copyright = '%d, The Pyrocko Developers' % dt.now().year

# The version info for the project yo're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = pyrocko_version
# The full version, including alpha/beta/rc tags.
release = pyrocko_version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['pyrocko.']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_sleekcat_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'bodyfont': '"Lucida Grande",Arial,sans-serif',
    'headfont': '"Lucida Grande",Arial,sans-serif',
    'codefont': 'monospace,sans-serif',
    'linkcolor': '#204a87',
    'visitedlinkcolor': '#204a87',
    'nosidebar': True,
    # 'appendcss': open('style.css').read(),
    # 'googlewebfonturl': 'https://fonts.googleapis.com/css?family=Roboto+Slab',
    # 'bodyfont': '"Roboto Slab",Arial,sans-serif',
}
pygments_style = 'friendly'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [sphinx_sleekcat_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = u"%s v%s Manual" % (project, release)

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = u"%s Manual" % project

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
html_use_opensearch = 'https://pyrocko.org/pyrocko/'

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'Pyrockodoc'


# -- Options for LaTeX output --------------------------------------------------

latex_engine = 'xelatex'

# The paper size ('letter' or 'a4').
#latex_paper_size = 'a4'
latex_elements = {
    'papersize': 'a4paper',
    'preamble': '''
\\usepackage[utf8x]{inputenc}
\\setcounter{tocdepth}{4}''',
    'utf8extra': '',

}

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'pyrocko.tex', 'Pyrocko Documentation',
   'The Pyrocko Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for autodoc

autodoc_member_order = 'bysource'

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'pyrocko', 'Pyrocko Documentation',
     ['The Pyrocko Developers'], 1)
]


def process_signature(app, what, name, obj, options, signature,
                      return_annotation):

    from pyrocko import guts

    if what == 'class' and issubclass(obj, guts.Object):
        if obj.dummy_for is not None:
            cls_name = obj.T.classname
            descr = obj.dummy_for.__name__
            if hasattr(obj, 'dummy_for_descripton'):
                descr = (
                    obj.dummy_for_description
                    if obj.dummy_for_description is not None
                    else descr)
            return ('(...)', 'dummy for %s' % (descr))

    return


def skip_member(app, what, name, obj, skip, options):
    from pyrocko import guts

    if what == 'class' and name == 'dummy_for':
        return True
    if what == 'class' and name == 'T':
        return True


def setup(app):
    app.connect('autodoc-process-signature', process_signature)
    app.connect('autodoc-skip-member', skip_member)
