import sys
import os
import ctypes
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QColorDialog,
    QFileDialog,
    QSizeGrip,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QInputDialog,
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QIcon, QFont, QKeySequence, QShortcut


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
        self.vault_dir = None
        self.note_files = []
        self.current_file_path = None
        self.is_dirty = False
        self.text_edit = None

        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("sleepy.cat.pro.v2")

        self.setMinimumSize(700, 420)
        self.resize(1000, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.apply_my_icon()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.start_language_selection()

    def tr(self, key):
        translations = {
            "de": {
                "language_title": "Sprache / Language",
                "vault": "Vault",
                "open": "Öffnen",
                "save": "Speichern",
                "save_as": "Speichern unter",
                "new": "Neue Notiz",
                "theme": "Farbe",
                "insert_link": "Link einfügen",
                "open_link": "Link öffnen",
                "app_title": "Notes App",
                "untitled": "Unbenannt",
                "select_vault_title": "Vault-Ordner wählen",
                "save_file_title": "Notiz speichern",
                "save_filter": "Markdown (*.md)",
                "save_changes_title": "Ungespeicherte Änderungen",
                "save_changes_body": "Du hast ungespeicherte Änderungen. Möchtest du sie speichern?",
                "error_open": "Datei konnte nicht geöffnet werden.",
                "error_save": "Datei konnte nicht gespeichert werden.",
                "error_vault_bounds": "Die Datei muss innerhalb des Vault-Ordners liegen.",
                "error_invalid_name": "Ungültiger Notizname.",
                "search_notes": "Notizen durchsuchen...",
                "new_note_title": "Neue Notiz",
                "new_note_prompt": "Notizname (mit oder ohne .md):",
                "words": "Wörter",
                "chars": "Zeichen",
                "notes": "Notizen",
                "editor_placeholder": "Schreibe deine Notizen hier... Nutze [[Notizname]] für Verlinkungen.",
                "choose_note_link_title": "Notiz verlinken",
                "choose_note_link_prompt": "Wähle eine Notiz:",
                "link_not_found": "Verlinkte Notiz wurde nicht gefunden.",
                "create_note_question": "Soll eine neue Notiz dafür erstellt werden?",
                "info": "Info",
            },
            "en": {
                "language_title": "Sprache / Language",
                "vault": "Vault",
                "open": "Open",
                "save": "Save",
                "save_as": "Save As",
                "new": "New Note",
                "theme": "Theme",
                "insert_link": "Insert Link",
                "open_link": "Open Link",
                "app_title": "Notes App",
                "untitled": "Untitled",
                "select_vault_title": "Select vault folder",
                "save_file_title": "Save note",
                "save_filter": "Markdown (*.md)",
                "save_changes_title": "Unsaved changes",
                "save_changes_body": "You have unsaved changes. Save before continuing?",
                "error_open": "Could not open file.",
                "error_save": "Could not save file.",
                "error_vault_bounds": "The file must stay inside the vault folder.",
                "error_invalid_name": "Invalid note name.",
                "search_notes": "Search notes...",
                "new_note_title": "New note",
                "new_note_prompt": "Note name (with or without .md):",
                "words": "Words",
                "chars": "Chars",
                "notes": "Notes",
                "editor_placeholder": "Write your notes here... Use [[note name]] to link notes.",
                "choose_note_link_title": "Link note",
                "choose_note_link_prompt": "Choose a note:",
                "link_not_found": "Linked note was not found.",
                "create_note_question": "Create a new note for this link?",
                "info": "Info",
            },
        }
        return translations[self.lang][key]

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
        label = QLabel(self.tr("language_title"))
        label.setStyleSheet("color: white; font-size: 18pt; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

        btns = QHBoxLayout()
        de = QPushButton("DE 🇩🇪")
        en = QPushButton("EN 🇺🇸")
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
            self.select_vault()

    def setup_main_ui(self):
        self.clear_layout()

        header = QHBoxLayout()
        header.addWidget(RoundButton("#FF605C", self.close, self))
        header.addWidget(RoundButton("#FFBD44", self.showMinimized, self))
        header.addWidget(RoundButton("#28C940", self.toggle_max, self))
        header.addStretch()

        header_buttons = [
            (self.tr("vault"), self.select_vault),
            (self.tr("new"), self.new_file),
            (self.tr("save_as"), self.save_file_as),
        ]
        for label, action in header_buttons:
            btn = QPushButton(label)
            btn.setFixedHeight(26)
            btn.setStyleSheet(
                "background: rgba(255,255,255,0.1); color: white; "
                "border-radius: 5px; font-size: 10px; padding: 0 8px;"
            )
            btn.clicked.connect(action)
            header.addWidget(btn)

        self.layout.addLayout(header)

        tools = QHBoxLayout()
        for t, f in [("B", self.set_bold), ("I", self.set_italic), ("U", self.set_underline)]:
            btn = QPushButton(t)
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("background: rgba(255,255,255,0.1); color: white; border-radius: 5px;")
            btn.clicked.connect(f)
            tools.addWidget(btn)

        color_btn = QPushButton("🎨")
        color_btn.setFixedSize(30, 30)
        color_btn.setStyleSheet("background: rgba(255,255,255,0.1); border-radius: 5px;")
        color_btn.setToolTip(self.tr("theme"))
        color_btn.clicked.connect(self.change_color)
        tools.addWidget(color_btn)

        link_btn = QPushButton("⛓")
        link_btn.setFixedSize(30, 30)
        link_btn.setStyleSheet("background: rgba(255,255,255,0.1); border-radius: 5px;")
        link_btn.setToolTip(self.tr("insert_link"))
        link_btn.clicked.connect(self.insert_link)
        tools.addWidget(link_btn)

        open_link_btn = QPushButton("↗")
        open_link_btn.setFixedSize(30, 30)
        open_link_btn.setStyleSheet("background: rgba(255,255,255,0.1); border-radius: 5px;")
        open_link_btn.setToolTip(self.tr("open_link"))
        open_link_btn.clicked.connect(self.open_mention_under_cursor)
        tools.addWidget(open_link_btn)

        tools.addStretch()
        self.layout.addLayout(tools)

        body = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("search_notes"))
        self.search_input.setStyleSheet(
            "background: rgba(0,0,0,0.35); color: white; border: 1px solid rgba(255,255,255,0.15); "
            "border-radius: 6px; padding: 6px;"
        )
        self.search_input.textChanged.connect(self.refresh_note_list)

        self.note_list = QListWidget()
        self.note_list.setStyleSheet(
            "QListWidget { background: rgba(0,0,0,0.25); color: white; border-radius: 6px; padding: 4px; } "
            "QListWidget::item { padding: 6px; border-radius: 4px; } "
            "QListWidget::item:selected { background: rgba(255,255,255,0.18); }"
        )
        self.note_list.itemClicked.connect(self.open_note_from_item)

        sidebar = QVBoxLayout()
        sidebar.addWidget(self.search_input)
        sidebar.addWidget(self.note_list)
        side_container = QWidget()
        side_container.setLayout(sidebar)
        side_container.setFixedWidth(280)
        body.addWidget(side_container)

        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(
            "background: rgba(0,0,0,0.3); color: white; border-radius: 5px; "
            "padding: 10px; font-size: 13pt; border: none;"
        )
        self.text_edit.setPlaceholderText(self.tr("editor_placeholder"))
        self.text_edit.textChanged.connect(self.on_text_changed)
        body.addWidget(self.text_edit, 1)

        self.layout.addLayout(body)

        footer = QHBoxLayout()
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 10px;")
        footer.addWidget(self.status_label)
        footer.addStretch()

        self.save_btn = QPushButton(self.tr("save"))
        self.save_btn.setFixedSize(120, 35)
        self.save_btn.setStyleSheet("background: #34C759; color: white; border-radius: 17px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_file)
        footer.addWidget(self.save_btn)
        footer.addStretch()

        self.grip = QSizeGrip(self)
        footer.addWidget(self.grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(footer)

        self.setup_shortcuts()
        self.update_stats()
        self.update_window_title()

    def setup_shortcuts(self):
        self.shortcuts = [
            QShortcut(QKeySequence.StandardKey.Open, self, activated=self.select_vault),
            QShortcut(QKeySequence.StandardKey.Save, self, activated=self.save_file),
            QShortcut(QKeySequence.StandardKey.New, self, activated=self.new_file),
            QShortcut(QKeySequence.StandardKey.SaveAs, self, activated=self.save_file_as),
            QShortcut(QKeySequence("Ctrl+L"), self, activated=self.insert_link),
            QShortcut(QKeySequence("Ctrl+Enter"), self, activated=self.open_mention_under_cursor),
        ]

    def update_window_title(self):
        filename = os.path.basename(self.current_file_path) if self.current_file_path else self.tr("untitled")
        dirty = "*" if self.is_dirty else ""
        self.setWindowTitle(f"{self.tr('app_title')} - {filename}{dirty}")

    def on_text_changed(self):
        if self.text_edit is None:
            return
        if not self.is_dirty:
            self.is_dirty = True
            self.update_window_title()
        self.update_stats()

    def update_stats(self):
        if self.text_edit is None:
            return
        text = self.text_edit.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.status_label.setText(
            f"{self.tr('words')}: {words}   {self.tr('chars')}: {chars}   {self.tr('notes')}: {len(self.note_files)}"
        )

    def maybe_save_changes(self):
        if not self.is_dirty:
            return True

        dialog = QMessageBox(self)
        dialog.setWindowTitle(self.tr("save_changes_title"))
        dialog.setText(self.tr("save_changes_body"))
        dialog.setIcon(QMessageBox.Icon.Warning)
        save_btn = dialog.addButton(self.tr("save"), QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton(QMessageBox.StandardButton.Discard)
        dialog.addButton(QMessageBox.StandardButton.Cancel)
        dialog.exec()

        clicked = dialog.clickedButton()
        if clicked == save_btn:
            return self.save_file()
        if dialog.standardButton(clicked) == QMessageBox.StandardButton.Discard:
            return True
        return False

    def is_inside_vault(self, path):
        if not self.vault_dir:
            return False
        vault_abs = os.path.abspath(self.vault_dir)
        path_abs = os.path.abspath(path)
        try:
            return os.path.commonpath([vault_abs, path_abs]) == vault_abs
        except ValueError:
            return False

    def select_vault(self):
        if self.text_edit is not None and not self.maybe_save_changes():
            return

        start_dir = self.vault_dir if self.vault_dir else os.path.expanduser("~")
        selected = QFileDialog.getExistingDirectory(self, self.tr("select_vault_title"), start_dir)
        if not selected:
            return

        self.vault_dir = selected
        self.scan_note_files()
        self.refresh_note_list()

        if self.note_files:
            self.load_note(self.note_files[0], prompt_save=False)
        else:
            self.text_edit.blockSignals(True)
            self.text_edit.clear()
            self.text_edit.blockSignals(False)
            self.current_file_path = None
            self.is_dirty = False
            self.update_stats()
            self.update_window_title()

    def scan_note_files(self):
        self.note_files = []
        if not self.vault_dir:
            return
        for root, _, files in os.walk(self.vault_dir):
            for name in files:
                if name.lower().endswith(".md"):
                    self.note_files.append(os.path.join(root, name))
        self.note_files.sort(key=lambda p: os.path.relpath(p, self.vault_dir).lower())

    def refresh_note_list(self, *_):
        if self.note_list is None:
            return
        selected = os.path.abspath(self.current_file_path) if self.current_file_path else None
        query = self.search_input.text().strip().lower() if self.search_input is not None else ""

        self.note_list.blockSignals(True)
        self.note_list.clear()
        for path in self.note_files:
            rel = os.path.relpath(path, self.vault_dir).replace("\\", "/")
            rel_no_ext = rel[:-3] if rel.lower().endswith(".md") else rel
            if query and query not in rel_no_ext.lower():
                continue
            item = QListWidgetItem(rel_no_ext)
            item.setData(Qt.ItemDataRole.UserRole, path)
            self.note_list.addItem(item)

        if selected:
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if os.path.abspath(item.data(Qt.ItemDataRole.UserRole)) == selected:
                    self.note_list.setCurrentRow(i)
                    break
        self.note_list.blockSignals(False)
        self.update_stats()

    def open_note_from_item(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        self.load_note(path)

    def load_note(self, path, prompt_save=True):
        if not path or not os.path.exists(path):
            return False
        if prompt_save and os.path.abspath(path) != os.path.abspath(self.current_file_path or ""):
            if not self.maybe_save_changes():
                self.refresh_note_list()
                return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as err:
            QMessageBox.critical(self, self.tr("open"), f"{self.tr('error_open')}\n\n{err}")
            return False

        self.text_edit.blockSignals(True)
        self.text_edit.setPlainText(content)
        self.text_edit.blockSignals(False)
        self.current_file_path = path
        self.is_dirty = False
        self.refresh_note_list()
        self.update_stats()
        self.update_window_title()
        return True

    def save_file(self):
        if self.current_file_path:
            return self.write_file(self.current_file_path)
        return self.save_file_as()

    def save_file_as(self):
        if not self.vault_dir:
            self.select_vault()
            if not self.vault_dir:
                return False

        start_path = self.current_file_path if self.current_file_path else os.path.join(self.vault_dir, "note.md")
        path, _ = QFileDialog.getSaveFileName(self, self.tr("save_file_title"), start_path, self.tr("save_filter"))
        if not path:
            return False
        if not path.lower().endswith(".md"):
            path = f"{path}.md"
        if not self.is_inside_vault(path):
            QMessageBox.critical(self, self.tr("save"), self.tr("error_vault_bounds"))
            return False
        return self.write_file(path)

    def write_file(self, path):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
        except OSError as err:
            QMessageBox.critical(self, self.tr("save"), f"{self.tr('error_save')}\n\n{err}")
            return False

        self.current_file_path = path
        self.is_dirty = False
        self.scan_note_files()
        self.refresh_note_list()
        self.update_window_title()
        return True

    def new_file(self):
        if not self.vault_dir:
            self.select_vault()
            if not self.vault_dir:
                return
        if not self.maybe_save_changes():
            return

        name, ok = QInputDialog.getText(self, self.tr("new_note_title"), self.tr("new_note_prompt"))
        if not ok:
            return
        name = name.strip()
        if not name or name.endswith(("\\", "/")):
            QMessageBox.warning(self, self.tr("new"), self.tr("error_invalid_name"))
            return
        if not name.lower().endswith(".md"):
            name = f"{name}.md"

        path = os.path.normpath(os.path.join(self.vault_dir, name.replace("/", os.sep).replace("\\", os.sep)))
        if not self.is_inside_vault(path):
            QMessageBox.warning(self, self.tr("new"), self.tr("error_invalid_name"))
            return

        if not os.path.exists(path):
            self.text_edit.blockSignals(True)
            self.text_edit.clear()
            self.text_edit.blockSignals(False)
            if not self.write_file(path):
                return

        self.scan_note_files()
        self.refresh_note_list()
        self.load_note(path, prompt_save=False)

    def link_options(self):
        if not self.vault_dir:
            return []
        options = []
        for path in self.note_files:
            rel = os.path.relpath(path, self.vault_dir).replace("\\", "/")
            options.append(rel[:-3] if rel.lower().endswith(".md") else rel)
        return sorted(options, key=lambda x: x.lower())

    def insert_link(self):
        options = self.link_options()
        if not options:
            return
        value, ok = QInputDialog.getItem(
            self,
            self.tr("choose_note_link_title"),
            self.tr("choose_note_link_prompt"),
            options,
            0,
            False,
        )
        if ok and value:
            self.text_edit.insertPlainText(f"[[{value}]]")

    def mention_at_cursor(self):
        text = self.text_edit.toPlainText()
        pos = self.text_edit.textCursor().position()
        start = text.rfind("[[", 0, pos + 1)
        end = text.find("]]", pos)
        if start == -1 or end == -1 or start >= end:
            return None
        raw = text[start + 2:end].strip()
        return raw or None

    def resolve_mention(self, reference):
        if not self.vault_dir:
            return None
        ref = reference.strip()
        if not ref:
            return None

        normalized = ref.replace("/", os.sep).replace("\\", os.sep)
        direct = os.path.normpath(os.path.join(self.vault_dir, normalized))
        if not direct.lower().endswith(".md"):
            direct = f"{direct}.md"
        if self.is_inside_vault(direct) and os.path.exists(direct):
            return direct

        needle = ref[:-3] if ref.lower().endswith(".md") else ref
        needle = needle.lower()
        matches = []
        for path in self.note_files:
            rel = os.path.relpath(path, self.vault_dir).replace("\\", "/")
            rel_no_ext = rel[:-3] if rel.lower().endswith(".md") else rel
            stem = os.path.splitext(os.path.basename(path))[0]
            if rel_no_ext.lower() == needle or stem.lower() == needle:
                matches.append(path)
        if len(matches) == 1:
            return matches[0]
        return None

    def open_mention_under_cursor(self):
        mention = self.mention_at_cursor()
        if not mention:
            return
        self.scan_note_files()
        target = self.resolve_mention(mention)
        if target:
            self.load_note(target)
            return

        response = QMessageBox.question(
            self,
            self.tr("info"),
            f"{self.tr('link_not_found')}\n\n{self.tr('create_note_question')}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if response != QMessageBox.StandardButton.Yes:
            return

        if not self.maybe_save_changes():
            return
        new_path = os.path.normpath(os.path.join(self.vault_dir, mention.replace("/", os.sep).replace("\\", os.sep)))
        if not new_path.lower().endswith(".md"):
            new_path = f"{new_path}.md"
        if not self.is_inside_vault(new_path):
            QMessageBox.warning(self, self.tr("info"), self.tr("error_invalid_name"))
            return

        self.text_edit.blockSignals(True)
        self.text_edit.clear()
        self.text_edit.blockSignals(False)
        if self.write_file(new_path):
            self.load_note(new_path, prompt_save=False)

    def open_file(self):
        self.select_vault()

    def change_color(self):
        color = QColorDialog.getColor(self.bg_color, self)
        if color.isValid():
            self.bg_color = color
            self.update()

    def toggle_max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

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
        if hasattr(self, "old_pos") and e.buttons() == Qt.MouseButton.LeftButton and e.position().y() < 40:
            delta = e.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = e.globalPosition().toPoint()

    def closeEvent(self, event):
        if self.text_edit is None or self.maybe_save_changes():
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SleepyCatApp()
    ex.show()
    sys.exit(app.exec())
