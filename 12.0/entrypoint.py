#!/usr/bin/env python3.7
import argparse
import time

parser = argparse.ArgumentParser(description='Odoo EntryPoint.')

subparsers = parser.add_subparsers(title="Commands", dest="action", required=False)

odoo_parser = subparsers.add_parser('odoo', help='Odoo Service')
echo_parser = subparsers.add_parser('echo', help='Echo Service')

args = parser.parse_args()

if args.action == "odoo":
    print("Starting Odoo")
    time.sleep(100)
elif args.action == "echo":
    print("Starting echo")
else:
    print("Start other command")
