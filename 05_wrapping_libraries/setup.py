# run: python setup.py build_ext --inplace

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
from Cython.Distutils import build_ext

from setuptools import setup
from setuptools import Extension
from os.path import abspath, dirname



# detect what library and linking use in process
import sys
if 'msvc-static' in sys.argv:
    libs = ['hellolib']
    sys.argv.remove('msvc-static')
elif 'msvc-shared' in sys.argv:
    libs = ['hellolib']
    sys.argv.remove('msvc-shared')
elif 'gcc-static' in sys.argv:
    libs = [':hellolib.a']
    sys.argv.remove('gcc-static')
elif 'gcc-shared' in sys.argv:
    libs = [':hellolib.so.1']
    sys.argv.remove('gcc-shared')
else:
    raise Exception(
        "Choose from: "
        "'msvc-static', 'msvc-shared', "
        "'gcc-static', 'gcc-shared"
    )


CURRENT_DIR = dirname(abspath(__file__))

name = 'cythonhellolib'

ext_modules = [Extension(
    name=name,
    sources=[
        'cythonhellolib.pyx',
    ],
    include_dirs=[CURRENT_DIR],
    library_dirs=[CURRENT_DIR],
    libraries=libs,
    language='c'
)]

for mod in ext_modules:
    mod.cython_directives = {
        'language_level': 3,
    }

setup(
    name=name,
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext}
)
