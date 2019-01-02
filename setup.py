from setuptools import setup
def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='kbr',
      version='0.0.1',
      description='python utils and tools collection',
      url='https://github.com/brugger/kbr-tools/',
      author='Kim Brugger',
      author_email='kbr@brugger.dk',
      license='MIT',
      packages=['kbr'],
      install_requires=[
          'records',
          'tornadoweb',
      ],
      classifiers=[
        'Development Status :: 0.0.1',
        'License :: MIT License',
        'Programming Language :: Python :: 3'
        ],      
#      scripts=[],
      # install our config files into an ehos share.
#      data_files=[],
      include_package_data=True,
      zip_safe=False)
