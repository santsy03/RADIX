import xmlrpclib2
import httplib
import datetime
from datetime import tzinfo,timedelta
import re
import logging

logger = logging.getLogger( 'airhandler.tools' )

class Transporter(xmlrpclib2.Transport):
	
	HTTP = 0
	HTTPS = 1

	def __init__( self, scheme=HTTP, ua='IVR/3.1/1.0' ):
		xmlrpclib2.Transport.__init__(self)

		self.scheme = scheme
		self.connection = None
		self.ua = ua
	
	def request(self, *args, **keys):
		try:
			result = self._request(*args, **keys)
		except httplib.BadStatusLine:
			self.connection.close()
			self.connection = None

			result = self._request(*args, **keys)

		return result

	def _request( self, host, handler, request_body, verbose=0 ):
		
		h = self.make_connection(host)
		if verbose:
			h.set_debuglevel( 1 )

		self.send_request(h, handler, request_body)
		self.send_host(h, host)
		h.putheader("User-Agent", self.ua)
		self.send_content(h, request_body)

		response = h.getresponse()

		if response.status != 200:
			raise xmlrpclib2.ProtocolError(
				host + handler,
				response.status, response.reason, response.getheaders()
				)

		self.verbose = verbose

		return self.parse_response(response)

	def make_connection(self, host):
		if self.connection is None:
			host, extra_headers, x509 = self.get_host_info(host)
			if self.scheme == self.HTTP:
				self.connection = httplib.HTTPConnection(host)
			else:
				if not x509:
					x509 = dict()
				self.connection = httplib.HTTPSConnection( host, None, **x509 )
		return self.connection
class GMT330( tzinfo ):
        '''
         Africa/Nairobi
        '''
        def utcoffset( self, dt ):
                return timedelta( hours=+3, minutes=+00 )

        def tzname( self ):
                return "GMT +03:00"

        def dst( self, dt ):
                return timedelta( 0 )

        def __repr__( self ):
                return self.tzname()
