from setuptools import setup, Extension, find_packages
import numpy as np
import os

extension = Extension("pesq_core",
                      sources=["pypesq/pesq.c", "pypesq/dsp.c", "pypesq/pesqdsp.c", "pypesq/pesqio.c", "pypesq/pesqmain.c", "pypesq/pesqmod.c"],
                      include_dirs=[os.path.join(np.get_include(), 'numpy')], 
                      language='c++')

setup(name='objective_speech_metric',
    version='0.0.1',
    description="A package to compute pesq score.",
    url='https://github.com/vBaiCai/python-pesq',
    license='MIT',
    packages=find_packages(),
    ext_modules=[extension],
    py_modules=['numpy'],
    zip_safe=False,
    install_requires=['numpy'],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, <4',
)
