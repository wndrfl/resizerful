from setuptools import setup

setup(name='resizerful',
      version='1.0.1',
      description='Serverless image handler wrapper',
      url='git@github.com:wndrfl/resizerful.git',
      author='Manuel Aguilera',
      author_email='manuel@wonderful.io',
      license='Matt',
      packages=['resizerful'],
      install_requires=[
        'rsa',
      ],
      zip_safe=False)
