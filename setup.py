from setuptools import setup

setup(
    name='remoteMultiCommand',
    version='0.1.1',
    author='Jonatan Dellagostin',
    author_email='jdellagostin@gmail.com',
    url='https://github.com/jonDel/remoteMultiCommand',
    packages=['remoteMultiCommand'],
    license='GPLv3',
    description='Provides execution of multiple commands in multiple servers in parallel (multiple processes)',
    long_description=open('README.rst').read(),
    classifiers=[
     'Development Status :: 3 - Alpha',
     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
     'Programming Language :: Python :: 2.6',
     'Programming Language :: Python :: 2.7',
     'Topic :: System :: Networking',
     'Topic :: System :: Systems Administration',
     'Topic :: System :: Shells',
     'Topic :: System :: Hardware :: Symmetric Multi-processing'
    ],
    keywords='ssh secure multi multi-processing parallel multiprocessing shell remote paramiko',
    install_requires=[
        "paramiko<=1.17.2",
        "sshParamiko",
        "pathos",
    ],
)
