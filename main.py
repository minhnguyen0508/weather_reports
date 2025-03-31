"""
Step 1: Project Setup
    1) Download requests pip install requests
    2) Download PyQt5
    3) Import libraries
"""
from requests import HTTPError, RequestException

import cred
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


#Step 2: Class definition
    #1) Initialize project object aka __init__(self)
    #2) declare instance of the class + attributes
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self) #label input city
        self.city_input = QLineEdit(self) #user input city
        self.get_weather_button= QPushButton("Get Weather", self) #get weather button
        self.temperature_label =QLabel("70°F", self) #temperature label
        self.emoji_label =QLabel("☀️", self)
        self.description_label = QLabel("Sunny", self)
        self.initUI()

#step 3: define User Interface
    #1) setting layout
    #2) setting alignment (left, right, center)
    #3) setting object name for CSS Styling using setStyleSheet

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox= QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        #center alignment for all elements listed below
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        #didn't know that CSS can be used in python LOL
        self.setStyleSheet(""" 
            QLabel{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size:40px;
            }
            QPushButton#get_weather_button{
                font-size:30px;
                font -weight:bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

#Step 4: define functionality
    def get_weather(self):
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={cred.api_key}"

        #try catch block
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API")
                case 403:
                    self.display_error("Forbidden\nAccess Denied")
                case 404:
                    self.display_error("404 Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe Request Timed Out")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)


    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_description  = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_f:.0f}°")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "🌦️️"
        elif 500 <= weather_id <= 531:
            return "🌧️️️"
        elif 600 <= weather_id <= 622:
            return "❄️️️️️"
        elif 701 <= weather_id <= 741:
            return "🌫️️️️️"
        elif weather_id == 800:
            return "☀️️️️️"
        elif 801 <= weather_id <= 804:
            return "☁️️️️️️"

#application window
if __name__=="__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
