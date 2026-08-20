import os
import base64
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CalculatorVaultApp(App):
    def build(self):
        self.secret_passcode = "7777"
        self.STORAGE_FILE = "vault_storage.dat"
        self.expression = ""

        # Main Layout (Swappable screens simulated using active references)
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Build Calculator Screen elements
        self.calc_screen = BoxLayout(orientation='vertical')
        self.display = TextInput(font_size=40, halign='right', readonly=True, size_hint_y=0.2, background_color=(0.15,0.15,0.15,1), foreground_color=(1,1,1,1))
        self.calc_screen.add_widget(self.display)
        
        grid = GridLayout(cols=4, spacing=5)
        buttons = [
            ['C', '/', '*', '-'],
            ['7', '8', '9', '+'],
            ['4', '5', '6', '='],
            ['1', '2', '3', '0']
        ]
        for row in buttons:
            for label in row:
                btn = Button(text=label, font_size=30, background_color=(0.23,0.23,0.23,1) if label not in ['=','C','/','*','-','+'] else (0.8,0.4,0,1))
                btn.bind(on_press=self.on_button_press)
                grid.add_widget(btn)
        self.calc_screen.add_widget(grid)
        
        # Build Vault Screen elements
        self.vault_screen = BoxLayout(orientation='vertical', spacing=10)
        self.vault_screen.add_widget(Label(text="🔒 AES Encrypted Vault", font_size=24, size_hint_y=0.1, color=(1,0.6,0,1)))
        self.secret_input = TextInput(multiline=True, font_size=18, background_color=(0.18,0.18,0.18,1), foreground_color=(1,1,1,1))
        self.vault_screen.add_widget(self.secret_input)
        
        control_panel = BoxLayout(size_hint_y=0.15, spacing=10)
        save_btn = Button(text="Save", background_color=(0.15,0.65,0.27,1))
        save_btn.bind(on_press=self.save_vault)
        lock_btn = Button(text="Lock", background_color=(0.85,0.2,0.27,1))
        lock_btn.bind(on_press=self.lock_vault)
        control_panel.add_widget(save_btn)
        control_panel.add_widget(lock_btn)
        self.vault_screen.add_widget(control_panel)

        # Show Calculator first
        self.main_layout.add_widget(self.calc_screen)
        return self.main_layout

    def get_crypto_key(self):
        salt = b'\x84\xfa\xbc\xdd\x0f\x91\xca\xfe'
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        return base64.urlsafe_b64encode(kdf.derive(self.secret_passcode.encode()))

    def on_button_press(self, instance):
        text = instance.text
        if text == "C":
            self.expression = ""
            self.display.text = ""
        elif text == "=":
            if self.expression == self.secret_passcode:
                self.expression = ""
                self.display.text = ""
                self.show_vault()
            else:
                try:
                    self.display.text = str(eval(self.expression))
                    self.expression = self.display.text
                except:
                    self.display.text = "Error"
                    self.expression = ""
        else:
            self.expression += text
            self.display.text = self.expression

    def show_vault(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.vault_screen)
        if os.path.exists(self.STORAGE_FILE):
            try:
                with open(self.STORAGE_FILE, "rb") as f:
                    encrypted_data = f.read()
                f_cipher = Fernet(self.get_crypto_key())
                self.secret_input.text = f_cipher.decrypt(encrypted_data).decode('utf-8')
            except:
                self.secret_input.text = "Error decrypting file."

    def save_vault(self, instance):
        try:
            content = self.secret_input.text.strip().encode('utf-8')
            f_cipher = Fernet(self.get_crypto_key())
            with open(self.STORAGE_FILE, "wb") as f:
                f.write(f_cipher.encrypt(content))
        except: pass

    def lock_vault(self, instance):
        self.secret_input.text = ""
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.calc_screen)

if __name__ == '__main__':
    CalculatorVaultApp().run()
