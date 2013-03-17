#! /usr/bin/env python

import pexpect
import time
import re
import ipdb as pdb



class SPIM(object):
    '''Main SPIM class. See main() below for demo.

    Requires the command line version of SPIM, available here:
    http://sourceforge.net/projects/spimsimulator/
    '''

    def __init__(self, debug = False):
        '''Spawns a SPIM instance'''

        self.debug = debug
        
        self.sp = pexpect.spawn ('spim')
        self._expect('\(spim\) ')
        if not '(spim)' in self.sp.after:
            print 'one more...'
            self._expect('.*')
            raise Exception('Could not get spim prompt. Is it installed?\n\nOutput was:\n%s' % self.sp.after)


    def _sendline(self, line):
        '''Expect a response from the underlying child process. Respects debug mode. Private.'''

        if not self.sp.isalive():
            raise Exception('Child spim process died.')
        if self.debug:
            print '\nSENDING:', line
        self.sp.sendline(line)


    def _expect(self, pattern, timeout = -1, searchwindowsize = None):
        '''Expect a response from the underlying child process. Respects debug mode. Private.'''
        
        if not self.sp.isalive():
            raise Exception('Child spim process died.')
        if self.debug:
            print '\nEXPECTING:', pattern
        index = self.sp.expect(pattern, timeout = timeout, searchwindowsize = searchwindowsize)
        if self.debug:
            print 'GOT BEFORE: "%s"' %self.sp.before
            print 'GOT  AFTER: "%s"' % self.sp.after
        return index


    def load(self, filename):
        '''Loads a program from a *.s file'''
        
        self._sendline('load "%s"' % filename)
        index = self._expect(['Cannot open file.*\(spim\) ',
                             '\(spim\) ',
                             pexpect.EOF,
                             pexpect.TIMEOUT],
                            timeout = 1)
        #print 'index:', index
        if index == 0:
            raise Exception('Could not load file "%s"' % filename)
        elif index == 1:
            pass
        elif index == 2:
            raise Exception('SPIM EOF: process died?')
        elif index == 3:
            raise Exception('SPIM timeout')
        else:
            raise Exception('Unknown error with expect.')


    def run(self, timeout = 10):
        '''Runs the (presumably) loaded program.'''

        self._sendline('run')
        index = self._expect(['.*\(spim\) ',
                             pexpect.EOF,
                             pexpect.TIMEOUT],
                            timeout = timeout)

        if index == 0:
            pass
        elif index == 1:
            raise Exception('SPIM EOF: process died?')
        elif index == 2:
            raise Exception('SPIM timeout')
        else:
            raise Exception('Unknown error with expect.')


    def reg(self, register, timeout = 1):
        '''Gets the current value from the given register.

        Any of the following calling conventions is fine:
        spim.reg(5)
        spim.reg("$5")
        spim.reg("t0")
        spim.reg("$v0")
        '''
        
        if type(register) is int:
            register = str(register)
        if register[0:1] is not '$':
            register = '$' + register
        self._sendline('print %s' % register)
        index = self._expect(['.*Reg.*0x([0-9a-f])+.*\(spim\) ',
                             '.*Unknown label:.*\(spim\) ',
                             pexpect.EOF,
                             pexpect.TIMEOUT],
                            timeout = timeout)

        if index == 0:
            #print 'good. got stuff.'
            match = re.search('.*Reg.* = (0x[0-9a-f]+) .*\(spim\) ', self.sp.after, re.DOTALL)
            value = int(match.group(1), 0)   # base 0 -> interpret 0x... as hex
            return value
        elif index == 1:
            raise Exception('SPIM: Unknown label: %s' % register)
        elif index == 2:
            raise Exception('SPIM EOF: process died?')
        elif index == 3:
            raise Exception('SPIM timeout')
        else:
            raise Exception('Unknown error with expect.')


    def quit(self, timeout = 1):
        '''Quits the child spim process'''
        
        self._sendline('quit')
        index = self._expect([pexpect.EOF,
                             pexpect.TIMEOUT],
                            timeout = timeout)

        if index == 0:
            pass
        elif index == 1:
            raise Exception('SPIM timeout')
        else:
            raise Exception('Unknown error with expect.')



def main():
    sp = SPIM(debug = False)

    sp.load('test.s')             # load a .s file
    sp.run()                      # run it
    print 't0 is', sp.reg(8)      # get the value from a register
    print '(should be 123)'

    # If this line is uncommented, it should produce an error:
    #print '999 is', sp.reg(999)

    # If this line is uncommented, it should produce an error:
    #sp.load('does_not_exist.s')

    sp.quit()                     # quit the underlying spim process
    
    print 'done.'



if __name__ == '__main__':
    main()
