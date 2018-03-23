import argparse, os, sys

from colorama import init
from helpers.defaultparser import set_default_subparser
from commands.done import item_done
from commands.list import list_items

init()

argparse.ArgumentParser.set_default_subparser = set_default_subparser

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='commands')
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('-a', '--all', action='store_true')
    parser_list.add_argument('-p', '--project', metavar='<project>', type=str, default='Inbox')
    parser_list.set_defaults(func=list_items)
    parser_done = subparsers.add_parser('done')
    parser_done.add_argument('pattern', type=str)
    parser_done.set_defaults(func=item_done)
    parser.set_default_subparser('list')
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
