# -*- coding: utf-8 -*-
"""parser

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/170nziwfwHCMzEhcxU2s9hxM7AvAzMVKg
"""

class RecursiveDescentParser:
    def __init__(self):
        self.grammar = {}
        self.non_terminals = []
        self.stack = []
        self.input_string = []
        self.accepted = False

    def input_grammar(self):
        print("👇 Enter Your Grammar 👇")
        self.grammar.clear()
        self.non_terminals = []
        num_non_terminals = int(input("Enter the number of non-terminals: "))

        for _ in range(num_non_terminals):
            nt = input("Enter the non-terminal: ").strip()
            self.non_terminals.append(nt)
            rules = []
            print(f"Enter rules for non-terminal '{nt}' (type 'end' to stop):")
            while True:
                rule = input(">> ").strip()
                if rule.lower() == 'end':
                    break
                rules.append(rule)
            self.grammar[nt] = rules

    def is_simple_grammar(self):
        for rules in self.grammar.values():
            for rule in rules:
                if rule.startswith(tuple(self.non_terminals)):
                    return False
        return True

    def parse(self, current, position):
        if position == len(self.input_string) and current == "":
            return True
        if current == "" or position == len(self.input_string):
            return False

        next_symbol = current[0]
        if next_symbol in self.grammar:  # Non-terminal
            for rule in self.grammar[next_symbol]:
                if self.parse(rule + current[1:], position):
                    self.stack.append((next_symbol, rule))
                    return True
        elif position < len(self.input_string) and next_symbol == self.input_string[position]:  # Terminal match
            return self.parse(current[1:], position + 1)
        return False

    def check_string(self, input_str):
        self.input_string = input_str
        self.stack.clear()
        self.accepted = self.parse(self.non_terminals[0], 0)  # Start with the first non-terminal
        return self.accepted

    def print_tree(self):
        print("\nParser Tree:")
        for nt, rule in reversed(self.stack):
            print(f"{nt} -> {rule}")
        print()

    def menu(self):
        while True:
            print("\n=======================================")
            print("1-Another Grammar.")
            print("2-Another String.")
            print("3-Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.input_grammar()
                if self.is_simple_grammar():
                    print("The Grammar is simple.")
                else:
                    print("The Grammar isn't simple.\nTry again.")
                    continue
            elif choice == '2':
                input_str = input("Enter the string want to be checked: ")
                input_list = list(input_str)
                print(f"The input String: {input_list}")
                if self.check_string(input_list):
                    print("Your input String is Accepted.")
                    self.print_tree()
                else:
                    print("Your input String is Rejected.")
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    parser = RecursiveDescentParser()
    parser.input_grammar()
    while not parser.is_simple_grammar():
        print("The Grammar isn't simple.\nTry again.")
        parser.input_grammar()
    print("The Grammar is simple.")
    parser.menu()