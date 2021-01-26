#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import ssl, socket, time, datetime, sys

try:
	mode = sys.argv[1]
except:
	sys.exit('ZBX_NOTSUPPORTED')

try:
	hostname = sys.argv[2]
except:
	sys.exit('ZBX_NOTSUPPORTED')

try:
	port = int(sys.argv[3])
except:
	port = 443

ctx = ssl.create_default_context()
s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
s.connect((hostname, port))
cert = s.getpeercert()

if mode == 'validate':
	not_after = cert['notAfter']
	format = '%b %d %H:%M:%S %Y %Z'
	due = datetime.datetime.strptime(not_after, format)
	now = datetime.datetime.now()
	print((due - now).days)
	sys.exit()

if mode == 'issuer':
	issuer = dict(x[0] for x in cert['issuer'])
	print(issuer['commonName'])
	sys.exit()

if mode:
	sys.exit('Mode not supported')