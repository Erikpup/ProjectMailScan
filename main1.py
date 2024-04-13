# import kivy
# from kivy.app import App
# from kivy.core.window import Window
# from kivy.graphics import Color, Rectangle
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.label import Label
# from kivy.uix.scrollview import ScrollView
#
#
# class WindowList(ScrollView):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         with self.canvas:
#             Color(1, 1, 1, .5)  # set the colour
#
#             # Setting the size and position of canvas
#             self.rect = Rectangle(pos=self.center,
#                                   size=(self.width / 2.,
#                                         self.height / 2.))
#             self.bind(pos=self.update_rect,
#                       size=self.update_rect)
#
#     def update_rect(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
#
#
# class MainMD(GridLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         with self.canvas:
#             Color(.234, .456, .678, .8)  # set the colour
#
#             # Setting the size and position of canvas
#             self.rect = Rectangle(pos=self.center,
#                                   size=(self.width / 2.,
#                                         self.height / 2.))
#             self.bind(pos=self.update_rect,
#                       size=self.update_rect)
#
#         self.cols = 2
#         arch = AnchorLayout(anchor_x='center', anchor_y='center')
#         list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
#         # Make sure the height is such that there is something to scroll.
#         list_layout.bind(minimum_height=list_layout.setter('height'))
#         for i in range(100):
#             btn = Button(text=str(i), size_hint_y=None, height=40)
#             list_layout.add_widget(btn)
#         left_layout = WindowList(size_hint=(.9, .8))
#         left_layout.add_widget(list_layout)
#         arch.add_widget(left_layout)
#         right_layout = FloatLayout()
#         btn = Button(text="Анализ", size_hint=(.8, .1), pos_hint={"buttom": 1, "x": .1})
#         right_layout.add_widget(btn)
#         self.add_widget(arch)
#         self.add_widget(right_layout)
#
#     def update_rect(self, *args):
#         self.rect.pos = self.pos
#         self.rect.size = self.size
#
#
# # Defining a class
# class MyFirstKivyApp(App):
#
#     # Function that returns
#     # the root widget
#     def build(self):
#         # Label with text Hello World is
#         # returned as root widget
#
#         return MainMD()
#
#     # Here our class is initialized
#
#
# # and its run() method is called.
# # This initializes and starts
# # our Kivy application.
# MyFirstKivyApp().run()

import ctypes

# Загружаем DLL
my_dll = ctypes.CDLL(".\\Dll1.dll")

# Текст для проверки
text = "интернет страницы, 3g вполне хватает, с opera mini тем более. Удобный, красивый телефон, именно удобный, за такую цену просто великолепен\nСовременны аппарат, для тех кто понимает что такое смарт на Symbian OS и готов к его плюсам и минусам\n9145596289231320\nПокупал себе и девушке. Телефоны разных партий.И оба плохо ловят сеть, оба зависают при включении  хватает. Дисплей - неплох, но под углами вижу искажение, в Ноуте получше. Не напрягает - больше придирки. Собе  седники говорят, что слышно хуже. ЛТЕ - придирки, для работы хватает. Автояркость - иногда глючит. На максимальной громкости звонок подхрипывает. Сенсорная клавиша \"домой\" - на ощупь непонятно где у телефона верх, а где низ.  Телефон ощущается литым, без скрипов. Очень качественная сборка. Интересная оболочка с приятным интерфейсом. В целом мне нравится. Особенно уменьшение диагонали)))"

# Определяем типы аргументов и возвращаемого значения
my_dll.leakDetection.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
my_dll.leakDetection.restype = ctypes.c_int

# Преобразуем text в bytes
text_bytes = text.encode('utf-8')

# Вызываем функцию
leak_type = b"\\b\\d{20}\\b|\\d{20}(?!\\d)"
result = my_dll.leakDetection(text_bytes, leak_type)

# Выводим результат
print(result)  # Output: 8
