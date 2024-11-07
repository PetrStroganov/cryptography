import hashlib
import io
import sys
import binascii


from PyQt6 import uic
from podpis import Signature
from cryptography.fernet import Fernet
from PyQt6.QtWidgets import QApplication, QMainWindow, QButtonGroup, QLabel, QLineEdit, QPushButton, QComboBox, QDialog
from PyQt6.QtWidgets import QVBoxLayout

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


class Dialog1(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        key = Fernet.generate_key()
        self.f = Fernet(key)
        self.setFixedSize(1000, 1000)
        self.pushButton.clicked.connect(self.shifr)
        self.pushButton_2.clicked.connect(self.deshifr)
        self.pushButton_3.clicked.connect(self.to_signature)
        self.pushButton_5.clicked.connect(self.hashing_soo)


    def to_signature(self):
        self.signature = Signature()
        self.signature.show()

    def shifr(self):
        if self.lineEdit.text() == "":
            pass
        else:
            self.lineEdit_3.setText(str(self.f.encrypt(self.lineEdit.text().encode()))[2:-1])
            self.lineEdit.clear()

    def deshifr(self):
        if self.lineEdit_2.text() == "":
            pass
        else:
            self.lineEdit_4.setText(self.f.decrypt(self.lineEdit_2.text().encode()).decode())
            self.lineEdit_2.clear()

    def hashing_soo(self):
        if self.lineEdit_6.text() == "":
            pass
        else:
            my_password = str(self.lineEdit_6.text())
            my_salt = str(self.lineEdit_9.text())
            message_do = hashlib.pbkdf2_hmac(hash_name='sha256',
                                     password=bytes(my_password, 'utf-8'),
                                     salt=bytes(my_salt, 'utf-8'),
                                     iterations=100000)
            result = str(binascii.hexlify(message_do[2:-1]))
            self.lineEdit_7.setText(result)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dialog1()
    ex.show()
    sys.exit(app.exec())
