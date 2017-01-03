#!/usr/bin/env python

from setuptools import setup

setup(	name='Pony',
        license = "LGPL-3",
        version='0.2.5',
        description='General purpose package and dependency manager based on MongoDB',
        author='Giuseppe Puoti',
        author_email='giuseppe.puoti@gmail.com',
        url='https://github.com/gpuoti/Artifact-PonyExpress',

        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Software Development :: Version Control",
            "Topic :: System :: Archiving :: Packaging"
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        ]
        
        py_modules=[
            'pony', 
            'bag',
            'config_constrainer',
            'dependencies',
            'alternative_set',

            'pony_scons',
            'cli'
            # list them here when you add any other modules!
            ],
            
        
        
        install_requires = [
            'tabulate', 
            'colorama', 
            'networkx',
            'pymongo'
            # add any other dependency package here in order to let pip install them as installation' side effect.
            ],
            
        scripts = ['pony.py']  
)