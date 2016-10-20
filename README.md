# lptrace

lptrace is strace for Python programs. It lets you see in real-time
what functions a Python program is running. It's particularly useful
to debug weird issues on production.

For example, let's debug a non-trivial program, the Python SimpleHTTPServer.
First, let's run the server:

```
vagrant@precise32:/vagrant$ python -m SimpleHTTPServer 8080 &
[1] 1818
vagrant@precise32:/vagrant$ Serving HTTP on 0.0.0.0 port 8080 ...
```

Now let's connect lptrace to it:

```
vagrant@precise32:/vagrant$ sudo python lptrace.py -p 1818
...
fileno (/usr/lib/python2.7/SocketServer.py:438)
meth (/usr/lib/python2.7/socket.py:223)

fileno (/usr/lib/python2.7/SocketServer.py:438)
meth (/usr/lib/python2.7/socket.py:223)

_handle_request_noblock (/usr/lib/python2.7/SocketServer.py:271)
get_request (/usr/lib/python2.7/SocketServer.py:446)
accept (/usr/lib/python2.7/socket.py:201)
__init__ (/usr/lib/python2.7/socket.py:185)
verify_request (/usr/lib/python2.7/SocketServer.py:296)
process_request (/usr/lib/python2.7/SocketServer.py:304)
finish_request (/usr/lib/python2.7/SocketServer.py:321)
__init__ (/usr/lib/python2.7/SocketServer.py:632)
setup (/usr/lib/python2.7/SocketServer.py:681)
makefile (/usr/lib/python2.7/socket.py:212)
__init__ (/usr/lib/python2.7/socket.py:246)
makefile (/usr/lib/python2.7/socket.py:212)
__init__ (/usr/lib/python2.7/socket.py:246)
handle (/usr/lib/python2.7/BaseHTTPServer.py:336)
handle_one_request (/usr/lib/python2.7/BaseHTTPServer.py:301)
^CReceived Ctrl-C, quitting
vagrant@precise32:/vagrant$
```

You can see that the server is handling the request in real time! After pressing Ctrl-C, the trace is removed and the program
execution resumes normally.

# How it works

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
sudo python lptrace -p <process_id> -d
```

# Requirements

lptrace requires Python 2.x and GDB 7.x. It has been tested on Linux
successfully, and it should run on most recent Unices.

# Issues

Please open a ticket [here](https://github.com/khamidou/lptrace/issues)

# Security

lptrace is a debugging tool. It uses temporary files, so it may be vulnerable to some race conditions. Caveat emptor!

# Special Thanks

I'd like to thank the [Pyrasite project](http://pyrasite.com/) for coming up with
the idea to inject code into a running Python process.
