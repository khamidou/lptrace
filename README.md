# lptrace

lptrace is strace for Python programs. It lets you see in real-time
what functions a Python program is running. It's particularly useful
to debug weird issues on production.

For example, let's take the following toy Python program:

```python
import time

def f():
    time.sleep(1)
    g()

def g():
    time.sleep(1)
    f()

f()
```

Let's run it and connect lptrace to it:

```
vagrant@precise32:/vagrant$ python /tmp/t.py &
[1] 1765
vagrant@precise32:/vagrant$ sudo python ttrace.py -p 1765
f (/tmp/t.py:3)
g (/tmp/t.py:7)
f (/tmp/t.py:3)
g (/tmp/t.py:7)
f (/tmp/t.py:3)
g (/tmp/t.py:7)
f (/tmp/t.py:3)
g (/tmp/t.py:7)
f (/tmp/t.py:3)
^CReceived Ctrl-C, quitting
vagrant@precise32:/vagrant$
```

That's it! After pressing Ctrl-C, the trace is removed and the program
execution resumes normally.

# Installing

lptrace was written to be run on production servers. Because of this,
you only need `lptrace.py` to run the whole program.

We may have a pypi package in the near future.

# Usage

## Tracing a Python program

```
sudo python lptrace -p <process_id>
```

## Getting a pdb prompt inside a Python program

Sometimes it's useful to get a pdb prompt inside a Python program.
Note that this requires that the Python program you're attaching to
has access to stdin.

```
sudo python lptrace -p <process_id>
```

# Requirements

lptrace requires Python 2.x and GDB 7.x. It has been tested on Linux
successfully, and it should run on most recent Unices.

# Technical details

lptrace is a relatively simple program but it uses some moderately crazy hacks to modify an already
running Python program. I encourage you to read the source (it's roughly 100 lines of Python), but
here's a 5 minute overview of how it works:

1. gdb is an awesome debugger. It lets you attach to any running program, as long as you're root. It
also lets you call any C function this program exposes.

2. Among the C functions the Python interpreter exposes, one function `PyRun\_SimpleString` lets you
run a single expression of Python code.

3. 

# Issues

Please open a ticket [here](https://github.com/khamidou/lptrace/issues)

# Special Thanks

I'd like to thank the [Pyrasite project](http://pyrasite.com/) for coming up with
the idea to inject code into a running Python process.
