import os
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith("~"):
                continue
            paths.append(os.path.join(path, filename))
    print( paths )
    return paths


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
          'tornado',
          'requests',
          'munch',
          'psycopg2-binary',
      ],
      classifiers=[
        'Development Status :: 0.0.1',
        'License :: MIT License',
        'Programming Language :: Python :: 3'
        ],      
      scripts=['bin/angular_code_gen.py',
               'bin/daemon_check.py',
                ],
      # install our config files into an ehos share.
#      data_files=[],
      data_files=[('share/kbr-tools/', package_files('share/'))],

      include_package_data=True,
      zip_safe=False)
