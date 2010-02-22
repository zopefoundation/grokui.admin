import httplib
import pkg_resources
import socket
import urllib
import urllib2


def getURLWithParams(url, data=None):
    """Get the url with data appended as URL parameters.

    This is a reimplementation of functionality from ``grokcore.view``
    to enable use of ``grokui.admin`` with Grok versions < 0.13.
    """
    if data:
        for k, v in data.items():
            if isinstance(v, unicode):
                data[k] = v.encode('utf-8')
            if isinstance(v, (list, set, tuple)):
                data[k] = [isinstance(item, unicode) and item.encode('utf-8')
                or item for item in v]
        url += '?' + urllib.urlencode(data, doseq=True)
    return url


def getVersion(pkgname):
    """Determine the version of `pkgname` used in background.
    """
    info = pkg_resources.get_distribution(pkgname)
    if info.has_version and info.version:
        return info.version
    return None


class TimeoutableHTTPConnection(httplib.HTTPConnection):
    """A customised HTTPConnection allowing a per-connection
    timeout, specified at construction.
    """

    def __init__(self, host, port=None, strict=None, timeout=None):
        httplib.HTTPConnection.__init__(self, host, port,
                strict)
        self.timeout = timeout

    def connect(self):
        """Override HTTPConnection.connect to connect to
        host/port specified in __init__."""

        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port,
                0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                if self.timeout:   # this is the new bit
                    self.sock.settimeout(self.timeout)
                self.sock.connect(sa)
            except socket.error, msg:
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg


class TimeoutableHTTPHandler(urllib2.HTTPHandler):
    """A customised HTTPHandler which times out connection
    after the duration specified at construction.
    """

    def __init__(self, timeout=None):
        urllib2.HTTPHandler.__init__(self)
        self.timeout = timeout

    def http_open(self, req):
        """Override http_open.
        """

        def makeConnection(host, port=None, strict=None):
            return TimeoutableHTTPConnection(
                host, port, strict, timeout=self.timeout)

        return self.do_open(makeConnection, req)
