from setuptools import setup


setup(name='Pymem',
      version='0.1',
      description='pymem: python memory access made easy',
      author='Fabien Reboia',
      author_email='srounet@gmail.com',
      maintainer='Fabien Reboia',
      maintainer_email='srounet@gmail.com',
      url=' http://www.pymem.org/',
      packages=['pymem', 'pymem.modules', 'pymem.constants', 'pymem.contrib'],
      long_description="A python library for windows, providing the needed \
functions to start working on your own with memory editing",
      license="postcard license",
      platforms=["windows"],
      keywords='memory win32 windows process',
      classifiers=[
          "License :: POSTCARD LICENCE",
          "Programming Language :: Python",
          "Development Status :: 1 - Beta",
          "Intended Audience :: Developers",
      ],
      install_requires=[
        'setuptools',
        'pywin32',
      ]
)
