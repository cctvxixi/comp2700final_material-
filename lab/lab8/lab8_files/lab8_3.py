from Crypto.Util.number import *
from Crypto.Util.strxor import *
import os
print(os.getcwd())
# read the encrypted document to bytes ct
with open('ofb2.enc', 'rb') as f:
    ct = f.read()

# known plaintext. 
with open('ofb1.txt', 'rb') as f:
    known_pt= f.read()




# Now you can use the key to decrypt doc.enc using the provided lcgcipher.py.

