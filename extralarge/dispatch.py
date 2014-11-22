from i18n import _
import os, sys, atexit, signal, pdb, socket, errno, shlex, time, traceback, re
#import util, commands, hg, fancyopts, extensions, hook, error
import error
#import cmdutil, encoding
#import ui as uimod
import git

class request(object):
    def __init__(self, args, ui=None, repo=None, fin=None, fout=None,
                 ferr=None):
        self.args = args
        self.ui = ui
        self.repo = repo

        # input/output/error streams
        self.fin = fin
        self.fout = fout
        self.ferr = ferr

def run():
    "run the command in sys.argv"
    sys.exit((dispatch(request(sys.argv[1:])) or 0) & 255)

def dispatch(req):
    "run the command specified in req.args"
    if req.ferr:
        ferr = req.ferr
    elif req.ui:
        ferr = req.ui.ferr
    else:
        ferr = sys.stderr

    try:
        if not req.ui:
            req.ui = uimod.ui()
        if '--traceback' in req.args:
            req.ui.setconfig('ui', 'traceback', 'on', '--traceback')

        # set ui streams from the request
        if req.fin:
            req.ui.fin = req.fin
        if req.fout:
            req.ui.fout = req.fout
        if req.ferr:
            req.ui.ferr = req.ferr
    except error.Abort, inst:
        ferr.write(_("abort: %s\n") % inst)
        if inst.hint:
            ferr.write(_("(%s)\n") % inst.hint)
        return -1
    except error.ParseError, inst:
        if len(inst.args) > 1:
            ferr.write(_("hg: parse error at %s: %s\n") %
                             (inst.args[1], inst.args[0]))
            if (inst.args[0][0] == ' '):
                ferr.write(_("unexpected leading whitespace\n"))
        else:
            ferr.write(_("hg: parse error: %s\n") % inst.args[0])
        return -1

    msg = ' '.join(' ' in a and repr(a) or a for a in req.args)
    starttime = time.time()
    ret = None
    try:
        ret = _runcatch(req)
        return ret
    finally:
        duration = time.time() - starttime
        req.ui.log("commandfinish", "%s exited %s after %0.2f seconds\n",
                   msg, ret or 0, duration)