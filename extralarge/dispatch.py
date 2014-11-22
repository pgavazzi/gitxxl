from i18n import _
import os, sys, atexit, signal, pdb, socket, errno, shlex, time, traceback, re
import error
from commands import parser
import git

class request(object):
    def __init__(self, repo=None, fin=None, fout=None,
                 ferr=None):
        self.args = parser.parse_args()
        self.repo = repo

        # input/output/error streams
        self.fin = fin
        self.fout = fout
        self.ferr = ferr

def run():
    "run the command in sys.argv"
    sys.exit((dispatch(request()) or 0) & 255)

def dispatch(req):
    "run the command specified in req.args"
    if req.ferr:
        ferr = req.ferr
    else:
        ferr = sys.stderr

    starttime = time.time()
    ret = None
    try:
        ret = req.args.func(req)
        return ret
    finally:
        duration = time.time() - starttime
