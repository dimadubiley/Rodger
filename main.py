from PIL import Image, ImageTk
from io import BytesIO
from pystray import Icon, Menu, MenuItem
from tkinter import messagebox, filedialog, simpledialog
import tkinter as tk
import requests
import sys
import os
import webbrowser
import json
import pyperclip
from random import randint, choice
import threading
import math

# Путь к папке с настройками
settings_folder = "C:\\Rodger"
settings_file = os.path.join(settings_folder, "settings.json")

# Глобальные переменные
show_ip = True
language = "ru"

# --- Переводы ---
translations = {
    "ru": {
        "ip": "Ваш IP: {}",
        "ip_hidden": "IP: [скрыт]",
        "open_internet": "Открыть в интернете:",
        "other": "Другое",
        "settings": "Настройки",
        "toggle_ip": "Показать/спрятать IP",
        "exit": "Выход",
        "dice": "Кубики",
        "app_name": "Rodger",
        "separator": "----------------------"
    },
}


def tr(key):
    return translations[language].get(key, key)


# Функции для работы с интернет-ресурсами
def discordInterner(icon, item): webbrowser.open("https://discord.com/app")


def instagramInterner(icon, item): webbrowser.open("https://www.instagram.com")


def steamInternet(icon, item): webbrowser.open("https://store.steampowered.com")


def telegramInterner(icon, item): webbrowser.open("https://web.telegram.org/a/")


def tikTokInterner(icon, item): webbrowser.open("https://www.tiktok.com/")


def twitchInterner(icon, item): webbrowser.open("https://www.twitch.tv")


def youTubeInterner(icon, item): webbrowser.open("https://www.youtube.com")


# Функции для работы с Google сервисами
def googleDisk(icon, item): webbrowser.open("https://drive.google.com/drive/")


def google(icon, item): webbrowser.open("https://www.google.com")


def googleGmail(icon, item): webbrowser.open("https://mail.google.com")


def googlePhoto(icon, item): webbrowser.open("https://photos.google.com")


def googleTranstale(icon, item): webbrowser.open("https://translate.google.com")


# Функции для работы с AI сервисами
def chatGPT(icon, item): webbrowser.open("https://chat.openai.com")


def copilot(icon, item): webbrowser.open("https://copilot.microsoft.com")


def leonardo(icon, item): webbrowser.open("https://app.leonardo.ai")


# DnD
def ttg(): webbrowser.open("https://ttg.club/")


def dndsu(): webbrowser.open("https://dnd.su/")


def aternia(): webbrowser.open("https://aternia.games/")


def longstoryshort(): webbrowser.open("https://longstoryshort.app/")


# Получение публичного IP
def fetch_public_ip():
    try:
        response = requests.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "Ошибка получения IP"


# Загрузка изображения для иконки
image_url = "https://cdn.icon-icons.com/icons2/640/PNG/512/windows-desktop-os-software_icon-icons.com_59116.png"
try:
    response = requests.get(image_url)
    response.raise_for_status()
    icon_image = Image.open(BytesIO(response.content)).resize((64, 64))
except requests.RequestException as e:
    print(f"Ошибка загрузки изображения: {e}")
    sys.exit(1)
except FileNotFoundError:
    print(f"Ошибка: Файл {image_url} не найден.")
    sys.exit(1)

# Проверка и создание папки для настроек
if not os.path.exists(settings_folder):
    os.makedirs(settings_folder)
    os.system('attrib +h "C:\\Rodger"')


# Загрузка или создание файла настроек
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as file:
            return json.load(file)
    else:
        return {"show_ip": True}


# Сохранение настроек в файл
def save_settings(settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file)


# Строим меню
def build_menu_with_ip():
    ip_text = tr("ip").format(fetch_public_ip()) if settings["show_ip"] else tr("ip_hidden")
    return Menu(
        MenuItem(tr("separator"), lambda icon, item: None, enabled=False),
        MenuItem(f"           {tr('app_name')}", lambda icon, item: None, enabled=False),
        MenuItem(tr("separator"), lambda icon, item: None, enabled=False),
        MenuItem(ip_text, lambda icon, item: pyperclip.copy(fetch_public_ip())),
        MenuItem(tr("open_internet"), workOnInternet),
        MenuItem(tr("other"), more),
        MenuItem(tr("settings"), Menu(
            MenuItem(tr("toggle_ip"), toggle_ip_visibility),
        )),
        MenuItem(tr("exit"), lambda icon, item: icon.stop())
    )

# Меню для AI сервисов
allAI = Menu(
    MenuItem("Chat GPT", chatGPT),
    MenuItem("Copilot", copilot),
    MenuItem("Leonardo", leonardo),
)

dnd = Menu(
    MenuItem("Aternia", aternia),
    MenuItem("D&D su", dndsu),
    MenuItem("Long Story Short", longstoryshort),
    MenuItem("TTG Club", ttg),
)


def calc():
    class AdvancedCalculator(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Калькулятор")
            self.geometry("255x545")
            self.resizable(False, False)

            self.display = tk.Entry(self, font=("Arial", 20), borderwidth=2, relief="solid", width=16, justify="right")
            self.display.grid(row=0, column=0, columnspan=4)

            self.create_buttons()

        def create_buttons(self):
            buttons = [
                ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
                ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
                ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
                ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
                ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("log", 5, 3),
                ("sqrt", 6, 0), ("ln", 6, 1), ("exp", 6, 2), ("pi", 6, 3),
                ("C", 7, 0)  # Кнопка очистки
            ]

            for (text, row, col) in buttons:
                button = tk.Button(self, text=text, font=("Arial", 15), width=4, height=2,
                                   command=lambda t=text: self.on_button_click(t))
                button.grid(row=row, column=col, padx=5, pady=5)

        def on_button_click(self, text):
            if text == "=":
                try:
                    result = eval(self.display.get())
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, result)
                except Exception as e:
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, "Ошибка")
            elif text == "sin":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.sin(math.radians(value)))
            elif text == "cos":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.cos(math.radians(value)))
            elif text == "tan":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.tan(math.radians(value)))
            elif text == "log":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.log10(value))
            elif text == "sqrt":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.sqrt(value))
            elif text == "ln":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.log(value))
            elif text == "exp":
                value = float(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, math.exp(value))
            elif text == "pi":
                self.display.delete(0, tk.END)
                # Форматируем Пи с четырьмя знаками после запятой
                self.display.insert(tk.END, f"{math.pi:.4f}")
            elif text == "C":  # Очистить поле
                self.display.delete(0, tk.END)
            else:
                current_text = self.display.get()
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, current_text + text)

    if __name__ == "__main__":
        app = AdvancedCalculator()
        app.mainloop()


# Меню для Google сервисов
allGoogle = Menu(
    MenuItem("Disk", googleDisk),
    MenuItem("Google", google),
    MenuItem("Gmail", googleGmail),
    MenuItem("Photo", googlePhoto),
    MenuItem("Translate", googleTranstale),
)

# Меню для настройки интернет-ресурсов
workOnInternet = Menu(
    MenuItem("AI", allAI),
    MenuItem("Discord", discordInterner),
    MenuItem("DnD", dnd),
    MenuItem("Instagram", instagramInterner),
    MenuItem("Google", allGoogle),
    MenuItem("Steam", steamInternet),
    MenuItem("Telegram", telegramInterner),
    MenuItem("TikTok", tikTokInterner),
    MenuItem("Twitch", twitchInterner),
    MenuItem("YouTube", youTubeInterner),
)


# Меню для кубиков
def make_die_menu():
    def roll_dice(sides, label):
        result = randint(1, sides)
        label.config(text=result)

    def open_window():
        root = tk.Tk()
        root.title("Кубики")
        root.geometry("650x300")
        root.resizable(False, False)

        title = tk.Label(root, text="Выбери кубик", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        result_label = tk.Label(root, text=" ", font=("Arial", 28, "bold"))
        result_label.pack(pady=20)

        dice_frame = tk.Frame(root)
        dice_frame.pack()

        # Кнопки для разных кубов
        for sides in [2, 4, 6, 8, 10, 12, 20, 100]:
            btn = tk.Button(
                dice_frame,
                text=f"D{sides}",
                font=("Arial", 12, "bold"),
                width=6,
                command=lambda s=sides: roll_dice(s, result_label)
            )
            btn.pack(side="left", padx=5, pady=5)

        close_btn = tk.Button(root, text="Закрыть", font=("Arial", 12), command=root.destroy)
        close_btn.pack(pady=10)

        root.mainloop()

    return lambda icon, item: threading.Thread(target=open_window).start()


def taro():
    tarot_deck = [
        "0 - Дурак",
        "I - Маг",
        "II - Верховная Жрица",
        "III - Императрица",
        "IV - Император",
        "V - Иерофант",
        "VI - Влюбленные",
        "VII - Колесница",
        "VIII - Сила",
        "IX - Отшельник",
        "X - Колесо фортуны",
        "XI - Справедливость",
        "XII - Повешенный",
        "XIII - Смерть",
        "XIV - Умеренность",
        "XV - Дьявол",
        "XVI - Башня",
        "XVII - Звезда",
        "XVIII - Луна",
        "XIX - Солнце",
        "XX - Суд",
        "XXI - Мир",
        "Кубки - Туз",
        "Кубки - Двойка",
        "Кубки - Тройка",
        "Кубки - Четверка",
        "Кубки - Пятерка",
        "Кубки - Шестерка",
        "Кубки - Семерка",
        "Кубки - Восьмерка",
        "Кубки - Девятка",
        "Кубки - Десятка",
        "Кубки - Паж",
        "Кубки - Рыцарь",
        "Кубки - Королева",
        "Кубки - Король",
        "Пентакли - Туз",
        "Пентакли - Двойка",
        "Пентакли - Тройка",
        "Пентакли - Четверка",
        "Пентакли - Пятерка",
        "Пентакли - Шестерка",
        "Пентакли - Семерка",
        "Пентакли - Восьмерка",
        "Пентакли - Девятка",
        "Пентакли - Десятка",
        "Пентакли - Паж",
        "Пентакли - Рыцарь",
        "Пентакли - Королева",
        "Пентакли - Король",
        "Мечи - Туз",
        "Мечи - Двойка",
        "Мечи - Тройка",
        "Мечи - Четверка",
        "Мечи - Пятерка",
        "Мечи - Шестерка",
        "Мечи - Семерка",
        "Мечи - Восьмерка",
        "Мечи - Девятка",
        "Мечи - Десятка",
        "Мечи - Паж",
        "Мечи - Рыцарь",
        "Мечи - Королева",
        "Мечи - Король",
        "Жезлы - Туз",
        "Жезлы - Двойка",
        "Жезлы - Тройка",
        "Жезлы - Четверка",
        "Жезлы - Пятерка",
        "Жезлы - Шестерка",
        "Жезлы - Семерка",
        "Жезлы - Восьмерка",
        "Жезлы - Девятка",
        "Жезлы - Десятка",
        "Жезлы - Паж",
        "Жезлы - Рыцарь",
        "Жезлы - Королева",
        "Жезлы - Король"
    ]

    card = choice(tarot_deck)

    # Создаём окно
    root = tk.Tk()
    root.title("Таро")
    root.geometry("300x150")
    root.resizable(False, False)

    label = tk.Label(root, text=card, font=("Arial", 14), wraplength=280, justify="center")
    label.pack(pady=20)

    close_button = tk.Button(root, text="ОК", command=root.destroy).pack()
    # close_button.pack()

    root.mainloop()


def desk():
    class InvestigationBoard:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Меню")
            self.root.geometry("400x600+100+100")
            self.add_mode = None
            self.create_menu()

            self.board = tk.Toplevel(self.root)
            self.board.title("Доска расследования")
            self.board.geometry("1000x800+600+100")
            self.canvas = tk.Canvas(self.board, bg="gray")
            self.canvas.pack(fill=tk.BOTH, expand=True)

            self.pins = []
            self.lines = []
            self.notes = []
            self.images = []
            self.drag_data = {}
            self.pin_connections = {}
            self.pin_colors = ["red", "green", "blue", "yellow", "purple"]
            self.middle_selected_pin = None

            self.selected_item = None

            # Привязываем события
            self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
            self.canvas.bind("<B1-Motion>", self.on_drag_motion)
            self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)
            self.canvas.bind("<Double-1>", self.on_double_click)
            self.canvas.bind("<MouseWheel>", self.on_scroll)
            self.canvas.bind("<Button-2>", self.on_middle_click)

            # Удаление через клавишу Delete
            self.root.bind("<Delete>", self.delete_selected)
            self.board.bind("<Delete>", self.delete_selected)

            self.root.mainloop()

        def create_menu(self):
            tk.Button(self.root, text="Добавить кнопку",
                      command=lambda: self.set_add_mode('pin')).pack(pady=10)
            tk.Button(self.root, text="Добавить записку",
                      command=lambda: self.set_add_mode('note')).pack(pady=10)
            tk.Button(self.root, text="Добавить фото",
                      command=lambda: self.set_add_mode('image')).pack(pady=10)

        def set_add_mode(self, mode):
            self.add_mode = mode

        def create_pin_at(self, x, y):
            pin = self.canvas.create_oval(x, y, x + 20, y + 20, fill="red", tags="pin")
            self.pins.append(pin)
            self.canvas.tag_bind(pin, "<Button-3>", self.change_pin_color)
            self.canvas.tag_raise(pin)

        def create_note_at(self, x, y):
            # Определим размеры заметки
            width, height = 150, 80
            note = self.canvas.create_rectangle(x, y, x + width, y + height, fill="white", tags="note")
            note_text = self.canvas.create_text(x + 5, y + 5, text="Дважды кликни", anchor="nw",
                                                tags="note_text", width=width - 10)
            self.notes.append((note, note_text))
            self.canvas.tag_raise(note)
            self.canvas.tag_raise(note_text)

        def create_image_at(self, x, y):
            file_path = filedialog.askopenfilename()
            if not file_path:
                return
            pil_image = Image.open(file_path).resize((100, 100))
            tk_image = ImageTk.PhotoImage(pil_image)
            img_id = self.canvas.create_image(x, y, image=tk_image, anchor="nw", tags="image")
            self.images.append((img_id, tk_image, pil_image))
            self.canvas.tag_raise(img_id)

        def change_pin_color(self, event):
            item = self.canvas.find_closest(event.x, event.y)[0]
            current_color = self.canvas.itemcget(item, "fill")
            next_color = self.pin_colors[(self.pin_colors.index(current_color) + 1) % len(self.pin_colors)]
            self.canvas.itemconfig(item, fill=next_color)

        def on_middle_click(self, event):
            item = self.canvas.find_closest(event.x, event.y)[0]
            tags = self.canvas.gettags(item)
            if "pin" not in tags:
                return
            if self.middle_selected_pin is None:
                self.middle_selected_pin = item
                self.canvas.itemconfig(item, width=3, outline="black")
            else:
                if item != self.middle_selected_pin:
                    self.connect_pins(self.middle_selected_pin, item)
                self.canvas.itemconfig(self.middle_selected_pin, width=1, outline="")
                self.middle_selected_pin = None

        def connect_pins(self, p1, p2):
            x1, y1, x2, y2 = self.canvas.coords(p1)
            cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2
            x3, y3, x4, y4 = self.canvas.coords(p2)
            cx2, cy2 = (x3 + x4) / 2, (y3 + y4) / 2
            line = self.canvas.create_line(cx1, cy1, cx2, cy2, fill="red", width=2, tags="line")
            self.lines.append((line, p1, p2))
            self.pin_connections.setdefault(p1, []).append(line)
            self.pin_connections.setdefault(p2, []).append(line)
            self.canvas.tag_raise(line)

        def on_double_click(self, event):
            # Редактирование текста заметки по двойному клику
            item = self.canvas.find_closest(event.x, event.y)[0]
            tags = self.canvas.gettags(item)
            if "note_text" in tags:
                new_text = simpledialog.askstring("Редактирование", "Введите текст:")
                if new_text:
                    self.canvas.itemconfig(item, text=new_text)

        def on_drag_start(self, event):
            # Если включен режим добавления объекта – создаем объект в координатах клика
            if self.add_mode is not None:
                if self.add_mode == 'pin':
                    self.create_pin_at(event.x, event.y)
                elif self.add_mode == 'note':
                    self.create_note_at(event.x, event.y)
                elif self.add_mode == 'image':
                    self.create_image_at(event.x, event.y)
                self.add_mode = None
                return

            # Если кликнули по тексту заметки, выбираем саму заметку (прямоугольник)
            item = self.canvas.find_closest(event.x, event.y)[0]
            tags = self.canvas.gettags(item)
            if "note_text" in tags:
                for note, note_text in self.notes:
                    if note_text == item:
                        item = note
                        break
            self.selected_item = item  # Запоминаем объект для удаления
            if any(tag in tags for tag in ("pin", "note", "image")):
                self.drag_data = {"item": item, "x": event.x, "y": event.y}

        def on_drag_motion(self, event):
            if not self.drag_data:
                return
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            item = self.drag_data["item"]
            self.canvas.move(item, dx, dy)
            # Если перемещается заметка – перемещаем и связанный с ней текст
            if "note" in self.canvas.gettags(item):
                for note, note_text in self.notes:
                    if note == item:
                        # Определяем новые координаты заметки и сдвигаем текст с отступом 5 пикселей
                        x1, y1, x2, y2 = self.canvas.coords(note)
                        self.canvas.coords(note_text, x1 + 5, y1 + 5)
                        break
            # Если перемещается пин – обновляем линии
            if "pin" in self.canvas.gettags(item):
                self.update_lines(item)
            self.drag_data["x"], self.drag_data["y"] = event.x, event.y

        def on_drag_stop(self, event):
            self.drag_data.clear()

        def update_lines(self, pin):
            if pin not in self.pin_connections:
                return
            x1, y1, x2, y2 = self.canvas.coords(pin)
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            for line in self.pin_connections[pin]:
                for l, p1, p2 in self.lines:
                    if l == line:
                        other = p2 if p1 == pin else p1
                        ox1, oy1, ox2, oy2 = self.canvas.coords(other)
                        ocx, ocy = (ox1 + ox2) / 2, (oy1 + oy2) / 2
                        if pin == p1:
                            self.canvas.coords(line, cx, cy, ocx, ocy)
                        else:
                            self.canvas.coords(line, ocx, ocy, cx, cy)
            self.canvas.tag_raise(pin)
            for line_id, _, _ in self.lines:
                self.canvas.tag_raise(line_id)

        def on_scroll(self, event):
            # Масштабирование заметок и изображений с помощью колесика мыши
            items = self.canvas.find_withtag("current")
            if not items:
                return
            item = items[0]
            tags = self.canvas.gettags(item)
            factor = 1.1 if event.delta > 0 else 0.9

            if "note" in tags:
                # Масштабирование заметки: пересчитываем координаты прямоугольника
                x1, y1, x2, y2 = self.canvas.coords(item)
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                new_width = (x2 - x1) * factor
                new_height = (y2 - y1) * factor
                new_x1, new_y1 = cx - new_width / 2, cy - new_height / 2
                new_x2, new_y2 = cx + new_width / 2, cy + new_height / 2
                self.canvas.coords(item, new_x1, new_y1, new_x2, new_y2)
                # Обновляем координаты текста заметки: отступ 5 пикселей от левого верхнего угла
                for note, note_text in self.notes:
                    if note == item:
                        self.canvas.coords(note_text, new_x1 + 5, new_y1 + 5)
                        # Обновляем ширину текста, чтобы при переносе он переносился по строкам
                        self.canvas.itemconfig(note_text, width=new_width - 10)
                        break

            elif "image" in tags:
                # Масштабирование изображения: пересоздаем его с новым размером
                for idx, (img_id, tk_img, pil_img) in enumerate(self.images):
                    if img_id == item:
                        new_width = int(pil_img.width * factor)
                        new_height = int(pil_img.height * factor)
                        resized = pil_image = pil_img.resize((new_width, new_height))
                        new_tk_img = ImageTk.PhotoImage(resized)
                        self.images[idx] = (img_id, new_tk_img, resized)
                        self.canvas.itemconfig(img_id, image=new_tk_img)
                        self.canvas.image = new_tk_img
                        break

        def delete_selected(self, event):
            # Удаляет выбранный объект (а для заметок удаляет и связанный текст)
            if self.selected_item:
                tags = self.canvas.gettags(self.selected_item)
                if "note" in tags:
                    for note, note_text in self.notes:
                        if note == self.selected_item:
                            self.canvas.delete(note_text)
                            self.notes.remove((note, note_text))
                            break
                if self.selected_item in self.pin_connections:
                    for line in self.pin_connections[self.selected_item]:
                        self.canvas.delete(line)
                    del self.pin_connections[self.selected_item]
                self.canvas.delete(self.selected_item)
                self.selected_item = None

    if __name__ == "__main__":
        InvestigationBoard()


def stonks():
    folder_path = "C:/Stonks"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_save = os.path.join(folder_path, "game.js")
    file_tranzaktion = os.path.join(folder_path, "tranzaktion.js")

    def save_data():
        with open(file_save, "w") as f:
            f.write(f"{money}\n{start}\n{cash}\n")

    def save_tranzaktion():
        with open(file_tranzaktion, "w") as f:
            for transaction in transactions:
                f.write(transaction + '\n')

    def load_data():
        global money, start, cash
        try:
            with open(file_save, "r") as f:
                lines = f.readlines()
                money = int(lines[0].strip())
                start = int(lines[1].strip())
                cash = int(lines[2].strip())
        except FileNotFoundError:
            money = 1000
            start = randint(800, 1000)
            cash = 1

    def load_tranzaktion():
        global transactions
        try:
            with open(file_save, "r") as f:
                lines = f.readlines()
                transactions = [line.strip() for line in lines[3:]]
        except FileNotFoundError:
            transactions = []

    def update_prices():
        global money, start, cash, chat
        cen = randint(1, 100)
        up = randint(1, 10)

        if up >= 1 and up <= 5:
            cen = cen * -1
            start = start + cen
            chat = f"Цена упала на: {cen}"
        elif up >= 6 and up <= 10:
            cen = cen * 1
            start = start + cen
            chat = f"Цена поднялась на: {cen}"

        transactions.append(chat)

        label_price.config(text=f"Стоимость Афромереканских денег: {start}")
        label_chat.config(text=chat)
        label_balance.config(text=f"Ваш баланс: {money}")
        label_currency.config(text=f"Ваши афромереканские деньги: {cash}")
        root.after(10000, update_prices)
        save_data()
        save_tranzaktion()

    def buy():
        global money, start, cash, chat
        if start <= money:
            money = money - start
            cash = cash + 1
            transactions.append(f"{chat} - игрок совершил покупку")
            update_labels()
        else:
            messagebox.showwarning("Ошибка", "Недостаточно средств")

    def sell():
        global money, start, cash
        if cash > 0:
            money = money + start
            cash = cash - 1
            update_labels()
        else:
            messagebox.showwarning("Ошибка", "У вас нет афромереканских денег")

        if cash <= 0:
            money = 1000

    def update_labels():
        label_balance.config(text=f"Ваш баланс: {money}")
        label_currency.config(text=f"Ваши афромереканские деньги: {cash}")

    def show_transactions():
        transaction_window = tk.Toplevel(root)
        transaction_window.title("История транзакций")
        transaction_window.geometry("400x300")
        root.resizable(width=False, height=False)

        scrollbar = tk.Scrollbar(transaction_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(transaction_window, yscrollcommand=scrollbar.set)
        for transaction in transactions:
            listbox.insert(tk.END, transaction)
        listbox.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

    load_data()
    load_tranzaktion()

    root = tk.Tk()
    root.title("Stonks")
    root.geometry("500x300")
    root.resizable(width=False, height=False)
    root.configure(bg="black")

    label_price = tk.Label(root, text=f"Стоимость Афромереканских денег: {start}", fg="lime", bg="black")
    label_price.pack()

    label_chat = tk.Label(root, text="", fg="lime", bg="black")
    label_chat.pack()

    label_balance = tk.Label(root, text=f"Ваш баланс: {money}", fg="lime", bg="black")
    label_balance.pack()

    label_currency = tk.Label(root, text=f"Ваши афромереканские деньги: {cash}", fg="lime", bg="black")
    label_currency.pack()

    button_buy = tk.Button(root, text="Купить", command=buy, fg="lime", bg="black")
    button_buy.pack()

    button_sell = tk.Button(root, text="Продать", command=sell, fg="lime", bg="black")
    button_sell.pack()

    button_transactions = tk.Button(root, text="Показать транзакции", command=show_transactions, fg="lime", bg="black")
    button_transactions.pack()

    update_prices()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()


dies = make_die_menu()
more = Menu(
    MenuItem(tr("Калькулятор"), calc),
    MenuItem(tr("Кубики"), dies),
    MenuItem(tr("Таро"), taro),
    MenuItem(tr("Доска расследования"), desk),
    MenuItem(tr("Stonks"), stonks),
)


def toggle_ip_visibility(icon, item):
    settings["show_ip"] = not settings["show_ip"]
    save_settings(settings)
    icon.menu = build_menu_with_ip()
    icon.update_menu()

settings = load_settings()

icon = Icon(
    "Roger",
    icon_image,
    menu=build_menu_with_ip()
)

icon.run()
