#!/usr/bin/env python3
"""Hmm docstring for cli."""

import argparse
from __init__ import __version__, __author__

VAR_x_DEFAULT = 'DefaultValue'


class Args:
    """Who knows why."""
    args = None


def get_parser():
    """Parse user selected and default attributes."""
    parser = argparse.ArgumentParser()
    parser.formatter_class = CustomHelpFormatter
    parser.description = """
Write your own description."""

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s: v{}'.format(__version__))

    # parser.add_argument('-x', '-xxxx',
    #                     dest='varXname',
    #                     metavar='XXXX',
    #                     type=str,
    #                     default=VAR_x_DEFAULT,
    #                     help="Syntax for this arg: scriptname [-x|-xxxx value_in_str]\n")

    parser.add_argument(dest='source', metavar='SOURCE',
                        help='Source project folder')
    parser.add_argument(dest='dest', metavar='DEST', nargs='+',
                        help='Destination project folders (1 or more)')

    # parser.add_argument(dest='OptModificator', nargs='?',
    #                     help='Optional... Syntax: scriptname FILENAME [OPTMODIFICATOR]')
    parser.epilog = """
Additional info after help parameters when scriptname -h|--help

Script author/maintainer: {}, version: v{}""".format(__author__, __version__)

    return parser.parse_args()


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    """ArgParse custom formatter that has LONGER LINES and RAW DescriptionHelp formatting."""

    def __init__(self, prog):
        super(CustomHelpFormatter, self).__init__(prog, max_help_position=80, width=80)


def main():
    """Main program."""
    # Parser arguments from CLI
    args = get_parser()
    Args.args = args

    # print("DEBUG: args:", args)
    # MyVar = args.varXname
    # filename = args.filename
    # if args.OptModificator:
    #     # do stuff
    #     pass


if __name__ == 'cli':
    main()

    # MAIN SCRIPT CODE
