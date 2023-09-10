from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='1',
      description='Garbadge sorter',
      url='https://github.com/JurijProcenko/clean_folder.git',
      author='Yurii Protsenko',
      author_email='elsoul@gmail.com',
      license='MIT',
      packages=find_namespace_packages()
      install-requires=['sys','os', 'pathlib', 'string']
      )