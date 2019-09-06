from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
        name = 'pgbackup',
        version = '0.1.0',
        author = 'Oleg Fortochnik',
        author_email = 'olen2006@gmail.com',
        description = 'A utility for backing up PostgreSQL DB',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        url = 'http://github.com/olen2006/pgbackup.git',
        packages = find_packages('src')

)
