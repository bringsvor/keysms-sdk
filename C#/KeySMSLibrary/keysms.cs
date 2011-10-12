﻿using System;
using System.Net;
using System.Collections.Generic;
using System.Collections;
using System.Text;
using System.IO;
using System.Runtime.Serialization.Json;
using System.Security.Cryptography;
using System.Runtime.Serialization;

namespace KeySMSLibrary
{    
    public class KeySMS
    {
        protected const String messageUri = "http://app.keysms.no/messages";
        protected const String infoUri = "http://app.keysms.no/auth/current.json";        

        protected String username;
        protected String APIKey;        

        public KeySMS() {}

        public KeySMS(String username, String APIKey) 
        {            
            auth(username, APIKey);                   
        }

        /// <summary>
        /// Sets your username and APIKey. The key is generated via the KeySMS-GUI        
        /// </summary>
        /// <param name="username">Usually the number the message is sent from.</param>
        /// <param name="APIKey">The key generated by the KeySMS-Web-GUI.</param>
        public void auth(String username, String APIKey)
        {
            this.username = username;
            this.APIKey = APIKey;            
        }

        /// <summary>
        /// Sends an SMS to multiple receivers.
        /// </summary>
        /// <param name="message">Your textmessage.</param>
        /// <param name="receivers">The receivers of the message.</param>
        /// <param name="options">Can be null.</param>
        /// <returns></returns>
        public SMSResponse sms(String message, String[] receivers, KeySMSOptions options)
        {
            KeySMSParameters parameters = new KeySMSParameters();

            parameters.values["message"] = message;
            parameters.values["receivers"] = receivers;

            if (options != null)
            {
                if(options.sender != null) parameters.values["sender"] = options.sender;

                if (options.datetime != null)
                {
                    parameters.values["date"] = options.datetime.Year + "-" + options.datetime.Month + "-" + options.datetime.Day;
                    parameters.values["time"] = options.datetime.Hour + ":" + options.datetime.Minute;
                }
            }

            String jsonPayload = JsonSerializer.Serialize<KeySMSParameters>(parameters);

            String jsonResponse = call(messageUri, jsonPayload);

            SMSResponse response = JsonSerializer.Deserialize<SMSResponse>(jsonResponse);

            return response;
        }

        /// <summary>
        /// Sends an SMS to a single receiver. Options are not required and may be null.
        /// </summary>
        /// <param name="message">Your textmessage.</param>
        /// <param name="receiver">The receiver of the message.</param>
        /// <param name="options">Can be null.</param>
        /// <returns></returns>
        public SMSResponse sms(String message, String receiver, KeySMSOptions options)
        {
            String[] receivers = new String[1];
            receivers[0] = receiver;

            return sms(message, receivers, options);
        }
        
        /// <summary>
        /// Retrives accountinformation.
        /// </summary>
        /// <param name="fields">The list data which you wish returned. (Not implemented.)</param>
        /// <returns>Information</returns>
        public Info info(List<String> fields)
        {
            if (fields == null) fields = new List<String>();

            fields.Add("user");
            fields.Add("account");

            KeySMSParameters table = new KeySMSParameters();

            foreach (String field in fields) table.values[field] = true;

            String response = call(infoUri, JsonSerializer.Serialize<KeySMSParameters>(table));

            Info info = JsonSerializer.Deserialize<Info>(response);

            return info;
        }        

        protected string sign(String payload)
        {                        
            String signatureBase = payload + APIKey;

            return md5(signatureBase);                     
        }

        protected string md5(String text)
        {
            byte[] textBytes = Encoding.UTF8.GetBytes(text);

            MD5CryptoServiceProvider cryptHandler = new MD5CryptoServiceProvider();

            byte[] hash = cryptHandler.ComputeHash(textBytes);

            string signature = "";

            foreach (byte a in hash) signature += a.ToString("x2");
 
            return signature;
        }

        protected String call(String uri, String payload)
        {            
            WebRequest request = WebRequest.Create(uri);            
            request.Method = "POST";
            request.ContentType = "application/x-www-form-urlencoded";

            String parameterString = "payload=" + payload + "&signature=" + sign(payload) + "&username=" + username;            
            byte[] byteArray = Encoding.UTF8.GetBytes(parameterString);
            request.ContentLength = byteArray.Length;
                                                
            Stream dataStream = request.GetRequestStream();            
            dataStream.Write(byteArray, 0, byteArray.Length);            
            dataStream.Close();
            
            WebResponse response = request.GetResponse();                                    
            dataStream = response.GetResponseStream();            
            StreamReader reader = new StreamReader(dataStream);            
            string responseFromServer = reader.ReadToEnd();
                                    
            reader.Close();
            dataStream.Close();
            response.Close();

            return responseFromServer;
        }
    }

    public class KeySMSOptions
    {
        /// <summary>
        /// The number the message appears to be sent from.
        /// </summary>
        public String sender;   
        /// <summary>
        /// The time within 5 minutes the message will be sent.
        /// </summary>
        public DateTime datetime;

        public KeySMSOptions()
        {
        }

        /// <summary>
        /// Constructor which assign necessary parameters.
        /// </summary>
        /// <param name="sender">The number the message appears to be sent from.</param>
        /// <param name="datetime">The time within 5 minutes the message will be sent.</param>
        public KeySMSOptions(String sender, DateTime datetime)
        {
            this.sender = sender;
            this.datetime = datetime;
        }
    }

    [Serializable]
    [KnownType(typeof(String[]))]
    public class KeySMSParameters : ISerializable
    {
        public Hashtable values { get; set; }

        public KeySMSParameters()
        {
            values = new Hashtable();
        }

        protected KeySMSParameters(SerializationInfo info, StreamingContext context)
        {
            values = new Hashtable();            
        }

        public virtual void GetObjectData(SerializationInfo info, StreamingContext context)
        {
            foreach (String key in values.Keys) info.AddValue(key, values[key]);
        }         
    }
    
    public static class JsonSerializer
    {
        public static string Serialize<T>(this T data)
        {
            try
            {
                DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(T));
                var stream = new MemoryStream();
                serializer.WriteObject(stream, data);
                string jsonData = Encoding.UTF8.GetString(stream.ToArray(), 0, (int)stream.Length);
                stream.Close();
                return jsonData;
            }
            catch
            {
                return "";
            }
        }
        public static T Deserialize<T>(this string jsonData)
        {
            try
            {
                DataContractJsonSerializer deserializer = new DataContractJsonSerializer(typeof(T));
                var stream = new MemoryStream(Encoding.UTF8.GetBytes(jsonData));
                T data = (T)deserializer.ReadObject(stream);
                stream.Close();
                return data;
            }
            catch
            {
                return default(T);
            }
        }
    }
}