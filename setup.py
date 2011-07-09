#!/usr/bin/env python

from distutils.core import setup

setup(name='upit',
	version='0.2',
	description='UpIt simple Fileupload service',
	author='Bernhard Posselt',
	author_email='bernhard.posselt@gmx.at',
	url='https://github.com/Raydiation/UpIt',
	packages=['upit', 'upit/inc', 'upit/upload'],
    # we dont need package_data since its recursively listed in the
    # MANIFEST.in file
    # see http://docs.python.org/distutils/sourcedist.html#manifest
    # New in version 2.7: MANIFEST files start with a comment indicating 
    # they are generated. Files without this comment are not overwritten 
    # or removed.
)

