from os import error
import requests, string, random, argparse, sys, time
import logging
import threading
import concurrent.futures


def getRandomString(length): #Letters and numbers
    pool=string.ascii_lowercase+string.digits
    return "".join(random.choice(pool) for i in range(length))

def getRandomText(length): #Chars only
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

def generate(name):
    nick = getRandomText(8)
    passw = getRandomString(12)
    email = nick+"@"+getRandomText(5)+".com"

    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.26 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.26",
             "X-Client-Id": getRandomString(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": "male" if random.randint(0, 1) else "female",
            "birth_year": random.randint(1990, 2000),
            "displayname": nick,
            "iagree": "true",
            "birth_month": random.randint(1, 11),
            "password_repeat": passw,
            "password": passw,
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": email,
            "birth_day": random.randint(1, 20)}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code==200:
        if r.json()['status']==1:
            file_object = open("accs.txt", 'a')
            file_object.write(email+":"+passw+"\n")
            file_object.close()
            print("account has been generated: "+email+":"+passw)
            return (True, email+":"+passw)
        else:
            print("[error]: (wait 2 mins) Could Not Create The Account, Some Errors Occurred.")
            time.sleep(120)
            return (False, "Could not create the account, some errors occurred")
    else:
        print("[error]: (wait 2 mins) Could Not Load The Page")
        time.sleep(120)
        return (False, "Could not load the page. Response code: "+ str(r.status_code))


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(generate, range(10000))

