#! /usr/bin/env python

'''
This is a demo grading script used to grade ASM submissions for
Cornell CS 3410:
    http://www.cs.cornell.edu/courses/cs3410/2013sp/
'''

import sys
import os
import StringIO
import csv
#import ipdb as pdb

from pyspim import Spim    # Available at https://github.com/yosinski/pyspim



fibs = {37: 24157817,
        38: 39088169,
        39: 63245986,
        40: 102334155,
        41: 165580141,
        42: 267914296}
maxRunTime = 5



def gradeSubmission(filename):
    '''Returns (grade, reason). Grade is -1 if submission could not be
    completely graded automatically.'''
    
    if not os.path.exists(filename):
        return 0, 'No submission.'

    spim = Spim()
    spim.load(filename)
    results = spim.run(timeout = maxRunTime)

    contains = {}
    if results is None:
        # program terminated
        registers = [spim.reg(ii) for ii in range(32)]
        for num,val in sorted(fibs.items()):
            #print num, 'yes' if val in registers else '-'
            contains[num] = (val in registers)
            ###print ii, reg, ' GOOD' if reg == fib40 else ''

        containsEarly = contains[37] or contains[38] or contains[39]
        containsLate  = contains[41] or contains[42]

        if containsLate:
            return 18, 'Went too far and computed Fib_41 and/or Fib_42 (-2).'
        elif contains[40]:
            return 20, 'Great!'
        elif containsEarly:
            return 18, 'Computed Fib_37, Fib_38, and/or Fib 39, but stopped before Fib_40 (-2).'
        else:
            # Must grade manually
            return -1, 'Program terminated but computed no nearby Fibonacci numbers.'
        
    else:
        # program did not terminate
        reason = StringIO.StringIO()
        errorLines = results.split('\n')
        errorLines = errorLines[1:]   # remove 'run' line
        if len(errorLines) > 0 and len(errorLines[0]) > 0:
            print >>reason, 'Program did not terminate after %.f seconds (infinite loop?). The following errors were reported:' % maxRunTime
            for errorline in errorLines[1:10]:
                print >>reason, errorline
            if len(errorLines) > 11:
                print >>reason, '... + %d more lines (after %.1f seconds).' % (len(errorLines) - 11, maxRunTime)
        else:
            print >>reason, 'Program did not terminate after %.f seconds (infinite loop?).' % maxRunTime
        return -1, reason.getvalue().strip()


def main():
    '''Run like this:
    ./gradeMips.py Submissions/netid/fibonacci.s

    If submission could be graded automatically:
        prints grade,reason
        exits with code 0
    else
        prints partial reason
        exits with code 1
    '''
    
    filename = sys.argv[1]

    grade, reason = gradeSubmission(filename)
    reason = reason.replace('\r\n', '\n')       # Use only \n for csv

    fields = StringIO.StringIO()
    writer = csv.writer(fields, quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    if grade >= 0:
        writer.writerow([grade, reason])
        print fields.getvalue().strip()
        #print '%s,"%s"' % (grade, reason)
    else:
        # Requires manual grade. Print only reason and set exit code to 1
        writer.writerow([reason])
        print repr(fields.getvalue().strip())[1:-1]    # strip containing quote from repr
        #pdb.set_trace()
        #print "%s" % reason
        sys.exit(1)



if __name__ == '__main__':
    main()
