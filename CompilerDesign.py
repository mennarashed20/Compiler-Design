import tkinter as tk
from tkinter import ttk
import re

TOKENS = {
    'KEYWORD': r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|restrict|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while|_Bool|_Complex|_Imaginary)\b',
    'PREPROCESSOR': r'#\s*(include|define|undef|if|ifdef|ifndef|else|elif|endif|error|pragma)\s*<([a-zA-Z0-9_.]+)>',
    'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    'NUMBER': r'\b\d+(\.\d+)?\b',
    'OPERATOR': r'[\+\-\*/=<>!]+',
    'PUNCTUATOR': r'[;,\(\)\{\}]',
    'COMMENT': r'//.*?$|/\*.*?\*/'
}

RESERVED_WORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
}

def analyze_tokens(code):
    tokens = []
    
    comments = re.findall(TOKENS['COMMENT'], code, re.DOTALL | re.MULTILINE)
    tokens.extend((comment.strip(), 'COMMENT') for comment in comments)
    code = re.sub(TOKENS['COMMENT'], '', code, flags=re.DOTALL | re.MULTILINE)

    directives = re.findall(TOKENS['PREPROCESSOR'], code, re.MULTILINE)
    tokens.extend((f"#{directive} <{header}>", 'PREPROCESSOR') for directive, header in directives)
    code = re.sub(TOKENS['PREPROCESSOR'], '', code)

    for token_type, pattern in TOKENS.items():
        if token_type not in ['COMMENT', 'PREPROCESSOR']:
            matches = re.finditer(pattern, code)
            for match in matches:
                token_value = match.group()
                if token_type == 'IDENTIFIER' and token_value in RESERVED_WORDS:
                    tokens.append((token_value, 'KEYWORD'))
                else:
                    tokens.append((token_value, token_type))

    return tokens


def show_tokens(tokens):
    output.delete('1.0', tk.END)
    for value, token_type in tokens:
        output.insert(tk.END, f"{value} ({token_type})\n", token_type.lower())

app = tk.Tk()
app.title("Python Language Scanner")
app.geometry("700x600")
app.configure(bg="#f0f4f8")

entry_frame = ttk.Frame(app, padding="10")
entry_frame.pack(pady=10)

input_code = tk.Text(entry_frame, width=80, height=15, wrap='word', font=("Arial", 12))
input_code.pack()


scan_btn = ttk.Button(entry_frame, text="Analyze Code", command=lambda: show_tokens(analyze_tokens(input_code.get("1.0", tk.END))))
scan_btn.pack(pady=10)

output_frame = ttk.Frame(app, padding="10")
output_frame.pack()
output = tk.Text(output_frame, width=80, height=20, wrap='word', font=("Arial", 12))
output.pack()


output.tag_configure("keyword", foreground="#1f77b4")
output.tag_configure("preprocessor", foreground="#9467bd")
output.tag_configure("identifier", foreground="#ff7f0e")
output.tag_configure("number", foreground="#d62728")
output.tag_configure("operator", foreground="#2ca02c")
output.tag_configure("punctuator", foreground="#8c564b")
output.tag_configure("comment", foreground="#7f7f7f")

app.mainloop()
