"""GUI module for the Malaphor Generator."""
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from malaphor_logic import MalaphorGenerator


class MalaphorApp:
    """GUI application for the Malaphor Generator."""
    
    MAX_HISTORY_LINES = 1000  # Maximum number of lines to keep in history
    HISTORY_CLEANUP_TRIGGER = 1200  # When to trigger cleanup
    
    def __init__(self, root=None):
        """Initialize the GUI application."""
        self.generator = MalaphorGenerator()
        self.root = root or tk.Tk()
        if not root:
            self.root.title("Malaphor Generator")
        self.tooltips = []  # Store tooltip references
        self.dialogs = {}  # Cache dialog references
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI components."""
        # Configure window
        self.root.geometry("600x500")
        self.root.configure(padx=20, pady=20)
        
        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both')
        
        # Create three button frames
        button_frame_top = tk.Frame(main_frame)
        button_frame_top.pack(pady=5)
        
        button_frame_middle = tk.Frame(main_frame)
        button_frame_middle.pack(pady=5)
        
        button_frame_bottom = tk.Frame(main_frame)
        button_frame_bottom.pack(pady=5)
        
        # Add buttons to top row with increased width
        manage_phrases_button = tk.Button(
            button_frame_top,
            text="Manage Phrases",
            command=self.show_manage_phrases_dialog,
            width=15
        )
        manage_phrases_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(manage_phrases_button, "View and edit the collection of proverbs")

        manual_combine_button = tk.Button(
            button_frame_top,
            text="Manual Combine",
            command=self.show_manual_combine_dialog,
            width=15
        )
        manual_combine_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(manual_combine_button, "Manually select two phrases to combine into a malaphor")

        add_proverb_button = tk.Button(
            button_frame_top,
            text="Add New Proverb",
            command=self.show_add_proverb_dialog,
            width=15
        )
        add_proverb_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(add_proverb_button, "Add a new proverb to the collection")

        generate_button = tk.Button(
            button_frame_top,
            text="Generate",
            command=self.generate_malaphor,
            width=15
        )
        generate_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(generate_button, "Generate a new random malaphor")

        copy_button = tk.Button(
            button_frame_top,
            text="Copy Malaphor",
            command=self.copy_to_clipboard,
            width=15
        )
        copy_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(copy_button, "Copy the current malaphor to clipboard")

        # Add import/export buttons to middle row
        import_button = tk.Button(
            button_frame_middle,
            text="Import Malaphors",
            command=self.import_malaphors_dialog,
            width=15
        )
        import_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(import_button, "Import malaphors from a JSON file")

        export_originals_button = tk.Button(
            button_frame_middle,
            text="Export Originals",
            command=self.export_originals_dialog,
            width=15
        )
        export_originals_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(export_originals_button, "Export original proverbs to a file")

        export_generated_button = tk.Button(
            button_frame_middle,
            text="Export Generated",
            command=self.export_generated_dialog,
            width=15
        )
        export_generated_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(export_generated_button, "Export generated malaphors to a file")

        # Add buttons to bottom row
        favorite_button = tk.Button(
            button_frame_bottom,
            text="Add to Favorites",
            command=self.add_to_favorites,
            width=15
        )
        favorite_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(favorite_button, "Add current malaphor to favorites")

        save_favorites_button = tk.Button(
            button_frame_bottom,
            text="Save Favorites",
            command=self.generator.save_favorites,
            width=15
        )
        save_favorites_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(save_favorites_button, "Save favorites to file")

        exit_button = tk.Button(
            button_frame_bottom,
            text="Exit",
            command=self.exit_program,
            width=15
        )
        exit_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(exit_button, "Exit the application")

        view_history_button = tk.Button(
            button_frame_bottom,
            text="Manage History",
            command=self.show_history_dialog,
            width=15
        )
        view_history_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(view_history_button, "View and manage generated malaphor history")

        view_favorites_button = tk.Button(
            button_frame_bottom,
            text="Manage Favorites",
            command=self.show_favorites_dialog,
            width=15
        )
        view_favorites_button.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(view_favorites_button, "View and manage favorite malaphors")

        # Create labels
        self.sentence_label = tk.Label(
            main_frame,
            text="Click 'Generate' to create a malaphor",
            wraplength=400,
            height=3
        )
        self.sentence_label.pack(pady=20)

        # Create history display
        history_frame = tk.LabelFrame(
            main_frame,
            text="History",
            padx=10,
            pady=10
        )
        history_frame.pack(fill='both', expand=True)

        self.history_text = tk.Text(history_frame, height=10, width=50)
        self.history_text.pack(side=tk.LEFT, fill='both', expand=True)
        self._create_tooltip(self.history_text, "Recently generated malaphors")

        # Add scrollbar to history
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure scrollbar
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a given widget."""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        label = tk.Label(
            tooltip, 
            text=text, 
            background="yellow",
            relief="solid", 
            borderwidth=1
        )
        label.pack()
        tooltip.withdraw()

        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

        # Store reference to prevent garbage collection
        self.tooltips.append((widget, tooltip, enter, leave))
        return tooltip
        
    def _cleanup_tooltips(self):
        """Clean up tooltip bindings and references."""
        for widget, tooltip, enter, leave in self.tooltips:
            try:
                widget.unbind("<Enter>")
                widget.unbind("<Leave>")
                tooltip.destroy()
            except tk.TclError:
                pass  # Widget already destroyed
        self.tooltips.clear()
        
    def show_add_proverb_dialog(self):
        """Show dialog for adding a new proverb."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Proverb")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create and pack widgets
        beginning_label = tk.Label(dialog, text="Enter the beginning of the proverb:")
        beginning_label.pack(pady=5)
        self._create_tooltip(beginning_label, "Enter the first part of the proverb (e.g., 'A bird in the hand')")
        
        beginning_entry = tk.Entry(dialog, width=40)
        beginning_entry.pack(pady=5)
        self._create_tooltip(beginning_entry, "Enter the first part of the proverb here")
        
        ending_label = tk.Label(dialog, text="Enter the ending of the proverb:")
        ending_label.pack(pady=5)
        self._create_tooltip(ending_label, "Enter the second part of the proverb (e.g., 'is worth two in the bush')")
        
        ending_entry = tk.Entry(dialog, width=40)
        ending_entry.pack(pady=5)
        self._create_tooltip(ending_entry, "Enter the second part of the proverb here")
        
        def save_proverb():
            beginning = beginning_entry.get().strip()
            ending = ending_entry.get().strip()
            
            if not beginning or not ending:
                tkinter.messagebox.showwarning(
                    "Input Error",
                    "Both beginning and ending must be filled out!"
                )
                return
                
            if self.generator.add_new_proverb(beginning, ending):
                tkinter.messagebox.showinfo(
                    "Success",
                    "New proverb added successfully!"
                )
                dialog.destroy()
            
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Save",
            command=save_proverb
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
    def generate_malaphor(self):
        """Generate and display a new malaphor."""
        result = self.generator.generate_malaphor()
        sentence = result["malaphor"]
        self.sentence_label.config(
            text=(f"{sentence}\n\n"
                  f"Created from:\n"
                  f"1. {result['source1']}\n"
                  f"2. {result['source2']}")
        )
        self.update_history()
        
    def copy_to_clipboard(self):
        """Copy the current malaphor to clipboard."""
        sentence = self.sentence_label.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(sentence)
        self.root.update()
        tkinter.messagebox.showinfo(
            "Copy Malaphor",
            "The malaphor has been copied to the clipboard."
        )
        
    def add_to_favorites(self):
        """Add the current malaphor to favorites."""
        current_malaphor = self.sentence_label.cget("text")
        default_text = "Click 'Generate' to create a malaphor"
        if (current_malaphor and current_malaphor != default_text):
            self.generator.add_to_favorites(current_malaphor)
            tkinter.messagebox.showinfo("Success", "Added to favorites!")
            
    def update_history(self):
        """Update the history display with malaphors and their sources."""
        # Check if cleanup is needed
        if self.history_text.index('end-1c').split('.')[0] > str(self.HISTORY_CLEANUP_TRIGGER):
            # Keep only the last MAX_HISTORY_LINES lines
            self.history_text.delete('1.0', f'end-{self.MAX_HISTORY_LINES}l')
        
        # Add new history entry
        self.history_text.delete(1.0, tk.END)
        for item in reversed(self.generator.history[-10:]):
            self.history_text.insert(tk.END, f"Malaphor: {item['malaphor']}\n")
            self.history_text.insert(tk.END, "From combining:\n")
            self.history_text.insert(tk.END, f"1. {item['source1']}\n")
            self.history_text.insert(tk.END, f"2. {item['source2']}\n\n")
            
    def exit_program(self):
        """Exit the program after confirming with the user."""
        if tkinter.messagebox.askokcancel(
            "Exit",
            "Do you want to exit the program?"
        ):
            self.root.quit()
            
    def import_malaphors_dialog(self):
        """Show dialog for importing malaphors from a JSON file."""
        from tkinter import filedialog
        
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filepath:
            self.generator.import_malaphors(filepath)
            
    def export_originals_dialog(self):
        """Show dialog for exporting original malaphors."""
        from tkinter import filedialog
        
        filetypes = [
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=filetypes,
            initialfile="original_malaphors"
        )
        
        if filepath:
            if filepath.endswith('.txt'):
                self.generator.export_malaphors_as_text(filepath)
            else:
                self.generator.export_malaphors(filepath)
            
    def export_generated_dialog(self):
        """Show dialog for exporting generated malaphors."""
        from tkinter import filedialog
        
        filetypes = [
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=filetypes,
            initialfile="generated_malaphors"
        )
        
        if filepath:
            if filepath.endswith('.txt'):
                self.generator.export_history_as_text(filepath)
            else:
                self.generator.export_history(filepath)

    def export_favorites_dialog(self):
        """Show dialog for exporting favorites."""
        from tkinter import filedialog
        
        filetypes = [
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=filetypes,
            initialfile="favorite_malaphors"
        )
        
        if filepath:
            if filepath.endswith('.txt'):
                self.generator.export_favorites_as_text(filepath)
            else:
                self.generator.export_favorites(filepath)
            
    def show_manage_phrases_dialog(self):
        """Show dialog for managing (viewing/editing/deleting) phrases."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Phrases")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create frames
        list_frame = tk.Frame(dialog)
        list_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)

        edit_frame = tk.Frame(dialog)
        edit_frame.pack(side=tk.RIGHT, fill='y', padx=10, pady=10)

        # Create listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        phrases_listbox = tk.Listbox(list_frame, width=60, height=20, yscrollcommand=scrollbar.set)
        phrases_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=phrases_listbox.yview)
        self._create_tooltip(phrases_listbox, "List of all available proverbs. Click one to edit.")

        # Populate listbox
        proverbs = self.generator.get_all_proverbs()
        for proverb in proverbs:
            phrases_listbox.insert(tk.END, proverb["original"])

        # Create edit fields
        beginning_label = tk.Label(edit_frame, text="Beginning:")
        beginning_label.pack(pady=5)
        self._create_tooltip(beginning_label, "Edit the first part of the selected proverb")

        beginning_entry = tk.Entry(edit_frame, width=40)
        beginning_entry.pack(pady=5)
        self._create_tooltip(beginning_entry, "Enter the first part of the proverb here")

        ending_label = tk.Label(edit_frame, text="Ending:")
        ending_label.pack(pady=5)
        self._create_tooltip(ending_label, "Edit the second part of the selected proverb")

        ending_entry = tk.Entry(edit_frame, width=40)
        ending_entry.pack(pady=5)
        self._create_tooltip(ending_entry, "Enter the second part of the proverb here")

        def on_select(event):
            try:
                index = phrases_listbox.curselection()[0]
                proverb = proverbs[index]
                beginning_entry.delete(0, tk.END)
                beginning_entry.insert(0, proverb["beginning"])
                ending_entry.delete(0, tk.END)
                ending_entry.insert(0, proverb["ending"])
            except IndexError:
                pass

        phrases_listbox.bind('<<ListboxSelect>>', on_select)

        def save_changes():
            try:
                index = phrases_listbox.curselection()[0]
                beginning = beginning_entry.get().strip()
                ending = ending_entry.get().strip()

                if not beginning or not ending:
                    tkinter.messagebox.showwarning(
                        "Input Error",
                        "Both beginning and ending must be filled out!"
                    )
                    return

                if self.generator.edit_proverb(index, beginning, ending):
                    # Update listbox
                    phrases_listbox.delete(index)
                    phrases_listbox.insert(index, f"{beginning} {ending}")
                    tkinter.messagebox.showinfo(
                        "Success",
                        "Phrase updated successfully!"
                    )
            except IndexError:
                tkinter.messagebox.showwarning(
                    "Selection Error",
                    "Please select a phrase to edit!"
                )

        def delete_phrase():
            try:
                index = phrases_listbox.curselection()[0]
                if tkinter.messagebox.askyesno(
                    "Confirm Delete",
                    "Are you sure you want to delete this phrase?"
                ):
                    if self.generator.delete_proverb(index):
                        phrases_listbox.delete(index)
                        beginning_entry.delete(0, tk.END)
                        ending_entry.delete(0, tk.END)
                        tkinter.messagebox.showinfo(
                            "Success",
                            "Phrase deleted successfully!"
                        )
            except IndexError:
                tkinter.messagebox.showwarning(
                    "Selection Error",
                    "Please select a phrase to delete!"
                )

        # Add buttons
        button_frame = tk.Frame(edit_frame)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Save Changes",
            command=save_changes
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            command=delete_phrase
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
    def show_manual_combine_dialog(self):
        """Show dialog for manually selecting phrases to combine."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manual Phrase Combination")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Create frames for the two listboxes
        left_frame = tk.LabelFrame(dialog, text="First Phrase")
        left_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)

        right_frame = tk.LabelFrame(dialog, text="Second Phrase")
        right_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)

        # Create search entries
        left_search = tk.Entry(left_frame, textvariable=tk.StringVar())
        left_search.pack(fill='x', padx=5, pady=5)
        self._create_tooltip(left_search, "Search for phrases in the left list")

        right_search = tk.Entry(right_frame, textvariable=tk.StringVar())
        right_search.pack(fill='x', padx=5, pady=5)
        self._create_tooltip(right_search, "Search for phrases in the right list")

        # Create listboxes with scrollbars
        left_scrollbar = tk.Scrollbar(left_frame)
        left_scrollbar.pack(side=tk.RIGHT, fill='y')
        left_listbox = tk.Listbox(left_frame, yscrollcommand=left_scrollbar.set)
        left_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        left_scrollbar.config(command=left_listbox.yview)
        self._create_tooltip(left_listbox, "Select the first phrase to combine")

        right_scrollbar = tk.Scrollbar(right_frame)
        right_scrollbar.pack(side=tk.RIGHT, fill='y')
        right_listbox = tk.Listbox(right_frame, yscrollcommand=right_scrollbar.set)
        right_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        right_scrollbar.config(command=right_listbox.yview)
        self._create_tooltip(right_listbox, "Select the second phrase to combine")

        # Populate listboxes
        proverbs = self.generator.get_all_proverbs()
        for i, proverb in enumerate(proverbs):
            left_listbox.insert(tk.END, proverb["original"])
            right_listbox.insert(tk.END, proverb["original"])

        def update_listbox(listbox, search_var, event=None):
            """Filter listbox based on search text."""
            search_text = search_var.get().lower()
            listbox.delete(0, tk.END)
            for proverb in proverbs:
                if search_text in proverb["original"].lower():
                    listbox.insert(tk.END, proverb["original"])

        # Bind search entries to update function
        left_search_var = tk.StringVar()
        left_search_var.trace('w', lambda *args: update_listbox(left_listbox, left_search_var))
        right_search_var = tk.StringVar()
        right_search_var.trace('w', lambda *args: update_listbox(right_listbox, right_search_var))

        def combine_selected():
            """Generate malaphor from selected phrases."""
            try:
                left_sel = left_listbox.curselection()[0]
                right_sel = right_listbox.curselection()[0]
                
                # Convert listbox indices to proverb indices
                left_text = left_listbox.get(left_sel)
                right_text = right_listbox.get(right_sel)
                
                left_index = next(i for i, p in enumerate(proverbs) if p["original"] == left_text)
                right_index = next(i for i, p in enumerate(proverbs) if p["original"] == right_text)
                
                result = self.generator.generate_malaphor(left_index, right_index)
                self.sentence_label.config(
                    text=(f"{result['malaphor']}\n\n"
                          f"Created from:\n"
                          f"1. {result['source1']}\n"
                          f"2. {result['source2']}")
                )
                self.update_history()
                dialog.destroy()
                
            except IndexError:
                tkinter.messagebox.showwarning(
                    "Selection Error",
                    "Please select both a first and second phrase!"
                )

        # Add combine button
        button_frame = tk.Frame(dialog)
        button_frame.pack(side=tk.BOTTOM, fill='x', pady=10)

        tk.Button(
            button_frame,
            text="Combine Selected",
            command=combine_selected
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
    def show_history_dialog(self):
        """Show dialog for managing history entries."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage History")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create search frame
        search_frame = tk.Frame(dialog)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(search_label, "Search through your generated malaphors")
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(search_entry, "Type to filter malaphors")
        
        # Create listbox with scrollbar
        list_frame = tk.Frame(dialog)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        history_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=history_listbox.yview)
        self._create_tooltip(history_listbox, "List of generated malaphors. Click one to manage.")

        def update_history_list(search_text=''):
            history_listbox.delete(0, tk.END)
            if (search_text):
                items = self.generator.search_history(search_text)
                for i, item in items:
                    history_listbox.insert(tk.END, f"{item['malaphor']}")
                    history_listbox.insert(tk.END, f"From: {item['source1']} + {item['source2']}")
                    history_listbox.insert(tk.END, '')  # Empty line for spacing
            else:
                for i, item in enumerate(self.generator.history):
                    history_listbox.insert(tk.END, f"{item['malaphor']}")
                    history_listbox.insert(tk.END, f"From: {item['source1']} + {item['source2']}")
                    history_listbox.insert(tk.END, '')  # Empty line for spacing
        
        def on_search(*args):
            update_history_list(search_var.get())
            
        search_var.trace('w', on_search)
        
        def delete_selected():
            try:
                sel = history_listbox.curselection()
                if sel:
                    index = sel[0] // 3  # Account for the three lines per entry
                    if tkinter.messagebox.askyesno(
                        "Confirm Delete",
                        "Are you sure you want to delete this entry?"
                    ):
                        self.generator.delete_from_history(index)
                        update_history_list(search_var.get())
            except Exception as e:
                tkinter.messagebox.showerror(
                    "Error",
                    f"Could not delete entry: {str(e)}"
                )
        
        # Add buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_selected
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Initial population
        update_history_list()
        
    def show_favorites_dialog(self):
        """Show dialog for managing favorite entries."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Manage Favorites")
        dialog.geometry("800x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create search frame
        search_frame = tk.Frame(dialog)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        self._create_tooltip(search_entry, "Type to filter favorites")
        
        # Create listbox with scrollbar
        list_frame = tk.Frame(dialog)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        favorites_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        favorites_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=favorites_listbox.yview)
        self._create_tooltip(favorites_listbox, "List of favorite malaphors. Click one to manage.")

        def update_favorites_list(search_text=''):
            favorites_listbox.delete(0, tk.END)
            if search_text:
                items = self.generator.search_favorites(search_text)
                for i, item in items:
                    favorites_listbox.insert(tk.END, item)
            else:
                for item in self.generator.favorites:
                    favorites_listbox.insert(tk.END, item)
        
        def on_search(*args):
            update_favorites_list(search_var.get())
            
        search_var.trace('w', on_search)
        
        def delete_selected():
            try:
                sel = favorites_listbox.curselection()
                if sel:
                    index = sel[0]
                    if tkinter.messagebox.askyesno(
                        "Confirm Delete",
                        "Are you sure you want to delete this favorite?"
                    ):
                        self.generator.delete_from_favorites(index)
                        update_favorites_list(search_var.get())
                        # Save changes
                        self.generator.save_favorites()
            except Exception as e:
                tkinter.messagebox.showerror(
                    "Error",
                    f"Could not delete favorite: {str(e)}"
                )
        
        # Add buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Delete Selected",
            command=delete_selected
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Initial population
        update_favorites_list()
        
    def run(self):
        """Start the application."""
        self.root.mainloop()
        
    def close(self):
        """Clean up resources."""
        self._cleanup_tooltips()
        for dialog in self.dialogs.values():
            try:
                dialog.destroy()
            except tk.TclError:
                pass  # Dialog already destroyed
        if hasattr(self, 'root') and self.root:
            self.root.quit()
            self.root.destroy()