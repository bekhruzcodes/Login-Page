from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel
)
from components import EditLine, MyButton, JsonHandling
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys
import re


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 800)
        self.setStyleSheet("background-color: #ffffff;")
        self.createGui()
        self.show()

    def createGui(self):
        self.v_box = QVBoxLayout()
        self.setWindowIcon(QIcon("Najot_Talim.png"))
        self.setWindowTitle("Chat")
        
        # Logo
        self.logo = QLabel()
        self.logo_pixmap = QPixmap("Najot_Talim.png")
        scaled_pixmap = self.logo_pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        self.logo.setPixmap(scaled_pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        
        # Other elements for V_BOX
        self.username_edit = EditLine("Username")
        self.pwd_edit = EditLine("Password")
        self.login_btn = MyButton("Login")
        self.login_btn.clicked.connect(self.check_user)
        self.create_new_account_btn = MyButton("Create new account", "#f1f0ee", "#0d1523")
        self.create_new_account_btn.clicked.connect(self.open_registration)
        self.footer=QLabel("""© Najot Ta'lim Chat by Bekhruzbek""")
        self.footer.setStyleSheet("font-family: Arial; font-size: 18px;color:#616161")
        
        
        # Add widgets => V_BOX
        self.v_box.addWidget(self.logo)
        self.v_box.addWidget(self.username_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.pwd_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.login_btn, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.create_new_account_btn, 0, Qt.AlignCenter)
        self.v_box.addSpacing(120)
        self.v_box.addWidget(self.footer, 0, Qt.AlignCenter)
        
        # Setting V_BOX
        self.setLayout(self.v_box)
    
    def check_user(self):
        tusername = self.username_edit.text()
        tpassword = self.pwd_edit.text()
        
        if not tusername:
            self.error_mes(self.username_edit)
            return False
        if not tpassword:
            self.error_mes(self.pwd_edit)
            return False
        
        users_list = JsonHandling.read_file()
        user_found = False

        for user in users_list:
            if tusername == user["username"]:
                user_found = True
                if tpassword == user["password"]:
                    print(f"{tusername} logged in successfully.")
                    self.welcome()
                    return
                
                else:
                    self.error_mes(self.pwd_edit, "Incorrect password")
                    return

        if not user_found:
            self.error_mes(self.username_edit, "No such user found")
                        
                
                
        
    def error_mes(self, editline, message="Please enter"):
        text = editline.placeholderText()
        editline.clear()
        if message not in text:
            editline.setPlaceholderText(" ")
            editline.setPlaceholderText(f"{message} ")
            editline.setStyleSheet("""
                border: 1px solid #e0a309;
                background-color: #ffffff;
                border-radius: 16px;
                color: red;
                padding: 8px;
                font-size: 26px;
            
        """)
            
        
    def open_registration(self):
        self.close()
        self.registration_page = Registration()
        
    def welcome(self):
        self.close()
        self.welcome_page = WelcomePage()
    


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 800)
        self.setWindowTitle("Join us")
        self.setWindowIcon(QIcon("Najot_Talim.png"))
        self.setStyleSheet("background-color: #ffffff;")
        self.createGui()
        self.show()
    
    
    def createGui(self):
        self.v_box = QVBoxLayout()
        
        self.sign=QLabel("👋")
        self.sign.setStyleSheet("font-size:120px")
        
        self.welcome_mes = QLabel("Welcome Chatty")
        self.welcome_mes.setStyleSheet("""
                                       font-size: 40px;
                                       color: #333333;
                                       """)
        # Edit Lines
        self.email_edit = EditLine("Email")
        self.fullname_edit = EditLine("Fullname")
        self.username_edit = EditLine("Username")
        self.pwd_edit = EditLine("Password")
        # Button
        self.signup_btn = MyButton("Sign Up")
        self.signup_btn.clicked.connect(self.add_user)
        # Footer Label
        self.footer=QLabel("""© Najot Ta'lim Chat by Bekhruzbek""")
        self.footer.setStyleSheet("font-family: Arial; font-size: 18px;color:#616161")
        
        
        
        self.v_box.addWidget(self.sign, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.welcome_mes, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.email_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.fullname_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.username_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.pwd_edit, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.signup_btn, 0, Qt.AlignCenter)
        self.v_box.addSpacing(140)
        self.v_box.addWidget(self.footer, 0, Qt.AlignCenter)
        
        
        self.setLayout(self.v_box)
        
        
    def add_user(self):
        tname = self.fullname_edit.text()
        tusername = self.username_edit.text()
        temail = self.email_edit.text()
        tpassword = self.pwd_edit.text()

        fields_empty = False

        if not tname:
            self.error_mes(self.fullname_edit)
            fields_empty = True
        if not tusername:
            self.error_mes(self.username_edit)
            fields_empty = True
        if not temail:
            self.error_mes(self.email_edit)
            fields_empty = True
        if not tpassword:
            self.error_mes(self.pwd_edit)
            fields_empty = True

        if not fields_empty:
            if self.validation():
               new_user={"fullname": tname, "username":tusername, "email":temail, "password":tpassword}
               if JsonHandling.write_file(new_user):
                   self.open_login()
               else:
                   # new error window
                   print("Error in writing to the file.")
                   pass


    def validation(self) -> bool:
        
        if not self.check_email(self.email_edit.text()):
            self.error_mes(self.email_edit, "Not a valid email")
            return False
        
        if len(self.username_edit.text()) < 5:
            self.error_mes(self.username_edit, "At least 5 characters")
            return False
            
        if len(self.pwd_edit.text())<8:
            self.error_mes(self.pwd_edit, "At least 8 characters")
            return False
        elif not re.search(r'[A-Z]', self.pwd_edit.text()):
            self.error_mes(self.pwd_edit, "At least 1 uppercase")
            return False
        elif not re.search(r'[a-z]', self.pwd_edit.text()):
            self.error_mes(self.pwd_edit, "At least 1 lowercase")
            return False
        elif not re.search(r'\d', self.pwd_edit.text()):
            self.error_mes(self.pwd_edit, "At least 1 digit")
            return False
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.pwd_edit.text()):
            self.error_mes(self.pwd_edit, "At least 1 special character")
            return False
             
        return True
    
    
    def check_email(self, email : str):
        email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", 
                         "icloud.com", "aol.com", "protonmail.com", "zoho.com", 
                         "mail.com", "gmx.com", "yandex.com", "microsoft.com", 
                         "apple.com", "amazon.com", "ibm.com", "intel.com", "tesla.com", 
                         "harvard.edu", "stanford.edu", "mit.edu", "ox.ac.uk", "cam.ac.uk", 
                         "gov.uk", "gov.au", "gov.ca", "gov.in", "gov.us"]

        userdomain = (email.split("@"))[-1]

        if userdomain in email_domains:
            return True
        return False


    def error_mes(self, editline, message="Please enter"):
        text = editline.placeholderText()
        editline.clear()
        if message not in text:
            editline.setPlaceholderText(" ")
            editline.setPlaceholderText(f"{message} ")
            editline.setStyleSheet("""
                border: 1px solid #e0a309;
                background-color: #ffffff;
                border-radius: 16px;
                color: red;
                padding: 8px;
                font-size: 26px;
            
        """)
    
       
    def open_login(self):
        self.close()
        self.login_page = Login()
        


class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 800)
        self.setStyleSheet("background-color: #ffffff;")
        self.setWindowTitle(" hellooo")
        self.setWindowIcon(QIcon("Najot_Talim.png"))
        
        self.v_box = QVBoxLayout() 
        
        self.label = QLabel("Welcome, happy to see you here")
        self.label.setStyleSheet("font-size: 30px; color: #333333; font-weight: bold;")
        
        self.smile = QLabel(":)")
        self.smile.setStyleSheet("font-size:100px; color: #bc8e5b")
        
        self.label2 = QLabel("We are yet to connect it to the real app.")
        self.label2.setStyleSheet("font-size: 24px; color: #617af1; font-family: arial;")
        
        self.footer=QLabel("""© Najot Ta'lim Chat by Bekhruzbek""")
        self.footer.setStyleSheet("font-family: Arial; font-size: 18px;color:#616161")
        
        self.v_box.addSpacing(80)
        self.v_box.addWidget(self.label, 0, Qt.AlignCenter)
        self.v_box.addWidget(self.smile, 80, Qt.AlignCenter)
        self.v_box.addWidget(self.label2, 0, Qt.AlignCenter)
        self.v_box.addStretch(50)
        self.v_box.addWidget(self.footer, 0, Qt.AlignCenter)
        
        self.setLayout(self.v_box)
        self.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Login()
    sys.exit(app.exec_())
