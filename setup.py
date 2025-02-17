import setuptools
import os
import sys
from skbuild import setup
from skbuild.constants import CMAKE_INSTALL_DIR, skbuild_plat_name
from packaging.version import Version
from skbuild.exceptions import SKBuildError
from skbuild.cmaker import get_cmake_version

# Add CMake as a build requirement if cmake is not installed or is too low a version
setup_requires = []
try:
    cmake_version = Version(get_cmake_version())
    if cmake_version < Version("3.5") or cmake_version >= Version("3.15"):
        setup_requires.append('cmake<3.15')
except SKBuildError:
    setup_requires.append('cmake<3.15')

# If you want to re-build the cython cpp file (DracoPy.cpp), run:
# cython --cplus -3 -I./_skbuild/linux-x86_64-3.7/cmake-install/include/draco/ ./src/TrakoDracoPy.pyx
# Replace "linux-x86_64-3.6" with the directory under _skbuild in your system
# Draco must already be built/setup.py already be run before running the above command

src_dir = './src'
lib_dir = os.path.abspath(os.path.join(CMAKE_INSTALL_DIR(), 'lib/'))
cmake_args = []
if sys.platform == 'darwin':
    plat_name = skbuild_plat_name()
    sep = [pos for pos, char in enumerate(plat_name) if char == '-']
    assert len(sep) == 2
    cmake_args = ['-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING='+plat_name[sep[0]+1:sep[1]],'-DCMAKE_OSX_ARCHITECTURES:STRING='+plat_name[sep[1]+1:]]
    library_link_args = ['-l{0}'.format(lib) for lib in ('dracoenc', 'draco', 'dracodec')]
else:
    library_link_args = ['-l:{0}'.format(lib) for lib in ('libdracoenc.a', 'libdraco.a', 'libdracodec.a')]
extra_link_args = ['-L{0}'.format(lib_dir)] + library_link_args

setup(
    name='TrakoDracoPy',
    version='0.0.13b2.dev9',
    description = 'Python wrapper for Google\'s Draco Mesh Compression Library with Trako support',
    author = 'Manuel Castro, Daniel Haehn',
    author_email = 'macastro@princeton.edu, haehn@mpsych.org',
    url = 'https://github.com/haehn/TrakoDracoPy',
    cmake_source_dir='./draco',
    cmake_args=cmake_args,
    setup_requires=setup_requires,
    install_requires=['pytest'],
    ext_modules=[
        setuptools.Extension(
            'TrakoDracoPy',
            sources=[ os.path.join(src_dir, 'TrakoDracoPy.cpp') ],
            depends=[ os.path.join(src_dir, 'TrakoDracoPy.h') ],
            language='c++',
            include_dirs = [ os.path.join(CMAKE_INSTALL_DIR(), 'include/')],
            extra_compile_args=[
              '-std=c++11','-O3'
            ],
            extra_link_args=extra_link_args
        )
    ]
)
