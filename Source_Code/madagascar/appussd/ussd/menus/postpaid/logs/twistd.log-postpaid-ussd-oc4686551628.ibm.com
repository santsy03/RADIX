2016-12-12 15:09:07+0530 [-] Log opened.
2016-12-12 15:09:07+0530 [-] twistd 10.0.0 (/usr/bin/python 2.7.5) starting up.
2016-12-12 15:09:07+0530 [-] reactor class: twisted.internet.selectreactor.SelectReactor.
2016-12-12 15:09:07+0530 [-] twisted.web.server.Site starting on 7191
2016-12-12 15:09:07+0530 [-] Starting factory <twisted.web.server.Site instance at 0x1ed23f8>
2016-12-12 15:09:13+0530 [HTTPChannel,0,127.0.0.1] Request-261331579926-1
2016-12-12 15:09:13+0530 [HTTPChannel,0,127.0.0.1] cdr-261331579926-menu-1-0-0-1-opt-0
2016-12-12 15:09:13+0530 [HTTPChannel,0,127.0.0.1] Response-261331579926-'1. My account\n2. Additionnal services\n3. Roaming\n4. Airtel money\n5. Internet Offers\n6. Find a store\n7. Super Valisoa\n'
2016-12-12 15:09:13+0530 [-] 127.0.0.1 - - [12/Dec/2016:09:39:13 +0000] "POST / HTTP/1.1" 200 484 "-" "xmlrpclib.py/1.0.1 (by www.pythonware.com)"
2016-12-12 15:09:23+0530 [HTTPChannel,1,127.0.0.1] Request-261331579926-1
2016-12-12 15:09:23+0530 [HTTPChannel,1,127.0.0.1] cdr-261331579926-menu-1-0-1-11-opt-1
2016-12-12 15:09:23+0530 [HTTPChannel,1,127.0.0.1] Response-261331579926-'1. Language change\n2. My number\n3. Outstanding balance\n4. SMS/ minutes left\n5. Credit limit\n0. Next Page\n#. Previous Menu\n'
2016-12-12 15:09:23+0530 [-] 127.0.0.1 - - [12/Dec/2016:09:39:22 +0000] "POST / HTTP/1.1" 200 490 "-" "xmlrpclib.py/1.0.1 (by www.pythonware.com)"
2016-12-12 15:09:26+0530 [HTTPChannel,2,127.0.0.1] Request-261331579926-1
2016-12-12 15:09:26+0530 [HTTPChannel,2,127.0.0.1] cdr-261331579926-menu-1-0-2-111-opt-1
2016-12-12 15:09:26+0530 [HTTPChannel,2,127.0.0.1] Response-261331579926-'1. Malagasy\n2. Francais\n3. English\n#.Previous Menu\n'
2016-12-12 15:09:26+0530 [-] 127.0.0.1 - - [12/Dec/2016:09:39:25 +0000] "POST / HTTP/1.1" 200 420 "-" "xmlrpclib.py/1.0.1 (by www.pythonware.com)"
