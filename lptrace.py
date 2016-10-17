import os
import sys
import signal
import tempfile
import subprocess

from optparse import OptionParser

trace_fn = """def __lptrace_trace_calls__(frame, event, arg):
    if event != 'call':
        return

    code = frame.f_code
    with open(__LPTRACE_FIFO_NAME__, 'w') as fifo:
        fifo.write("{} ({}:{})".format(code.co_name,
                                       code.co_filename, frame.f_lineno))

__LPTRACE_FIFO_NAME__ = "%s"
__LPTRACE_OUTPUT_FIFO__ = None
import os
import sys ; sys.settrace(__lptrace_trace_calls__)
print 'INJECTED'"""


def strace(pid):
    fifo_name = tempfile.mktemp()
    os.mkfifo(fifo_name)
    os.chmod(fifo_name, 0777)

    with tempfile.NamedTemporaryFile() as tmp:
        name = tmp.name
        tmp.write(trace_fn % fifo_name)

        tmp.file.flush()
        os.chmod(tmp.name, 0666)

        cmd = 'execfile(\\"{}\\")'.format(name)
        inject(pid, cmd)

    with open(fifo_name) as fd:
        while True:
            print fd.read()


def pdb_prompt(pid):
    code = 'import pdb ; pdb.set_trace()'
    inject(pid, code)


def inject(pid, code):
    """Executes a file in a running Python process."""
    gdb_cmds = [
        'PyGILState_Ensure()',
        'PyRun_SimpleString("{}")'.format(code),
        'PyGILState_Release($1)',
        ]

    cmdline = 'gdb -p %d -batch %s' % (pid,
        ' '.join(["-eval-command='call %s'" % cmd for cmd in gdb_cmds]))
    print cmdline
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out, err


def main():
    parser = OptionParser()
    parser.add_option("-p", "--process", dest="pid",
                      help="Attach to prod $pid")

    parser.add_option("-d", "--debugger",
                      action="store_true", dest="debugger", default=False,
                      help="Inject a pdb prompt")

    (options, args) = parser.parse_args()

    if options.pid is None:
        print "You need to specify a process to attach to."
        sys.exit(-1)

    pid = int(options.pid)

    if options.debugger is True:
        pdb_prompt(pid)
    else:
        strace(pid)


if __name__ == '__main__':
    main()
