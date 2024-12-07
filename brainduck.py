import customtkinter as ctk
from tkinter import filedialog, messagebox
#is it ethical to say f**k when talking abt brainf**k

class BrainfCompiler:
    def __init__(self, master):
        self.master = master
        master.title("Brainf**k Compiler")
        master.geometry("540x520")

        self.input_label = ctk.CTkLabel(master, text="Brainf**k Code:")
        self.input_label.pack(pady=(5, 0))
        self.input_text = ctk.CTkTextbox(master, width=500, height=100)
        self.input_text.pack(pady=(0, 10))

        self.file_buttons_frame = ctk.CTkFrame(master)
        self.file_buttons_frame.pack(pady=(0, 10))

        self.save_button = ctk.CTkButton(self.file_buttons_frame, text="Save Code", command=self.save_code)
        self.save_button.grid(row=0, column=0, padx=5)

        self.load_button = ctk.CTkButton(self.file_buttons_frame, text="Load Code", command=self.load_code)
        self.load_button.grid(row=0, column=1, padx=5)

        self.memory_label = ctk.CTkLabel(master, text="Memory Size:")
        self.memory_label.pack()
        self.memory_size = ctk.IntVar(value=30000)
        self.memory_entry = ctk.CTkEntry(master, textvariable=self.memory_size, width=100)
        self.memory_entry.pack(pady=(0, 10))

        self.output_format = ctk.StringVar(value="ASCII")
        self.format_dropdown = ctk.CTkOptionMenu(
            master,
            values=["ASCII", "Decimal", "Hex"],
            variable=self.output_format
        )
        self.format_dropdown.pack(pady=10)

        self.run_button = ctk.CTkButton(master, text="Run", command=self.run_code)
        self.run_button.pack(pady=5)

        self.output_label = ctk.CTkLabel(master, text="Output:")
        self.output_label.pack(pady=(5, 0))
        self.output_text = ctk.CTkTextbox(master, width=500, height=100, state="disabled")
        self.output_text.pack(pady=(0, 10))

        self.copy_button = ctk.CTkButton(master, text="Copy Output", command=self.copy_output)
        self.copy_button.pack(pady=5)

    def run_code(self):
        code = self.input_text.get("1.0", "end").strip()
        error = self.check_syntax(code)
        if error:
            messagebox.showerror("Syntax Error", error)
            return

        memory_size = self.memory_size.get()
        if memory_size <= 0:
            messagebox.showerror("Invalid Memory Size", "Memory size must be greater than zero.")
            return

        raw_output = self.execute_brainf(code, memory_size)
        selected_format = self.output_format.get()

        if selected_format == "ASCII":
            output = raw_output  # plaintext
        elif selected_format == "Decimal":
            output = " ".join(str(ord(c)) for c in raw_output)
        elif selected_format == "Hex":
            output = " ".join(hex(ord(c))[2:].zfill(2) for c in raw_output)

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", output)
        self.output_text.configure(state="disabled")

    def check_syntax(self, code):
        stack = []
        for i, c in enumerate(code):
            if c == '[':
                stack.append(i)
            elif c == ']':
                if not stack:
                    return f"Unmatched ']' at position {i}"
                stack.pop()
        if stack:
            return f"Unmatched '[' at position {stack.pop()}"
        return None

    def execute_brainf(self, code, memory_size):
        code = ''.join(c for c in code if c in "><+-.,[]")
        tape = [0] * memory_size
        pointer = 0
        code_pointer = 0
        output = []
        stack = []

        while code_pointer < len(code):
            command = code[code_pointer]

            if command == '>':
                pointer += 1
                if pointer >= len(tape):
                    tape.append(0)

            elif command == '<':
                pointer = max(0, pointer - 1)

            elif command == '+':
                tape[pointer] = (tape[pointer] + 1) % 256

            elif command == '-':
                tape[pointer] = (tape[pointer] - 1) % 256

            elif command == '.':
                output.append(chr(tape[pointer]))

            elif command == ',':
                tape[pointer] = 0

            elif command == '[':
                if tape[pointer] == 0:
                    loop = 1
                    while loop > 0:
                        code_pointer += 1
                        if code[code_pointer] == '[':
                            loop += 1
                        elif code[code_pointer] == ']':
                            loop -= 1
                else:
                    stack.append(code_pointer)

            elif command == ']':
                if tape[pointer] != 0:
                    code_pointer = stack[-1]
                else:
                    stack.pop()

            code_pointer += 1

        return ''.join(output)

    def save_code(self):
        code = self.input_text.get("1.0", "end").strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".bf", filetypes=[("Brainf**k files", "*.bf"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(code)
            messagebox.showinfo("Saved", f"Code saved to {file_path}")

    def load_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Brainf**k files", "*.bf"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", code)

    def copy_output(self):
        output = self.output_text.get("1.0", "end").strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(output)
        self.master.update()
        messagebox.showinfo("Copied", "Output copied to clipboard!")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = BrainfCompiler(root)
    root.mainloop()
