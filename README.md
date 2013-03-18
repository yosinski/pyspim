About pyspim
=====================

[pyspim](https://github.com/yosinski/pyspim) is a very minimal Python
interface to [SPIM](http://sourceforge.net/projects/spimsimulator/), a
MIPS32 simulator. Pyspim is known to work on Linux and Mac. It almost
certainly does not work under Windows.



Installing pyspim
=====================

First install the requirements:

1. [SPIM](http://spimsimulator.sourceforge.net/)

2. The [pexepct](http://sourceforge.net/projects/pexpect/) Python module. Users with ```pip``` can install pexpect via

        sudo pip install pexpect

Then, install pyspim itself:

    git clone git@github.com:yosinski/pyspim.git
    cd pyspim/
    sudo python setup.py install



Example Usage
=====================

Quick demo
---------------------

For a quick demo, run ```pyspim.py``` directly:

    python pyspim.py

This should print something like the following:

    t0 is 123
    (should be 123)
    done.

Quick demo
---------------------

The basic commands for interacting with SPIM to load and run the included [```test.s```](https://github.com/yosinski/pyspim/blob/master/test.s) are shown below.

    spim = Spim(debug = False)      # Start the underlying SPIM process

    spim.load('test.s')             # Load a .s file
    spim.run()                      # Run the loaded file
    print 't0 is', spim.reg(8)      # Get the value from a register

    spim.quit()                     # Quit the underlying spim process


Use in grading
---------------------

See [```examples/gradeMipsSubmission.py```](https://github.com/yosinski/pyspim/blob/master/examples/gradeMipsSubmission.py) and [```examples/gradeAll.sh```](https://github.com/yosinski/pyspim/blob/master/examples/gradeAll.sh) for examples of how to use pyspim to automate grading of simple MIPS programs.



License
=======================

Pyspim is released under the [GNU GPL v3](http://www.gnu.org/licenses/gpl.txt).




![-](http://s.yosinski.com/1px_pyspim.png)
