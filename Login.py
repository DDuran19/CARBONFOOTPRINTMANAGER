import customtkinter as CTk

from PIL import Image
from functools import partial

class Login(CTk.CTk):
    def __init__(self, login, register, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_window()
        self.title("Carbong Footprint Manager")
        self.loginCommand = login
        self.registerCommand = register
        self.isLogin = True
        self.registerOnHover = False
        self.left_rectangle()
        self.right_rectangle()
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 1440) // 2
        y = (screen_height - 900) // 2
        self.geometry(f"{1440}x{900}+{x}+{y}")
        self.resizable(False,False)
    def left_rectangle(self):
        self.left_background_image = Image.open("assets/leftLogin.png")
        self.left_background = CTk.CTkImage(self.left_background_image,size=(860,900))
        left_rectangle = CTk.CTkLabel(self,width=860,height=900, image=self.left_background, text="Carbon Footprint Manager      \n\n\n\n", font=("Poppins",43))
        left_rectangle.place(x=0,y=0)
        title=CTk.CTkLabel(self, text="Empowering Greener Lives: Your Carbon Conscious Companion", font=("Poppins",16),fg_color="#098624",
                            text_color="white")
        title.place(x=145,y=380)
        read_more = CTk.CTkButton(self, text="Read More", font=("Poppins",13),corner_radius=15, bg_color="#098624", fg_color="#05E637", text_color="black")
        read_more.place(x=145,y=420)

    def right_rectangle(self):
        colors = {"fg_color":"white", "bg_color":"white"}

        right_frame = CTk.CTkFrame(self,width=580,height=900, corner_radius=0, **colors)
        right_frame.place(x=860,y=0)

        self.greeting1=CTk.CTkLabel(self,text="Hello Again!", text_color="black", font=("poppins",26, "bold"), **colors)
        self.greeting1.place(x=993, y=272)
        self.greeting2=CTk.CTkLabel(self,text="Welcome Back", text_color="black", font=("poppins",20), **colors)
        self.greeting2.place(x=993, y=302)

        self.username_icon = Image.open("assets/username.png")
        self.password_icon = Image.open("assets/password.png")
        self.username = CTk.CTkImage(self.username_icon, size=(45,45))
        self.password = CTk.CTkImage(self.password_icon, size=(40,40))
        self.username_frame = CTk.CTkFrame(self, width=307,height=50, corner_radius=30, border_color="lightgray", border_width=2,**colors)
        self.username_frame.place(x=993, y=361)
        self.usernameIcon=CTk.CTkLabel(self, width=45, height=45, text="", image=self.username, fg_color="white")
        self.usernameIcon.place(x=1013, y=363)

        self.password_frame = CTk.CTkFrame(self, width=307,height=50, corner_radius=30, border_color="lightgray", border_width=2,bg_color="white", fg_color="white")
        self.password_frame.place(x=993, y=422)
        self.usernameIcon=CTk.CTkLabel(self, width=40, height=40, text="", image=self.password, fg_color="white", bg_color="white")
        self.usernameIcon.place(x=1016, y=426)

        self.username_value = CTk.StringVar(self,"")
        self.usernameEntry = CTk.CTkEntry(self, width=210,height=43, border_width=0, bg_color="white", 
                                          fg_color="white", font=("poppins",21), text_color="black", textvariable=self.username_value)
        self.usernameEntry.place(x=1055,y=365)

        self.password_value = CTk.StringVar(self,"")
        self.passwordEntry = CTk.CTkEntry(self, width=210,height=43, border_width=0, bg_color="white", 
                                          fg_color="white", font=("Poppins",21), text_color="black", show="*", textvariable=self.password_value)
        self.passwordEntry.place(x=1055,y=427)
        
        self.login_button = CTk.CTkButton(self,307, height=50, corner_radius=30,font=("Poppins",21, "bold"), text_color="black", 
                                          text="Login", bg_color="white", fg_color="#05E637", hover_color="#05c02e", command=self.login)
        self.login_button.place(x=993,y=510)

        self.register_link = CTk.CTkLabel(self,text="Register Now", text_color="lightgray", font=("poppins",18), cursor = "hand2", **colors)
        self.register_link.place(x=1100, y=570)
        self.register_link.bind('<Button-1>', self.switch)
        self.register_link.bind('<Enter>', partial(self.onEnterLogin, self.register_link))
        self.register_link.bind('<Leave>', partial(self.onLeaveLogin, self.register_link))

    def login(self):
        self.loginCommand(self.username_value.get(), self.password_value.get())

    def regUser(self):
        self.registerCommand(self.username_value.get(), self.password_value.get())
      
    def switch(self, event):
        if self.isLogin:
            self.greeting1.configure(text="Hello!")
            self.greeting2.configure(text="Sign Up to Get Started")
            self.username_frame.configure(border_color="#05E637")
            self.password_frame.configure(border_color="#05E637")
            self.login_button.configure(text="Register", command = self.regUser)
            self.isLogin = False
            return
        self.greeting1.configure(text="Hello Again!")
        self.greeting2.configure(text="Welcome Back")
        self.username_frame.configure(border_color="lightgray")
        self.password_frame.configure(border_color="lightgray")
        self.login_button.configure(text="Login", command = self.login)
        self.isLogin = True
        return
    
    def onEnterLogin(self, label: CTk.CTkLabel, _):
        label.configure(text_color="red")

    def onLeaveLogin(self, label: CTk.CTkLabel, _):
        label.configure(text_color="lightgray")
        

if __name__ == '__main__':

    app = Login(lambda x, y: print(f'{x}, {y}'), lambda x, y: print(f'{x}, {y}'))
    app.mainloop()