from i18n import _
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-v','--version', help='show current version', action='store_true', default=False, required=False)
subparsers = parser.add_subparsers(title='The most commonly used gitxxl commands are',
								   metavar='<command>',
								   help='command help')

def init(req):
	print "running init with req:", req

parser_init = subparsers.add_parser('init', help='create an empty gitxxl repository or reinitialize an existing one')
parser_init.add_argument('--convert', help='will convert an existing git repository to use xxl', action='store_true', default=False)
parser_init.add_argument('path', help='path where the git repository is located and gitxxl repository will be initialized', default='.')
parser_init.set_defaults(func=init)
