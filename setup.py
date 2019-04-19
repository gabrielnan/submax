from setuptools import setup, find_packages

setup(
   name='submax',
   version='1.0',
   description='Submodular maximization algorithms with cardinality '
               'constraints',
   author='Gabriel Nakajima An',
   author_email='gabriel.nakajima.an@gmail.com',
   url='https://github.com/gabrielnan/submax',
   packages=find_packages(),
   install_requires=['tqdm', 'numpy', 'networkx', 'matplotlib', 'colormath'],
)
