import argparse
import getpass
from collections import defaultdict
from lib.crypto import encrypt_string_aes_256, decrypt_aes_256_cbc 
from lib.migration import Migration
import base64

ACTIONS=set(['encrypt', 'decrypt', 'search', 'migrate', 'runserver'])

parser   = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help', dest="cmdaction")

parser_encrypt = subparsers.add_parser('encrypt', help='TODO') 
parser_encrypt.add_argument("to_encrypt", help=f"TODO")

parser_decrypt = subparsers.add_parser('decrypt', help='TODO') 
parser_decrypt.add_argument("to_decrypt", help=f"TODO")

parser_search = subparsers.add_parser('search', help='TODO') 
parser_search.add_argument("directory", help=f"TODO")

parser_migrate = subparsers.add_parser('migrate', help='TODO') 
parser_migrate.add_argument("directory", help=f"TODO")

parser_runserver = subparsers.add_parser('runserver', help='TODO') 

args = parser.parse_args()

def encrypt(to_encrypt):
    password = getpass.getpass("Enter your password: ")
    encrypted = encrypt_string_aes_256(to_encrypt, password)
    encrypted = base64.b64encode(encrypted).decode()
    print(f'<span class="inline-protected">{encrypted}</span>')

def decrypt(to_decrypt):
    password = getpass.getpass("Enter your password: ")
    to_decrypt = base64.b64decode(to_decrypt)
    print(decrypt_aes_256_cbc(to_decrypt, password))

def search(directory):
    Migration(directory, None, None).search()

def migrate(directory):
    last_password = getpass.getpass("Enter current password: ")
    new_password = getpass.getpass("Enter new password: ")
    Migration(directory, last_password, new_password).migrate()

def runserver():
    from lib.server import run
    run()

cmdactions = defaultdict(lambda *args: parser.print_help())
cmdactions['encrypt'] = lambda kwargs: encrypt(kwargs['to_encrypt'])
cmdactions['decrypt'] = lambda kwargs: decrypt(kwargs['to_decrypt'])
cmdactions['search'] = lambda kwargs: search(kwargs['directory'])
cmdactions['migrate'] = lambda kwargs: migrate(kwargs['directory'])
cmdactions['runserver'] = lambda kwargs: runserver()

cmdaction = args.cmdaction
kwargs = vars(args)
del kwargs['cmdaction']
cmdactions[cmdaction](kwargs)

