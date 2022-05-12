from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    readme = fh.read()
with open('requirements.txt', 'r') as fh2:
    reqs = fh2.read()

setup(
    name='VBPatcher',
    version="0.6.0",
    description=
    'The Valheim BepInEx Patcher (VBPatcher) is a personal script created to solve the weird automatic version downgrading of the BepInEx modding tool.',
    url='https://github.com/schlopp96/VBPatcher',
    author='schlopp96',
    author_email='schloppdaddy@gmail.com',
    license='GPL v3.0',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={'console_scripts': ['start_vbp=VBPatcher.VBPatcher:main']},
    include_package_data=True,
    install_requires=[reqs],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    keywords=[
        'python,'
        'Valheim', 'BepInEx', 'patcher', 'mods', 'nexus', 'vbp', 'stable',
        'bleeding', ' edge', 'VBPatcher', 'vortex'
    ])
