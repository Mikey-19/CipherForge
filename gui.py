import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QTabWidget, QComboBox, QHBoxLayout, QSpinBox, QFileDialog
)
from crackers import caesar, vigenere

class CipherForgeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CipherForge - Cryptanalysis Suite")
        self.setGeometry(200, 200, 900, 600)

        # ---------------- Tabs ----------------
        self.tabs = QTabWidget()
        self.init_crack_tab()
        self.init_encrypt_tab()

        # ---------------- Theme Toggle ----------------
        self.theme_dark = True  # start with dark theme
        toggle_btn = QPushButton("Toggle Theme")
        toggle_btn.clicked.connect(self.toggle_theme)

        # Layout for toggle button + tabs
        self.tabs_layout_widget = QWidget()
        tabs_layout = QVBoxLayout()
        tabs_layout.addWidget(toggle_btn)
        tabs_layout.addWidget(self.tabs)
        self.tabs_layout_widget.setLayout(tabs_layout)
        self.setCentralWidget(self.tabs_layout_widget)

        # Apply initial dark theme
        self.apply_dark_theme()

    # ---------------- Dark & Light Themes ----------------
    def apply_dark_theme(self):
        dark_style = """
        QWidget {
            background-color: #2e2e2e;
            color: #f0f0f0;
            font-family: Arial;
            font-size: 12pt;
        }
        QTextEdit, QSpinBox, QComboBox {
            background-color: #3c3c3c;
            color: #f0f0f0;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton {
            background-color: #555;
            color: #f0f0f0;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #777;
        }
        QTabWidget::pane {
            border: 1px solid #444;
            background: #2e2e2e;
        }
        QTabBar::tab {
            background: #3c3c3c;
            padding: 6px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #555;
        }
        QLabel {
            font-weight: bold;
        }
        """
        self.setStyleSheet(dark_style)

    def apply_light_theme(self):
        light_style = """
        QWidget {
            background-color: #f5f5f5;
            color: #2e2e2e;
            font-family: Arial;
            font-size: 12pt;
        }
        QTextEdit, QSpinBox, QComboBox {
            background-color: #ffffff;
            color: #2e2e2e;
            border: 1px solid #aaa;
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton {
            background-color: #ddd;
            color: #2e2e2e;
            border-radius: 6px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #bbb;
        }
        QTabWidget::pane {
            border: 1px solid #ccc;
            background: #f5f5f5;
        }
        QTabBar::tab {
            background: #e0e0e0;
            padding: 6px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #ddd;
        }
        QLabel {
            font-weight: bold;
        }
        """
        self.setStyleSheet(light_style)

    def toggle_theme(self):
        if self.theme_dark:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()
        self.theme_dark = not self.theme_dark

    # ---------------- Crack Tab ----------------
    def init_crack_tab(self):
        self.crack_tab = QWidget()
        layout = QVBoxLayout()

        self.cipher_selector = QComboBox()
        self.cipher_selector.addItems(["Caesar", "Vigenère"])
        layout.addWidget(QLabel("Select Cipher:"))
        layout.addWidget(self.cipher_selector)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Paste ciphertext here...")
        layout.addWidget(QLabel("Ciphertext:"))
        layout.addWidget(self.input_box)

        options_layout = QHBoxLayout()
        options_layout.addWidget(QLabel("Show top N candidates:"))
        self.top_n_spin = QSpinBox()
        self.top_n_spin.setRange(1, 26)
        self.top_n_spin.setValue(5)
        options_layout.addWidget(self.top_n_spin)
        options_layout.addStretch()
        layout.addLayout(options_layout)

        crack_btn = QPushButton("Crack Cipher")
        crack_btn.clicked.connect(self.run_crack)
        layout.addWidget(crack_btn)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.result_box)

        # Export button
        export_btn = QPushButton("Export Results")
        export_btn.clicked.connect(self.export_crack_results)
        layout.addWidget(export_btn)

        self.crack_tab.setLayout(layout)
        self.tabs.addTab(self.crack_tab, "Crack Cipher")

    def run_crack(self):
        cipher = self.cipher_selector.currentText()
        ciphertext = self.input_box.toPlainText().strip()
        top_n = self.top_n_spin.value()

        if not ciphertext:
            self.result_box.setPlainText("⚠️ Please enter ciphertext.")
            return

        try:
            if cipher == "Caesar":
                results = caesar.crack(ciphertext, top_n=top_n)
            elif cipher == "Vigenère":
                results = vigenere.crack(ciphertext)
            else:
                self.result_box.setPlainText("⚠️ Cipher not supported.")
                return

            output_lines = []
            for score, key, plaintext in results:
                output_lines.append(f"Key/Shift {key} | Score: {score:.4f}\n{plaintext}")

            self.result_box.setPlainText("\n\n".join(output_lines))
        except Exception as e:
            self.result_box.setPlainText(f"❌ Error: {e}")

    def export_crack_results(self):
        if not self.result_box.toPlainText().strip():
            self.result_box.setPlainText("⚠️ No results to export.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Crack Results",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.result_box.toPlainText())
                self.result_box.setPlainText(f"✅ Results saved to:\n{file_path}")
            except Exception as e:
                self.result_box.setPlainText(f"❌ Error saving file: {e}")

    # ---------------- Encrypt Tab ----------------
    def init_encrypt_tab(self):
        self.encrypt_tab = QWidget()
        layout = QVBoxLayout()

        self.encrypt_cipher_selector = QComboBox()
        self.encrypt_cipher_selector.addItems(["Caesar", "Vigenère"])
        layout.addWidget(QLabel("Select Cipher:"))
        layout.addWidget(self.encrypt_cipher_selector)

        self.plaintext_box = QTextEdit()
        self.plaintext_box.setPlaceholderText("Enter plaintext here...")
        layout.addWidget(QLabel("Plaintext:"))
        layout.addWidget(self.plaintext_box)

        key_layout = QHBoxLayout()
        self.key_input = QTextEdit()
        self.key_input.setFixedHeight(30)
        self.key_input.setPlaceholderText("Enter key (or shift for Caesar)")
        key_layout.addWidget(QLabel("Key / Shift:"))
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        encrypt_btn = QPushButton("Generate Ciphertext")
        encrypt_btn.clicked.connect(self.run_encrypt)
        layout.addWidget(encrypt_btn)

        self.encrypt_result_box = QTextEdit()
        self.encrypt_result_box.setReadOnly(True)
        layout.addWidget(QLabel("Ciphertext:"))
        layout.addWidget(self.encrypt_result_box)

        # Export button
        export_encrypt_btn = QPushButton("Export Ciphertext")
        export_encrypt_btn.clicked.connect(self.export_encrypt_results)
        layout.addWidget(export_encrypt_btn)

        self.encrypt_tab.setLayout(layout)
        self.tabs.addTab(self.encrypt_tab, "Encrypt Cipher")

    def run_encrypt(self):
        cipher = self.encrypt_cipher_selector.currentText()
        plaintext = self.plaintext_box.toPlainText().strip()
        key = self.key_input.toPlainText().strip()

        if not plaintext:
            self.encrypt_result_box.setPlainText("⚠️ Please enter plaintext.")
            return

        try:
            if cipher == "Caesar":
                if not key.isdigit():
                    self.encrypt_result_box.setPlainText("⚠️ Enter numeric shift for Caesar.")
                    return
                shift = int(key)
                ciphertext = caesar.encrypt(plaintext, shift)
            elif cipher == "Vigenère":
                if not key.isalpha():
                    self.encrypt_result_box.setPlainText("⚠️ Enter alphabetic key for Vigenère.")
                    return
                ciphertext = vigenere.encrypt(plaintext, key)
            else:
                self.encrypt_result_box.setPlainText("⚠️ Cipher not supported.")
                return

            self.encrypt_result_box.setPlainText(ciphertext)
        except Exception as e:
            self.encrypt_result_box.setPlainText(f"❌ Error: {e}")

    def export_encrypt_results(self):
        if not self.encrypt_result_box.toPlainText().strip():
            self.encrypt_result_box.setPlainText("⚠️ No ciphertext to export.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Ciphertext",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.encrypt_result_box.toPlainText())
                self.encrypt_result_box.setPlainText(f"✅ Ciphertext saved to:\n{file_path}")
            except Exception as e:
                self.encrypt_result_box.setPlainText(f"❌ Error saving file: {e}")

# ---------------- Main ----------------
def main():
    app = QApplication(sys.argv)
    gui = CipherForgeGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
