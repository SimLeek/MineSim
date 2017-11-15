from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='minesim',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description= 'A voxel engine for simulation testing',
    long_description=long_description,
    url='https://github.com/SimLeek/MineSim',

    author='Josh Miklos',
    author_email='simulator.leek@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Natural Language :: English',
        'Programming Language :: Other',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],

    keywords='simulation voxel glsl opengl engine',

    packages=find_packages(exclude=['tests']),

    install_requires=['ModernGL','opensimplex']

    #extras_require=[],
    #entry_points={ # none yet
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},
)