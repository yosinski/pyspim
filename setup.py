#! /usr/bin/env python

import sys
import os
from distutils.core import setup

setup(name='pyspim',
      version='0.1',
      url='https://github.com/yosinski/pyspim',
      author='Jason Yosinski',
      author_email='pyspim.jyo@0sg.net',
      py_modules=['pyspim'],
      )



print 'Looking for dependency: spim...',
sys.stdout.flush()
if os.system('which spim > /dev/null') == 0:
    print 'found.'
else:
    print 'not found.'
    print '\nERROR: spim is required before using pyspim. You can get it here:'
    print '    http://sourceforge.net/projects/spimsimulator/'


print 'Checking for dependency: pexpect module...',
sys.stdout.flush()
try:
    import pexpect
    print 'found.'    
except ImportError:
    print 'not found.'
    print '\nERROR: The pexpect module is required by pyspim. Install via'
    print '    sudo pip install pexpect'
    print 'or by downloading it directly from http://sourceforge.net/projects/pexpect/'
