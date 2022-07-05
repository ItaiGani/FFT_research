from setuptools import setup

setup(
   name='FFT_research',
   version='1.0',
   description='FFT heavy coefficients interface.',
   author='Omri, Itay, Ron, Yotam',
   author_email='',
   packages=['FFT_research'],  # same as name
   install_requires=['scipy', 'numpy', 'matplotlib'], # external packages as dependencies
   scripts=[]
)