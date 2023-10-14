# vEditor developed by Vihaan Mody
# Enjoy the Text Editor!

from CTkMessagebox import CTkMessagebox
import customtkinter as CTk
import tkinter.filedialog
import webbrowser
import pyperclip
import datetime
import time
import sys
import os

class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.title("vEditor")
        self.Width = 840
        self.Height = 500
        self.geometry(f"{self.Width}x{self.Height}")
        self.minsize(840, 500)
        self.resizable(False, False)
        self.FontsRoot = tkinter.Tk()
        self.Fonts = self.FontsRoot.tk.call("font", "families")
        self.FontsRoot.destroy()
        self.Saved = False
        self.FontList = ("Arial", 20)
        self.Line = "————————————————————————————————————————"
        self.filetypes = [
        ("Text Files", "*.txt"),
        ("Rich Text Files", "*.rtf"),
        ("Markdown Files", ".md"),
        ("Python Files", "*.py"),
        ("CSV Files", "*.csv"),
        ("JSON Files", "*.json"),
        ("HTML Files", "*.html"),
        ("CSS Files", "*.css"),
        ("JavaScript Files", "*.js"),
        ("XML Files", "*.xml"),
        ("C/C++ Files", "*.c"),
        ("Ruby Files", "*.rb"),
        ("Perl Files", "*.pl"),
        ("Shell Script Files", "*.sh"),
        ("All Files", "*.*")
    ]
        #Top Frame for Buttons
        self.TopFrame = CTk.CTkFrame(self)
        self.TopFrame.grid(row=0, pady=10, padx=0)
        #File Button
        self.File = CTk.CTkOptionMenu(self.TopFrame, values=["New", "Save", "Save As", "Open", "Close File", "Exit"], width=100, command=self.FileFunc)
        self.File.grid(row=0, column=0, pady=10, padx=10)
        self.File.set("File")
        #Edit Button
        self.Edit = CTk.CTkOptionMenu(self.TopFrame, values=["Copy", "Paste", "Cut", "Undo", "Clipboard", "Select All"], width=100, command=self.EditFunc)
        self.Edit.grid(row=0, column=1, pady=10, padx=10)
        self.Edit.set("Edit")
        #Search Button
        self.Format = CTk.CTkOptionMenu(self.TopFrame, values=["Font Style", "Find & Replace", "Trim Whitespace", "Delete Empty Lines", "Insert Line", "Insert Time"], width=100, command=self.FormatFunc)
        self.Format.grid(row=0, column=2, pady=10, padx=10)
        self.Format.set("Format")
        #View
        self.View = CTk.CTkOptionMenu(self.TopFrame, values=["File Info", "Word Count", "File History"], width=100, command=self.ViewFunc)
        self.View.grid(row=0, column=3, pady=10, padx=10)
        self.View.set("View")
        #Tools
        self.Tools = CTk.CTkOptionMenu(self.TopFrame, values=["View In Browser"], width=100, command=self.ToolsFunc)
        self.Tools.grid(row=0, column=4, pady=10, padx=10)
        self.Tools.set("Tools")
        #Settings
        self.Settings = CTk.CTkOptionMenu(self.TopFrame, values=["Appearance", "Shortcuts"], width=100, command=self.SettingsFunc)
        self.Settings.grid(row=0, column=5, pady=10, padx=10)
        self.Settings.set("Settings")
        #Help Button
        self.Help = CTk.CTkOptionMenu(self.TopFrame, values=["Docs", "Version", "Troubleshooting"], width=100, command=self.HelpFunc)
        self.Help.grid(row=0, column=6, pady=10, padx=10)
        self.Help.set("Help")
        #Text Box
        self.Entry = CTk.CTkTextbox(self, width=816, height=420, font=self.FontList, undo=True)
        self.Entry.grid(row=1, column=0)

    def Theme(self):
        CTk.set_appearance_mode(self.LD_Mode.get().lower())
        try:
            self.FontNum = int(self.FontSize.get())
        except:
            self.FontNum = 20
        self.custom_font = (self.Font.get(), self.FontNum)
        self.Entry.configure(font=self.custom_font)
        self.Root1.destroy()

    def SaveAs(self):
        self.File.set("File")
        Data = self.Entry.get("1.0", "end-1c")
        FileDialog = tkinter.filedialog.asksaveasfile(filetypes=self.filetypes, defaultextension="*.txt")
        try:
            FileDialog.name
        except:
            return
        with open(FileDialog.name, "a") as New:
            New.write(Data)
            New.close()
        self.Saved = FileDialog.name
        self.title(f"vEditor - {FileDialog.name}")

    def FileFunc(self, option):
        if option == "Exit":
            self.File.set("File")
            sys.exit()

        elif option == "Save As":
            self.File.set("File")
            self.SaveAs()

        elif option == "Save":
            if self.Saved == False:
                self.File.set("File")
                self.SaveAs()
            else:
                self.File.set("File")
                try:
                    with open(self.Saved, "w") as File:
                        File.write(self.Entry.get("1.0", "end-1c"))
                        File.close()
                except:
                    CTkMessagebox(title="vEditor", message="File Moved or Deleted", icon="cancel", sound=True)

        elif option == "New":
            self.File.set("File")
            self.Entry.delete("1.0", CTk.END)
            self.Saved = False
            self.title("vEditor")

        elif option == "Open":
            self.File.set("File")
            try:
                self.FileDialog = tkinter.filedialog.askopenfile(filetypes=self.filetypes, defaultextension="*.txt")
                try:
                    self.FileDialog.name
                except:
                    return
                with open(self.FileDialog.name, "r") as File:
                    self.Data = File.read()
                    File.close()
            except:
                CTkMessagebox(title="vEditor", message="Filetype Not Supported", icon="cancel", sound=True)
            else:
                self.Entry.delete("1.0", CTk.END)
                self.Entry.insert("1.0", self.Data)
                self.title(f"vEditor - {self.FileDialog.name}")
                self.Saved = self.FileDialog.name

        elif option == "Close File":
            self.File.set("File")
            self.Entry.delete("1.0", CTk.END)
            self.Saved = False
            self.title("vEditor")                

    def EditFunc(self, option):
        if option == "Paste":
            self.Edit.set("Edit")
            self.Entry.insert(CTk.INSERT, text=pyperclip.paste())

        elif option == "Select All":
            self.Edit.set("Edit")
            self.Entry.tag_add("sel", "1.0", "end")

        elif option == "Copy":
            self.Edit.set("Edit")
            self.SelectedCopy = self.Entry.get(CTk.SEL_FIRST, CTk.SEL_LAST)
            pyperclip.copy(self.SelectedCopy)

        elif option == "Clipboard":
            self.Edit.set("Edit")
            self.clipboard = self.clipboard_get()
            CTkMessagebox(title="vEditor", message=self.clipboard, sound=True)

        elif option == "Cut":
            self.Edit.set("Edit")
            self.Entry.delete(CTk.SEL_FIRST, CTk.SEL_LAST)
        
        elif option == "Undo":
            self.Edit.set("Edit")
            self.Entry.edit_undo()

    def FormatFunc(self, option):
        if option == "Font Style":
            self.Format.set("Format")
            self.Root1 = CTk.CTk()
            self.Root1.geometry("350x190") #add40
            self.Root1.resizable(width=False, height=False)
            self.Root1.title("vEditor")
            self.LD_Label = CTk.CTkLabel(self.Root1, text="Dark/Light Mode:", height=30)
            self.LD_Label.grid(row=0, column=0, pady=10, padx=10)
            self.LD_Mode = CTk.CTkOptionMenu(self.Root1, values=["Dark", "Light", "System"])
            self.LD_Mode.grid(row=0, column=1, pady=10, padx=10)
            self.LD_Mode.set("System")
            self.FontL = CTk.CTkLabel(self.Root1, text="Font:", height=30)
            self.FontL.grid(row=1, column=0, pady=10, padx=10)
            self.Font = CTk.CTkOptionMenu(self.Root1, values=list(self.Fonts))
            self.Font.grid(row=1, column=1, pady=10, padx=10)
            self.Font.set("System")
            self.FontSizeL = CTk.CTkLabel(self.Root1, text="Font Size", height=30)
            self.FontSizeL.grid(row=2, column=0, pady=10, padx=10)
            self.FontSize = CTk.CTkEntry(self.Root1, placeholder_text="e.x. 20")
            self.FontSize.grid(row=2, column=1, pady=10, padx=10)
            self.LD_Change = CTk.CTkButton(self.Root1, text="Set Changes", command=self.Theme)
            self.LD_Change.grid(pady=10, padx=10)
            self.Root1.mainloop()
            
        elif option == "Find & Replace":
            self.Format.set("Format")
            self.FindDialog = CTk.CTkInputDialog(title="vEditor", text="Find:")
            self.Find = self.FindDialog.get_input()
            if self.Find == None:
                return
            self.ReplaceDialog = CTk.CTkInputDialog(title="vEditor", text="Replace:")
            self.Replace = self.ReplaceDialog.get_input()
            if self.Replace == None:
                return
            self.OldText = self.Entry.get("1.0", CTk.END)
            self.NewText = self.OldText.replace(self.Find, self.Replace)
            self.Entry.delete("1.0", CTk.END)
            self.Entry.insert("1.0", self.NewText)

        elif option == "Insert Line":
            self.Format.set("Format")
            self.Entry.insert(CTk.INSERT, text=f"\n{self.Line}\n")

        elif option == "Insert Time":
            self.Format.set("Format")
            self.Entry.insert(CTk.INSERT, text=datetime.datetime.now())

        elif option == "Trim Whitespace":
            self.Format.set("Format")
            self.TrimSpace = self.Entry.get("1.0", CTk.END).strip()
            self.Entry.delete("1.0", CTk.END)
            self.Entry.insert("1.0", self.TrimSpace)
        
        elif option == "Delete Empty Lines":
            self.Format.set("Format")
            self.EmptyLines = [line for line in self.Entry.get("1.0", CTk.END).splitlines() if line.strip()]
            self.Entry.delete("1.0", CTk.END)
            self.Entry.insert("1.0", "\n".join(self.EmptyLines))

    def ViewFunc(self, option):
        if option == "File Info":
            self.View.set("View")
            if self.Saved == False:
                CTkMessagebox(title="vEditor", message="Save File To Retrieve Information", icon="warning", sound=True)
            else:
                self.FileSize = os.path.getsize(self.Saved)
                self.FileModified = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(self.Saved)))
                self.ABSpath = os.path.abspath(self.Saved)
                self.FileName = os.path.basename(self.Saved)
                self.FileEXT = os.path.splitext(self.Saved)[1]
                self.FileInfo = f"""File Name: {self.FileName}\n
File Size: {self.FileSize} Bytes\n
Modification Time: {self.FileModified}\n
File Extension: {self.FileEXT.upper()}\n
Absolute File Path: {self.ABSpath}"""
                CTkMessagebox(title="vEditor", message=self.FileInfo, sound=True)

        elif option == "Word Count":
            self.View.set("View")
            CTkMessagebox(title="vEditor", message=f""" {len(self.Entry.get('1.0', CTk.END).split(' '))} Words
 {len(self.Entry.get('1.0', CTk.END))-1} Characters
 {len(self.Entry.get('1.0', CTk.END).replace(" ", ""))-1} Characters Excluding Spaces""", sound=True)

    def ToolsFunc(self, option):
        if option == "View In Browser":
            self.Tools.set("Tools")
            if self.Saved == False:
                CTkMessagebox(title="vEditor", message="Save File To Show In Browser", icon="warning", sound=True)
            else:
                webbrowser.open("file://" + self.Saved)

    def SettingsFunc(self, option):
        if option == "Shortcuts":
            self.Settings.set("Settings")
            CTkMessagebox(title="vEditor", icon=None, message="""Ctrl-C ---> Copy\n
Ctrl-V ---> Paste\n
Ctrl-A ---> Select All\n
Ctrl-Z ---> Undo
""", sound=True)

    def HelpFunc(self, option):
        if option == "Version":
            self.Help.set("Help")
            CTkMessagebox(title="vEditor", message="Version 1.0", sound=True)

        elif option == "Docs":
            self.Help.set("Help")
            webbrowser.open("https://github.com/Vihaanmody21/vEditor")

        elif option == "Troubleshooting":
            self.Help.set("Help")
            webbrowser.open("https://github.com/Vihaanmody21/vEditor/issues")

app = App()
app.mainloop()