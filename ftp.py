import ftplib
import tkinter as tk
import os, re, wget
#ftp.cwd('dir') -- Changes directory
class app():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg = 'white')
        self.full_Width, self.full_Height  = self.root.winfo_screenwidth(), self.root.winfo_screenheight() # Settings general widths and heights for 16:9 and 16:10 screens
        self.root.geometry('%dx%d+0+0' % (self.full_Width, self.full_Height)) 
        self.width1, self.height1 = int(round((self.root.winfo_screenwidth() / 15))), int(round((self.root.winfo_screenheight() / 15))) #General widths and heights to be used for widgets
        self.width2, self.height2 = int(round((self.root.winfo_screenwidth() / 20))), int(round((self.root.winfo_screenheight() / 20))) 
        self.width3, self.height3 = int(round((self.root.winfo_screenwidth() / 25))), int(round((self.root.winfo_screenheight() / 25))) 
        self.width4, self.height4 = int(round((self.root.winfo_screenwidth() / 30))), int(round((self.root.winfo_screenheight() / 30)))
        self.width5, self.height5 = int(round((self.root.winfo_screenwidth() / 45))), int(round((self.root.winfo_screenheight() / 45)))
        self.width6, self.height6 = int(round((self.root.winfo_screenwidth() / 55))), int(round((self.root.winfo_screenheight() / 55)))
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        self.Main()

    def MyScrollControl(self, canvas, width, height): #Canvas Scroll Controller
        canvas.configure(scrollregion=canvas.bbox("all"),width=width, height = height) #Allows Scrolling for multiple sized canvases
        canvas.update() 

    def Main(self):
        self.frame.pack_forget() #Resets the frame to be used again
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        tk.Label(self.frame, text = "Filebox", font=("Bradley Hand ITC", self.height2, "bold"), bg = 'white').pack(pady = (0, self.height2))
        
        tk.Label(self.frame, text = "Host", font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white').pack(pady = (0, self.height5))
        host_Entry = tk.Entry(self.frame, width = 30, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', justify = "center")
        host_Entry.pack(pady = (0, self.height5))
        host_Entry.insert(tk.END, "files.000webhost.com")

        tk.Label(self.frame, text = "Username", font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white').pack(pady = (0, self.height5))
        username_Entry = tk.Entry(self.frame, width = 30, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', justify = "center")
        username_Entry.pack(pady = (0, self.height5))
        username_Entry.insert(tk.END, "llysfaen-village-hall")

        tk.Label(self.frame, text = "Password", font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white').pack(pady = (0, self.height5))
        password_Entry = tk.Entry(self.frame, width = 30, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', justify = "center", show = "*")
        password_Entry.pack(pady = (0, self.height5))
        password_Entry.insert(tk.END, "Swimwear123")

        tk.Label(self.frame, text = "Port", font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white').pack(pady = (0, self.height5))
        port_Entry = tk.Entry(self.frame, width = 30, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', justify = "center")
        port_Entry.pack(pady = (0, self.height3))
        port_Entry.insert(tk.END, "21")

        tk.Button(self.frame, text = "Login", font=("Bradley Hand ITC", self.height5, "bold"), width = 10, bg = 'white', command = lambda:self.User_Login(host_Entry, username_Entry, password_Entry, port_Entry)).pack(pady = self.height3)
        tk.Button(self.frame, text = "Exit", font=("Bradley Hand ITC", self.height5, "bold"), width = 10, fg = 'red', bg = 'white', command = lambda: self.Main()).pack()



    def User_Login(self, host_Entry, username_Entry, password_Entry, port_Entry):
        self.host = host_Entry.get()
        self.username = username_Entry.get()
        self.password = password_Entry.get()
        self.port = port_Entry.get()        
        self.ftp = ftplib.FTP(self.host)     # Uses default port (21)
        self.ftp.login(user = self.username, passwd = self.password)
        self.frame.pack_forget()
        self.frame = tk.Frame(self.root, bg = 'white')
        self.frame.pack()
        tk.Label(self.frame, text = "Filebox", font=("Bradley Hand ITC", self.height3, "bold"), bg = 'white').pack(pady = (0, self.height3))
        tk.Label(self.frame, text = "Host: " + self.host, font=("Bradley Hand ITC", self.height6, "bold"), bg = 'white').pack(pady = (0, self.height5), anchor = tk.W)
        tk.Label(self.frame, text = "Username: " + self.username, font=("Bradley Hand ITC", self.height6, "bold"), bg = 'white').pack(pady = (0, self.height5), anchor = tk.W)
        self.current_dir = ""
        self.dir_list = []

        width, height = int(self.full_Width / 1.05), int(self.full_Height/1.6)
        outer_Frame = tk.Frame(self.frame, bg = 'white')
        outer_Frame.pack(side=tk.LEFT)  
        scroll_frame = tk.Frame(outer_Frame, bg = 'white')
        scroll_frame.pack(side=tk.LEFT)
        Canvas=tk.Canvas(scroll_frame, bg='white')
        self.inner_Frame = tk.Frame(Canvas, bg='white')
        myscrollbar = tk.Scrollbar(scroll_frame, orient="vertical",command = Canvas.yview)
        Canvas.configure(yscrollcommand = myscrollbar.set)
        myscrollbar.pack(side = tk.RIGHT,fill = tk.Y)
        Canvas.pack(side=tk.LEFT)
        Canvas.create_window((0,0),window=self.inner_Frame, anchor = tk.NW)
        self.inner_Frame.bind("<Configure>", lambda event, canvas = Canvas:self.MyScrollControl(Canvas, width, height))
        
        for x in self.ftp.nlst(self.ftp.pwd()):
            tk.Button(self.inner_Frame, text = x, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', relief = tk.FLAT, command = lambda name = x: self.File_Navigation(
                name, width, height, outer_Frame)).pack(pady = (0, self.height2), anchor = tk.W)
        tk.Button(self.frame, text = "Disconnect", font=("Bradley Hand ITC", self.height6, "bold"), width = 15, fg = 'red', bg = 'white', command = lambda: self.Main()).pack(side=tk.BOTTOM, pady = (self.height4,0))
    


    def File_Navigation(self, name, width, height, outer_Frame):
        if name == "." or name == "..":
            del self.dir_list[-1]
        else:
            self.dir_list.append(name)
        self.current_dir = ""
        for x in self.dir_list:
            self.current_dir = self.current_dir + "/" + x
        self.current_dir = self.current_dir + "/"
        
        self.ftp.cwd(self.current_dir)
        outer_Frame.pack_forget()
        outer_Frame = tk.Frame(self.frame, bg = 'white')
        outer_Frame.pack(side=tk.LEFT)  
        scroll_frame = tk.Frame(outer_Frame, bg = 'white')
        scroll_frame.pack(side=tk.LEFT)
        Canvas=tk.Canvas(scroll_frame, bg='white')
        self.inner_Frame = tk.Frame(Canvas, bg='white')
        myscrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command = Canvas.yview)
        Canvas.configure(yscrollcommand = myscrollbar.set)
        myscrollbar.pack(side = tk.RIGHT,fill = tk.Y)
        Canvas.pack(side=tk.LEFT)
        Canvas.create_window((0,0),window=self.inner_Frame, anchor = tk.NW)
        self.inner_Frame.bind("<Configure>", lambda event, canvas = Canvas:self.MyScrollControl(Canvas, width, height))


        self.inner_Grid_Frame = tk.Frame(self.inner_Frame, bg = 'white')
        self.inner_Grid_Frame.pack(side=tk.LEFT)

        counter = 0
        
        for x in self.ftp.nlst(self.ftp.pwd()):
            if x == "." or x == "..":
                tk.Button(self.inner_Grid_Frame, text = x, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', relief = tk.FLAT, command = lambda name = x: self.File_Navigation(
                    name, width, height, outer_Frame)).grid(row = counter, column = 1, padx = self.width1 * 3, sticky = tk.W)
            else:
                tk.Radiobutton(self.inner_Grid_Frame, bg = 'white', relief = tk.FLAT, font=("Bradley Hand ITC", self.height4, "bold")).grid(row = counter, column = 0)

                tk.Button(self.inner_Grid_Frame, text = x, font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', relief = tk.FLAT, command = lambda name = x: self.File_Navigation(
                    name, width, height, outer_Frame)).grid(row = counter, column = 1, padx = self.width1 * 3, sticky = tk.W)

                tk.Button(self.inner_Grid_Frame, text = "Download", font=("Bradley Hand ITC", self.height5, "bold"), bg = 'white', relief = tk.FLAT, command = lambda name = x: self.File_Download(name)).grid(row = counter, column = 2)
                
            counter = counter + 1

    def File_Download(self, name):
        try:
            self.ftp.retrbinary("RETR " + name ,open(".//Downloaded//" + name, 'wb').write)
        except FileNotFoundError:
            os.makedirs(".//Downloaded")
            self.ftp.retrbinary("RETR " + name ,open(".//Downloaded//" + name, 'wb').write)
        except ftplib.error_perm:
            name = self.current_dir + "//" + name
            destination = ".//Downloaded/ "
            self.Folder_Download(name, destination)
            
    def Folder_Download(self, path, destination):
        try:
            self.ftp.cwd(path)
            #clone path to destination
            os.chdir(destination)
            os.mkdir(destination[0:len(destination)-1]+path)
        except FileNotFoundError::
            os.makedirs(
            #folder already exists at destination

        filelist = self.ftp.nlst()

        for file in filelist:
            try:
                #this will check if file is folder:
                self.ftp.cwd(path+file+"/")
                #if so, explore it:
                downloadFiles(path+file,destination)
            except ftplib.error_perm:
                #not a folder with accessible content
                #download & return
                os.chdir(destination[0:len(destination)-1]+path)
                #possibly need a permission exception catch:
                self.ftp.retrbinary("RETR "+file, open(os.path.join(destination,file),"wb").write)
        return

# https://stackoverflow.com/questions/2605119/downloading-a-directory-tree-with-ftplib - final comment
my_Gui = app()
