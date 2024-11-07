import base64
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QFileDialog
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature


class Signature(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Цифровая подпись")
        layout = QVBoxLayout()
        self.text_label = QLabel("Текст для подписи:")
        self.text_edit = QTextEdit()
        self.generate_key_button = QPushButton("Сгенерировать ключи")
        self.save_key_button = QPushButton("Сохранить ключи")
        self.public_key_label = QLabel("Публичный ключ:")
        self.public_key_edit = QLineEdit()
        self.public_key_edit.setReadOnly(True)
        self.sign_button = QPushButton("Подписать")
        self.verify_button = QPushButton("Проверить подпись")
        self.signature_label = QLabel("Подпись:")
        self.signature_edit = QLineEdit()
        self.signature_edit.setReadOnly(True)
        self.result_label = QLabel("Результат проверки:")
        self.result_edit = QLineEdit()
        self.result_edit.setReadOnly(True)
        self.generate_key_button.clicked.connect(self.generate_keys)
        self.verify_button.clicked.connect(self.verify_signature)
        self.sign_button.clicked.connect(self.sign_text)
        self.save_key_button.clicked.connect(self.save_keys)
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.generate_key_button)
        layout.addWidget(self.save_key_button)
        layout.addWidget(self.public_key_label)
        layout.addWidget(self.public_key_edit)
        layout.addWidget(self.sign_button)
        layout.addWidget(self.signature_label)
        layout.addWidget(self.signature_edit)
        layout.addWidget(self.verify_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_edit)
        self.setLayout(layout)

        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.public_key_edit.setText(
            self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
        )

    def save_keys(self):
        if self.private_key and self.public_key:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить ключи", "", "Ключи (*.pem)")
            if file_path:
                try:
                    with open(file_path, "wb") as f:
                        f.write(
                            self.private_key.private_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
                            )
                        )
                    public_key_path = file_path.replace(".pem", "_public.pem")
                    with open(public_key_path, "wb") as f:
                        f.write(
                            self.public_key.public_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PublicFormat.SubjectPublicKeyInfo,
                            )
                        )
                    print("Ключи успешно сохранены!")
                except Exception:
                    print(f"Ошибка при сохранении ключей: {Exception}")
        else:
            print("Сначала сгенерируйте ключи.")

    def sign_text(self):
        text = self.text_edit.toPlainText().encode("utf-8")
        if self.private_key:
            signature = self.private_key.sign(
                text,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            self.signature_edit.setText(base64.b64encode(signature).decode("utf-8"))
        else:
            self.result_edit.setText("Сначала сгенерируйте ключи")

    def verify_signature(self):
        signature = base64.b64decode(self.signature_edit.text())
        text = self.text_edit.toPlainText().encode("utf-8")
        if self.public_key:
            try:
                self.public_key.verify(
                    signature,
                    text,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                self.result_edit.setText("Подпись верна")
            except InvalidSignature:
                self.result_edit.setText("Подпись неверна")
        else:
            self.result_edit.setText("Сначала сгенерируйте ключи")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Signature()
    ex.show()
    sys.exit(app.exec())
