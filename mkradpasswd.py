"""
Autor: Christian Prinsler
Datum: 23.07.2020
Version 0.01
Zweck: Generierung von salted-Hashes für Freeradius Passwörter
"""

import hashlib
import base64
import secrets
from argparse import ArgumentParser
import getpass

class radpasswd:
    
                
    def __init__(self, args):
        self.algorithms={"md5":"SMD5","sha1":"SSHA", "sha224":"SSHA2-224", "sha256":"SSHA2-256","sha384":"SSHA2-384", "sha512":"SSHA2-512"}
        self.salt=self.mksalt(args.salt)        
        self.algorithm=args.algorithm
        self.password=self.mkpassword()
        self.hash=self.mkhash(self.algorithm,self.salt,self.password)

    #Random Salt der Länge n generieren (sicherer als selbst eins zu wählen)
    def mksalt(self,n):
        return secrets.token_bytes(n)

    #das Passwort wird über input erzeugt, da es nicht als Argument übergeben und so in der History erscheinen soll
    def mkpassword(self):        
        while True:
            #pw1=input("Geben Sie Ihr Passwort ein: ")
            pw1=getpass.getpass("Geben Sie Ihr Passwort ein: ")
            pw2=getpass.getpass("Bestätigen Sie Ihr Passwort: ")
            #zur Sicherheit wird das PW zweimal abgefragt
            if pw1==pw2:                
                return pw1
            else:
                print("Passwörter stimmen nicht überein.\n")
            

    def mkhash(self,algorithm,salt,pw):        
        #Hash für PW+Salt erstellen
        hashed=hashlib.new(algorithm)
        hashed.update((bytes(pw,'utf-8')+salt))        

        #Salt an den Hash anhängen
        hashed_salt=base64.b64encode(hashed.digest() + salt)
        return hashed_salt

    #Ausgabe von Passwort Zeile für users-Datei unter freeradius
    def show(self):
        print('{}-Password := "{}"'.format(self.algorithms[self.algorithm],str(self.hash).split("'")[1]))
        
        

def main(): 
    parser=ArgumentParser()
    parser.add_argument("-s",dest="salt",default=16,help="Länge des Salts")
    parser.add_argument("-a",dest="algorithm",default="sha256",help="Verwendeter Hash-Algorithmus (md5, sha1, sha224, sha256, sha384, sha512)")
    #parser.add_argument("password",help="Ihr Passwort")
    args=parser.parse_args()

    new_passwd=radpasswd(args)
    new_passwd.show()

main()
