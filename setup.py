import os
from setuptools import setup
import json

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

def get_version():
    with open('version.json') as json_file:
        data = json.load(json_file)

    return "{}.{}.{}".format( data['major'], data['minor'], data['patch'])


setup(name='kbr',
      version= get_version(),
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
        "Development Status :: 0.0.1".format( get_version()),
        'License :: MIT License',
        'Programming Language :: Python :: 3'
        ],      
      scripts=['bin/angular_code_gen.py',
               'bin/daemon_check.py',
               'bin/kbr-dev-utils.py'
                ],
      data_files=[('share/kbr-tools/', package_files('share/'))],
      include_package_data=True,
      zip_safe=False)
