import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key="###PASTE PRIVATE KEY HERE###"

rsakey=RSA.importKey(private_key)
rsakey=PKCS1_OAEP..new(rsakey)

#Maybe use this
encrypted=input("Paste cipher here:")

chunk_size=256
offset=0
decrypted=""
encrypted=base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted+=rsakey.decrypt(encrypted[offset:offset + chunk_size])
    offset+=chunk_size

#解压负载
plaintext=zlib.decompress(decrypted)

print(plaintext)
