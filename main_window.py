import hashlib
import io
import sys
import binascii

from PyQt6 import uic

from signature import Signature
from database import DatabasePasswords
from cryptography.fernet import Fernet
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>893</width>
    <height>817</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <widget class="QPushButton" name="pushButton">
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>150</y>
     <width>111</width>
     <height>61</height>
    </rect>
   </property>
   <property name="text">
    <string>шифровка</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit">
   <property name="geometry">
    <rect>
     <x>70</x>
     <y>190</y>
     <width>113</width>
     <height>20</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>76</x>
     <y>120</y>
     <width>121</width>
     <height>71</height>
    </rect>
   </property>
   <property name="text">
    <string>Шифровка сообщения</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton_2">
   <property name="geometry">
    <rect>
     <x>220</x>
     <y>230</y>
     <width>111</width>
     <height>61</height>
    </rect>
   </property>
   <property name="text">
    <string>дешифровка</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>70</x>
     <y>230</y>
     <width>131</width>
     <height>31</height>
    </rect>
   </property>
   <property name="text">
    <string>Дешифровка сообщения</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_2">
   <property name="geometry">
    <rect>
     <x>70</x>
     <y>270</y>
     <width>113</width>
     <height>20</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_3">
   <property name="geometry">
    <rect>
     <x>370</x>
     <y>170</y>
     <width>131</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_4">
   <property name="geometry">
    <rect>
     <x>370</x>
     <y>250</y>
     <width>131</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>700</x>
     <y>130</y>
     <width>61</width>
     <height>51</height>
    </rect>
   </property>
   <property name="text">
    <string>Цифровые
 подписи</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton_3">
   <property name="geometry">
    <rect>
     <x>690</x>
     <y>190</y>
     <width>75</width>
     <height>23</height>
    </rect>
   </property>
   <property name="text">
    <string>К подписям</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_5">
   <property name="geometry">
    <rect>
     <x>190</x>
     <y>330</y>
     <width>161</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string>Хэширование сообщения</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_6">
   <property name="geometry">
    <rect>
     <x>50</x>
     <y>400</y>
     <width>121</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QComboBox" name="comboBox">
   <property name="geometry">
    <rect>
     <x>270</x>
     <y>71</y>
     <width>69</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>270</x>
     <y>20</y>
     <width>71</width>
     <height>51</height>
    </rect>
   </property>
   <property name="text">
    <string>Выбор
 алгоритма
 шифрования</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_7">
   <property name="geometry">
    <rect>
     <x>390</x>
     <y>440</y>
     <width>121</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="lineEdit_9">
   <property name="geometry">
    <rect>
     <x>40</x>
     <y>500</y>
     <width>121</width>
     <height>41</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label_6">
   <property name="geometry">
    <rect>
     <x>50</x>
     <y>370</y>
     <width>161</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string>Сообщение</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_8">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>470</y>
     <width>201</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string>Salt ( для усложнения расшифровки )</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pushButton_5">
   <property name="geometry">
    <rect>
     <x>230</x>
     <y>430</y>
     <width>111</width>
     <height>61</height>
    </rect>
   </property>
   <property name="text">
    <string>хэширование</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        design = io.StringIO(template)
        uic.loadUi(design, self)
        key = Fernet.generate_key()
        self.f = Fernet(key)
        self.setFixedSize(900, 600)
        self.setAutoFillBackground(False)
        self.setWindowTitle("Шифратор")
        self.setStyleSheet('QMainWindow#MainWindow {background-image: url(background.jpg);}')
        self.algorithm_comboBox = self.comboBox
        self.encrypt_button = self.pushButton
        self.decrypt_button = self.pushButton_2
        self.to_signature_button = self.pushButton_3
        self.hashing_soo_button = self.pushButton_5
        self.message_before_encrypt = self.lineEdit
        self.message_after_encrypt = self.lineEdit_3
        self.message_before_decrypt = self.lineEdit_2
        self.message_after_decrypt = self.lineEdit_4
        self.message_before_hex = self.lineEdit_6
        self.message_after_hex = self.lineEdit_7
        self.message_salt = self.lineEdit_9
        self.signature = None
        self.database = None
        self.hash_algorithm = "md5"
        self.algorithm_comboBox.addItems(["md5", "sha1", "sha256"])
        self.algorithm_comboBox.currentIndexChanged.connect(self.update_hash_algorithm)
        self.to_db_button = QPushButton("К БАЗЕ ДАННЫХ", self)
        self.to_db_button.move(680, 350)
        self.to_db_button.clicked.connect(self.to_db)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.to_signature_button.clicked.connect(self.to_signature)
        self.hashing_soo_button.clicked.connect(self.hashing_soo)

    def to_db(self):
        self.database = DatabasePasswords()
        self.database.show()

    def to_signature(self):
        self.signature = Signature()
        self.signature.show()

    def update_hash_algorithm(self):
        algorithm = self.algorithm_comboBox.currentText()
        self.hash_algorithm = algorithm

    def encrypt(self):
        if self.message_before_encrypt.text() == "":
            pass
        else:
            message_before = self.message_before_encrypt.text().encode()
            self.message_after_encrypt.setText(
                str(self.f.encrypt(
                    message_before)
                )[2:-1]
            )
            self.message_before_encrypt.clear()

    def decrypt(self):
        if self.message_before_decrypt.text() == "":
            pass
        else:
            message_before = self.message_before_decrypt.text().encode()
            self.message_after_decrypt.setText(
                self.f.decrypt(
                    message_before
                ).decode()
            )
            self.message_before_decrypt.clear()

    def hashing_soo(self):
        if self.message_before_hex.text() == "":
            pass
        else:
            my_password = str(self.message_before_hex.text())
            my_salt = str(self.message_salt.text())
            message_do = hashlib.pbkdf2_hmac(hash_name=self.hash_algorithm,
                                             password=bytes(my_password, 'utf-8'),
                                             salt=bytes(my_salt, 'utf-8'),
                                             iterations=100000)
            result = str(binascii.hexlify(message_do[2:-1]))
            self.message_after_hex.setText(result)
            self.message_before_hex.clear()
            self.message_salt.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
