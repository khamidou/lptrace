from distutils.core import setup
setup(
  name = 'lptrace',
  packages = [], # this must be the same as the name above
  version = '1.0.0',
  description = 'lptrace is strace for Python. It lets you trace any running Python program.',
  author = 'Karim Hamidou',
  author_email = 'hello@khamidou.com',
  url = 'https://github.com/khamidou/lptrace',
  download_url = 'http://github.com/khamidou/lptrace/tarball/1.0.0',
  keywords = ['debugging', 'production', 'tracing'],
  classifiers = [],
  scripts=['lptrace'],
)
