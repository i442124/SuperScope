from OpenSSL.crypto import *

f = open('file.pfx', 'rb')
p12 = load_pkcs12(f.read(), 'MyPassword')

pkey = p12.get_privatekey()
open(cd + 'pkey.pem', 'wb').write(dump_privatekey(FILETYPE_PEM, pkey))

cert = p12.get_certificate()
open(cd + 'cert.pem', 'wb').write(dump_certificate(FILETYPE_PEM, cert))