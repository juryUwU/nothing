#khai báo thư viện (input library)

import pyttsx3
import datetime 
import speech_recognition as sr
import webbrowser as wb
import os
from pyowm import OWM
from subprocess import *
#import cv2
import numpy as np
import pyautogui
from tkinter import *
import tkinter as tk
import requests
import wikipedia
from gtts import gTTS
import playsound
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"



friday=pyttsx3.init()
voices = friday.getProperty('voices')
friday.setProperty('voice', voices[1].id) 


class Calculator:#Máy tính
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x600")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()



def face_reg():#nhận diện khuôn mặt
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while(True):
        #Hcamera ghi hình
        ret , frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for ( x , y , w , h ) in faces :
            cv2.rectangle (frame, (x, y), (x + w, y + h ), (8,255,0), 2)
        cv2.imshow('Detecting face',frame)
   #ADoi trong 1 miligiay hoac nhan gi de thoạt
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cap.release ( )
    cv2.destroyAllWindows()     
def bmi():#thuật toán chỉ số cơ thể
    a = Tk()
    a.title("Chương trình tính chỉ số đo cơ thể")
    a.geometry("300x400")
    a.attributes("-topmost", True)
    
    #background_image = PhotoImage(file='cyanbg.png')
    #background_label = Label(a, image=background_image)
    #background_label.place(relwidth=1, relheight=1)
    #tạo ra label1
    name1 = Label(a, font = ("Arial",10), text = "Nhập Chiều Cao(m): ")
    name1.place(x = 10, y = 10)
    #tạo ra label2
    name2 = Label(a, font = ("Arial",10), text = "Nhập Cân nặng(kg): ")
    name2.place(x = 10, y = 50)
    #tạo ra label3
    #tạo ra entry1
    entry = Entry(a, width = 15, font = ("Time New Roman",10))
    entry.place(x = 160, y = 10)
    entry.focus()
    #tạo ra entry2
    entry2 = Entry(a, width = 15, font = ("Time New Roman",10))
    entry2.place(x = 160, y = 50)
    #def dieukien():
        
    #Tạo ra button
    def anvao():
        name1 = Label(a , font = ("Arial",10), text =  "Chỉ số BMI của bạn là: " + str(float(entry2.get()) /( float(entry.get()) * 2)), fg="red")
        name1.place(x= 20, y = 110)
        name3 = Label(a, font = ("Arial",10), text = "BMI <18,5 : Bạn đang gầy")
        name3.place(x = 10, y = 140)
        #tạo ra label4
        name4 = Label(a, font = ("Arial",10), text = "BMI = 18,5 - 22,9: Bạn đang bình thường")
        name4.place(x = 10, y = 160)
        #tạo ra label5
        name5 = Label(a, font = ("Arial",10), text = "BMI >=23,0 : Bạn đang thừa cân")
        name5.place(x = 10, y = 180)
        #tạo ra label6
        name6 = Label(a, font = ("Arial",10), text = "BMI > 25,0 : Bạn đang béo phì")
        name6.place(x = 10, y = 200)
    but = Button(a, text = "Tính Toán", width = 10, height = 1, font = ("Time New Roman",10), command = anvao )
    but.place(x=105 , y = 80)

    a.mainloop()    
def current_weather():#dự báo thời tiết(fix)
    speak("Where do you want to see the weather?")
    ow_url = "https://api.openweathermap.org/data/2.5/weather?"
    city = command()
    if not city:
        pass
    api_key = "d2715dcf1ff713e59095eddc07088c23"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        visibility = data["visibility"]
        wind = data["wind"]
        wind_speed = wind["speed"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Thời tiết tại {city} ngày {day} tháng {month} năm {year} lúc {hour} giờ {minute} phút là
        Nhiệt độ {temp} độ C
        Áp suất không khí {pressure} hetopascal 
        Độ ẩm {humidity}%
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Tầm nhìn xa trên {visibility} met
        Tốc độ gió khoảng {wind} met trên giây
        """.format(city=city, hour=now.hour,minute=now.minute,\
         day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour,\
          minrise = sunrise.minute,hourset = sunset.hour, minset = sunset.minute,\
        wind=wind_speed, visibility=visibility, temp = current_temperature,\
         pressure = current_pressure, humidity = current_humidity)
        print(content)
    else:
        speak("Not Found .\
            please type again")

dk = ""  
HEIGHT = 500
WIDTH = 600
def weather():#dự báo thời tiết final
    def test_function(entry):
        print("This is the entry:", entry)

    # api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
    # a4aa5e3d83ffefaba8c00284de6ef7c3

    def format_response(weather):
        try:
            name = weather['name']
            desc = weather['weather'][0]['description']
            temp = float(weather['main']['temp'])
            doc = (temp - 32)*0.555
            final_str = 'City: %s \nConditions: %s \nTemperature (°C): %s' % (name, desc, doc)
        except:
            final_str = 'There was a problem retrieving that information'

        return final_str

    def get_weather(city):
        weather_key = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=params)
        weather = response.json()

        label['text'] = format_response(weather)



    root = tk.Tk()
    root = tk.title("Weather")
    canvas = tk.Canvas(root, height= HEIGHT, width= WIDTH)
    canvas.pack()

    background_image = tk.PhotoImage(file='landscape.png')
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

    entry = tk.Entry(frame, font=40)
    entry.place(relwidth=0.65, relheight=1)

    button = tk.Button(frame, text="Get Weather", font=40, command=lambda: get_weather(entry.get()))
    button.place(relx=0.7, relheight=1, relwidth=0.3)

    lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

    label = tk.Label(lower_frame)
    label.place(relwidth=1, relheight=1)

    root.mainloop()
def speak_tv(audio):#hàm nói tiếng việt
    print('Juny : '+ audio)
    time= datetime.datetime.now().strftime("%H%M%S%m%d%Y")
    musicfile=str('music' + time + '.mp3')
    tts = gTTS(text=audio , tld = "com.vn" , lang='vi', slow=False)
    tts.save(musicfile)
    playsound.playsound(musicfile)
def speak(audio):#hàm nói tiếng anh
    print('Juny: ' + audio)
    friday.say(audio)
    friday.runAndWait()
dk = ""    
#wikicmd tiếng anh(phần command tiếng anh)
def tell_me_about_cmd():
    try:
        speak("what do you want to hear about?")
        text = command()
        if "who" in text:
            text = text.replace("who","")
        if "what is" in text:
            text = text.replace("it is","")
        wikipedia.set_lang("en")
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        for content in contents[1:]:
            speak(f"Do you want to hear more about it?")
            ans = command()
            if "có" not in ans:
                break    
            speak(content)

        speak('Thanks for listen !!!')
        
    except:
        speak("NOT FOUND")
#wikicmd tiếng việt (phần command tiếng việt)
def tell_me_about_cmd_tv():
    try:
        speak_tv("Bạn muốn nghe về cái gì?")
        text = command()
        if "ai" in text:
            text = text.replace("ai","")
        if "là gì" in text:
            text = text.replace("đó là","")
        wikipedia.set_lang("vi")
        contents = wikipedia.summary(text).split('\n')
        speak_tv(contents[0])
        for content in contents[1:]:
            speak_tv(f"Bạn có muốn nghe thêm về nó không?")
            ans = command()
            if "có" not in ans:
                break    
            speak_tv(content)

        speak_tv('Cảm ơn bạn đã lắng nghe !!!')
        
    except:
        speak_tv("KHÔNG TÌM THẤY")
#wikivoice tiếng anh
def tell_me_about():
    try:
        speak("what do you want to hear about?")
        text = giongnoi()
        if "who" in text:
            text = text.replace("who","")
        if "what is" in text:
            text = text.replace("it is","")
        wikipedia.set_lang("en")
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        for content in contents[1:]:
            speak(f"Do you want to hear more about it?")
            ans = giongnoi()
            if "có" not in ans:
                break    
            speak(content)

        speak('Thanks for listen !!!')
        
    except:
        speak("NOT FOUND")        
#wikivoice tiếng việt
def tell_me_about_tv():
    try:
        speak_tv("Bạn muốn nghe về cái gì?")
        text = giongnoi_tv()
        if "ai" in text:
            text = text.replace("ai","")
        if "là gì" in text:
            text = text.replace("đó là","")
        wikipedia.set_lang("vi")
        contents = wikipedia.summary(text).split('\n')
        speak_tv(contents[0])
        for content in contents[1:]:
            speak_tv(f"Bạn có muốn nghe thêm về nó không?")
            ans = giongnoi_tv()
            if "có" not in ans:
                break    
            speak_tv(content)

        speak_tv('Cảm ơn bạn đã lắng nghe !!!')
        
    except:
        speak_tv("KHÔNG TÌM THẤY")

def time():
    Time=datetime.datetime.now().strftime("%I:%M:%p") 
    speak("It is")
    speak(Time)
def welcome():
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            speak("Good Morning Sir!")
        elif hour>=12 and hour<18:
            speak("Good Afternoon Sir!")
        elif hour>=18 and hour<24:
            speak("Good Evening sir") 
        speak("How can I help you,boss")         
def welcome_tv():
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            speak_tv("Chào buổi sáng!")
        elif hour>=12 and hour<18:
            speak_tv("Chào buổi chiều!")
        elif hour>=18 and hour<24:
            speak_tv("Chào buổi tối") 
        speak_tv("Tôi có thể giúp gì cho bạn")         
def nhap():
    speak("Hello!, please choose input method: ")
    speak("1.Voice          2.Keyboard")
    speak("please choose 1 or 2")
    nhap = str(input("Your choose:"))
def command_tv():
    query = str(input('Yêu cầu của bạn là: '))
    return query

def command():
    query = str(input('Your order is: '))
    return query   
def giongnoi():
    c=sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold=2
        audio=c.listen(source)
    try:
        query = c.recognize_google(audio,language='en-US')
        print("Tony: "+query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Your order is: '))
    return query         
def giongnoi_tv():
    c=sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold=2
        audio=c.listen(source)
        
    try:
        query = c.recognize_google(audio,language='vi-VN')
        print("Tony: "+query)
    except sr.UnknownValueError:
        print('Xin lỗi tôi không thể hiểu, hãy thử lại bằng cách nhập!')
        query = str(input('Yêu cầu của bạn là: '))
    return query             
def choose():
    speak("Please choose your language")
    speak("1.English        2.Tiếng Việt")
    tam = str(input("Your answer: "))
    if tam =="1":
        speak("please choose input method")
        speak("1.Keyboard       2.Voice")
        temp  = str(input("Your anwers:"))
    elif tam =="2":
        speak_tv("Hãy chọn cách nhập của bạn")
        speak_tv("1.Bàn Phím    2.Giọng Nói")
        temp = str(input("Câu trả lời của bạn: "))
    if tam == "1":
        if temp == "1":
            if __name__  =="__main__": #Keyboard-EN
                #nhap()
                
                welcome()
                
                while True:
                    query=command().lower()   
                        #All the command will store in lower case for easy recognition
                    if "google" in query:
                            speak("What should I search,boss")
                            search=command().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on google')
                            
                    elif "youtube" in query:
                            speak("What should I search,boss")
                            search=command().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on youtube')

                    elif "quit" in query:
                            speak("Juny is off. Goodbye boss")
                            quit()
                    elif "open video" in query:
                            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                            os.startfile(meme)
                    elif 'time' in query:
                                time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            speak(f"here is your Facebook")    
                    elif "weather" in query:
                            #speak("here your application weather")
                            current_weather()

                    elif "screenshot" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            speak("the screen has been captured")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            speak("Here your chrome")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            speak("here your command promt")
                    elif "face" in query:
                            speak("Here your face regconition")  
                            face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            speak("here your messages")
                    elif "bmi" in query:
                            speak("here your BMI application")
                            bmi()    
                    elif "calculator" in query:
                        speak("here you calculator application")
                        if __name__ == "__main__":
                            calc = Calculator()
                            calc.run()
                            
                    elif "wikipedia" in query:
                        tell_me_about_cmd()
                    elif "change" in query:
                        choose()    
        elif temp == "2":
            if __name__  =="__main__": #Voice-EN
                #nhap()
                
                welcome()
                
                while True:
                    query=giongnoi().lower()   
                        #All the giongnoi will store in lower case for easy recognition
                    if "google" in query:
                            speak("What should I search,boss")
                            search=giongnoi().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on google')
                            
                    elif "youtube" in query:
                            speak("What should I search,boss")
                            search=giongnoi().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            speak(f'Here is your {search} on youtube')

                    elif "quit" in query:
                            speak("Juny is off. Goodbye boss")
                            quit()
                    elif "open video" in query:
                            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                            os.startfile(meme)
                    elif 'time' in query:
                                time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            speak(f"here is your Facebook")    
                    elif "weather" in query:
                            #speak("here your application weather")
                            current_weather()

                    elif "screenshot" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            speak("the screen has been captured")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            speak("Here your chrome")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            speak("here your command promt")
                    elif "face" in query:
                            speak("Here your face regconition")  
                            face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            speak("here your messages")
                    elif "bmi" in query:
                            speak("here your BMI application")
                            bmi()    
                    elif "calculator" in query:
                        speak("here you calculator application")
                        if __name__ == "__main__":
                            calc = Calculator()
                            calc.run()
                    elif "wikipedia" in query:
                        tell_me_about()
                    elif "change" in query:
                        choose()    
    elif tam == "2":
        if temp == "1":
            if __name__  =="__main__": #Keyboard-VN
                #nhap()
                
                welcome_tv()
                
                while True:
                    query=command_tv().lower()   
                        #All the command will store in lower case for easy recognition
                    if "google" in query:
                            speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=command_tv().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            speak_tv(f'đây là {search} trên google')
                            
                    elif "youtube" in query:
                            speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=command_tv().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            speak_tv(f'đây là {search} trên youtube')

                    elif "quit" in query:
                            speak_tv("Juny đã tắt. chúc bạn có 1 ngày tốt lành.")
                            quit()
                    elif "open video" in query:
                            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                            os.startfile(meme)
                    elif 'time' in query:
                                time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            speak_tv(f"đây là Facebook của bạn")    
                    elif "weather" in query:
                            speak_tv("đây là ứng dụng thời tiết của bạn")
                            current_weather()

                    elif "screenshot" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            speak_tv("ảnh màn hình đã được chụp")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            speak_tv("đây là Chrome của bạn")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            speak_tv("đây là cmd của bạn")
                    elif "face" in query:
                            speak_tv("đây là trình nhận diện khuôn mặt")  
                            face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            speak_tv("đây là messages của bạn")
                    elif "bmi" in query:
                            speak_tv("đây là ứng dụng tính chỉ số đo cơ thể")
                            bmi()    
                    elif "calculator" in query:
                        speak_tv("đây là ứng dụng máy tính")
                        if __name__ == "__main__":
                            calc = Calculator()
                            calc.run()
                            
                    elif "wikipedia" in query:
                        tell_me_about_cmd_tv()
                    elif "change" in query:
                        choose()    
        elif temp == "2":
            if __name__  =="__main__": #Voice-VN
                #nhap()
                
                welcome_tv()
                
                while True:
                    query=giongnoi_tv().lower()   
                        #All the command will store in lower case for easy recognition
                    if "google" in query:
                            speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=giongnoi_tv().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            speak_tv(f'đây là {search} trên google')
                            
                    elif "youtube" in query:
                            speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=giongnoi_tv().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            speak_tv(f'đây là {search} trên youtube')

                    elif "quit" in query:
                            speak_tv("Juny đã tắt. chúc bạn có 1 ngày tốt lành.")
                            quit()
                    elif "open video" in query:
                            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                            os.startfile(meme)
                    elif 'time' in query:
                                time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            speak_tv(f"đây là Facebook của bạn")    
                    elif "weather" in query:
                            speak_tv("đây là ứng dụng thời tiết của bạn")
                            current_weather()

                    elif "screenshot" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            speak_tv("ảnh màn hình đã được chụp")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            speak_tv("đây là Chrome của bạn")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            speak_tv("đây là cmd của bạn")
                    elif "face" in query:
                            speak_tv("đây là trình nhận diện khuôn mặt")  
                            face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            speak_tv("đây là messages của bạn")
                    elif "bmi" in query:
                            speak_tv("đây là ứng dụng tính chỉ số đo cơ thể")
                            bmi()    
                    elif "calculator" in query:
                        speak_tv("đây là ứng dụng máy tính")
                        if __name__ == "__main__":
                            calc = Calculator()
                            calc.run()
                            
                    elif "wikipedia" in query:
                        tell_me_about_cmd_tv()
                    elif "change" in query:
                        choose()    

choose()


            

           