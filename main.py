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

        # Main Layout (Acts as a container for swapping screens)
        self.main_layout = BoxLayout(orientation='vertical')
        
        # 1. Build Calculator Screen
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
        
        # 2. Build Vault Screen
        self.vault_screen = BoxLayout(orientation='vertical', spacing=10)
        self.vault_screen.add_widget(Label(text="🔒 AES Encrypted Vault", font_size=24, size_hint_y=0.1, color=(1,0.6,0,1)))
        
        self.secret_input = TextInput(multiline=True, font_size=18, background_color=(0.18,0.18,0.18,1), foreground_color=(1,1,1,1))
        self.vault_screen.add_widget(self.secret_input)
        
        # Action buttons for the Vault
        vault_btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        save_btn = Button(text="Save & Lock", background_color=(0.1, 0.6, 0.2, 1))
        save_btn.bind(on_press=self.save_vault_data)
        
        exit_btn = Button(text="Exit Vault", background_color=(0.7, 0.1, 0.1, 1))
        exit_btn.bind(on_press=self.exit_vault)
        
        vault_btn_layout.add_widget(save_btn)
        vault_btn_layout.add_widget(exit_btn)
        self.vault_screen.add_widget(vault_btn_layout)

        # Initialize with the Calculator Screen visible
        self.main_layout.add_widget(self.calc_screen)
        return self.main_layout

    # --- Cryptography Helpers ---
    def _derive_key(self):
        """Derives a secure Fernet key from the passcode string."""
        salt = b'fixed_salt_for_demo'  # In production, use a unique file-based salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.secret_passcode.encode()))

    # --- Button & Screen Logic ---
    def on_button_press(self, instance):
        text = instance.text

        if text == 'C':
            self.expression = ""
        elif text == '=':
            # Check secret trigger condition before evaluating
            if self.expression == self.secret_passcode:
                self.open_vault()
                return
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "Error"
        else:
            if self.expression == "Error":
                self.expression = ""
            self.expression += text

        self.display.text = self.expression

    def open_vault(self):
        """Swaps calculator layout with vault layout and decrypts saved data."""
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.vault_screen)
        self.secret_input.text = self.load_vault_data()

    def exit_vault(self, instance=None):
        """Clears vault layout and restores the calculator display."""
        self.expression = ""
        self.display.text = ""
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.calc_screen)

    # --- Storage & Encryption Logic ---
    def save_vault_data(self, instance):
        """Encrypts data inside text input and saves it to a local file."""
        try:
            key = self._derive_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(self.secret_input.text.encode())
            
            with open(self.STORAGE_FILE, "wb") as f:
                f.write(encrypted_data)
            
            self.exit_vault()
        except Exception as e:
            self.secret_input.text = f"Error saving data: {str(e)}"

    def load_vault_data(self):
        """Loads and decrypts data from local storage if file exists."""
        if not os.path.exists(self.STORAGE_FILE):
            return "Type your secrets here..."
        
        try:
            key = self._derive_key()
            fernet = Fernet(key)
            with open(self.STORAGE_FILE, "rb") as f:
                encrypted_data = f.read()
            return fernet.decrypt(encrypted_data).decode()
        except Exception:
            return "Error: Could not decrypt or load data."

if __name__ == '__main__':
    CalculatorVaultApp().run()
