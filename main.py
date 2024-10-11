import tkinter as tk
import tkinter.filedialog as fd
import os
import winreg
import webbrowser

class Blitznote:
    def __init__(self, root_class):
        self.default_filename = "blitznote.txt"
        self.default_save_dir = "C:/Users/"+os.getlogin()+"/blitznotes/"
        if not os.path.exists(self.default_save_dir):
            os.makedirs(self.default_save_dir)
        self.save_dir = self.default_save_dir
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\blitznote", 0, winreg.KEY_READ)
            if winreg.QueryValueEx(key, "SaveDir")[0] != "":
                self.save_dir = winreg.QueryValueEx(key, "SaveDir")[0]
            winreg.CloseKey(key)
        except FileNotFoundError:
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, "Software\\blitznote", 0, winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY)
            winreg.CloseKey(key)

        self.root = root_class
        self.root.title("Blitznote")
        self.root.geometry("300x150")
        self.app_menu = tk.Menu(root)
        self.root.config(menu=self.app_menu)
        self.app_menu.add_command(label="Save", command=self.SaveNote)
        self.app_menu.add_command(label="Save to...", command=self.SaveNoteTo)
        self.app_menu.add_command(label="Set directory", command=self.SetSaveDir)
        self.app_menu.add_command(label="Unset directory", command=self.UnsetSaveDir)
        self.app_menu.add_command(label="?", command=self.AboutApp)

        self.input = tk.Text(self.root)
        self.input.pack(fill="both", expand=True)

    @staticmethod
    def WriteDirToReg(save_dir):
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\blitznote", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SaveDir", 0, winreg.REG_SZ, save_dir)
        winreg.CloseKey(key)

    @staticmethod
    def ClearReg():
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, "Software\\blitznote", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SaveDir", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)

    def OpenVk(self):
        webbrowser.open("https://vk.com/veryshortnamereallyshort")

    def SetSaveDir(self):
        temp_dir = fd.askdirectory()
        if temp_dir:
            self.save_dir = temp_dir + "/"
            self.WriteDirToReg(self.save_dir)
        else:
            del temp_dir

    def UnsetSaveDir(self):
        self.ClearReg()
        self.save_dir = self.default_save_dir

    def SaveNote(self):
        text_to_save = self.input.get("1.0", "end-1c")
        text_first_line = self.input.get("1.0", "2.0").strip()
        if text_first_line.startswith("{") and text_first_line.endswith("}"):
            text_to_save = self.input.get("2.0", "end-1c")
            filename = text_first_line[1:-1]+".txt"
        else:
            filename = self.default_filename
            serialized_filename = self.default_filename
            i = 1
            while os.path.exists(self.save_dir+serialized_filename):
                serialized_filename = f"blitznote{i}.txt"
                i += 1
                filename = serialized_filename
        with open(self.save_dir+filename, "w") as f:
            f.write(text_to_save)

    def SaveNoteTo(self):
        text_to_save = self.input.get("1.0", "end-1c")
        text_first_line = self.input.get("1.0", "2.0").strip()
        if text_first_line.startswith("{") and text_first_line.endswith("}"):
            text_to_save = self.input.get("2.0", "end-1c")
            filename = text_first_line[1:-1]+".txt"
        else:
            filename = self.default_filename
        temp_save_dir = fd.askdirectory()+"/"
        with open(temp_save_dir+filename, "w") as f:
            f.write(text_to_save)

    def AboutApp(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About the app")
        about_window.geometry("650x427")
        about_window.resizable(False, False)
        about_text = tk.Text(about_window, wrap="word")
        about_text.insert("1.0", "Designed by @CITRUS (Chukakabra).\nAn open-source project. GNU General Public License v3.0.\n\n--------------------------------------------------------\n\nVersion: 1.0 (11.10.24)\nFeel free to give your feedback!\n\n--------------------------------\n\nIf you want to save a file with a specific name, rather than 'blitznote-blah blah blah...', then write {ANY TEXT} on the first line. The contents of the curly brackets will be taken as the file name.\n\nThe 'Save' command saves the text file to the installed directory (if you have not changed it, then this is the default C:/Users/[CURRENT USER]/blitznotes/\n\nThe 'Save to...' command saves the text file to a different directory that you choose.\n\nThe 'Set directory' command sets a new directory that will be used for saving by default.\n\nThe 'Unset directory' command restores the original default directory.")
        button_vk = tk.Button(about_window, text="Моя страничка в ВК для связи.", font="Arial 15", command=self.OpenVk)
        about_text.pack(fill="x", expand=False)
        button_vk.place(x=176, y=387)

        about_window.focus_get()

if __name__ == "__main__":
    root = tk.Tk()
    app = Blitznote(root)
    root.mainloop()
