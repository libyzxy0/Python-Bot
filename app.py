

#Copyright (c) 2022 Jan Liby Dela Costa (libyzxy0.github.io). All Rights Reserved.



#License under the Libyzxy0 License, version 1.0 (the "License");

#you may not use this file except in compliance with the License.

#You may obtain a copy of the License at



#     https://github.com/libyzxy0/MessengerBot/blob/main/LICENSE



#Unless required by the applicable law or agreed in writing, software

#distributed under the License is distributed on an "AS IS" BASIS

#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

#See the License for the specific language governing permissions and

#limitations under the License.





from fbchat import Client, log, _graphql
from fbchat.models import *
import json
import random
import wolframalpha
import requests
import time
import math
import sqlite3
import os
import concurrent.futures
from difflib import SequenceMatcher, get_close_matches

with open("config.json") as conf:
    config = json.load(conf)

prefix = config["PREFIX"]
character = config["CHARACTER"]
botName = config["BOTNAME"]

class ChatBot(Client):

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        time.sleep(0.5)
        try:
            msg = str(message_object).split(",")[15][14:-1]
            if (".mp4" in msg):
                msg = msg
            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg = (message_object.text).lower()
            except:
                pass

        def sendMsg():
            if (author_id != self.uid):
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)

        def sendQuery():
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)
        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                c = conn.cursor()
                c.execute("""
                CREATE TABLE IF NOT EXISTS "{}" (
                    mid text PRIMARY KEY,
                    message text NOT NULL
                );

                """.format(str(author_id).replace('"', '""')))

                c.execute("""

                INSERT INTO "{}" VALUES (?, ?)

                """.format(str(author_id).replace('"', '""')), (str(mid), msg))
                conn.commit()
                conn.close()
            except:
                pass

        def corona_details(country_name):
            from datetime import date, timedelta
            today = date.today()
            today = date.today()
            yesterday = today - timedelta(days=1)

            url = "https://covid-193.p.rapidapi.com/history"

            querystring = {"country": country_name, "day": yesterday}

            headers = {
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66",
                'x-rapidapi-host': "covid-193.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data_str = response.text
            print(data_str)
            data = eval(data_str.replace("null", "None"))
            country = data["response"][0]["country"]
            new_cases = data["response"][0]["cases"]["new"]
            active_cases = data["response"][0]["cases"]["active"]
            total_cases = data["response"][0]["cases"]["total"]
            critical_cases = data["response"][0]["cases"]["critical"]
            total_deaths = data["response"][0]["deaths"]["total"]
            total_recovered = data["response"][0]["cases"]["recovered"]
            new_deaths = data["response"][0]["deaths"]["new"]
            reply = f'New cases: {new_cases}\nActive cases: {active_cases}\nNew deaths: {new_deaths}\nTotal deaths: {total_deaths}\nCritical cases: {critical_cases}\nTotal cases: {total_cases}\nTotal recovered: {total_recovered}'
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

        def weather(city):
            api_address = "https://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
            url = api_address + city
            json_data = requests.get(url).json()
            kelvin_res = json_data["main"]["temp"]
            feels_like = json_data["main"]["feels_like"]
            description = json_data["weather"][0]["description"]
            celcius_res = kelvin_res - 273.15
            max_temp = json_data["main"]["temp_max"]
            min_temp = json_data["main"]["temp_min"]
            visibility = json_data["visibility"]
            pressure = json_data["main"]["pressure"]
            humidity = json_data["main"]["humidity"]
            wind_speed = json_data["wind"]["speed"]
            print(
                f"maximum temperature {max_temp-273.15} *C \nminimum temperature {min_temp-273.15} *C")
            print(f"visibilty {visibility}m")
            print(f"pressure {pressure}")
            print(f"humidity {humidity}")
            print(f"wind speed {wind_speed}m/s")
            return(
                f"The current temperature of {city} is %.1f degree celcius with {description}" % celcius_res +" ")

        def stepWiseCalculus(query):
            query = query.replace("+", "%2B")
            try:
                try:
                    api_address = f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
                    answer = answer.replace("sqrt", "")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                except:
                    pass
                try:
                    api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
                    answer = answer.replace("sqrt", "")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                except:
                    try:
                        answer = json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                        answer = answer.replace("sqrt", "")

                        if(thread_type == ThreadType.USER):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                        elif(thread_type == ThreadType.GROUP):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                    except:
                        pass
            except:
                pass

        def stepWiseAlgebra(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input=solve%203x^2+4x-6=0&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][2]["plaintext"]
                answer = answer.replace("sqrt", "")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][3]["plaintext"]
                answer = answer.replace("sqrt", "")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][4]["plaintext"]
                answer = answer.replace("sqrt", "")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                answer = answer.replace("sqrt", "")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                answer = answer.replace("sqrt", "")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass

        def stepWiseQueries(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                try:
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "")
                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                    answer = answer.replace("sqrt", "")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
            except:
                self.send(Message(text="Cannot find the solution of this problem"), thread_id=thread_id,
                          thread_type=thread_type)

        try:
            def searchForUsers(self, name=" ".join(msg.split()[2:4]), limit=1):
                try:
                    limit = int(msg.split()[4])
                except:
                    limit = 1
                params = {"search": name, "limit": limit}
                (j,) = self.graphql_requests(
                    _graphql.from_query(_graphql.SEARCH_USER, params))
                users = ([User._from_graphql(node)
                          for node in j[name]["users"]["nodes"]])
                for user in users:
                    reply = f"{user.name} \n\n Link : {user.url}"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
        except:
            pass
        def translator(self, query, target):
            query = " ".join(query.split()[1:-2])
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"

            querystring = {"to": target, "api-version": "3.0",
                           "profanityAction": "NoAction", "textType": "plain"}

            payload = f'[{{"Text": "{query}"}}]'
            print("PAYLOAD>>", payload)
            headers = {
                'content-type': "application/json",
                'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66"
            }

            response = requests.request(
                "POST", url, data=payload, headers=headers, params=querystring)

            json_response = eval(response.text)
            print(json_response[0]["translations"][0]["text"])
            print(json_response)
            return json_response[0]["translations"][0]["text"]
        
        def bible():
        	import random
        	from modules.words import bible
        	a = random.choice(bible)
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
                  
        def jokes():
        	import random
        	from modules.words import jokes
        	a = random.choice(jokes)
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
        def advice():
        	import random
        	from modules.words import advice
        	a = random.choice(advice)
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
        def help_page_1():
        	help_1 = f"<====>Command List<====>\n\n\n• {prefix}Find img (Query)\n\n• {prefix}Find covid (Country)\n\n• {prefix}Find user (Username)\n\n• {prefix}Weather of (City)\n\n• {prefix}Translate (Msg) to (Lg) \n\n• {prefix}Generate (Query)\n\n• {prefix}Calc (Math)\n\n• {prefix}Bible ()\n\n• {prefix}Advice ()\n\n• {prefix}Jokes ()\n\n• {prefix}Test ()\n\n• {prefix}{character} (Msg)\n\n\n\nPage(1|3)»\n\n\nBot : {botName}"
        	a = help_1
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
        def help_page_2():
        	help_2 = f"<====>Command List<====>\n\n\n• {prefix}Find img (Query)\n\n• {prefix}Find covid (Country)\n\n• {prefix}Find user (Username)\n\n• {prefix}Weather of (City)\n\n• {prefix}Translate (Msg) to (Lg) \n\n• {prefix}Generate (Query)\n\n• {prefix}Calc (Math)\n\n• {prefix}Bible ()\n\n• {prefix}Advice ()\n\n• {prefix}Jokes ()\n\n• {prefix}Test ()\n\n• {prefix}{character} (Msg)\n\n\n\nPage«(2|3)»\n\n\nBot : {botName}"
        	a = help_2
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
        def help_page_3():
        	help_3 = f"<====>Command List<====>\n\n\n• {prefix}Find img (Query)\n\n• {prefix}Find covid (Country)\n\n• {prefix}Find user (Username)\n\n• {prefix}Weather of (City)\n\n• {prefix}Translate (Msg) to (Lg) \n\n• {prefix}Generate (Query)\n\n• {prefix}Calc (Math)\n\n• {prefix}Bible ()\n\n• {prefix}Advice ()\n\n• {prefix}Jokes ()\n\n• {prefix}Test ()\n\n• {prefix}{character} (Msg)\n\n\n\nPage«(3|3)\n\n\nBot : {botName}"
        	a = help_3
        	reply = f"{a}"
        	self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
                    
        def iLoveYou():
        	for i in range(101):
        		reply = f"I love you {i} "
        		self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)
	               
        def imageSearch(self, msg):
            try:
                count = int(msg.split()[-1])
            except:
                count = 3
            query = " ".join(msg.split()[2:])
            try:
                x = int(query.split()[-1])
                if type(x) == int:
                    query = " ".join(msg.split()[2:-1])
            except:
                pass
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": str(count)}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "8cd2881885msh9933f89c5aa2186p1d8076jsn7303d42b3c66"
            }
            print("sending requests...")
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            print("got response..")
            data = json.loads(response.text)
            img_contents = (data["value"])
            # print(img_contents)
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)
                
                global prefix, character, botName
                
        try:
            if(f"{prefix}find img" in msg):
                imageSearch(self, msg)

            elif(f"{prefix}translate" in msg):
                reply = translator(self, msg, msg.split()[-1])
                print(reply)
                sendQuery()
            elif(f"{prefix}weather of" in msg):
                indx = msg.index("weather of")
                query = msg[indx+11:]
                reply = weather(query)
                sendQuery()
            elif(f"{prefix}find covid" in msg):
                corona_details(msg.split()[2])
            elif ("calculus" in msg):
                stepWiseCalculus(" ".join(msg.split(" ")[1:]))
            elif ("algebra" in msg):
                stepWiseAlgebra(" ".join(msg.split(" ")[1:]))
            elif ("query" in msg):
                stepWiseQueries(" ".join(msg.split(" ")[1:]))
            elif(f"{prefix}bible" in msg):
              bible()
            elif(f"{prefix}jokes" in msg):
              jokes()
            elif(f"{prefix}advice" in msg):
              advice()
            elif(f"{prefix}test" in msg):
              iLoveYou()
            elif(f"{prefix}solve" in msg or f"{prefix}generate" in msg or f"{prefix}calc" in msg):
                app_id = "Y98QH3-24PWX83VGA"
                client = wolframalpha.Client(app_id)
                query = msg.split()[1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                reply = f'{answer.replace("sqrt", "")}'
                sendQuery()

            elif (f"{prefix}find user" in msg):
                searchForUsers(self)
                
            elif (f"{prefix}{character} test" in msg):
                reply = "Test"
                sendMsg() 

            elif (f"{prefix}{character} i love you" in msg):
                reply = "I love you too"
                sendMsg() 
                
            elif (msg == prefix):
                reply = f"Error command please type '{prefix}help' to show command list."
                sendMsg()
                
            elif (msg == f"{prefix}help" or msg == f"{prefix}help 1"):
            	help_page_1()
            elif (msg == f"{prefix}help 2"):
            	help_page_2()
            elif (msg == f"{prefix}help 3"):
            	help_page_3()
            
        except:
            pass

        self.markAsDelivered(author_id, thread_id)

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):

        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                c = conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg = c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg = fetched_msg[0][1]

                if(".mp4" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You unsent this video : "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} unsent this video : "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                elif("//scontent.xx.fbc" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You unsent this image : "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} Unsent this image : "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    if(thread_type == ThreadType.USER):
                        reply = f"You unsent this message : \n '{unsent_msg}'"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} unsent this message : \n\n '{unsent_msg}'"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)

            except:
                pass


    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You changed the theme"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onEmojiChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="You changed the emoji."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onImageChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply="Group Photo Change"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

cookies = {
    "sb": "qfsGY180yQ4tLNg1wsXVj2-i",
    "fr": "00nisAOc345AvzOf7.AWWKbjRSyh6RO4LvYSxeZTJWj50.BjBvup.-1.AAA.0.0.BjBvvA.AWW1P8PyAig",
    "c_user": "100084389502600",
    "datr": "qfsGYwoHniN3cOUVAuOZGU9_",
    "xs": "8%3AFL54kojn7RtOmA%3A2%3A1661415797%3A-1%3A9829" 
}

client=ChatBot("",
                "", session_cookies=cookies)
print(client.isLoggedIn())

try:
    client.listen()
except:
    time.sleep(3)
    client.listen()
