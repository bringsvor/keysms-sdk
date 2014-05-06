from Python.KeySMS import KeySMS

__author__ = 'Torvald Baade Bringsvor <bringsvor@bringsvor.com>'

 # Method for invoking KeySMS


if __name__ == '__main__':
    # Instansiate variables
    userName 	= "98800000"							# Username used to authenicate with
    apiKey		= "7912390aeeb9db0e2db4f7e4a6430f07"	# API key. Key is obtained through "Min side" at app.keysms.no
    message 		= "SMS to myself"
    recievers 	= ["98855555"]
    # String[] recievers 	= {"98800000", "98800001"};			Could be several receivers :
    date 		= "2011-03-10"							# If prior to todays date - assumes date == today.
    time			= "16:00"								# Time converted downwards to nearest quarter. eg 14:41 => 14:30

    # Instansiate KeySMS and send SMS
    keySms 		= KeySMS()
    keySms.auth(userName, apiKey)		 									# Define what user to authenticate with.
    # Object response = keySms.sms(message, recievers, date, time); 			// Send SMS to recievers. Returnes response from server. Date and time are optional.
    response = keySms.sms(message, recievers)
    print(response)
