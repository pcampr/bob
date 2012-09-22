#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Mar 21 20:09:18 2011 +0100
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import pkg_resources

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
  'sphinx.ext.todo',
  'sphinx.ext.coverage',
  'sphinx.ext.pngmath',
  'sphinx.ext.ifconfig',
  'sphinx.ext.autodoc',
  'sphinx.ext.autosummary',
  'sphinx.ext.doctest',
  'sphinx.ext.intersphinx',
  #'matplotlib.sphinxext.plot_directive',
  'bob.sphinxext.plot', # ours add source copying to install directory
  ]

# The viewcode extension appeared only on Sphinx >= 1.0.0
import sphinx
if sphinx.__version__ >= "1.0":
  extensions.append('sphinx.ext.viewcode')

# Always includes todos
todo_include_todos = True

# If we are on OSX, the 'dvipng' path maybe different
dvipng_osx = '/opt/local/libexec/texlive/binaries/dvipng'
if os.path.exists(dvipng_osx): pngmath_dvipng = dvipng_osx

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Bob'
import time
copyright = u'%s, Idiap Research Institute' % time.strftime('%Y')

# Grab the setup entry
distribution = pkg_resources.require('bob')[0]

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = distribution.version
# The full version, including alpha/beta/rc tags.
release = distribution.version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['links.rst']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
if sphinx.__version__ >= "1.0":
  html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = 'bob'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'img/bob+reflection-sphinx.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'img/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

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
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'bobdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'bobman.tex', u'Bob',
   u'Biometrics Group, Idiap Research Institute', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = 'img/bob.pdf'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True

# Included after all input documents
rst_epilog = """
.. Some variables
.. |project| replace:: Bob
.. |bobweb| replace:: https://www.idiap.ch/software/bob
.. |current-year| date:: %Y
"""

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'bob', u'Bob Documentation', [u'Idiap Research Institute'], 1)
]


# We want to remove all private (i.e. _. or __.__) members 
# that are not in the list of accepted functions
accepted_private_functions = ['__call__']

def member_function_test(app, what, name, obj, skip, options):
  # test if we have a private function
  if len(name) > 1 and name[0] == '_':
    # test if this private function should be allowed
    if name not in accepted_private_functions:
      # omit privat functions that are not in the list of accepted private functions
      return True
    else:
      # test if the method is documented
      if not hasattr(obj, '__doc__') or not obj.__doc__:
        return True
  
  # Skips selected members in auto-generated documentation. Unfortunately, old
  # versions of Boost.Python will not generate a __self__ member for static
  # methods and that screws-up Sphinx processing. 
  if sphinx.__version__ < "1.0":
    # We have to remove objects that do not have a __self__ attribute set
    import types
    if isinstance(obj, types.BuiltinFunctionType) and \
      not hasattr(obj, '__self__') and what == 'class':
        app.warn("Skipping %s %s (no __self__)" % (what, name))
        return True

    return False
  
# Default processing flags for sphinx
autoclass_content = 'both'
autodoc_member_order = 'bysource'
autodoc_default_flags = ['members', 'undoc-members', 'special-members', 'inherited-members', 'show-inheritance']

# Used to filter some documentation in/out
bob_modules = dir(__import__('bob'))
has_libsvm = hasattr(__import__('bob').machine, 'SupportVector')
has_visioner = hasattr(__import__('bob'), 'visioner')

def smaller_than(v1, v2):
  """Compares scipy/numpy version numbers"""

  c1 = v1.split('.')
  c2 = v2.split('.')[:len(c1)] #clip to the compared version
  for i, k in enumerate(c2):
    n1 = c1[i]
    n2 = c2[i]
    try:
      n1 = int(n1)
      n2 = int(n2)
    except ValueError:
      n1 = str(n1)
      n2 = str(n2)
    if n1 > n2: return False
  return True

# Some name mangling to find the correct sphinx manuals for some packages
numpy_version = __import__('numpy').version.version
if smaller_than(numpy_version, '1.5.z'):
  numpy_version = '.'.join(numpy_version.split('.')[:-1]) + '.x'
else:
  numpy_version = '.'.join(numpy_version.split('.')[:-1]) + '.0'
numpy_manual = 'http://docs.scipy.org/doc/numpy-%s/' % numpy_version

scipy_version = __import__('scipy').version.version
if smaller_than(scipy_version, '0.8.z'):
  scipy_version = '.'.join(scipy_version.split('.')[:-1]) + '.x'
else:
  scipy_version = '.'.join(scipy_version.split('.')[:-1]) + '.0'
scipy_manual = 'http://docs.scipy.org/doc/scipy-%s/reference/' % scipy_version

sqlalc_version = __import__('sqlalchemy').__version__
sqlalc_major = sqlalc_version.split('.')[1] in ('5', '6')
if sqlalc_major in ('5', '6'):
 sqlalc_manual = 'http://docs.sqlalchemy.org/en/rel_0_%s' % sqlalc_major
else:
 sqlalc_manual = 'http://docs.sqlalchemy.org/en/latest'

# For inter-documentation mapping:
intersphinx_mapping = {
  'http://docs.python.org/%d.%d/' % sys.version_info[:2]: None,
  numpy_manual: None,
  scipy_manual: None,
  sqlalc_manual: None,
  'http://matplotlib.sourceforge.net/': None,
  'http://opencv.itseez.com/': None,
  }

def setup(app):
  app.connect('autodoc-skip-member', member_function_test)
  app.add_config_value('bob_modules', bob_modules, True)
  app.add_config_value('has_libsvm', has_libsvm, True)
  app.add_config_value('has_visioner', has_visioner, True)