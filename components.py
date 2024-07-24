from PyQt5.QtWidgets import (
    QPushButton,
    QLineEdit
)
import json



class EditLine(QLineEdit):
    def __init__(self, text: str):
        super().__init__()
        self.setFixedSize(320, 60)
        self.setPlaceholderText(text)
        self.setStyleSheet("""
            border: 1px solid #e0a309;
            background-color: #ffffff;
            border-radius: 16px;
            color: #080808;
            padding: 8px;
            font-size: 26px;
        """)

class MyButton(QPushButton):
    def __init__(self, text: str, color="#bc8f5b", font_color="#ffffff"):
        super().__init__(text)
        self.setFixedSize(320, 60)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                font-size: 26px;
                padding: 8px;
                border-radius: 16px;
                border: none;
                color: {font_color};
            }}
            QPushButton:hover {{
                background-color: #ffffff;
                border: 2px solid "#bc8f5b";
                color: "#bc8f5b";
            }}
        """)
        

class JsonHandling:
    
    @staticmethod
    def read_file():
        try:
            with open("users.json", "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    @staticmethod
    def write_file(data: dict):
        try:
            temp = JsonHandling.read_file()
            temp.append(data)
            with open("users.json", "w") as file:
                json.dump(temp, file, indent=4)
            return True
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        