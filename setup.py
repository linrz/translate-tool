from setuptools import setup, find_packages

VERSION = '0.3.2'

setup(name='ptrans',
      version=VERSION,
      description="A command line tool help you trans other lauguages to Chinese each other",
      long_description='',
      keywords='trans terminal',
      author='linrz',
      author_email='1246533834@qq.com',
      url='https://github.com/linrz/trans-tool',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      package_data={
        '': ['*.ini']
      },
      install_requires=[
        'requests',
      ],
      entry_points={
        'console_scripts': [
            'trans = trans.translate:main'
        ]
      },
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5'
      ]
)
