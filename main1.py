import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import sqlite3
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
import scan_mails


class WindowRight(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)  # set the colour


            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.))
            self.bind(pos=self.update_rect,
                      size=self.update_rect)


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class WindowList(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(.12, .14, .17, 1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.))
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class MainMD(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        with self.canvas:
            Color(.234, .456, .678, .8)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width / 2.,
                                        self.height / 2.))
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        left_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(.5,1))
        list_layout = WindowList(cols=1, spacing=10, size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        self.dict_check = {}

        for i in self.open_data_db():
            # Создание объектов
            yacheyka = GridLayout(cols=2, spacing=0, size_hint_y=None)
            ck = CheckBox(size_hint=(.2, 1))
            txt = Label(text=i[1], halign="left", valign="middle")
            txt.bind(size=txt.setter('text_size'))

            self.dict_check.setdefault(ck,{str(i[0]):i[2]})

            # Добавление объектов в список
            yacheyka.add_widget(ck)
            yacheyka.add_widget(txt)
            list_layout.add_widget(yacheyka)

        # Создание бегунка для списка
        scroll_list = ScrollView(size_hint=(.9, .8))
        scroll_list.add_widget(list_layout)
        left_layout.add_widget(scroll_list)

        # Создание объектов
        right = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(.5, .9))
        right_layout = GridLayout(rows=2, spacing=20, size_hint=(.8, .9))
        right_layout_top = GridLayout(rows=2, spacing=40)
        right_layout_buttom = GridLayout(rows=2, spacing=40)
        btn_analys = MDButton( MDButtonText( text= "Analys" , pos_hint= {"center_x": .5, "center_y": .5}),style= "tonal", pos_hint= {"center_x": .5, "center_y": .5}, theme_width= "Custom", height="56dp", size_hint_x= 1,on_press=self.analys)
        btn_add_type = MDButton(MDButtonIcon(icon= "plus"), MDButtonText( text= "Добавить фильтр" , pos_hint= {"center_x": .5, "center_y": .5}),style= "tonal", pos_hint= {"center_x": .5, "center_y": .5}, theme_width= "Custom", height="56dp", size_hint_x= 1)
        btn_remove_type = MDButton(MDButtonIcon(icon= "trash-can"), MDButtonText( text= "Удалить фильтр" , pos_hint= {"center_x": .5, "center_y": .5}),style= "tonal", pos_hint= {"center_x": .5, "center_y": .5}, theme_width= "Custom", height="56dp", size_hint_x= 1)
        self.input_path = MDTextField(text="Путь к данным")

        right_layout_top.add_widget(btn_add_type)
        right_layout_top.add_widget(btn_remove_type)
        right_layout_buttom.add_widget(self.input_path)
        right_layout_buttom.add_widget(btn_analys)
        right_layout.add_widget(right_layout_top)
        right_layout.add_widget(right_layout_buttom)
        right.add_widget(right_layout)

        # Добавление объектов на окно
        self.add_widget(left_layout)
        self.add_widget(right)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


    def open_data_db(self):
        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('typeDB.db')
        cursor = connection.cursor()

        # Выбираем всех пользователей
        cursor.execute('SELECT * FROM tablepatterns')
        types = cursor.fetchall()

        connection.close()
        # Выводим результаты
        return types


    def analys(self, bnt):
        for check in self.dict_check.keys():
            if (check.state=="down"):
                print(self.dict_check[check])
                print(self.input_path.text)

                print(scan_mails.start_analys(self.input_path.text,self.dict_check[check]))


# Defining a class
class MyFirstKivyApp(MDApp):

    # Function that returns
    # the root widget
    def build(self):
        # Label with text Hello World is
        # returned as root widget

        return MainMD()

    # Here our class is initialized


# and its run() method is called.
# This initializes and starts
# our Kivy application.
MyFirstKivyApp().run()
