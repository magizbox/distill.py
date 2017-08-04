from os import getcwd
from os.path import dirname, join

cwd = getcwd()
site_folder = join(cwd, 'site')
doc_folder = join(cwd, 'docs')
template_folder = join(dirname(__file__), "distill_template")
temp_site_folder = join(cwd, '_site')

