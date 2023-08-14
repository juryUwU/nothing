import random
import string
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, QObject
from GUIBotVoice import Ui_MainWindow
from time import sleep
import threading
import pyttsx3
import playsound
import datetime 
import speech_recognition as sr
import webbrowser as wb
import os
import wikipedia
from gtts import gTTS
from pyowm import OWM
import pyautogui
import requests
import cv2
from tkinter import *
import tkinter as tk


class communicate(QObject):
    message = pyqtSignal()


class MainWindow(QMainWindow):
    def __init__(self,  *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        QMainWindow.__init__(self)
        self.quitall = True
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.c = communicate()
        self.friday=pyttsx3.init()
        self.voices = self.friday.getProperty('voices')
        self.friday.setProperty('voice', self.voices[1].id)
        self.c.message.connect(self.popup_input_text)

        self.ui.cb_vi.setChecked(True)
        self.ui.cb_en.toggled.connect(self.language)

        self.ui.btn_speak.clicked.connect(self.thread_runVoice)
        self.ui.btn_input.clicked.connect(self.threadRunText)

    def language(self):
        if self.ui.cb_en.isChecked():
            self.ui.label.setText("Status ...")
            self.ui.btn_input.setText("Input Text")
            self.ui.btn_speak.setText("Press to speak")
            self.ui.groupBox_2.setTitle("Select Language")
        elif self.ui.cb_vi.isChecked():
            self.ui.label.setText("Trạng thái ...")
            self.ui.btn_input.setText("Nhập nội dung")
            self.ui.btn_speak.setText("Ấn để nói")
            self.ui.groupBox_2.setTitle("Chọn ngôn ngữ")


    def thread_runVoice(self):
        new_thread = threading.Thread(target=self.runVoice)
        new_thread.start()

    def speak(self, audio):#hàm nói tiếng anh
        print('Juny: ' + audio)
        self.friday.say(audio)
        self.friday.runAndWait()

    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def speak_tv(self,audio):#hàm nói tiếng việt
        print('Juny : '+ audio)
        time= datetime.datetime.now().strftime("%H%M%S%m%d%Y")
        musicfile=str('music' + self.id_generator() + '.mp3')
        tts = gTTS(text=audio , tld = "com.vn" , lang='vi', slow=False)
        tts.save(musicfile)
        playsound.playsound(musicfile)
        os.remove(musicfile)
    
    

    def tell_me_about_cmd(self):
        try:
            self.speak("what do you want to hear about?")
            text = self.command()
            if "who" in text:
                text = text.replace("who","")
            if "what is" in text:
                text = text.replace("it is","")
            wikipedia.set_lang("en")
            contents = wikipedia.summary(text).split('\n')
            self.speak(contents[0])
            for content in contents[1:]:
                self.speak(f"Do you want to hear more about it?")
                ans = self.command()
                if "có" not in ans:
                    break    
                self.speak(content)

            self.speak('Thanks for listen !!!')
            
        except:
            self.speak("NOT FOUND")
    

    def tell_me_about(self):
        try:
            self.speak("what do you want to hear about?")
            text = self.giongnoi()
            if "who" in text:
                text = text.replace("who","")
            if "what is" in text:
                text = text.replace("it is","")
            wikipedia.set_lang("en")
            contents = wikipedia.summary(text).split('\n')
            self.speak(contents[0])
            for content in contents[1:]:
                self.speak(f"Do you want to hear more about it?")
                ans = self.giongnoi()
                if "có" not in ans:
                    break    
                self.speak(content)

            self.speak('Thanks for listen !!!')
            
        except:
            self.speak("NOT FOUND")      

    def tell_me_about_tv(self):
        try:
            self.speak_tv("Bạn muốn nghe về cái gì?")
            text = self.giongnoi_tv()
            if "ai" in text:
                text = text.replace("ai","")
            if "là gì" in text:
                text = text.replace("đó là","")
            wikipedia.set_lang("vi")
            contents = wikipedia.summary(text).split('\n')
            self.speak_tv(contents[0])
            for content in contents[1:]:
                self.speak_tv(f"Bạn có muốn nghe thêm về nó không?")
                ans = self.giongnoi_tv()
                if "có" not in ans:
                    break    
                self.speak_tv(content)

            self.speak_tv('Cảm ơn bạn đã lắng nghe !!!')
            
        except:
            self.speak_tv("KHÔNG TÌM THẤY")

    def welcome(self):
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            self.speak("Good Morning Sir!")
        elif hour>=12 and hour<18:
            self.speak("Good Afternoon Sir!")
        elif hour>=18 and hour<24:
            self.speak("Good Evening sir") 
        self.speak("How can I help you,boss")

    def giongnoi(self):
        while True:
            c=sr.Recognizer()
            with sr.Microphone() as source:
                c.pause_threshold=2
                audio=c.listen(source)
            try:
                query = c.recognize_google(audio,language='en-US')
                print("Tony: "+query)
            except sr.UnknownValueError:
                try:
                    self.speak('''I'm still listening, do you want to continue?''')
                    c=sr.Recognizer()
                    with sr.Microphone() as source:
                        c.pause_threshold=2
                        audio=c.listen(source)
                    query2 = c.recognize_google(audio,language='en-US')
                    print(query2)
                    if "yes" in query2.lower():
                        self.speak('''I'm ready to listen to the command''')
                        continue
                    elif "no" in query2.lower():
                        self.speak('Goodbye')
                        break
                except:
                    self.speak('''I don't understand what you are saying, please enter the command you want here''')
                    query = self.command()
            return query 

    def time(self):
        Time=datetime.datetime.now().strftime("%I:%M:%p") 
        self.speak("It is")
        self.speak(Time)

    def command(self):
        c=sr.Recognizer()
        with sr.Microphone() as source:
            c.pause_threshold=2
            audio=c.listen(source)
        try:
            query = c.recognize_google(audio,language='en-US')
            print("Tony: "+query)
        except sr.UnknownValueError:
            self.speak("Sorry sir! I didn't get that! Try typing the command!")
            query = str(input('Your order is: '))
        return query         
        


    def current_weather(self):#dự báo thời tiết(fix)
        self.speak("Where do you want to see the weather?")
        ow_url = "https://api.openweathermap.org/data/2.5/weather?"
        city = self.command()
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
            self.speak_tv(content)
        else:
            self.speak("Not Found .\
                please type again")

    def face_reg(self):#nhận diện khuôn mặt
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        while(True):
            #Hcamera ghi hình
            ret , frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray)
            for ( x , y , w , h ) in faces :
                cv2.rectangle (frame, (x, y), (x + w, y + h ), (8,255,0), 2)
            cv2.imshow('Detecting Face',frame)
        #ADoi trong 1 miligiay hoac nhan gi de thoạt
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def bmi(self):#thuật toán chỉ số cơ thể
        self.speak("Exception")

    def popup_input_text(self):
        if self.ui.cb_en.isChecked():
            text, pressed = QInputDialog.getText(
                self, 'Input Text', 'Please enter the command here :')
        elif self.ui.cb_vi.isChecked():
            text, pressed = QInputDialog.getText(
                self, 'Nhập nội dung', 'Vui lòng nhập câu lệnh của bạn vào đây :')
        if pressed:
            print(str(text))
            self.text += text
            
    #wikivoice tiếng anh
    def tell_me_about(self):
        try:
            self.speak("what do you want to hear about?")
            text = self.giongnoi()
            if "who" in text:
                text = text.replace("who","")
            if "what is" in text:
                text = text.replace("it is","")
            wikipedia.set_lang("en")
            contents = wikipedia.summary(text).split('\n')
            self.speak(contents[0])
            for content in contents[1:]:
                self.speak(f"Do you want to hear more about it?")
                ans = self.giongnoi()
                if "có" not in ans:
                    break    
                self.speak(content)

            self.speak('Thanks for listen !!!')
            
        except:
            self.speak("NOT FOUND")   

    def welcome_tv(self):
        #Chao hoi
        hour=datetime.datetime.now().hour
        if hour >= 6 and hour<12:
            self.speak_tv("Chào buổi sáng!")
        elif hour>=12 and hour<18:
            self.speak_tv("Chào buổi chiều!")
        elif hour>=18 and hour<24:
            self.speak_tv("Chào buổi tối") 
        self.speak_tv("Tôi có thể giúp gì cho bạn") 

    def tell_me_about_cmd_tv(self):
        try:
            self.speak_tv("Bạn muốn nghe về cái gì?")
            text = self.command()
            if "ai" in text:
                text = text.replace("ai","")
            if "là gì" in text:
                text = text.replace("đó là","")
            wikipedia.set_lang("vi")
            contents = wikipedia.summary(text).split('\n')
            self.speak_tv(contents[0])
            for content in contents[1:]:
                self.speak_tv(f"Bạn có muốn nghe thêm về nó không?")
                ans = self.command()
                if "có" not in ans:
                    break    
                self.speak_tv(content)

            self.speak_tv('Cảm ơn bạn đã lắng nghe !!!')
            
        except:
            self.speak_tv("KHÔNG TÌM THẤY")
    
    def giongnoi_tv(self):
        while True:
            c=sr.Recognizer()
            with sr.Microphone() as source:
                c.pause_threshold=2
                audio=c.listen(source)
                
            try:
                query = c.recognize_google(audio,language='vi-VN')
                print("Tony: "+query)
            except sr.UnknownValueError:
                try:
                    self.speak_tv('Tôi vẫn đang lắng nghe, bạn có muốn tiếp tục không')
                    c=sr.Recognizer()
                    with sr.Microphone() as source:
                        c.pause_threshold=2
                        audio=c.listen(source)
                    query2 = c.recognize_google(audio,language='vi-VN')
                    print(query2)
                    if "có" in query2.lower():
                        self.speak_tv('Tôi đang sẵn sàng lắng nghe câu lệnh')
                        continue
                    elif "không" in query2.lower():
                        self.speak_tv('Tạm biệt bạn')
                        break
                except:
                    self.speak_tv('Tôi không hiểu bạn nói gì, vui lòng nhập câu lệnh bạn muốn vào đây')
                    query = self.command()
            return query             

    def runVoice(self):
        if self.ui.cb_en.isChecked():
            self.speak("English language")
            self.welcome()
            try:
                while True:
                    self.ui.label.setText("I'm listening to you...") # Set trạng thái label
                    query=self.giongnoi().lower()   
                        #All the giongnoi will store in lower case for easy recognition
                    if "google" in query:
                            self.speak("What should I search,boss")
                            search=self.giongnoi().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            self.speak(f'Here is your {search} on google')
                            
                    elif "youtube" in query:
                            self.speak("What should I search,boss")
                            search=self.giongnoi().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            self.speak(f'Here is your {search} on youtube')

                    elif "quit" in query:
                            self.speak("Juny is off. Goodbye boss")
                            quit()
                    elif "open video" in query:
                            namevideo = ""
                            meme = os.getcwd() + "\Video\{}".format(namevideo)
                            os.startfile(meme)
                    elif 'time' in query:
                                self.time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            self.speak(f"here is your Facebook")    
                    elif "weather" in query:
                            #speak("here your application weather")
                            self.current_weather()

                    elif "screenshot" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            self.speak("the screen has been captured")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            self.speak("Here your chrome")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            self.speak("here your command promt")
                    elif "face" in query:
                            self.speak("Here your face regconition")  
                            self.face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            self.speak("here your messages")
                    elif "bmi" in query:
                            self.speak("here your BMI application")
                            self.bmi()    
                    elif "calculator" in query:
                        self.speak("here you calculator application")
                        calc = Calculator()
                        calc.run()
                    elif "wikipedia" in query:
                        self.tell_me_about()
            except:
                self.speak("If you need me, press the button to order")  

        if self.ui.cb_vi.isChecked():
            self.welcome_tv()
            try:
                while True:
                    self.ui.label.setText("Tôi đang lắng nghe bạn ...") # Set trạng thái label
                    query=self.giongnoi_tv().lower()
                        #All the command will store in lower case for easy recognition
                    if "google" in query:
                            self.speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=self.giongnoi_tv().lower()
                            url = f"https://google.com/search?q={search}"
                            wb.get().open(url)
                            self.speak_tv(f'đây là {search} trên google')
                            
                    elif "youtube" in query:
                            self.speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                            search=self.giongnoi_tv().lower()
                            url = f"https://youtube.com/search?q={search}"
                            wb.get().open(url)
                            self.speak_tv(f'đây là {search} trên youtube')

                    elif "thoát" in query:
                            self.speak_tv("Juny đã tắt. chúc bạn có 1 ngày tốt lành.")
                            quit()
                    elif "mở video" in query:
                            meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                            os.startfile(meme)
                    elif 'mấy giờ' in query:
                                self.time()    
                    elif "facebook" in query:
                            url = f"https://facebook.com"
                            wb.get().open(url)          
                            self.speak_tv(f"đây là Facebook của bạn")    
                    elif "thời tiết" in query:
                            self.speak_tv("đây là ứng dụng thời tiết của bạn")
                            self.current_weather()

                    elif "chụp màn hình" in query:
                            myScreenshot = pyautogui.screenshot()
                            myScreenshot.save(r'ảnh.png') 
                            self.speak_tv("ảnh màn hình đã được chụp")    
                    elif "chrome" in query:
                            os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                            self.speak_tv("đây là Chrome của bạn")
                    elif "cmd" in query:
                            os.startfile("C:\WINDOWS\system32\cmd.exe")
                            self.speak_tv("đây là cmd của bạn")
                    elif "nhận diện khuôn mặt" in query:
                            self.speak_tv("đây là trình nhận diện khuôn mặt")  
                            self.face_reg()
                    elif "mess" in query:
                            url = f"facebook.com/messages"
                            wb.get().open(url)    
                            self.speak_tv("đây là messages của bạn")
                    elif "bmi" in query:
                            self.speak_tv("đây là ứng dụng tính chỉ số đo cơ thể")
                            self.bmi()    
                    elif "máy tính" in query:
                        self.speak_tv("đây là ứng dụng máy tính")
                        calc = Calculator()
                        calc.run()
                            
                    elif "wikipedia" in query:
                        self.tell_me_about_cmd_tv()
            except:
                self.speak_tv("Nếu bạn cần tôi, hãy bấm nút để ra lệnh")     

    def command(self):
        self.text = ""
        self.c.message.emit()
        while True:
            if len(self.text) == 0:
                sleep(1)
            else:
                return self.text

    def threadRunText(self):
        new_thread = threading.Thread(target=self.runText)
        new_thread.start()

    def runText(self):
        if self.ui.cb_vi.isChecked():
            self.welcome_tv()
            while True:
                self.ui.label.setText("Tôi đang chờ câu lệnh từ bạn ...")
                query=self.command()
                    #All the command will store in lower case for easy recognition
                if "google" in query:
                        self.speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                        search=self.command().lower()
                        url = f"https://google.com/search?q={search}"
                        wb.get().open(url)
                        self.speak_tv(f'đây là {search} trên google')
                        
                elif "youtube" in query:
                        self.speak_tv("tôi có thể tìm kiếm gì cho bạn?")
                        search=self.command().lower()
                        url = f"https://youtube.com/search?q={search}"
                        wb.get().open(url)
                        self.speak_tv(f'đây là {search} trên youtube')

                elif "thoát" in query:
                        self.speak_tv("Juny đã tắt. chúc bạn có 1 ngày tốt lành.")
                        quit()
                elif "mở video" in query:
                        meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                        os.startfile(meme)
                elif 'mấy giờ' in query:
                            self.time()    
                elif "facebook" in query:
                        url = f"https://facebook.com"
                        wb.get().open(url)          
                        self.speak_tv(f"đây là Facebook của bạn")    
                elif "thời tiết" in query:
                        self.speak_tv("đây là ứng dụng thời tiết của bạn")
                        self.current_weather()

                elif "chụp màn hình" in query:
                        myScreenshot = pyautogui.screenshot()
                        myScreenshot.save(r'ảnh.png') 
                        self.speak_tv("ảnh màn hình đã được chụp")    
                elif "chrome" in query:
                        os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                        self.speak_tv("đây là Chrome của bạn")
                elif "cmd" in query:
                        os.startfile("C:\WINDOWS\system32\cmd.exe")
                        self.speak_tv("đây là cmd của bạn")
                elif "nhận diện khuôn mặt" in query:
                        self.speak_tv("đây là trình nhận diện khuôn mặt")  
                        self.face_reg()
                elif "mess" in query:
                        url = f"facebook.com/messages"
                        wb.get().open(url)    
                        self.speak_tv("đây là messages của bạn")
                elif "bmi" in query:
                        self.speak_tv("đây là ứng dụng tính chỉ số đo cơ thể")
                        self.bmi()    
                elif "máy tính" in query:
                    self.speak_tv("đây là ứng dụng máy tính")
                    if __name__ == "__main__":
                        calc = Calculator()
                        calc.run()
                        
                elif "wikipedia" in query:
                    self.tell_me_about_cmd_tv()
                
                else:
                    self.speak_tv("Tôi không hiểu câu lệnh của bạn")

        if self.ui.cb_en.isChecked():
            self.welcome()
            while True:
                self.ui.label.setText("I'm waiting for your order ...")
                query=self.command().lower()   
                    #All the command will store in lower case for easy recognition
                if "google" in query:
                        self.speak("What should I search,boss")
                        search=self.command().lower()
                        url = f"https://google.com/search?q={search}"
                        wb.get().open(url)
                        self.speak(f'Here is your {search} on google')
                        
                elif "youtube" in query:
                        self.speak("What should I search,boss")
                        search=self.command().lower()
                        url = f"https://youtube.com/search?q={search}"
                        wb.get().open(url)
                        self.speak(f'Here is your {search} on youtube')

                elif "quit" in query:
                        self.speak("Juny is off. Goodbye boss")
                        quit()
                elif "open video" in query:
                        meme =r"C:\Users\Admin\Desktop\test\meme.mp4"
                        os.startfile(meme)
                elif 'time' in query:
                            self.time()    
                elif "facebook" in query:
                        url = f"https://facebook.com"
                        wb.get().open(url)          
                        self.speak(f"here is your Facebook")    
                elif "weather" in query:
                        #speak("here your application weather")
                        self.current_weather()

                elif "screenshot" in query:
                        myScreenshot = pyautogui.screenshot()
                        myScreenshot.save(r'ảnh.png') 
                        self.speak("the screen has been captured")    
                elif "chrome" in query:
                        os.startfile("C:\Program Files\Google\Chrome\Application\CHROME.exe")
                        self.speak("Here your chrome")
                elif "cmd" in query:
                        os.startfile("C:\WINDOWS\system32\cmd.exe")
                        self.speak("here your command promt")
                elif "face" in query:
                        self.speak("Here your face regconition")  
                        self.face_reg()
                elif "mess" in query:
                        url = f"facebook.com/messages"
                        wb.get().open(url)    
                        self.speak("here your messages")
                elif "bmi" in query:
                        self.speak("here your BMI application")
                        self.bmi()    
                elif "calculator" in query:
                    self.speak("here you calculator application")
                    calc = Calculator()
                    calc.run()
                        
                elif "wikipedia" in query:
                    self.tell_me_about_cmd()
                else:
                    self.speak("I don't understand your command")




LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
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
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())