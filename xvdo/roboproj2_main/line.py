import requests

def notify(msg):
    if type(msg) == 'tuple':
        for i in msg:
            notify(i)
    else:
        url = 'https://notify-api.line.me/api/notify'
        token = 'g8qmd2kClnMnQSKVHZovuqgH38dktkYUYBnO5TW33lN'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        r = requests.post(url, headers=headers, data = {'message':msg})
        print (r.text, msg, sep='\n')

def ipinfo():
    r = requests.get('https://ipinfo.io/')
    s =  eval(r.text)
    location = s['loc'].split(",")
    return s.items(), f"\nlatitude: {location[0]}\nlongitude: {location[1]}"