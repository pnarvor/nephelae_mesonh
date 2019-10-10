from setuptools import setup, find_packages

setup(name='nephelae_mesonh',
      version='0.1',
      description='MesoNH utilities for nephelae_project',
      url='ssh://git@redmine.laas.fr/laas/users/simon/nephelae/nephelae-devel/nephelae_simulation.git',
      author='Pierre Narvor',
      author_email='pnarvor@laas.fr',
      licence='bsd3',
      packages=find_packages(include=['nephelae_mesonh']),
      install_requires=[
        'numpy',
        'utm',
        'matplotlib',
        'sh',
        'xarray'
      ],
      zip_safe=False)


