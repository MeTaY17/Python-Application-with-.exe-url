import tkinter  # Importing the tkinter library for GUI
from tkinter import ttk, filedialog, colorchooser, simpledialog, messagebox  # Importing additional modules from tkinter
import os  # Importing os for file operations
import subprocess # Importing subprocess for opening external files

class NotepadApp:

    def __init__(self, master):
        self.master = master
        self.master.title("No Paper Notepad") # Setting the title of the application window
        self.master.geometry("900x600")  # Setting the default window size

        # Default settings for font styles, theme, and text properties
        self.current_font_family = "Helvetica"  # Default font family
        self.current_font_size = 14  # Default font size
        self.bold_active = False  # Bold formatting status
        self.italic_active = False  # Italic formatting status
        self.underline_active = False  # Underline formatting status
        self.word_count = 0  # Word count initialization
        self.char_count = 0  # Character count initialization
        self.current_theme = "Dark"  # Default theme setting

        self.setup_styles()  # Setting up styles
        self.create_toolbar()  # Creating the toolbar for text formatting
        self.create_text_widget()  # Creating the main text area
        self.create_status_bar()  # Creating the status bar
        self.setup_menu()  # Creating the menu bar
        self.update_word_char_count()  # Initial word and character count update

        # Apply the selected theme
        self.apply_theme(self.current_theme)

    def setup_styles(self):
        """
        Sets up the styles for different UI elements.
        """
        style = ttk.Style()
        style.theme_use('clam') # Setting the theme style

        # Light theme styles
        self.light_bg = "#f4f7fb"
        self.light_fg = "#333333"
        self.light_button_bg = "#ffffff"
        self.light_button_fg = "#333333"
        
        # Dark theme styles
        self.dark_bg = "#2e2e2e"
        self.dark_fg = "#ffffff"
        self.dark_button_bg = "#444444"
        self.dark_button_fg = "#ffffff"

        # Styling for status bar
        style.configure('Light.Status.TLabel', background=self.light_bg, foreground=self.light_fg, padding=5)
        style.configure('Dark.Status.TLabel', background=self.dark_bg, foreground=self.dark_fg, padding=5)

        # Styling for buttons: Light, flat, with rounded corners
        style.configure('RoundedButton.TButton', font=('Helvetica', 12), padding=10, relief="flat", 
                        background=self.light_button_bg, foreground=self.light_button_fg, borderwidth=0)
        style.map('RoundedButton.TButton', 
                  background=[('active', '#e0e0e0'), ('pressed', '#ccc')],
                  foreground=[('active', '#333333')])

    def apply_theme(self, theme):
        """
        Applies the selected theme (Light or Dark).
        """
        if theme == "Light":
            self.master.configure(bg=self.light_bg)
            self.text_widget.configure(bg="#ffffff", fg=self.light_fg, insertbackground="black")
            self.status_bar.configure(style="Light.Status.TLabel")
        elif theme == "Dark":
            self.master.configure(bg=self.dark_bg)
            self.text_widget.configure(bg="#333333", fg=self.dark_fg, insertbackground="white")
            self.status_bar.configure(style="Dark.Status.TLabel")

    def toggle_theme(self):
        """
        This method will toggle between light and dark themes.
        """
        if self.current_theme == "Light":
            self.current_theme = "Dark"
        else:
            self.current_theme = "Light"
        self.apply_theme(self.current_theme)

    def create_toolbar(self):
        """
        Creates a toolbar with text formatting options.
        """
        self.toolbar = tkinter.Frame(self.master, bg=self.light_bg)
        self.toolbar.grid(row=0, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        # Font Family Dropdown
        self.font_family = ttk.Combobox(self.toolbar, values=["Helvetica", "Arial", "Verdana", "Courier New"])
        self.font_family.set(self.current_font_family)
        self.font_family.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.font_family.bind("<<ComboboxSelected>>", self.change_font_family)

        # Font Size Dropdown
        self.font_size = ttk.Combobox(self.toolbar, values=[10, 12, 14, 16, 18, 20, 24, 28, 32])
        self.font_size.set(self.current_font_size)
        self.font_size.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.font_size.bind("<<ComboboxSelected>>", self.change_font_size)

        # Bold Button
        self.bold_button = ttk.Button(self.toolbar, text="B", style="RoundedButton.TButton", command=self.toggle_bold)
        self.bold_button.grid(row=0, column=2, padx=10, pady=5)

        # Italic Button
        self.italic_button = ttk.Button(self.toolbar, text="I", style="RoundedButton.TButton", command=self.toggle_italic)
        self.italic_button.grid(row=0, column=3, padx=10, pady=5)

        # Underline Button
        self.underline_button = ttk.Button(self.toolbar, text="U", style="RoundedButton.TButton", command=self.toggle_underline)
        self.underline_button.grid(row=0, column=4, padx=10, pady=5)

        # Font Color Button
        self.font_color_button = ttk.Button(self.toolbar, text="A", style="RoundedButton.TButton", command=self.change_font_color)
        self.font_color_button.grid(row=0, column=5, padx=10, pady=5)

        # Highlight Button
        self.highlight_button = ttk.Button(self.toolbar, text="✎", style="RoundedButton.TButton", command=self.change_highlight_color)
        self.highlight_button.grid(row=0, column=6, padx=10, pady=5)

        # Spell Check Button
        self.spell_check_button = ttk.Button(self.toolbar, text="Spell Check", style="RoundedButton.TButton", command=self.spell_check)
        self.spell_check_button.grid(row=0, column=7, padx=10, pady=5)

        # Export to PDF Button
        self.export_pdf_button = ttk.Button(self.toolbar, text="Export PDF", style="RoundedButton.TButton", command=self.export_to_pdf)
        self.export_pdf_button.grid(row=0, column=8, padx=10, pady=5)

        # Theme Toggle Button
        self.theme_toggle_button = ttk.Button(self.toolbar, text="Toggle Theme", style="RoundedButton.TButton", command=self.toggle_theme)
        self.theme_toggle_button.grid(row=0, column=9, padx=10, pady=5)

    def create_text_widget(self):
        """
        Creates the main text area where users can type.
        """
        self.text_widget = tkinter.Text(self.master, undo=True, wrap="word", font=(self.current_font_family, self.current_font_size))
        self.text_widget.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=20, pady=10)
        self.text_widget.config(bg="#ffffff", fg=self.light_fg, insertbackground="black", padx=10, pady=10, relief="flat")
        self.text_widget.bind("<<Modified>>", lambda e: self.update_word_char_count())

        # Allow resizing of rows and columns
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_status_bar(self):
        """
        Creates the status bar at the bottom.
        """
        self.status_bar = ttk.Label(self.master, text="Words: 0 | Characters: 0", anchor="e", style="Light.Status.TLabel")
        self.status_bar.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10)

    def setup_menu(self):
        """
        Sets up the menu bar with file-related options.
        """
        self.menu = tkinter.Menu(self.master)  # Create a menu bar
        self.master.config(menu=self.menu)  # Attach the menu to the main window

        self.file_menu = tkinter.Menu(self.menu, tearoff=0)  # Create a File menu
        self.menu.add_cascade(label="File", menu=self.file_menu)  # Add File menu to the menu bar
        
        # Adding commands to the File menu
        self.file_menu.add_command(label="Open PDF", command=self.open_pdf_external)  # Opens a PDF file
        self.file_menu.add_command(label="Open Text File", command=self.open_file)  # Opens a text file
        self.file_menu.add_separator()  # Adds a separator line in the menu
        self.file_menu.add_command(label="Exit", command=self.master.quit)  # Exits the application


    def open_file(self):
        """
        Opens a text file and loads its content into the text widget.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])  # Prompt file selection
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()  # Read file content
            self.text_widget.delete("1.0", tkinter.END)  # Clear existing text
            self.text_widget.insert(tkinter.END, content)  # Insert new text into the editor


    def open_pdf_external(self):
        """
        Opens a selected PDF file using the system's default PDF viewer.
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Prompt file selection
        if file_path:
            try:
                if os.name == "nt":  # For Windows
                    os.startfile(file_path)  # Open the file using default application
                elif os.name == "posix":  # For macOS and Linux
                    subprocess.run(["open", file_path], check=True)  # Open PDF using default viewer
                else:
                    messagebox.showerror("Error", "Unsupported OS for opening PDFs.")  # Show error for unsupported OS
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF: {e}")  # Show error if file cannot be opened


    def update_word_char_count(self):
        """
        Updates the word and character count in the status bar.
        """
        text = self.text_widget.get("1.0", "end-1c")  # Get the text from the text widget
        self.word_count = len(text.split())  # Count words
        self.char_count = len(text)  # Count characters
        self.status_bar.config(text=f"Words: {self.word_count} | Characters: {self.char_count}")  # Update status bar

    def change_font_family(self, event=None):
        """
        Changes the font family of the text widget.
        """
        self.current_font_family = self.font_family.get()  # Get selected font family
        self.text_widget.configure(font=(self.current_font_family, self.current_font_size))  # Apply the font

    def change_font_size(self, event=None):
        """
        Changes the font size of the text widget.
        """
        self.current_font_size = int(self.font_size.get())  # Get selected font size
        self.text_widget.configure(font=(self.current_font_family, self.current_font_size))  # Apply the font size
    
    def update_text_style(self):
        """
        Updates the text style (bold, italic, underline) based on the current selections.
        """
        try:
            font_style = (self.current_font_family, self.current_font_size)  # Base font style

            if self.bold_active:
                font_style += ("bold",)  # Apply bold if active
            if self.italic_active:
                font_style += ("italic",)  # Apply italic if active
            if self.underline_active:
                font_style += ("underline",)  # Apply underline if active

            self.text_widget.tag_add("custom_style", "sel.first", "sel.last")  # Apply style to selected text
            self.text_widget.tag_configure("custom_style", font=font_style)  # Configure the tag with the selected font style
        except tkinter.TclError:
            pass  # If no text is selected, do nothing

    def toggle_bold(self):
        """
        Toggles bold formatting for selected text.
        """
        self.bold_active = not self.bold_active  # Toggle bold status
        self.update_text_style()  # Apply the change

    def toggle_italic(self):
        """
        Toggles italic formatting for selected text.
        """
        self.italic_active = not self.italic_active  # Toggle italic status
        self.update_text_style()  # Apply the change

    def toggle_underline(self):
        """
        Toggles underline formatting for selected text.
        """
        self.underline_active = not self.underline_active  # Toggle underline status
        self.update_text_style()  # Apply the change

    def change_font_color(self):
        """
        Opens a color picker dialog and changes the font color for selected text.
        """
        color = colorchooser.askcolor(title="Choose Font Color")[1]  # Open color chooser
        if color:
            self.current_font_color = color  # Save the selected color
            self.text_widget.tag_add("font_color", "sel.first", "sel.last")  # Apply color to selected text
            self.text_widget.tag_configure("font_color", foreground=self.current_font_color)  # Configure color tag

    def change_highlight_color(self):
        """
        Opens a color picker dialog and changes the background highlight color for selected text.
        """
        color = colorchooser.askcolor(title="Choose Highlight Color")[1]  # Open color chooser
        if color:
            self.current_highlight_color = color  # Save the selected color
            self.text_widget.tag_add("highlight", "sel.first", "sel.last")  # Apply highlight color to selected text
            self.text_widget.tag_configure("highlight", background=self.current_highlight_color)  # Configure highlight tag

    def spell_check(self):
        """
        Checks for misspelled words by identifying non-alphabetic words.
        """
        words = self.text_widget.get("1.0", "end-1c").split()  # Get words from text
        for word in words:
            if not word.isalpha():  # Check if the word contains non-alphabetic characters
                start_idx = self.text_widget.search(word, "1.0", stopindex="end")  # Find the word in text
                if start_idx:
                    end_idx = f"{start_idx}+{len(word)}c"  # Determine end index
                    self.text_widget.tag_add("misspelled", start_idx, end_idx)  # Apply misspelled tag
        self.text_widget.tag_config("misspelled", underline=True, foreground="red")  # Configure misspelled tag

    def find_and_replace(self):
        """
        Finds a specific word and replaces it with another word.
        """
        find_word = simpledialog.askstring("Find", "Enter the word to find:")  # Ask for the word to find
        replace_word = simpledialog.askstring("Replace", "Enter the replacement word:")  # Ask for the replacement word
        if find_word and replace_word:
            content = self.text_widget.get("1.0", "end-1c")  # Get the current text
            new_content = content.replace(find_word, replace_word)  # Replace occurrences
            self.text_widget.delete("1.0", "end")  # Clear the text widget
            self.text_widget.insert("1.0", new_content)  # Insert updated content

    def export_to_pdf(self):
        """
        Exports the current text content to a PDF file (as a .txt file for now).
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])  # Ask for save location
        if file_path:
            content = self.text_widget.get("1.0", "end-1c")  # Get text content
            with open(file_path, "w") as file:
                file.write(content)  # Save content as a text file
            print(f"File saved as: {file_path}")  # Print save confirmation

if __name__ == "__main__":
    root = tkinter.Tk()  # Create the main application window
    app = NotepadApp(root)  # Initialize the NotepadApp
    root.mainloop()  # Start the Tkinter event loop
