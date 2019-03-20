from setuptools import setup

setup(name='ogs_cli',
      version='0.1',
      description='Command line interface for online-go.com',
      url='http://github.com/simonseyock/ogs_cli',
      author='Milan Kroemer, Simon Seyock',
      author_email='milan.kroemer@pm.me, simonseyock@gmail.com',
      license='MIT',
      packages=['ogs_cli'],
      install_requires=[
        'colorama',
        'requests',
        'pyyaml',
        'sgfmill'
      ],
      entry_points = {
          'console_scripts': ['ogs=ogs_cli.cli:main']
      },
      zip_safe=False)
