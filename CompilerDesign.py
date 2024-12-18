import tkinter as tk
from tkinter import ttk
import re

# Define token patterns
TOKEN_TYPES = {
    'KEYWORD': r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|_Imaginary)\b',
    'PREPROCESSOR_DIRECTIVE': r'#\s*(include|define|undef|if|ifdef|ifndef|else|elif|endif|error|pragma)\s*<([a-zA-Z0-9_.]+)>',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'NUMBER': r'\b\d+(\.\d+)?\b',
    'OPERATOR': r'[\+\-\*/=<>!]+',
    'PUNCTUATOR': r'[;,\(\)\{\}]',
    'COMMENT': r'//.*?$|/\*.*?\*/'
}

RESERVED_WORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'inline', 'int', 'long', 'register', 'restrict', 'return', 'short',
    'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
    'unsigned', 'void', 'volatile', 'while', '_Bool', '_Complex', '_Imaginary'
}

# Scan code and classify tokens
def scan_code(code):
    tokens = []
    comments = re.findall(TOKEN_TYPES['COMMENT'], code, re.DOTALL | re.MULTILINE)
    for comment in comments:
        tokens.append((comment.strip(), 'COMMENT'))
    code = re.sub(TOKEN_TYPES['COMMENT'], '', code, flags=re.DOTALL | re.MULTILINE)
    directives = re.findall(TOKEN_TYPES['PREPROCESSOR_DIRECTIVE'], code, re.MULTILINE)
    for directive, header in directives:
        token = f"#{directive} <{header}>"
        tokens.append((token, 'PREPROCESSOR_DIRECTIVE'))
    code = re.sub(TOKEN_TYPES['PREPROCESSOR_DIRECTIVE'], '', code)
    for token_type, pattern in TOKEN_TYPES.items():
        if token_type not in ['COMMENT', 'PREPROCESSOR_DIRECTIVE']:
            matches = re.finditer(pattern, code)
            for match in matches:
                token_value = match.group()
                if token_type == 'IDENTIFIER' and token_value in RESERVED_WORDS:
                    continue
                tokens.append((token_value, token_type))
    return tokens

# Display tokens
def display_tokens(tokens):
    t2.delete('1.0', tk.END)
    for token, token_type in tokens:
        t2.insert(tk.END, f"{token} : {token_type}\n", token_type.lower())

# Welcome screen
# Welcome screen
def show_welcome_screen():
    welcome_frame = ttk.Frame(root)
    welcome_frame.pack(padx=10, pady=10)

    # Welcome message
    welcome_label = ttk.Label(welcome_frame, text="Welcome to the Python Language Scanner!", font=('Arial', 16))
    welcome_label.pack(pady=10)

    # Button to go to the main screen
    start_button = ttk.Button(welcome_frame, text="Start Analysis", command=lambda: go_to_main_screen(welcome_frame))
    start_button.pack(pady=20)

# Go to main screen
def go_to_main_screen(welcome_frame):
    welcome_frame.destroy()
    frame.pack(pady=10)

# Main GUI setup
root = tk.Tk()
root.title("Python Language Scanner")
frame = ttk.Frame(root)
frame.pack_forget()
t1 = tk.Text(frame, width=50, height=10, bg="#f0f8ff", fg="#000080", wrap='word')
t1.pack(pady=5)
scan_button = ttk.Button(frame, text="Scan Code", command=lambda: display_tokens(scan_code(t1.get("1.0", tk.END))))
scan_button.pack(pady=5)
t2 = tk.Text(frame, width=50, height=10, bg="#fff8dc", fg="#8b0000", wrap='word')
t2.pack(pady=5)
t2.tag_configure("keyword", foreground="blue")
t2.tag_configure("preprocessor", foreground="purple")
t2.tag_configure("identifier", foreground="orange")
t2.tag_configure("number", foreground="red")
t2.tag_configure("operator", foreground="brown")
t2.tag_configure("punctuator", foreground="black")
t2.tag_configure("comment", foreground="grey")
show_welcome_screen()
root.mainloop()
