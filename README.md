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

# Running lptrace

lptrace was written to be run on production servers. Because of this,
you only need `lptrace.py` to run the whole program.

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

gdb is an awesome debugger. It lets you attach to any running program, as long as you're root. It
also lets you call any C function this program exposes.

What's interesting is that among the C functions the Python interpreter exposes,
one function `PyRun\_SimpleString`, lets you run a single expression of Python code.

We use this function to ask the Python process to read a temporary file `lptrace` created. This file
contains a hook to the `sys.settrace` function, which allows us to get notified whenever a function is
called.

Finally, we need to output the tracing data somewhere. We could do this in the program we're tracing
but that wouldn't be very useful. Instead, we write it to a FIFO so that `lptrace` can display it in
its own window.

That's about it. I encourage you to read the source --- it's short and pretty simple!

# Issues

Please open a ticket [here](https://github.com/khamidou/lptrace/issues)

# Security

lptrace is a debugging tool. It uses temporary files, so it may be vulnerable to some race conditions. Caveat emptor!

# Special Thanks

I'd like to thank the [Pyrasite project](http://pyrasite.com/) for coming up with
the idea to inject code into a running Python process.
