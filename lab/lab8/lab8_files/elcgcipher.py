#!/usr/bin/env python3

# ANU COMP2700 Cyber Security Foundations
# A simple (and flawed) stream cipher using a linear congruence generator
# Alwen Tiu, 2022
# Michael Purcell, 2023

import argparse
import json 
from Crypto.Util.number import *
from Crypto.Util.strxor import *

# Each block is 16 bytes
BLOCK_SIZE=16

# Fixed the modulus, which is a 128-bit prime
MODULUS=334875488192674307082291203874744941083


# All key material S0, A, B and n are 128-bit integers
def elcg(S0, S1, A, B, n):
  Sa = S0
  Sb = S1 
  keystream = bytearray()

  # generate a 16-byte pseudo-random number at a time.  
  for i in range(n):
    Sc = (A*Sa + B*Sb) % MODULUS
    R = long_to_bytes(Sc,BLOCK_SIZE)
    keystream.extend(R)
    Sa = Sb 
    Sb = Sc 
  return bytes(keystream)

# NOTE: since this is a streamcipher, encryption and decryption are the same function. 
def encrypt(S0, S1, A, B, inbytes):
  sz = len(inbytes)

  # generate keystream
  # n = how many random numbers need to be generated. 
  # Each number is BLOCK_SIZE byte long. 
  n  = sz//BLOCK_SIZE + 1
  keystream = elcg(S0,S1,A,B,n)

  # byte-wise XOR plaintext with keystream
  outbytes = strxor(inbytes, keystream[0:sz])
  return outbytes

# NOTE: since this is a streamcipher, encryption and decryption are the same function. 
def encfile(S0, S1, A, B, infile, outfile):
  with open(infile, 'rb') as f: 
    inbytes = f.read()
  outbytes = encrypt(S0,S1,A,B, inbytes)

  with open(outfile, 'wb') as g:
    g.write(outbytes)

def main(): 
  parser = argparse.ArgumentParser()
  parser.add_argument('keyfile', type=str, help='keyfile in JSON format')
  parser.add_argument('infile', type=str, help='file to encrypt/decrypt' )
  parser.add_argument('outfile', type=str, help='file to store the result of encryption/decryption' )

  args = parser.parse_args()    

  with open(args.keyfile, "r") as f: 
    key = json.loads(f.read())

  S0 = key["S0"] % MODULUS
  S1 = key["S1"] % MODULUS
  A  = key["A"] % MODULUS
  B  = key["B"] % MODULUS

  encfile(S0,S1,A,B,args.infile, args.outfile)


if __name__ == "__main__":
  main()
   
