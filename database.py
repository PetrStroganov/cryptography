import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QMessageBox, QInputDialog


class DatabasePasswords(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.password_table = QTableWidget(self)
        self.password_table.setColumnCount(3)
        self.password_table.setHorizontalHeaderLabels(["Название сайта", "Логин", "Пароль"])
        self.password_table.cellClicked.connect(self.edit_password)
        self.password_table.resizeColumnsToContents()

        self.add_password_button = QPushButton("Добавить пароль")
        self.add_password_button.clicked.connect(self.add_password)
        self.delete_password_button = QPushButton("Удалить пароль")
        self.delete_password_button.clicked.connect(self.delete_password)

        password_layout = QVBoxLayout()
        password_layout.addWidget(self.password_table)
        password_layout.addWidget(self.add_password_button)
        password_layout.addWidget(self.delete_password_button)

        self.password_widget = QWidget()
        self.password_widget.setLayout(password_layout)

        self.widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.password_widget)
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
        self.create_db_table()
        self.load_passwords()

    def create_db_table(self):
        con = sqlite3.connect("passwords.db")
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    def load_passwords(self):
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM passwords")
        passwords = cur.fetchall()
        conn.close()
        self.password_table.setRowCount(len(passwords))
        for row_index, password in enumerate(passwords):
            self.password_table.setItem(row_index, 0, QTableWidgetItem(password[1]))
            self.password_table.setItem(row_index, 1, QTableWidgetItem(password[2]))
            self.password_table.setItem(row_index, 2, QTableWidgetItem(password[3]))

    def add_password(self):
        dialog = QInputDialog()
        dialog.setWindowTitle("Добавить пароль")
        dialog.setLabelText("Введите название сайта:")
        dialog.setTextValue("")
        dialog.setInputMode(QInputDialog.InputMode.TextInput)
        if dialog.exec():
            site = dialog.textValue()
            dialog.setLabelText("Введите логин:")
            dialog.setTextValue("")
            if dialog.exec():
                login = dialog.textValue()
                dialog.setLabelText("Введите пароль:")
                dialog.setTextValue("")
                if dialog.exec():
                    password = dialog.textValue()
                    conn = sqlite3.connect("passwords.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO passwords (site, login, password) VALUES (?, ?, ?)",
                        (site, login, password),
                    )
                    conn.commit()
                    conn.close()
                    self.load_passwords()

    def edit_password(self, row, col):
        if row < 0:
            return
        site = self.password_table.item(row, 0).text()
        login = self.password_table.item(row, 1).text()
        password = self.password_table.item(row, 2).text()
        dialog = QInputDialog()
        dialog.setWindowTitle("Редактировать пароль")
        dialog.setLabelText("Название сайта:")
        dialog.setTextValue(site)
        if dialog.exec():
            new_site = dialog.textValue()
            dialog.setLabelText("Логин:")
            dialog.setTextValue(login)
            if dialog.exec():
                new_login = dialog.textValue()
                dialog.setLabelText("Пароль:")
                dialog.setTextValue(password)
                if dialog.exec():
                    new_password = dialog.textValue()
                    conn = sqlite3.connect("passwords.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE passwords SET site = ?, login = ?, password = ? WHERE site = ? AND login = ?",
                        (new_site, new_login, new_password, site, login),
                    )
                    conn.commit()
                    conn.close()
                    self.load_passwords()

    def delete_password(self):
        if self.password_table.currentRow() < 0:
            return
        site = self.password_table.item(self.password_table.currentRow(), 0).text()
        login = self.password_table.item(self.password_table.currentRow(), 1).text()
        reply = QMessageBox.question(self, "Удаление пароля",
                                     f"Вы уверены, что хотите удалить пароль для {site} ({login})?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No,
                                     )
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("passwords.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE site = ? AND login = ?", (site, login))
            conn.commit()
            conn.close()
            self.load_passwords()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatabasePasswords()
    window.show()
    sys.exit(app.exec())