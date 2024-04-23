import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QTextCursor, QFont
import socket
from threading import Thread
import io
import random

username = str() # Логин пользователя
ip = str() # IP адрес сервера

# Объект сервера
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Следующее сообщение - файл
message_is_file = False

# Коды цветов
COLORS = {
    "[r]": "red",
    "[g]": "green",
    "[y]": "yellow",
    "[b]": "blue",
    "[p]": "purple",
    "[c]": "cyan",
    "[w]": "white",
    "[x]": "black"
}

# Главный экран авторизации
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        # Заголовок окна
        self.setWindowTitle("Login")

        # Текст заголовка
        self.title = QLabel("Введите ваш логин", self)
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.title.setFont(font)

        # Поле ввода логина
        self.input_field = QLineEdit(self)

        # Кнопка Ок
        self.login_button = QPushButton("Ок", self)
        self.login_button.clicked.connect(self.login) # Авторизация
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.login_button.setFont(font)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.input_field)
        layout.addWidget(self.login_button)

        # Изменение размера окна
        self.resize(200, 100)
    
    # Авторизация
    def login(self):
        # Запоминание логина
        global username
        username = self.input_field.text()

        # Переход на экран подключения
        self.w = ConnectWindow()
        self.w.show()
        self.hide()

# Экран подключения
class ConnectWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Заголовок окна
        self.setWindowTitle("Connection")

        # Текст заголовка
        self.title = QLabel("Введите IP адрес сервера", self)
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.title.setFont(font)

        # Поле ввода
        self.input_field = QLineEdit(self)
        self.input_field.setText("192.168.2.202")

        # Кнопка Ок
        self.login_button = QPushButton("Ок", self)
        self.login_button.clicked.connect(self.connect) # Подключение к серверу
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.login_button.setFont(font)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.input_field)
        layout.addWidget(self.login_button)

        # Изменение размера окна
        self.resize(200, 100)
    
    # Подключение к серверу
    def connect(self):
        # Запоминание IP адреса
        global ip
        ip = self.input_field.text()

        # Подключение
        try:
            print(f"[DEBUG] Подключение к серверу ({ip})...")
            # socket.create_connection((ip, 5050))
            server.connect((ip, 5050)) # Соединение с сервером по заданному IP адресу
            print(f"[DEBUG] Успешно подключено к серверу ({ip})!")

            # Переход на экран чата
            self.w = ChatWindow()
            self.w.show()
            self.hide()
        except Exception as e:
            print('[DEBUG] Не удалось подключиться!')
            print(f"[ERROR] {e}")

        
# Экран чата
class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Запуск потока получения сообщений с сервера
        Thread(target = self.receiver).start()

        # Заголовок окна
        self.setWindowTitle("Chat")

        # История сообщений
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.chat_history.setFont(font)

        # Поле ввода сообщения
        self.input_field = QLineEdit(self)
        self.input_field.returnPressed.connect(self.send) # Отправка сообщения при нажатии на Enter

        # Кнопка отправить
        self.send_button = QPushButton("Отправить", self)
        self.send_button.clicked.connect(self.send) # Отправка сообщения при нажатии на кнопку
        # Установка шрифта
        font = QFont()
        font.setPointSize(15)
        self.send_button.setFont(font)

        # Кнопка отправить файл
        self.send_file_button = QPushButton("Отправить файл", self)
        self.send_file_button.clicked.connect(self.send_file) # Отправка сообщения при нажатии на кнопку
        # Установка шрифта
        font = QFont()
        font.setPointSize(12)
        self.send_file_button.setFont(font)

        layout = QVBoxLayout(self)
        layout.addWidget(self.chat_history)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        layout.addWidget(self.send_file_button)

        # Изменение размера окна
        self.resize(400, 600)

        # Автоматическая отправка логина
        self.input_field.setText(f"{username}")
        self.send()

    # Отправка сообщения
    def send(self):
        print("[DEBUG] Отправка сообщения...")
        message = str(self.input_field.text())
        try:
            server.send(bytes(message, 'utf-8')) # Отправка
            self.input_field.setText("") # Очищение поля ввода
            print("[DEBUG] Сообщение отправлено!")
        except:
            print("[DEBUG] Ошибка отправки сообщения!")

    # Отправка файла
    def send_file(self):
        # Открытие диалогового окна выбора файла
        fileName, _ = QFileDialog.getOpenFileName(self, str("Open File"),
                                       "/home",
                                       str("*.*"))
        # fileName = f"\"{fileName}\""
        if fileName:
            # Отправка команды об отправке файла
            print(f"[DEBUG] Отправка файла... ({fileName})")
            server.send(bytes(f"/sendfile {fileName}", 'utf-8'))
            print(f"[DEBUG] Файл отправлен...")

    # Отображение сообщения в чате
    def display_message(self, message):
        cursor = self.chat_history.textCursor()
        # self.chat_history.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)
        # cursor.insertText(message + "\n") # Добавление сообщения в историю
        # m = str(message).replace("[r]", f"<font color={COLORS['[r]']}>")
        # cursor.insertHtml(f"<font color={COLORS[message[:3]]}>{message[3:]}</font>")

        # Форматирование цветов
        m = self.format_colors(message)

        # Вставка сообщения в QTextEdit
        cursor.insertHtml(f"{m}<br>")

    # Форматирование цветов
    def format_colors(self, message):
        m = str(message)
        count = 0
        for char in m:
            if char == '[' and m[m.index(char) + 2] == ']':
                if count == 0:
                    m = m[:m.index(char)] + f"<font color={COLORS[m[m.index(char):m.index(char) + 3]]}>" + m[m.index(char) + 3:]
                    m = m + "</font>"
                    count += 1
                else: 
                    m = m[:m.index(char)] + "</font>" + f"<font color={COLORS[m[m.index(char):m.index(char) + 3]]}>" + m[m.index(char) + 3:]
        return m
    
    # Получатель сообщений
    def receiver(self):
        while True:
            try:
                global message_is_file
                
                # Если текущее сообщение - файл 
                if message_is_file:
                    # Создание окна сохранения
                    print("[DEBUG] Создание окна сохранения")
                    options = QFileDialog.Options()
                    # options |= QFileDialog.DontUseNativeDialog
                    # Получение пути сохранения фалйа
                    print("[DEBUG] Получение пути сохранения фалйа")
                    file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Все файлы (*.*)", options=options)
                    # Если путь был указан
                    if file_path:
                        # Открытие файла в режиме записи (w) по байтам (b)
                        with open(file_path, 'wb') as f:
                            while True:
                                # Получение байтов файла
                                print("[DEBUG] Ожидание байтов")
                                file_bytes = server.recv(2048)
                                print(f"[LUTIY DEBUG] {file_bytes}")

                                if file_bytes[-len(b'transaction_end'):] == b'transaction_end':
                                    file_bytes = file_bytes[:-len(b'transaction_end')]
                                    # Запись байтов файла
                                    rnd = random.randint(0, 10)
                                    print("[DEBUG] Запись байтов" + "."*rnd)
                                    f.write(file_bytes)
                                    print("[DEBUG] Запись байтов завершена")
                                    print(f"[DEBUG] Файл полностью получен и сохранён по пути {file_path}")
                                    break
                                # Запись байтов файла
                                rnd = random.randint(0, 10)
                                print("[DEBUG] Запись байтов" + "."*rnd)
                                f.write(file_bytes)
                                print("[DEBUG] Запись байтов завершена")
                                # if not file_bytes:
                                #     print(f"[DEBUG] Файл полностью получен и сохранён по пути {file_path}")
                                #     break

                    # # Получение файла в байтах
                    # print("[DEBUG] Получение файла в байтах")
                    # file_bytes = server.recv(2048)
                    # print("[DEBUG] Файл получен")
                    
                    message_is_file = False
                # Если текущее сообщение - НЕ файл 
                else:
                    # Получение сообщения и его расшифровка через UTF-8
                    message = server.recv(2048).decode("utf-8")

                    # Если был отправлена команда /file
                    if (message[:5] == "/file"):
                        # Следующее сообщение - файл
                        print("[DEBUG] След. сообщение - файл!")
                        message_is_file = True

                    # Отображение сообщения
                    self.display_message(message)
            # Ошибка соединения с сервером
            except (OSError, ConnectionResetError):
                print("[DEBUG] Соединение с сервером разорвано")
                break
            # Другая ошибка
            except Exception as e:
                print("[DEBUG] Не удалось отобразить сообщение")
                print(f"[DEBUG] e = {e}")

# Главный цикл программы
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
