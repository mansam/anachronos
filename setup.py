from setuptools import setup, find_packages

version = '0.1.0'

setup(name='anachronos',
      version=version,
      description="A turn-based strategy game with time travel.",
      classifiers=[
          #"Development Status :: some_dev_status",
          #"Intended Audience :: if_ya_got_one",
          #"License :: ????",
          "Programming Language :: Python :: 2",
          "Topic :: Games/Entertainment :: Turn Based Strategy",
      ],
      keywords='anachronos game turn-based strategy time',
      author='Samuel Lucidi',
      #author_email='whatever@ya.like',
      url='http://github.com/mansam/anachronos',
      #license='????',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=["fabulous"],
      #entry_points="""
      #[console_scripts]
      #anachronos = anachronos:???
      #"""
      )
