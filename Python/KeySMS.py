
# KeySMS API client.
from json import JSONEncoder

__author__ = 'Torvald Baade Bringsvor <bringsvor@bringsvor.com>'

# Based upon the Java api.
"""
import org.json.simple.*;
import java.math.BigInteger;
import java.net.*;
import java.security.MessageDigest;
import java.util.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;
"""
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
        """
        Define what user to auth with. All actions taken will be tied to this user in KeySMS
        """
        auth = {"username" : userName,
                "apiKey" : apiKey}
        self.options['auth'] = auth

    def sms(self, message, receivers, date = None, time = None):
        """
        Send an SMS some time in the future.
        """
        self.message = message
        response = self.call("/messages", receivers, date, time)
        return response

    def call(self, inputUrl, receivers, date, time):
        """
        Abstracts making HTTP calls
        """
        jsonPayload = JSONEncoder().encode(
            { 'message' : self.message,
            'receivers' : receivers,
            'date' : date,
            'time' : time }
        )
        # urllib.urlencode
        # https://docs.python.org/2/library/urllib.html?highlight=urlencode#urllib.urlopen

        """
		JSONArray jsonArray 		= new JSONArray();
		for (String tlf : recievers)
		{
			jsonArray.add(tlf);
		}
		JSONObject jsonPayload 		= new JSONObject();
		jsonPayload.put("message", message);
		jsonPayload.put("receivers", jsonArray);
		jsonPayload.put("date", date);
		jsonPayload.put("time", time);

		String host 				= (String) options.get("host");
		String scheme 				= (String) options.get("scheme");
		String requestURL 			= scheme + "://" + host + inputUrl;
		String signature		 	= this.sign(jsonPayload);
		String username 			= (String)((HashMap)options.get("auth")).get("username");
		printVariablesToConsole(jsonPayload, host, requestURL, signature, username);

		//Build parameter string
		String data;
		try {
			data = 	"payload="+URLEncoder.encode(jsonPayload.toString(),"UTF-8") +
					"&signature="+URLEncoder.encode(signature,"UTF-8")			 +
					"&username="+URLEncoder.encode(username,"UTF-8");
			System.out.println(data);
	        try {

	            // Send the request
	            URL url = new URL(requestURL);
	            URLConnection conn = url.openConnection();
	            conn.setDoOutput(true);
	            OutputStreamWriter writer = new OutputStreamWriter(conn.getOutputStream());

	            //write parameters
	            writer.write(data);
	            writer.flush();

	            // Get the response
	            StringBuffer answer = new StringBuffer();
	            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
	            String line;
	            while ((line = reader.readLine()) != null) {
	                answer.append(line);
	            }
	            writer.close();
	            reader.close();

	            //Return response from server
	            return answer.toString();

	        } catch (UnsupportedEncodingException e)
	        {
	        	e.printStackTrace();
	        }

        } catch (MalformedURLException ex)
        {
            ex.printStackTrace();
        } catch (IOException ex)
        {
            ex.printStackTrace();
        }

		return null; 		//Returns null on exception.
	}
        """
    """
	/**
	 * Print the variables to console to verify their content.
	 */
	private void printVariablesToConsole(JSONObject jsonPayload, String host, String requestURL, String signature, String username)
	{
		System.out.println("Host: "			+ host);
		System.out.println("URL " 			+ requestURL);
		System.out.println("Signature: " 	+  signature);
		System.out.println("username: " 	+ username);
		System.out.println("Json Payload: " + jsonPayload);
		System.out.println();
	}
    """
    def sign(self, json):
        """
        Create completely sign string based on payload

        @param array $payload The complete payload to ship
        @return string Ready to use sign string, just include in request
        """

        #stringToEncode = json.toString() + (String)((HashMap)options.get("auth")).get("apiKey");
        stringToEncode = json + self.options['auth'] + self.options['apiKey']

        md5engine = hashlib.md5()
        md5engine.update(stringToEncode)

        hashtext = ''.join([ '0' for x in range(32-len(md5engine.hexdigest())) ])
        hashtext += md5engine.hexdigest()
        return hashtext




        """
		try {
			MessageDigest md5 = java.security.MessageDigest.getInstance("MD5");
			md5.update(stringToEncode.getBytes("UTF-8"));

			byte[] digest = md5.digest();
			BigInteger bigInt = new BigInteger(1,digest);
			String hashtext = bigInt.toString(16);
			while(hashtext.length() < 32 ){
			  hashtext = "0"+hashtext;
			}

			return hashtext;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;

	}
    """


