import sys
import os
import time
import webbrowser

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
    QGraphicsOpacityEffect
)

from PySide6.QtGui import (
    QMovie,
    QIcon
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QUrl,
    QPropertyAnimation
)

from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)

# =========================================================
# APP
# =========================================================

app = QApplication(sys.argv)

window = QMainWindow()
window.resize(1200, 750)
window.setMinimumSize(1000, 650)
window.setWindowTitle("MOGSINT V0.02")

icon = "icon.ico" if os.path.exists("icon.ico") else "icon.png"

if os.path.exists(icon):
    window.setWindowIcon(QIcon(icon))

root = QWidget()
window.setCentralWidget(root)

# =========================================================
# AUDIO
# =========================================================

player = QMediaPlayer()
audio = QAudioOutput()
player.setAudioOutput(audio)

boot_started = False

def play_boot():
    global boot_started

    if boot_started:
        return

    path = os.path.abspath("boot.mp3")

    if os.path.exists(path):
        player.setSource(QUrl.fromLocalFile(path))
        player.play()

    boot_started = True

# =========================================================
# BACKGROUND
# =========================================================

bg = QLabel(root)
bg.setScaledContents(True)

movie = None

if os.path.exists("background.gif"):
    movie = QMovie("background.gif")
    bg.setMovie(movie)
    movie.start()

overlay = QFrame(root)
overlay.setStyleSheet("background-color: rgba(8,10,14,140);")

# =========================================================
# LOADING SCREEN
# =========================================================

loading = QFrame(root)
loading.setStyleSheet("background-color: rgb(8,10,14);")

loading_text = QLabel("M O G S I N T", loading)
loading_text.setAlignment(Qt.AlignCenter)
loading_text.setStyleSheet("color:white;font-size:22px;font-weight:bold;")

bar_bg = QFrame(loading)
bar_bg.setStyleSheet("background-color: rgba(255,255,255,40);border-radius:3px;")

bar = QFrame(bar_bg)
bar.setStyleSheet("background-color: rgb(80,160,255);border-radius:3px;")

# =========================================================
# TITLE
# =========================================================

title = QLabel("MOGSINT", root)
title.setAlignment(Qt.AlignCenter)
title.setStyleSheet("color:white;font-size:18px;font-weight:bold;")

# =========================================================
# SIDEBAR
# =========================================================

sidebar_width = 260
sidebar = QFrame(root)
sidebar.setStyleSheet("background-color: rgba(12,16,22,240);")

sidebar_open = False

# =========================================================
# HAMBURGER
# =========================================================

hamburger = QPushButton("☰", root)
hamburger.setStyleSheet("""
QPushButton {
    color:white;
    background:rgba(25,25,25,220);
    border-radius:6px;
    font-size:16px;
}
QPushButton:hover {
    background:rgba(50,50,50,220);
}
""")

def toggle_sidebar():
    global sidebar_open
    sidebar_open = not sidebar_open
    update_positions()

hamburger.clicked.connect(toggle_sidebar)

# =========================================================
# USERS + TIME
# =========================================================

users_box = QFrame(root)
users_box.setStyleSheet("background:rgba(20,25,35,190);border-radius:8px;")

users_label = QLabel("ACTIVE USERS: 128", users_box)
users_label.setStyleSheet("color:white;font-size:10px;")

time_box = QFrame(root)
time_box.setStyleSheet("background:rgba(20,25,35,190);border-radius:8px;")

time_label = QLabel(time.strftime("%H:%M:%S"), time_box)
time_label.setStyleSheet("color:white;font-size:10px;")

# =========================================================
# CREDIT
# =========================================================

credit = QLabel("made by mogger with ❤️", root)
credit.setStyleSheet("color:rgba(120,180,255,180);font-size:11px;")

# =========================================================
# CATEGORIES (UPDATED ONLY IMAGE INTEL)
# =========================================================

categories = {

    "HOME": [],

    "USERNAME / ANALYSIS": [
        ("Instant Username", "https://instantusername.com/"),
        ("Namechk", "https://namechk.com/"),
        ("UserSearch", "https://usersearch.org/"),
        ("SearchPOF", "https://searchpof.com/")
    ],

    "MAPS & GEO": [
        ("OpenStreetMap", "https://openstreetmap.org"),
        ("Google Maps", "https://maps.google.com"),
        ("Google Earth", "https://earth.google.com/web/"),
        ("Mapillary", "https://www.mapillary.com/app/"),
        ("EarthKit Geo", "https://earthkit.app/geoclip")  # kept working version
    ],

    "SEARCH ENGINES": [
        ("Google", "https://google.com"),
        ("Bing", "https://bing.com"),
        ("DuckDuckGo", "https://duckduckgo.com")
    ],

    "IMAGE INTEL": [
        ("TinEye", "https://tineye.com"),
        ("Google Images", "https://images.google.com"),
        ("ShadowMap", "https://shadowmap.org"),
        ("SunCalc", "https://suncalc.io"),
        ("Picarta AI", "https://picarta.ai")
    ],

    "AIRPLANE INTEL": [
        ("ADS-B Exchange", "https://globe.adsbexchange.com/"),
        ("FlightAware", "https://uk.flightaware.com/"),
        ("LiveATC", "https://www.liveatc.net/"),
        ("Flightradar24", "https://www.flightradar24.com/")
    ],

    "PHONE INTEL": [
        ("Sync.me", "https://sync.me/"),
        ("Truecaller", "https://www.truecaller.com/"),
        ("Thatsthem", "https://thatsthem.com/reverse-phone-lookup")
    ]
}

# =========================================================
# HOME TEXT
# =========================================================

welcome_message = """WELCOME TO MOGSINT

A unified intelligence environment built for analysis, mapping, reconnaissance, and structured digital awareness. Designed for clarity, speed, and control in complex data environments. The update of this software will take place in a month or so, Please keep in mind that i have a life myself and that i am the only developer of this program."""

welcome_label = QLabel(root)
welcome_label.setWordWrap(True)
welcome_label.setAlignment(Qt.AlignCenter)
welcome_label.setStyleSheet("""
color: white;
font-size: 15px;
font-weight: 500;
text-shadow: 0px 0px 12px rgba(255,255,255,180);
""")
welcome_label.hide()

typing_index = 0
typing_timer = QTimer()

def type_writer():
    global typing_index

    if typing_index <= len(welcome_message):
        welcome_label.setText(welcome_message[:typing_index])
        typing_index += 1
    else:
        typing_timer.stop()

typing_timer.timeout.connect(type_writer)

# =========================================================
# FADE SYSTEM
# =========================================================

fade_anims = []

def fade_widget(widget, start, end):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(250)
    anim.setStartValue(start)
    anim.setEndValue(end)

    fade_anims.append(anim)
    anim.start()

# =========================================================
# CONTENT
# =========================================================

content_buttons = []

def clear_content():
    global content_buttons
    for b in content_buttons:
        b.deleteLater()
    content_buttons = []

def make_site_button(name, url, x, y):
    btn = QPushButton(name, root)
    btn.setGeometry(x, y, 240, 70)
    btn.setStyleSheet("""
    QPushButton {
        background:rgba(25,30,40,220);
        color:white;
        border-radius:10px;
        font-size:12px;
    }
    QPushButton:hover {
        background:rgb(0,170,255);
        color:black;
    }
    """)
    btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
    btn.show()
    content_buttons.append(btn)

# =========================================================
# LOAD CATEGORY
# =========================================================

def load_category(category):

    global typing_index

    clear_content()
    welcome_label.hide()

    if category == "HOME":

        welcome_label.setGeometry(
            window.width()//2 - 350,
            window.height()//2 - 120,
            700,
            220
        )

        welcome_label.setText("")
        welcome_label.show()

        fade_widget(welcome_label, 0, 1)

        typing_index = 0
        typing_timer.start(10)

        return

    items = categories.get(category, [])

    x, y = 320, 120
    col = 0

    for name, url in items:
        make_site_button(name, url, x, y)
        fade_widget(content_buttons[-1], 0, 1)

        x += 260
        col += 1

        if col % 3 == 0:
            x = 320
            y += 90

# =========================================================
# SIDEBAR
# =========================================================

sidebar_buttons = []

def create_sidebar_categories():

    y = 80

    for cat in categories.keys():

        btn = QPushButton(cat, sidebar)
        btn.setGeometry(15, y, 230, 45)

        btn.setStyleSheet("""
        QPushButton {
            background:rgba(25,30,40,220);
            color:white;
            border-radius:8px;
            padding-left:15px;
            font-size:11px;
        }
        QPushButton:hover {
            background:rgb(0,170,255);
            color:black;
        }
        """)

        btn.clicked.connect(lambda _, c=cat: load_category(c))
        btn.show()

        sidebar_buttons.append(btn)

        y += 55

# =========================================================
# POSITIONING
# =========================================================

def update_positions():

    w, h = window.width(), window.height()

    bg.setGeometry(0,0,w,h)
    overlay.setGeometry(0,0,w,h)
    loading.setGeometry(0,0,w,h)

    loading_text.setGeometry(0,h//2 - 70,w,40)

    bar_bg.setGeometry(w//2 - 180, h//2, 360, 6)

    title.setGeometry(0,10,w,40)
    hamburger.setGeometry(10,10,35,35)

    if sidebar_open:
        sidebar.setGeometry(0,0,260,h)
    else:
        sidebar.setGeometry(-260,0,260,h)

    users_box.setGeometry(w-170,10,155,24)
    users_label.move(10,4)

    time_box.setGeometry(w-170,40,155,24)
    time_label.move(10,4)

    credit.adjustSize()
    credit.move(w-credit.width()-15,h-25)

# =========================================================
# LOADING (ONLY CHANGE: 4.4s)
# =========================================================

duration = 4.4   # 👈 ONLY CHANGE
start = time.perf_counter()

def tick():

    progress = min((time.perf_counter()-start)/duration,1)

    bar.setGeometry(0,0,int(360*progress),6)

    if progress >= 0.02:
        play_boot()

    time_label.setText(time.strftime("%H:%M:%S"))

    if progress >= 1:
        timer.stop()
        loading.hide()
        load_category("HOME")

timer = QTimer()
timer.timeout.connect(tick)
timer.start(16)

# =========================================================
# START
# =========================================================

create_sidebar_categories()
update_positions()

window.resizeEvent = lambda e: update_positions()

window.show()

sys.exit(app.exec())