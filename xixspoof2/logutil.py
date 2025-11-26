import sys

def info(*a): print(*a, flush=True)

def warn(m): print('[WARN]',m,flush=True)

def error(m): print('[ERROR]',m,file=sys.stderr,flush=True)
