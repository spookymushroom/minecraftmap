#!/usr/bin/env python

from setuptools import setup

setup(
  name             = 'minecraftmap',
  version          = '0.2',
  description      = 'Minecraft Map Reader/Writer',
  author           = 'Michael Korotkov',
  author_email     = 'github.spookymushroom@gmail.com',
  url              = 'https://github.com/spookymushroom/minecraftmap/',
  download_url     = 'https://github.com/spookymushroom/minecraftmap/tarball/0.2',
  license          = open("LICENSE.txt").read(),
  long_description = open("README.txt").read(),
  include_package_data = True,
  packages         = ["minecraftmap"],
  install_requires = ["Pillow","nbt"],
  keywords         = ["minecraft","map","nbt"],
  classifiers      = [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules"
  ]
)
