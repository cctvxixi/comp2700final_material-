#lab8 ex1
from Crypto.Util.number import inverse  # 导入逆元函数

# 已知的模数和生成的随机数
m = 64283
S1 = 7667
S2 = 50997
S3 = 6447

# 定义方程 (S2 - S3) 和 (S1 - S2)
diff1 = S2 - S3
diff2 = S1 - S2

# 求出 A 的值
A_val = (diff1 * inverse(diff2, m)) % m

# 通过已知的 A 和 S1, S2 计算 B 的值
B_val = (S2 - A_val * S1) % m

# 打印 A 和 B
print(f"A = {A_val}, B = {B_val}")

# 反推出种子 S0
S0 = (S1 - B_val) * inverse(A_val, m) % m
print(f"S0 = {S0}")
# A = 177, B = 43881
# S0 = 45193


#5

from Crypto.Util.strxor import strxor

# 已知的明文: <html>，转换为字节形式
known_pt = b'<html>'

# 读取加密文件中的密文（ciphertext）
with open('doc.enc', 'rb') as f:
    ct = f.read()

# 用 XOR 操作计算密钥流的前几个字节
# 将加密的前几个字节与明文进行异或，得到前几个密钥字节
keystream = strxor(known_pt, ct[:len(known_pt)])

# 输出推测出的密钥流前几个字节
print(f"推测出的密钥流前几个字节: {keystream.hex()}")

# 从推测的密钥流中提取 S1, S2, S3
S1 = int.from_bytes(keystream[:2], byteorder='big')
S2 = int.from_bytes(keystream[2:4], byteorder='big')
S3 = int.from_bytes(keystream[4:6], byteorder='big')

print(f"S1 = {S1}, S2 = {S2}, S3 = {S3}")

