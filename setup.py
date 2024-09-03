from setuptools import setup, find_packages

setup(
    name='ImmunoCube',
    version='0.1',
    author='Benedikt Clemens',
    author_email='benedikt@uni-bonn.de',
    description='Python (OOP) code to compute the spatial relationship of proteins across cell compartments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', # ToDo
    ############
    install_requires=["math","warnings","sklearn","matplotlib.pyplot", "deprecated"],
    packages=find_packages(),
    ############
    url='http://example.com', # ToDo
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
