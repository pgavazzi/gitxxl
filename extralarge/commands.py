import os, sys, stat
from i18n import _
from argparse import ArgumentParser
from pygit2 import Repository
from error import Abort
import shutil

parser = ArgumentParser()
parser.add_argument('-v','--version', help=_('show current version'), action='store_true', default=False, required=False)
subparsers = parser.add_subparsers(title=_('The most commonly used gitxxl commands are'),
								   metavar=_('<command>'),
								   help=_('command help'))

def init(req):
	print "args:", req.args, req.args.path
	repo_path = os.path.join(req.args.path,'.git')
	if not os.path.isdir(repo_path):
		raise Abort("no repository found in '%s' (.git not found)!" % (os.path.abspath(req.args.path)))
	repo = Repository(req.args.path)
	print "repo references:", repo.listall_references()
	xxl_path = os.path.join(req.args.path,'.gitxxl')
	if os.path.exists(xxl_path):
		print "reinitializing existing XXL repo"
	else:
		print "initialiling XXL repo"
		os.mkdir(xxl_path)
		
	#install commit hooks
	dst = os.path.join(repo_path,"hooks","pre-commit")
	if not os.path.isfile(dst):
		src = os.path.join(sys.exec_prefix,"dist","hooks","pre-commit")
		print "installing pre-commit hook from:", src
		shutil.copyfile(src, dst)
		perm = os.stat(dst)
		os.chmod(dst,perm.st_mode | stat.S_IXUSR)

	dst = os.path.join(repo_path,"hooks","post-commit")
	if not os.path.isfile(dst):
		src = os.path.join(sys.exec_prefix,"dist","hooks","post-commit")
		print "installing post-commit hook from:", src
		shutil.copyfile(src, dst)
		perm = os.stat(dst)
		os.chmod(dst,perm.st_mode | stat.S_IXUSR)

	#install push hooks


#TODO make decorator for declarations or use argh
parser_init = subparsers.add_parser('init', help=_('create an empty gitxxl repository or reinitialize an existing one'))
parser_init.add_argument('--convert', help=_('will convert an existing git repository to use xxl'), action='store_true', default=False)
parser_init.add_argument('path', help=_('path where the git repository is located and gitxxl repository will be initialized'), default='.')
parser_init.set_defaults(func=init)
