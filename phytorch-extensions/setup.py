import os
from pathlib import Path

import torch.cuda
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension
from sys import platform

os.environ['TORCH_SHOW_CPP_STACKTRACES'] = '1'

if platform == "darwin":
    cc_env = "/Users/runner/work/caustic/boost"
elif platform == "linux":
    cc_env = "/home/runner/work/caustic/boost"
else:
    cc_env = "D:\a\caustic\boost"
    

use_cuda = torch.cuda.is_available()
extensions = ('.cpp', '.cu') if use_cuda else ('.cpp',)


COMPLIER_ARGS = {
    'cxx': ['-Wno-unused-local-typedefs', '-std=c++17'] + (['-DPHYTORCH_CUDA'] if use_cuda else []),
    'nvcc': ['--expt-relaxed-constexpr', '--extended-lambda',
             '-O2', '--relocatable-device-code=true',
             '--maxrregcount=128', '-std=c++17']
}


def filefilter(path: Path):
    return path.suffix.lower() in extensions and not path.name.startswith('_')


def ext_from_folder(folder: str):
    return (CUDAExtension if use_cuda else CppExtension)(
        folder, list(map(str, filter(filefilter, Path(folder).iterdir()))),
        extra_compile_args=COMPLIER_ARGS, dlink=True)


setup(
    name='phytorch.extensions',
    ext_modules=list(map(ext_from_folder, (
        'elliptic', 'roots', 'special'
    ))),
    include_dirs = cc_env,
    cmdclass={'build_ext': BuildExtension}
)
