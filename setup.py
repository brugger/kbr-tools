import os
from setuptools import setup
import json
import glob

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

def get_requirements():

    file_handle = open('requirements.txt', 'r')
    data = file_handle.read()
    file_handle.close()


    print( data )
    return data.split("\n")
#    return "{}.{}.{}".format( data['major'], data['minor'], data['patch'])

def scripts(directory='bin/*') -> []:
    return glob.glob( directory )


setup(name='kbr',
      version= get_version(),
      description='python utils and tools collection',
      url='https://github.com/brugger/kbr-tools/',
      author='Kim Brugger',
      author_email='kbr@brugger.dk',
      license='MIT',
      packages=['kbr'],
      install_requires=get_requirements(),
      classifiers=[
        "Development Status :: 0.0.1".format( get_version()),
        'License :: MIT License',
        'Programming Language :: Python :: 3'
        ],      
      scripts=scripts(),
#      data_files=[('share/kbr-tools/', package_files('share/'))],
#      include_package_data=True,
      zip_safe=False)
