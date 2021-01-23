import setuptools


setuptools.setup(
    name='kill3d',
    version='0.0.1',
    author='RimoChan',
    author_email='the@librian.net',
    description='kill3d',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/kill3d',
    packages=['kill3d'],
    package_data={
        'kill3d': ['莉沫.png'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'glfw>=1.12.0',
        'rimo-utils>=1.4.1',
        'opencv-python>=4.5.1.48',
        'numpy>=1.16.6',
        'pywin32>=300',
        'PyFaceDet>=0.2.0',
    ],
    python_requires='>=3.6',
)
