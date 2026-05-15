import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QColorDialog, QFileDialog, QSizeGrip
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QIcon, QFont, QGuiApplication

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RoundButton(QWidget):
    def __init__(self, color, action, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.action = action
        self.setFixedSize(14, 14)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.action()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 14, 14)

class SleepyCatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.bg_color = QColor(25, 25, 25)
        self.lang = "de"
        self.old_pos = QPoint()
        
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("sleepy.cat.pro.v2")

        self.setMinimumSize(400, 300)
        self.resize(800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.apply_my_icon()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.start_language_selection()

    def apply_my_icon(self):
        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_sub_layout(item.layout())

    def clear_sub_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_sub_layout(child.layout())

    def start_language_selection(self):
        self.clear_layout()
        label = QLabel("Sprache / Language")
        label.setStyleSheet("color: white; font-size: 18pt; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)
        
        btns = QHBoxLayout()
        de = QPushButton("DE 🇩🇪"); en = QPushButton("EN 🇺🇸")
        for b in [de, en]:
            b.setFixedSize(150, 50)
            b.setStyleSheet("background: #333; color: white; border-radius: 10px;")
            btns.addWidget(b)
        de.clicked.connect(lambda: self.set_language("de"))
        en.clicked.connect(lambda: self.set_language("en"))
        self.layout.addLayout(btns)

    def set_language(self, lang):
        self.lang = lang
        self.start_color_selection()

    def start_color_selection(self):
        self.clear_layout()
        btn = QPushButton("🎨")
        btn.setFixedSize(80, 80)
        btn.setStyleSheet("background: #444; border-radius: 40px; font-size: 30pt;")
        btn.clicked.connect(self.pick_initial_color)
        self.layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def pick_initial_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color
            self.setup_main_ui()

    def setup_main_ui(self):
        self.clear_layout()
        
        header = QHBoxLayout()
        header.addWidget(RoundButton("#FF605C", self.close, self))
        header.addWidget(RoundButton("#FFBD44", self.toggle_max, self))
        header.addWidget(RoundButton("#28C940", self.showMinimized, self))
        header.addStretch()
        
        t_open = "Öffnen" if self.lang == "de" else "Open"
        self.open_btn = QPushButton(t_open)
        self.open_btn.setFixedSize(80, 25)
        self.open_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px; font-size: 10px;")
        self.open_btn.clicked.connect(self.open_file)
        header.addWidget(self.open_btn)
        self.layout.addLayout(header)

        tools = QHBoxLayout()
        for t, f in [("B", self.set_bold), ("I", self.set_italic), ("U", self.set_underline)]:
            btn = QPushButton(t)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px;")
            btn.clicked.connect(f)
            tools.addWidget(btn)
        tools.addStretch()
        self.layout.addLayout(tools)
        
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("background: rgba(0,0,0,0.3); color: white; border-radius: 5px; padding: 10px; font-size: 13pt; border: none;")
        self.layout.addWidget(self.text_edit)

        footer = QHBoxLayout()
        footer.addStretch()
        t_save = "Speichern" if self.lang == "de" else "Save"
        self.save_btn = QPushButton(t_save)
        self.save_btn.setFixedSize(120, 35)
        self.save_btn.setStyleSheet("background: #34C759; color: white; border-radius: 17px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_file)
        footer.addWidget(self.save_btn)
        footer.addStretch()
        
        self.grip = QSizeGrip(self)
        footer.addWidget(self.grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(footer)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", "", "Text (*.txt);;Python (*.py);;Alle Dateien (*)")
        if path:
            with open(path, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Speichern", "", "Text (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())

    def toggle_max(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()

    def set_bold(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal)
        self.text_edit.setCurrentCharFormat(fmt)

    def set_italic(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.text_edit.setCurrentCharFormat(fmt)

    def set_underline(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.text_edit.setCurrentCharFormat(fmt)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(self.bg_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.rect(), 15, 15)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and e.position().y() < 40:
            self.old_pos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'old_pos') and e.buttons() == Qt.MouseButton.LeftButton and e.position().y() < 40:
            delta = e.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = e.globalPosition().toPoint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SleepyCatApp()
    ex.show()
    sys.exit(app.exec())
