"""
simple class and command line tool to genereate salted password-hashes for FreeRadius
"""
__version__ = '0.03'
__author__ = "Christian Prinsler"

import hashlib
import base64
import secrets
from argparse import ArgumentParser
import getpass


class RadPwdHash:
    """class that generates salted password-hashes from user input"""

    def __init__(self, args):
        self.algorithms = {"md5": "SMD5", "sha1": "SSHA", "sha224": "SSHA2-224", "sha256": "SSHA2-256",
                           "sha384": "SSHA2-384", "sha512": "SSHA2-512"}
        self.salt = self.mk_salt(args.salt)
        self.algorithm = args.algorithm
        self.password = self.get_pwd()
        self.hash = self.mk_hash()

    def mk_salt(self, n):
        """generate random salt of length n"""
        return secrets.token_bytes(n)

    def get_pwd(self):
        """get user input password without showing it on screen or in the history"""
        while True:
            pw1 = getpass.getpass("Enter your password: ")
            pw2 = getpass.getpass("Enter your password again: ")
            if pw1 == pw2:
                return pw1
            else:
                print("Password don't match.\n")

    def mk_hash(self):
        """generate the salted password-hash"""
        hashed = hashlib.new(self.algorithm)
        hashed.update((bytes(self.password, 'utf-8') + self.salt))
        hashed_salt = base64.b64encode(hashed.digest() + self.salt)
        return hashed_salt

    def show(self):
        """print the password-hash in FreeRadius syntax"""
        print('{}-Password := "{}"'.format(self.algorithms[self.algorithm], str(self.hash).split("'")[1]))


def main():
    """parse cli arguments and generate the password-hash from user input"""
    parser = ArgumentParser()
    parser.add_argument("-s", dest="salt", default=16, help="salt length")
    parser.add_argument("-a", dest="algorithm", default="sha256",
                        help="used hash-algorithmus (md5, sha1, sha224, sha256, sha384, sha512)")
    args = parser.parse_args()

    new_passwd = RadPwdHash(args)
    new_passwd.show()

if __name__ == "__main__":
    main()
