from cx_Freeze import setup, Executable

packages = ['pkg_resources._vendor']
includefiles = ['graph.py']

setup(
    name = 'Veil Map Creator',
    version = '0.1',
    description = 'Creates relationship maps for The Veil RPG',
    author = 'Maddie',
    author_email = 'maddie.violets@gmail.com',
    options = {'build_exe': {'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('gui.py')]
)