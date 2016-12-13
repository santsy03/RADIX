import sys
import xmlrpclib
from twisted.web import resource, server
from twisted.internet import defer
from twisted.python import log, reflect

Fault = xmlrpclib.Fault


def withRequest(f):
    """
    Decorator to cause the request to be passed as the first argument
    to the method.
    """
    f.withRequest = True
    return f


class NoSuchFunction(Fault):
    """
    There is no function by the given name.
    """


class Handler:
    """
    Handle a XML-RPC request and store the state for a request in progress.

    Override the run() method and return result using self.result,
    a Deferred.
    """

    def __init__(self, resource, *args):
        self.resource = resource
        # the XML-RPC resource we are connected to
        self.result = defer.Deferred()
        self.run(*args)

    def run(self, *args):
        # event driven equivalent of 'raise UnimplementedError'
        self.result.errback(
            NotImplementedError("Implement run() in subclasses"))


class XMLRPC(resource.Resource):
    """
    A resource that implements XML-RPC.
    """
    # Error codes for Twisted, if they conflict with yours then
    # modify them at runtime.
    NOT_FOUND = 8001
    FAILURE = 8002

    isLeaf = 1
    separator = '.'
    allowedMethods = ('POST',)

    def __init__(self, allowNone=False, useDateTime=False):
        resource.Resource.__init__(self)
        self.subHandlers = {}
        self.allowNone = allowNone
        self.useDateTime = useDateTime

    def __setattr__(self, name, value):
        if name == "useDateTime" and value and sys.version_info[:2] < (2, 5):
            raise RuntimeError("useDateTime requires Python 2.5 or later.")
        self.__dict__[name] = value

    def putSubHandler(self, prefix, handler):
        self.subHandlers[prefix] = handler

    def getSubHandler(self, prefix):
        return self.subHandlers.get(prefix, None)

    def getSubHandlerPrefixes(self):
        return self.subHandlers.keys()

    def render_POST(self, request):
        request.content.seek(0, 0)
        request.setHeader("content-type", "text/xml")
        try:
            if self.useDateTime:
                args, functionPath = xmlrpclib.loads(request.content.read(),
                                                     use_datetime=True)
            else:
                # Maintain backwards compatibility with Python < 2.5
                args, functionPath = xmlrpclib.loads(request.content.read())
        except Exception, e:
            f = Fault(self.FAILURE, "Can't deserialize input: %s" % (e,))
            self._cbRender(f, request)
        else:
            try:
                function = self.lookupProcedure(functionPath)
            except Fault, f:
                self._cbRender(f, request)
            else:
                # Use this list to track whether the response failed or not.
                # This will be used later on to decide if the result of the
                # Deferred should be written out and Request.finish called.
                responseFailed = []
                request.notifyFinish().addErrback(responseFailed.append)
                if getattr(function, 'withRequest', False):
                    d = defer.maybeDeferred(function, request, *args)
                else:
                    d = defer.maybeDeferred(function, *args)
                d.addErrback(self._ebRender)
                d.addCallback(self._cbRender, request, responseFailed)
        return server.NOT_DONE_YET

    def _cbRender(self, result, request, responseFailed=None):
        if responseFailed:
            return

        if isinstance(result, Handler):
            result = result.result
        if not isinstance(result, Fault):
            result = (result,)
        try:
            try:
                content = xmlrpclib.dumps(
                    result, methodresponse=True,
                    allow_none=self.allowNone)
            except Exception, e:
                f = Fault(self.FAILURE, "Can't serialize output: %s" % (e,))
                content = xmlrpclib.dumps(f, methodresponse=True,
                                          allow_none=self.allowNone)

            request.setHeader("content-length", str(len(content)))
            request.write(content)
        except:
            log.err()
        request.finish()

    def _ebRender(self, failure):
        if isinstance(failure.value, Fault):
            return failure.value
        log.err(failure)
        return Fault(self.FAILURE, "error")

    def lookupProcedure(self, procedurePath):
        """
        Given a string naming a procedure, return a callable object for that
        procedure or raise NoSuchFunction.

        The returned object will be called, and should return the result of the
        procedure, a Deferred, or a Fault instance.

        @since: 11.1
        """
        if procedurePath.find(self.separator) != -1:
            prefix, procedurePath = procedurePath.split(self.separator, 1)
            handler = self.getSubHandler(prefix)
            if handler is None:
                raise NoSuchFunction(self.NOT_FOUND,
                                     "no such subHandler %s" % prefix)
            return handler.lookupProcedure(procedurePath)

        f = getattr(self, "xmlrpc_%s" % procedurePath, None)
        if not f:
            raise NoSuchFunction(self.NOT_FOUND,
                                 "procedure %s not found" % procedurePath)
        elif not callable(f):
            raise NoSuchFunction(self.NOT_FOUND,
                                 "procedure %s not callable" % procedurePath)
        else:
            return f

    def listProcedures(self):
        """
        Return a list of the names of all xmlrpc procedures.

        @since: 11.1
        """
        return reflect.prefixedMethodNames(self.__class__, 'xmlrpc_')
