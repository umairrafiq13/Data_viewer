from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.graphics import Line
import paho.mqtt.client as mqtt
import threading
from kivy.core.window import Window
from kivy.uix.image import Image
import json

LabelBase.register(name= 'BigNoodleTooOblique',
                   fn_regular= 'BigNoodleTooOblique.ttf')

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

Window.size = (1366,768)
Window.fullscreen = True




MQTT_SERVER = "192.168.100.3"
MQTT_PATH = "sensors"


class Painter(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud["Line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud["Line"].points += [touch.x, touch.y]


class Thread(Screen):
    def __init__(self, *args,**kwargs):
        Screen.__init__(self,**kwargs)
        self.start_thread()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("sensors")

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        self.ids.sensor1.text = "%.1f"%(float(payload['sensor1']))
        self.ids.sensor2.text = "%.1f"%(float(payload['sensor2']))
        self.ids.sensor3.text = "%.1f"%(float(payload['sensor3']))
        self.ids.sensor4.text = "%.1f"%(float(payload['sensor4']))

    def first_thread(self):
        print("started")
        client = mqtt.Client()
        client.connect("192.168.100.3", 1883, 60)

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.loop_forever()

    def start_thread(self):
        threading.Thread(target=self.first_thread).start()


class AnotherScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("thread.kv")


class MainApp(App):

    def build(self):
        self.load_kv("thread.kv")
        return Thread()


if __name__ == "__main__":
    MainApp().run()