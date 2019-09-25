import os
from setuptools import setup

# pire
# Python Interactive Regular Expression


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pire",
    version="0.1.0",
    description="Python Interactive Regular Expression",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="python regex re regular expressions",
    url="https://github.com/johannestaas/pire",
    packages=['pire'],
    package_dir={'pire': 'pire'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=['ezcurses'],
    entry_points={
        'console_scripts': [
            'pire=pire:main',
        ],
    },
)
