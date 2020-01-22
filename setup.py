from setuptools import setup

setup(name='resizeful',
      version='0.1',
      description='Serverless image handler wrapper',
      url='git@github.com:wndrfl/resizerful.git',
      author='Manuel Aguilera',
      author_email='manuel@wonderful.io',
      license='MIT',
      packages=['resizeful'],
      install_requires=[
        'm2crypto',
      ],
      zip_safe=False)
