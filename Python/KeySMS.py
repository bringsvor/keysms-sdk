
# KeySMS API client.
from json import JSONEncoder, JSONDecoder
from urllib import urlencode
from urllib2 import urlopen

__author__ = 'Torvald Baade Bringsvor <bringsvor@bringsvor.com>'

# Based upon the Java api.
import hashlib

class KeySMS(object):
    options = {}
    message = ''

    def __init__(self):
        """
        Constructor, defines what address to connect to and other options
	    @param array $options The API wide options
	    """
        self.options = {}
        self.options["host"] = "app.keysms.no"
        self.options["scheme"] = "http"

    def auth(self, userName, apiKey):
        " Define what user to auth with. All actions taken will be tied to this user in KeySMS "

        auth = {"username" : userName,
                "apiKey" : apiKey}
        self.options['auth'] = auth

    def sms(self, message, receivers, date = None, time = None):
        """ Send an SMS some time in the future (or right now if you don't specify)
        Returns a dist with the response from the KeySMS service """

        self.message = message
        response = self._call("/messages", receivers, date, time)

        response_json = JSONDecoder().decode(response[0])
        return response_json

    def _call(self, inputUrl, receivers, date, time):
        " Abstracts making HTTP calls "

        jsonPayload = JSONEncoder().encode(
            { 'message' : self.message,
            'receivers' : receivers,
            'date' : date,
            'time' : time }
        )

        host 				= self.options['host']
        scheme 				= self.options['scheme']
        requestURL 			= "%s://%s%s" % (scheme, host, inputUrl)
        signature		 	= self.sign(jsonPayload)
        username 			= self.options['auth']['username']

        data = urlencode( [('payload', jsonPayload),
                           ('signature', signature),
                           ('username', username)])

        conn = urlopen(requestURL, data)
        resp = conn.readlines()
        return resp

    def sign(self, json):
        """
        Create completely sign string based on payload

        @param array $payload The complete payload to ship
        @return string Ready to use sign string, just include in request
        """

        stringToEncode = json + self.options['auth']['apiKey']

        md5engine = hashlib.md5()
        md5engine.update(stringToEncode)

        hashtext = ''.join([ '0' for x in range(32-len(md5engine.hexdigest())) ])
        hashtext += md5engine.hexdigest()
        return hashtext
