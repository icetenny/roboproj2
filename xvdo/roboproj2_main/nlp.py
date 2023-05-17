import azure.cognitiveservices.speech as speechsdk
import requests, uuid, json

#Region
Region = "southeastasia"

#speech
Speech_key = "3b66785c9d73403b99708544933c45a2"
Endpoint = "https://southeastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

#translate
Translate_key = "ca0e0d8f2c774ba5abfeeb1a7d0b5397"
endpoint = "https://api.cognitive.microsofttranslator.com"

#utility
Thai_set = {'ก', 'ข', 'ฃ', 'ค', 'ฅ', 'ฆ', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ฌ', 'ญ', 'ฎ', 'ฏ', 'ฐ', 'ฑ', 'ฒ', 'ณ', 'ด', 'ต', 'ถ', 'ท', 'ธ', 'น', 'บ', 'ป', 'ผ', 'ฝ', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', 'ศ', 'ษ', 'ส', 'ห', 'ฬ', 'อ', 'ฮ'}
Thai = "th-TH-NiwatNeural"
# Thai = "th-TH-PremwadeeNeural"
Eng = "en-US-AIGenerate1Neural"
Ind = "en-IN-PrabhatNeural"

#config
speech_config = speechsdk.SpeechConfig(subscription=Speech_key, region =Region)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
source_language_config = speechsdk.languageconfig.SourceLanguageConfig("th-TH")

# ? -------------------------------------------------------------------------------------------
# ? functions

# check if there are any Thai in the text
def check(text):
    if set(text).intersection(Thai_set) == set():
         return Eng
    return Thai

#  speak out the text  
def speak(text):
    #just speak
    speech_config.speech_synthesis_voice_name = check(text)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(text).get()

# listen to the user and return what they speak in all lower case
def recog():
    result = speech_recognizer.recognize_once()
    text = result.text.lower()
    return text

# listen to the user and return what they speak in thai
def recog_Thai():
    speech_recognizer_th = speechsdk.SpeechRecognizer(speech_config=speech_config, source_language_config=source_language_config)
    result = speech_recognizer_th.recognize_once()
    text = result.text.lower()
    return text

# speak and print out the text
def speak_print(text):
    speak(text)
    print(text)

def onlyfan():
    speak_print("OnlyFan has been activated")

# join the list items together from start+1, stop+1
# list must only contains strings
def joinlist(l,start,stop):
    return " ".join(l[start+1:stop+1])

# separate long text into groups of Thai and English
def sep(text):
    #split text into parts
    phrase = text.split()
    #output
    out = []
    #index container
    temp = []
    #list the breaking points
    for i in range(0,len(phrase)-1,1):
        if check(phrase[i]) != check(phrase[i+1]):
            temp.append(i)
    order = [-1] + temp + [len(phrase)-1]

    #form the pieces
    for i in range(len(order)-1):
        obj = joinlist(phrase,order[i],order[i+1])
        out.append((obj,check(obj)))    
    return out

# speak with better accent
def speak2(text):
     #speak but separate Thai and English
     phrase = sep(text)
     for part, lang in phrase:
        speak(part)

#  transform a long text into a more usable one
def transform(text):
    return text.strip().replace("\n"," ")

# loop for continuos speaking
def speech_loop():
    #loop for speak2()
    while True:
        text = transform(input("Enter text to read: "))
        if text == 'q': 
                return 
        speak2(text)

# speak in Inglish
# def indianvoice(text):
#     speech_config.speech_synthesis_voice_name = Ind
#     speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
#     speech_synthesizer.speak_text_async(text).get()

# translate the given text
def translate(text, mode=0):

    fr = 'th'
    to = 'en'

    if mode == 0:
        fr = 'en'
        to = 'th'
        
    path = '/translate'
    constructed_url = endpoint + path

    params = { 'api-version': '3.0', 'from': fr, 'to': [to] }

    headers = {'Ocp-Apim-Subscription-Key': Translate_key, 'Ocp-Apim-Subscription-Region': Region, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}

    body = [{ 'text': text }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text

# transalte the given mixed language text to Thai
def translate2Thai(text):
    phrase = sep(text)
    for part, lang in phrase:
        if lang == Eng:
            speak(translate(part))
        else:
            speak(part)

# translate loop
def translate_loop():
    #loop for speak2()
    while True:
        text = transform(input("Enter text to translate: "))
        if text == 'q': 
                return 
        translate2Thai(text)

# def in_thai(key, text):
#     return

# ? -----------------------------------------------------------------------------------------------------------------------------------
# ! Real project functions underneath

# ! NEEDED FOR THE ACTUAL PROJECT 
def translate_from_speech_loop(escape='เลิกทำ'):
    speak_print(f"ให้พูดว่า {escape} เพื่อปิดการใช้งานโหมดที่สี่ \nเริ่มพูดหลังจบเสียงสัญญาณ")
    while True:
        text = recog_Thai()
        if escape in text:
            speak_print("ปิดการใช้งานโปรแกรม")
            break
        print(text)
        translated = translate(text, mode=1)
        speak_print(translated)

# select the mode the user want to use
# ! NEEDED FOR THE ACTUAL PROJECT 
def mode_selection():
    speak_print("Select your mode")
    text = recog()
    print(f"Your respond: {text}")
    if "1" in text or "one" in text:
        speak_print("You want to use mode one reading right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            print("Mode 1: reading has been selected")
            return 1
        else:
            mode_selection()
    elif "2" in text or "two" in text:
        speak_print("You want to use mode two translating right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            speak_print("Mode 2: translating has been selected")
            return 2
        else:
            mode_selection()
    elif "3" in text or "three" in text:
        speak_print("You want to use mode three identifying right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            speak_print("Mode 3: indentifying has been selected")
            return 3
        else:
            mode_selection()
    elif "4" in text or "four" in text:
        speak_print("You want to use mode four translating from voice right?")
        ans = recog()
        print(f"Your respond: {ans}")
        if "yes" in ans or "yeah" in ans or "exactly" in ans:
            speak_print("Mode 4: translating from voice has been selected")
            translate_from_speech_loop()
            return 4
        else:
            mode_selection()
    elif "only fan" in text or "turn on" in text:
        onlyfan()
    else:
        speak_print("No mode has been selected")


# select the mode the user want to use
# ! NEEDED FOR THE ACTUAL PROJECT 
def mode_selection_Thai(mode=True):
    if mode:
        speak_print("เลือกโหมดที่ต้องการ หากต้องการรายชื่อโหมดพูดศูนย์")
    text = recog_Thai()
    print(f"Your respond: {text}")
    if "1" in text or "หนึ่ง" in text:
        speak_print("คุณต้องการเปิดใช้งานโหมดที่หนึ่ง อ่านหนังสือ ใช่หรือไม่")
        ans = recog_Thai()
        print(f"Your respond: {ans}")
        if "ใช่" in ans or "ค่ะ" in ans or "ครับ" in ans or "เยส" in ans:
            speak_print("โหมดที่หนึ่ง อ่านหนังสือ")
            return 1
        else:
            mode_selection_Thai()
    elif "2" in text or "สอง" in text:
        speak_print("คุณต้องการเปิดใช้งานโหมดที่สอง อ่านและแปลภาษา ใช่หรือไม่") #You want to use mode two translating right?
        ans = recog_Thai()
        print(f"Your respond: {ans}")
        if "ใช่" in ans or "ค่ะ" in ans or "ครับ" in ans or "เยส" in ans:
            speak_print("โหมดที่สอง อ่านและแปลภาษา") #Mode 2: translating has been selected 
            return 2
        else:
            mode_selection_Thai()
    elif "3" in text or "สาม" in text:
        speak_print("คุณต้องการเปิดใช้งานโหมดที่สาม หาวัตถุ ใช่หรือไม่") #You want to use mode three identifying right?
        ans = recog_Thai()
        print(f"Your respond: {ans}")
        if "ใช่" in ans or "ค่ะ" in ans or "ครับ" in ans or "เยส" in ans:
            speak_print("โหมดที่สาม หาวัตถุ") #Mode 3: indentifying has been selected
            return 3
        else:
            mode_selection_Thai()
    elif "4" in text or "สี่" in text:
        speak_print("คุณต้องการเปิดใช้งานโหมดที่สี่ แปลภาษาจากเสียง ใช่หรือไม่") #You want to use mode four translating from voice right?
        ans = recog_Thai()
        print(f"Your respond: {ans}")
        if "ใช่" in ans or "ค่ะ" in ans or "ครับ" in ans or "เยส" in ans:
            speak_print("โหมดที่สี่ แปลภาษาจากเสียง") #Mode 4: translating from voice has been selected
            translate_from_speech_loop()
            return 4
        else:
            mode_selection_Thai()
    elif "0" in text or "ศูนย์" in text:
        speak_print("""
        พูด หนึ่ง เพื่อ ใช้งานโหมดที่หนึ่ง อ่านหนังสือ
        พูด สอง เพื่อ ใช้งานโหมดที่สอง อ่านและแปลภาษา
        พูด สาม เพื่อ ใช้งานโหมดที่สาม หาวัตถุ
        และ พูด สี่ เพื่อ ใช้งานโหมดที่สี่ แปลภาษาจากเสียง
        """)
        mode_selection_Thai(mode=False)
    elif "only fan" in text or "turn on" in text:
        onlyfan()
    else:
        speak_print("ไม่มีโหมดที่เปิดใช้งาน ณ ขณะนี้") #No mode has been selected

        