
########################
#                                       #
#       주석 지우지 말것
#       kivy                           #
#       커뮤니티 활동
#       yona
#       okky
#       분석 설계 구현 검증
#                                       #
########################

import time
import locale
import requests
import json
import feedparser
import threading
import datetime
import subprocess
import os
import tkinter
import forecastio


from random import sample
from tkinter import *
from tkinter import ttk

from tkinter import messagebox
from PIL import Image, ImageTk
from contextlib import contextmanager

text_xsmall = 15
text_small = 20
text_medium = 25
text_big = 45
text_xlarge = 90

latitude = None
longitude = None

weather_api = '0f4eba3ba474e004be5a7b11986d8bd6'
weather_lang = 'ko'
weather_unit = 'auto'

weather_icons = {
    'clear-day': 'weather_icon/Sun.png',
    'wind': 'weather_icon/Wind.png',
    'cloudy': 'weather_icon/Cloud.png',
    'partly-cloudy-day': "weather_icon/PartlySunny.png",
    'rain': "weather_icon/Rain.png",
    'snow': "weather_icon/Snow.png",
    'snow-thin': "weather_icon/Snow.png",
    'fog': "weather_icon/Haze.png",
    'clear-night': "weather_icon/Moon.png",
    'partly-cloudy-night': "weather_icon/PartlyMoon.png",
    'thunderstorm': "weather_icon/Storm.png",
    'tornado': "weather_icon/Tornado.png",
    'hail': "weather_icon/Hail.png"
}

recommend_icon = 'Icon/Recommendation.png'
youtube_icon = 'Icon/YouTube.png'


class FaceRecognition(Frame):

    def __new__(self):
        client_id = "kJE6_Me4KcxkDvJ_JIKI"
        client_secret = "QC1yX6yao0"

        url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
        files = {'image': open('유재석.png', 'rb')}
        headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code
        # if(rescode==200):
        #     print (response.text)
        # else:
        #     print("Error Code:" + rescode)

        #print(json.dumps(json.loads(response.text), indent = 4, ensure_ascii=False))

        detect_result = json.loads(response.text)

        detect_summary = detect_result['faces'][0] # 여기서 가끔 out of range라고 에러 뜸
        x, y, w, h = detect_summary['roi'].values()
        gender, gen_confidence = detect_summary['gender'].values()
        emotion, emotion_confidence = detect_summary['emotion'].values()
        #age, age_confidence = detect_summary['age'].values()

        who = 0
        png_file_name = f'{who}.png'
        # txt_file_name = f'{who}.png.txt'
        if os.path.isfile(png_file_name):
            os.remove(png_file_name)
            # os.remove(txt_file_name)
            file_name = f'{who+1}.png'

        #======================================================================

        img_face = Image.open('유재석.png')
        img_face_cropped = img_face.crop((x-30, y-30, x+w+50, y+h+50))
        img_face_cropped = img_face_cropped.resize((300, 300))
        # img_face_cropped.show()
        img_face_cropped.save(png_file_name)

        #======================================================================

        # annotation = gender + ' : ' + str(gen_confidence) + \
        #                 '\n' + emotion + ' : ' + str(emotion_confidence) + \
        #                 '\n' + age + ' : ' + str(age_confidence)+'\n'
        # print(annotation)

        result = []
        result.append(gender)
        result.append(emotion)
        # #result.append(age)

        # print(result)
        return gender, emotion

        # f = open(f'{png_file_name}.txt', mode = 'wt', encoding = 'utf-8')
        # f.write(gender+'\n')
        # f.write(emotion+'\n')
        # f.write(age+'\n')
        # f.close()

class Time(Frame):

    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # Get Time
        self.time = time.strftime('%H:%M')
        self.date = time.strftime('%A, %d. %B')

        # Make Time Labels
        self.timeLabel = Label(self, font=(
            'Helvetica', text_big), text=self.time, fg='white', bg='black')
        self.dateLabel = Label(self, font=(
            'Helvetica', text_small), text=self.date, fg='white', bg='black')

        # Display Labels
        self.timeLabel.pack(side=TOP, anchor=W)
        self.dateLabel.pack(side=TOP, anchor=W)


class Weather(Frame):

    def get_ip(self):
        try:
            url = 'http://jsonip.com'
            req = requests.get(url)
            ip_json = json.loads(req.text)
            ip = ip_json['ip']
            return ip

        except Exception as e:
            return 'Error: %s. Cannot get ip'

    def get_weather(self):
        try:
            if latitude is None and longitude is None:
                # get location
                api_key = 'df8e1a9da2cf6464817b3b30e43c08ce'  # IP Stack Api Key
                url = 'http://api.ipstack.com/{}?access_key={}'.format(self.get_ip(), api_key)
                req = requests.get(url)
                res = json.loads(req.text)

                # set location
                lat = res['latitude']
                lon = res['longitude']
                location2 = '%s' % (res['city'])

                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, lat, lon, weather_lang, weather_unit)
            else:
                location = ''
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, latitude, longitude, weather_lang, weather_unit)

            req = requests.get(weather_req_url)
            weather = json.loads(req.text)

            degree_sign = u'\N{DEGREE SIGN}'
            temperature2 = '{}{}'.format(
                int(weather['currently']['temperature']), degree_sign)
            weather_summary2 = weather['currently']['summary']
            icon_id = weather['currently']['icon']
            weather_icon2 = None

            if icon_id in weather_icons:
                weather_icon2 = weather_icons[icon_id]

            if weather_icon2 is not None:
                if self.weather_icon != weather_icon2:
                    self.weather_icon = weather_icon2
                    image = Image.open(weather_icon2)
                    image = image.resize((65, 65), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLabel.config(image=photo)
                    self.iconLabel.image = photo
            else:
                # remove image
                self.iconLabel.config(image='')

            # set attributes
            if self.weather_summary != weather_summary2:
                self.weather_summary = weather_summary2
                self.summaryLabel.config(text=weather_summary2)

            if self.temperature != temperature2:
                self.temperature = temperature2
                self.tempLabel.config(text=temperature2)

            if self.location != location2:
                if location2 == ', ':
                    self.location = '지역을 찾을수 없습니다'
                    self.locationLabel.config(text='지역을 찾을수 없습니다')
                else:
                    self.location = location2
                    self.locationLabel.config(text='지역 : {}'.format(location2))


        except Exception as e:
            print('Error {}. 날씨를 찾을수 없습니다'.format(e))

        self.after(60000, self.get_weather)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # Init attributes
        self.temperature = ''
        self.location = ''
        self.weather_summary = ''
        self.weather_icon = None
        # Make Widgets
        self.weather_frame = Frame(self, bg='black')
        self.weather_frame.pack(side=TOP, anchor=W)

        self.tempLabel = Label(self.weather_frame, font=(
            'Helvetica', text_xlarge), fg='white', bg='black')
        self.tempLabel.pack(side=LEFT, anchor=N)

        self.iconLabel = Label(self.weather_frame, bg='black')
        self.iconLabel.pack(side=LEFT, anchor=N, padx=20, pady=20)

        self.summaryLabel = Label(self, font=(
            'Helvetica', text_small), fg='white', bg='black')
        self.summaryLabel.pack(side=TOP, anchor=E)

        self.locationLabel = Label(self, font=(
            'Helvetica', text_xsmall), fg='white', bg='black')
        self.locationLabel.pack(side=TOP, anchor=E)

        self.get_weather()


class Recommend(Frame):

    def click(self, event):
        user_gender, user_emotion = FaceRecognition()

        #p = subprocess.Popen(["recommend_ver1.py"], stdout=subprocess.PIPE)
        #recommend_py = 'recommend_ver4.py'

        # 한양대학교 ERICA캠퍼스
        lat = 37.297178
        lng = 126.834285

        forecast = forecastio.load_forecast(weather_api, lat, lng)
        weather = forecast.currently()
        temperature = weather.temperature
        season = ""

        if(temperature >= 10 or temperature <= 22): season = "springfall"
        elif(temperature > 22): season = "summer"
        else: season = "winter"

        user_style = subprocess.check_output(['python', 'recommend_ver4.py'], universal_newlines = True)
        user_style = user_style[:-1]
        print(user_gender, user_emotion, user_style, season)

        file = open('user_info.txt','w')
        file.write(user_gender + "\n")
        file.write(user_style + "\n")
        file.write(season)
        file.close()

        result = subprocess.check_output(['python', 'box.py'], universal_newlines=True)
        print(result)


    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # make Label
        Label(self, text="오늘의 옷추천", font=('맑은 고딕', text_xsmall), fg='white',
              bg='black').pack(side=BOTTOM, pady=10)

        #setting image
        image = Image.open(recommend_icon)
        image = image.resize((200, 240), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        # make button
        label = Label(self, image=photo, bg='black')
        label.image = photo
        label.bind("<Button>", self.click)
        label.pack(side=BOTTOM, anchor=W)


class Tube(Frame):

    def click(self, event):
        messagebox.showinfo("massage Box", "Youtube")
        # thread = threading.Thread(target=self.stream, args=(self,))
        # thread.daemon = 1
        # thread.start()


    def __init__(self, parent, *args, **krwargs):
        Frame.__init__(self, parent, bg='black')

        # Init attributes

        # make Label
        Label(self, text="YouTube", font=('맑은 고딕', text_xsmall), fg='white',
              bg='black',).pack(side=BOTTOM, pady=10)

        #setting image
        image = Image.open(youtube_icon)
        image = image.resize((240, 200), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        # make button
        label = Label(self, image=photo, bg='black')
        label.image = photo
        label.bind("<Button>", self.click)
        label.pack(side=BOTTOM, anchor=W)


class Screen:

    def __init__(self):
        self.tk = Tk()
        self.state = False
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background='black')
        self.bottomFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.centerTopFrame = Frame(self.tk, background='black')
        self.centerTopFrame.pack(side=TOP, fill=X, expand=YES)
        self.centerBottomFrame = Frame(self.tk, background='black')
        self.centerBottomFrame.pack(side=TOP, fill=Y, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.tk.bind('<Return>', self.toggle_fullscreen)
        self.tk.bind('<Escape>', self.end_fullscreen)

        self.time = Time(self.topFrame)
        self.time.pack(side=LEFT, anchor=N, padx=100, pady=60)

        self.weather = Weather(self.topFrame)
        self.weather.pack(side=RIGHT, anchor=N, padx=100, pady=60)

        self.recommend = Recommend(self.bottomFrame)
        self.recommend.pack(side=LEFT, anchor=N, padx=50, pady=20)

        self.tube = Tube(self.bottomFrame)
        self.tube.pack(side=LEFT, anchor=N, padx=50, pady=20)





    # def quit(self):
    #     self.tk.destroy()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return 'break'

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', False)
        return 'break'


if __name__ == '__main__':
    w = Screen()
    w.tk.mainloop()
