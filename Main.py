import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from io import BytesIO
import os
import re
import ftplib


class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='white')
        # Settings general widths and heights for 16:9 and 16:10 screens
        self.full_Width, self.full_Height = self.root.winfo_screenwidth(
        ), self.root.winfo_screenheight()
        self.root.geometry('%dx%d+0+0' % (self.full_Width, self.full_Height))
        self.width1, self.height1 = int(round((self.root.winfo_screenwidth() / 15))), int(round(
            (self.root.winfo_screenheight() / 15)))  # General widths and heights to be used for widgets
        self.width2, self.height2 = int(round((self.root.winfo_screenwidth(
        ) / 20))), int(round((self.root.winfo_screenheight() / 20)))
        self.width3, self.height3 = int(round((self.root.winfo_screenwidth(
        ) / 25))), int(round((self.root.winfo_screenheight() / 25)))
        self.width4, self.height4 = int(round((self.root.winfo_screenwidth(
        ) / 30))), int(round((self.root.winfo_screenheight() / 30)))
        self.width5, self.height5 = int(round((self.root.winfo_screenwidth(
        ) / 45))), int(round((self.root.winfo_screenheight() / 45)))
        self.width6, self.height6 = int(round((self.root.winfo_screenwidth(
        ) / 55))), int(round((self.root.winfo_screenheight() / 55)))
        self.frame = tk.Frame(self.root, bg='white')
        self.frame.pack()
        self.login()

    def myscrollcontrol(self, canvas):  # Canvas Scroll Controller
        canvas.configure(scrollregion=canvas.bbox("all"), width=self.scroll_width,
                         height=self.scroll_height)  # Allows Scrolling for multiple sized canvases
        canvas.update()

    def login(self):
        self.frame.pack_forget()  # Resets the frame to be used again
        self.frame = tk.Frame(self.root, bg='white')
        self.frame.pack()
        tk.Label(self.frame, text="Filebox", font=("Bradley Hand ITC",
                                                   self.height2, "bold"), bg='white').pack(pady=(0, self.height2))
        tk.Label(self.frame, text="Host", font=("Bradley Hand ITC",
                                                self.height5, "bold"), bg='white').pack(pady=(0, self.height5))
        host_Entry = tk.Entry(self.frame, width=30, font=(
            "Bradley Hand ITC", self.height5, "bold"), bg='white', justify="center")
        host_Entry.pack(pady=(0, self.height5))
        tk.Label(self.frame, text="Username", font=("Bradley Hand ITC",
                                                    self.height5, "bold"), bg='white').pack(pady=(0, self.height5))
        username_Entry = tk.Entry(self.frame, width=30, font=(
            "Bradley Hand ITC", self.height5, "bold"), bg='white', justify="center")
        username_Entry.pack(pady=(0, self.height5))
        tk.Label(self.frame, text="Password", font=("Bradley Hand ITC",
                                                    self.height5, "bold"), bg='white').pack(pady=(0, self.height5))
        password_Entry = tk.Entry(self.frame, width=30, font=(
            "Bradley Hand ITC", self.height5, "bold"), bg='white', justify="center", show="*")
        password_Entry.pack(pady=(0, self.height5))
        tk.Button(self.frame, text="Login", font=("Bradley Hand ITC", self.height5, "bold"), width=10, bg='white',
                  command=lambda: self.user_login(host_Entry, username_Entry, password_Entry)).pack(pady=self.height3)
        tk.Button(self.frame, text="Exit", font=("Bradley Hand ITC", self.height5, "bold"),
                  width=10, fg='red', bg='white', command=lambda: self.root.destroy()).pack()

    def user_login(self, host_Entry, username_Entry, password_Entry):
        self.host = host_Entry.get()
        self.username = username_Entry.get()
        self.password = password_Entry.get()
        try:  # Looks for multiple errors such as authentication errors or ip
            self.ftp = ftplib.FTP(self.host)     # Uses default port (21)
            self.ftp.login(user=self.username, passwd=self.password)
            self.frame.pack_forget()
            self.frame = tk.Frame(self.root, bg='white')
            self.frame.pack()
            tk.Label(self.frame, text="Filebox", font=("Bradley Hand ITC",
                                                       self.height4, "bold"), bg='white').pack(pady=(0, self.height3))
            tk.Label(self.frame, text="Host: " + self.host, font=("Bradley Hand ITC",
                                                                  self.height6, "bold"), bg='white').pack(pady=(0, self.height6), anchor=tk.W)
            tk.Label(self.frame, text="Username: " + self.username, font=("Bradley Hand ITC",
                                                                          self.height6, "bold"), bg='white').pack(pady=(0, self.height6), anchor=tk.W)
            tk.Button(self.frame, text="Upload", font=("", self.height6), bg='white', width=10,
                      command=lambda: self.upload()).pack(pady=(0, self.height6), anchor=tk.W)
            self.current_dir = ""
            name = ""
            self.dir_list = []
            self.scroll_width, self.scroll_height = int(
                self.full_Width / 1.05), int(self.full_Height/2)
            self.outer_Frame = tk.Frame(self.frame, bg='white')
            self.outer_Frame.pack(side=tk.LEFT)
            tk.Button(self.frame, text="Disconnect", font=("Bradley Hand ITC", self.height6, "bold"), width=15,
                      fg='red', bg='white', command=lambda: self.login()).pack(side=tk.BOTTOM, pady=(self.height4, 0))
            self.file_navigation(name)
        except:
            messagebox.showerror(
                "Error", "Could Not Login - Incorrect Credentials")

    def file_navigation(self, name):
        try:
            if name == "." or name == "..":
                del self.dir_list[-1]
            else:
                self.dir_list.append(name)
            self.current_dir = ""
            for x in self.dir_list:
                self.current_dir = self.current_dir + "/" + x
            self.current_dir = self.current_dir + "/"

            self.ftp.cwd(self.current_dir)
            self.outer_Frame.pack_forget()
            self.outer_Frame = tk.Frame(self.frame, bg='white')
            self.outer_Frame.pack(side=tk.LEFT)
            scroll_frame = tk.Frame(self.outer_Frame, bg='white')
            scroll_frame.pack(side=tk.LEFT)
            Canvas = tk.Canvas(scroll_frame, bg='white')
            self.inner_Frame = tk.Frame(Canvas, bg='white')
            myscrollbar = tk.Scrollbar(
                scroll_frame, orient="vertical", command=Canvas.yview)
            Canvas.configure(yscrollcommand=myscrollbar.set)
            myscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            Canvas.pack(side=tk.LEFT)
            Canvas.create_window((0, 0), window=self.inner_Frame, anchor=tk.NW)
            self.inner_Frame.bind(
                "<Configure>", lambda event, canvas=Canvas: self.myscrollcontrol(Canvas))
            self.inner_Grid_Frame = tk.Frame(self.inner_Frame, bg='white')
            self.inner_Grid_Frame.pack(side=tk.LEFT)
            counter = 0c
            for x in self.ftp.nlst(self.ftp.pwd()):
                if x == "." or x == "..":
                    tk.Button(self.inner_Grid_Frame, text=x, font=("Bradley Hand ITC", self.height5, "bold"), bg='white', relief=tk.FLAT, command=lambda name=x: self.file_navigation(
                        name)).grid(row=counter, column=1, padx=(0, self.full_Width / 2),  sticky=tk.W)
                else:
                    tk.Button(self.inner_Grid_Frame, text=x, font=("Bradley Hand ITC", self.height5, "bold"), bg='white', relief=tk.FLAT, command=lambda name=x: self.file_navigation(
                        name)).grid(row=counter, column=1, padx=(0, self.full_Width / 2), sticky=tk.W)
                    tk.Button(self.inner_Grid_Frame, text="Download", font=("Bradley Hand ITC", self.height5, "bold"),
                              bg='white', relief=tk.FLAT, command=lambda name=x: self.file_download(name)).grid(row=counter, column=2)
                    tk.Button(self.inner_Grid_Frame, text="⌫", font=("Bradley Hand ITC", self.height5, "bold"), bg='white',
                              fg='red', relief=tk.FLAT, command=lambda name=x: self.Delete_Prompt(name)).grid(row=counter, column=3)
                counter = counter + 1
        except ftplib.error_perm:
            r = BytesIO()
            self.ftp.retrbinary('RETR ' + name, r.write)
            file_content = r.getvalue().decode()
            popup = tk.Toplevel(self.root, bg='white')
            popup.geometry('%dx%d+100+50' %
                           (self.full_Width / 1.1, self.full_Height / 1.2))
            tk.Label(popup, text=name, font=(" Verdana", self.height6,
                                             "bold"), bg='white').pack(pady=(0, self.height6))
            textbox = tk.Text(popup, width=int(self.full_Width / 1.1), height=int(
                self.full_Height / 1.2), font=(" Verdana", self.height6), wrap=tk.WORD, bg='white')
            textbox.insert(tk.END, file_content)
            scrollbar = tk.Scrollbar(
                popup, orient="vertical", command=textbox.yview)
            yscrollcommand = scrollbar.set
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            textbox.configure(state=tk.DISABLED)
            textbox.pack(side=tk.LEFT)

    def file_download(self, name):
        try:
            self.ftp.retrbinary(
                "RETR " + name, open(".//Downloaded//" + name, 'wb').write)
        except FileNotFoundError:
            os.makedirs(".//Downloaded")
            self.ftp.retrbinary(
                "RETR " + name, open(".//Downloaded//" + name, 'wb').write)
        except:
            messagebox.showerror("Error", "You Cannot Download Folders")

    def upload(self):
        try:
            filepath = filedialog.askopenfilename()
            filename = str(filepath.split("/")[-1:])
            filename = filename.replace("['", "").replace("']", "")
            self.ftp.storbinary("STOR " + filename, open(filepath, 'rb'))
            messagebox.showinfo("Success", filename +
                                " Was Sucessfully Uploaded")
            self.FileNavigation("")
        except:
            messagebox.showerror(
                "Error", "A Error Occoured With The Upload, Please Try Again")

    def Delete_Prompt(self, name):
        result = tk.messagebox.askquestion(
            'Delete a file?', 'Are you sure you want to delete this file / folder?', icon='warning')
        if result == 'yes':
            try:
                self.ftp.rmd(name)
            except:
                self.ftp.delete(name)
        else:
            return




my_Gui = app()
