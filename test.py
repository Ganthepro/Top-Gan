import base64
import zlib

k = "80e32263"
kh = "6f8af44abea0"
kf = "351039f4a7b5"
p = "0UlYyJHG87EJqEz6"
s = "ISAG{" + kh
g = kf + p + "}"
flag = "I'm not telling you."


def x(t, k):
    c = len(k)
    l = len(t)
    o = bytearray()
    for i in range(0, l):
        o.append(t[i] ^ k[i % c])
    return bytes(o)


r = "QKyWH2MdGPwXGiv+/sE+QjowQu83Dw=="
encrypted_string = base64.b64decode(r)
k = bytes.fromhex(k)  # Convert k from hex to bytes
decrypted_string = x(encrypted_string, k)
original_input = zlib.decompress(decrypted_string).decode()

print(original_input)
