'''from Crypto.Util.number import *
from Crypto.Util.strxor import *
import os
print(os.getcwd())
# read the encrypted document to bytes ct
with open('quiz.enc', 'rb') as f:
    ct = f.read()
m = 64283
# known plaintext. 
known_pt = b'COMP2700'

# TODO: use the known plaintext to find S1, S2 and S3

# Calculate S1, S2, and S3 as byte XOR results
S1_bytes = strxor(ct[:2], known_pt[:2])
S2_bytes = strxor(ct[2:4], known_pt[2:4])
S3_bytes = strxor(ct[4:6], known_pt[4:6])
S4_bytes = strxor(ct[6:8], known_pt[6:8])

# Convert the byte results to integers
S1 = bytes_to_long(S1_bytes)
S2 = bytes_to_long(S2_bytes)
S3 = bytes_to_long(S3_bytes)

# TODO: calculate the key (S0, A, B) using S1, S2 and S3
A = (S3 - S2) * inverse(S2 - S1, m) % m 
B =(S2 - A * S1) % m 
S0 = (S1 - B) * inverse(A, m) % m 

#print("The key is (S0 = %d, A = %d, B = %d)" % (S0, A, B))

# Now you can use the key to decrypt doc.enc using the provided lcgcipher.py.

#ex5:The key is (S0 = 1234, A = 678, B = 2532)'''



from Crypto.Util.number import *
from Crypto.Util.strxor import *
import os

print(os.getcwd())
# Define the modulus
m = 64283

# Read the encrypted document to bytes `ct`
with open('quiz.enc', 'rb') as f:
    ct = f.read()

# Known plaintext
known_pt = b'COMP2700'

# Calculate S1, S2, S3, and S4 using the known plaintext as byte XOR results
S1_bytes = strxor(ct[:2], known_pt[:2])
S2_bytes = strxor(ct[2:4], known_pt[2:4])
S3_bytes = strxor(ct[4:6], known_pt[4:6])
S4_bytes = strxor(ct[6:8], known_pt[6:8])

# Convert the byte results to integers
S1 = bytes_to_long(S1_bytes)
S2 = bytes_to_long(S2_bytes)
S3 = bytes_to_long(S3_bytes)
S4 = bytes_to_long(S4_bytes)

# Calculate the key values (S0, A, B) using S1, S2, S3, and S4
A = (S3 - S2) * inverse(S2 - S1, m) % m 
B = (S2 - A * S1) % m 
S0 = (S1 - B) * inverse(A, m) % m

print("The key is (S0 = %d, A = %d, B = %d)" % (S0, A, B))

# 生成的keystream将和ct的长度匹配
def generate_keystream(S0, A, B, length):
    keystream = []
    S = S0
    for _ in range((length + 1) // 2):  # 调整生成的字节数
        S = (A * S + B) % m
        keystream.extend(long_to_bytes(S, 2))  # 每次生成2字节并添加到keystream中
    return bytes(keystream[:length])  # 确保返回的keystream与ct长度相等


# Generate the keystream for the ciphertext length
keystream = generate_keystream(S0, A, B, len(ct))

# Decrypt the ciphertext by XOR-ing with the keystream
decrypted = strxor(ct, keystream)

# Print the decrypted content as a string
print("Decrypted content:", decrypted.decode())
