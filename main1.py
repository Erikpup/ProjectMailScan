import os

# os.environ["KIVY_NO_CONSOLELOG"]="1"
import kivy
import sqlite3
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
import scan_mails

class AddFilterPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Добавить фильтр"
        self.size_hint = (0.8, 0.6)  # Устанавливаем размер окна

        # Создаем контент окна
        content = GridLayout(cols=1)
        self.threat_name_input = MDTextField(id="threat_name", hint_text="Имя угрозы", theme_text_color="Custom", text_color_normal="white",  text_color_focus="white")
        self.pattern_input = MDTextField(id="pattern", hint_text="Шаблон", theme_text_color="Custom", text_color_normal="white",  text_color_focus="white")
        add_button = MDButton(MDButtonText(text="Добавить"), on_press=self.add_filter, )


        content.add_widget(self.threat_name_input)
        content.add_widget(self.pattern_input)
        content.add_widget(add_button)

        self.content = content

    def add_filter(self, instance):

        print(self.threat_name_input.text)
        print(self.pattern_input.text)

        connection = sqlite3.connect('typeDB.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO tablepatterns (id, name, pattern) VALUES ((SELECT MAX(id) FROM tablepatterns) + 1, ?, ?)',
            (self.threat_name_input.text, self.pattern_input.text))
        connection.commit()
        connection.close()

        self.dismiss()


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

        left_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(.5, 1))
        list_layout = WindowList(cols=1, spacing=10, size_hint_y=None)
        list_layout.bind(minimum_height=list_layout.setter('height'))
        self.dict_check = {}

        for i in self.open_data_db():
            # Создание объектов
            yacheyka = GridLayout(cols=2, spacing=0, size_hint_y=None)
            ck = CheckBox(size_hint=(.2, 1))
            txt = Label(text=i[1], halign="left", valign="middle")
            txt.bind(size=txt.setter('text_size'))

            self.dict_check.setdefault(ck,[str(i[0]), i[2]])

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
        btn_analys = MDButton(MDButtonText(text="Analys", pos_hint={"center_x": .5, "center_y": .5}), style="tonal",
                              pos_hint={"center_x": .5, "center_y": .5}, theme_width="Custom", height="56dp",
                              size_hint_x=1, on_press=self.analys)
        btn_add_type = MDButton(
            MDButtonIcon(icon="plus"), MDButtonText(text="Добавить фильтр", pos_hint={"center_x": .5, "center_y": .5}),
            style="tonal",
            pos_hint={"center_x": .5, "center_y": .5},
            theme_width="Custom",
            height="56dp",
            size_hint_x=1,
        )
        btn_add_type.bind(on_press=self.add_filter)
        btn_remove_type = MDButton(MDButtonIcon(icon="trash-can"),
                                   MDButtonText(text="Удалить фильтр", pos_hint={"center_x": .5, "center_y": .5}),
                                   style="tonal", pos_hint={"center_x": .5, "center_y": .5}, theme_width="Custom",
                                   height="56dp", size_hint_x=1)
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

    def add_filter(self, instance):
        popup = AddFilterPopup()
        popup.open()

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

    def save_result(self,result):
        data_db = self.open_data_db()
        for info in data_db:
            if str(info[0]) in result.keys():
                if result[str(info[0])] == []:
                    print("Данная угроза: "+info[1]+" не найдена")
                else:
                    for i in range(len(result[str(info[0])])):
                        print("Угроза найдена "+info[1]+" | "+result[str(info[0])][i][0]+" | "+result[str(info[0])][i][1])


    def analys(self, btn):
        self.input_path.text = self.input_path.text.replace(r"\\", r'\\\\')
        # print(self.input_path.text)
        dictPattern = {}
        for check in self.dict_check.keys():
            if (check.state == "down"):
                dictPattern[self.dict_check[check][0]] = self.dict_check[check][1]
                # print(self.dict_check[check])
                # print(self.input_path.text)
        if dictPattern == {}: return 0

        self.save_result(scan_mails.start_analys(self.input_path.text, dictPattern))


class MyFirstKivyApp(MDApp):

    def build(self):
        return MainMD()


MyFirstKivyApp().run()


