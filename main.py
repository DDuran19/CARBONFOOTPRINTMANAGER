import customtkinter as CTk
import json

from tkinter import messagebox
from PIL import Image
from functools import partial
from Card import Card
from userQuery import UserAuthentication
from dataProcessor import DataProcessor
from CarbonFootprint import CarbonFootprint
from calculations import VEHICLES
with open("household.json", "r") as file:
    HOUSEHOLD = json.load(file)

with open("activities.json", "r") as file:
    ACTIVITIES = json.load(file)

class Login(CTk.CTk):
    def __init__(self, login, register, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_window()
        self.household_cards={}
        self.transportation_cards={}
        self.activities_cards={}
        self.title("Carbong Footprint Manager")
        self.loginCommand = login
        self.registerCommand = register
        self.isLogin = True
        self.registerOnHover = False
        self.setupLoginScreen()
    def setupLoginScreen(self, event = None):
        if event is not None:
            response = messagebox.askyesno(title="Sign Out", message="Are you sure you want to sign out?")
            if not response:
                return False
        self.left_rectangle()
        self.right_rectangle()
        return True        
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
        self.left_rectangleLabel = CTk.CTkLabel(self,width=860,height=900, image=self.left_background, text="Carbon Footprint Manager      \n\n\n\n", font=("Poppins",43))
        self.left_rectangleLabel.place(x=0,y=0)
        self.title=CTk.CTkLabel(self, text="Empowering Greener Lives: Your Carbon Conscious Companion", font=("Poppins",16),fg_color="#098624",
                            text_color="white")
        self.title.place(x=145,y=380)
        self.read_more = CTk.CTkButton(self, text="Read More", font=("Poppins",13),corner_radius=15, bg_color="#098624", fg_color="#05E637", text_color="black")
        self.read_more.place(x=145,y=420)
    def right_rectangle(self):
        colors = {"fg_color":"white", "bg_color":"white"}

        self.right_frame = CTk.CTkFrame(self,width=580,height=900, corner_radius=0, **colors)
        self.right_frame.place(x=860,y=0)

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
        self.passwordIcon=CTk.CTkLabel(self, width=40, height=40, text="", image=self.password, fg_color="white", bg_color="white")
        self.passwordIcon.place(x=1016, y=426)

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
        isLoggedIn = self.loginCommand(self.username_value.get(), self.password_value.get())
        if not isLoggedIn:
            messagebox.showwarning(title="Unsuccessful", message="Invalid username or password")
            return
        # Hide ALL EXISTING WIDGETS
        modal_components = [self.left_rectangleLabel.destroy, 
        self.title.destroy, 
        self.read_more.destroy, 
        self.right_frame.destroy, 
        self.username_frame.destroy, 
        self.usernameIcon.destroy, 
        self.passwordIcon.destroy, 
        self.usernameEntry.destroy, 
        self.greeting1.destroy, 
        self.greeting2.destroy, 
        self.passwordEntry.destroy, 
        self.password_frame.destroy, 
        self.login_button.destroy, 
        self.register_link.destroy]
        for component in modal_components:
            try:
                component()
            except AttributeError:
                continue

        self.selected = None
        self.setSideBar()
        self.setMainComponent()

    def regUser(self):
        validRegistration = self.registerCommand(self.username_value.get(), self.password_value.get())
        if not validRegistration:
            messagebox.showwarning(title="Unsuccessful", message="Username already exists. Try a new username.")
            return
        messagebox.showinfo(title="Successful!", message="User registered successfully!")
        
        self.switch()

    def switch(self, event = None):
        self.username_value.set("")
        self.password_value.set("")
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
        
# Below part is for CarbonFootprint main interface
    def setSideBar(self):
        self.sideBarImage = Image.open("assets/sidebar.png")
        self.sideBar = CTk.CTkImage(self.sideBarImage,size=(376,900))

        left_rectangle = CTk.CTkLabel(self, width=376, height=900, image=self.sideBar, text="Carbon Footprint\n             Manager\n\n\n\n\n\n\n\n", font=("Poppins",43))
        left_rectangle.place(x=0,y=0)

        self.householdImage = Image.open("assets/householdMenu.png")
        self.transportationImage = Image.open("assets/transportationMenu.png")
        self.activitiesImage = Image.open("assets/activitiesMenu.png")
        self.signoutImage = Image.open("assets/signoutMenu.png")

        self.household=CTk.CTkImage(self.householdImage, size=(376,40))
        self.transportation=CTk.CTkImage(self.transportationImage, size=(376,40))
        self.activities=CTk.CTkImage(self.activitiesImage, size=(376,40))
        self.signout=CTk.CTkImage(self.signoutImage, size=(376,40))

        self.householdButton = CTk.CTkLabel(self,text="Household", cursor="hand2",image=self.household, width=376, height=40)
        self.transportationButton = CTk.CTkLabel(self,text="Transportation", cursor="hand2", image=self.transportation, width=376, height=40)
        self.activitiesButton = CTk.CTkLabel(self,text="Activities", cursor="hand2", image=self.activities, width=376, height=40)
        self.signoutButton = CTk.CTkLabel(self,text="Sign Out", cursor="hand2", image=self.signout, width=376, height=40)

        self.householdButton.place(x=70, y=320)
        self.transportationButton.place(x=70, y=360)
        self.activitiesButton.place(x=70, y=400)
        self.signoutButton.place(x=70, y=440)
        self.householdButton.bind('<Enter>', partial(self.onEnter, self.householdButton))
        self.householdButton.bind('<Leave>', partial(self.onLeave, self.householdButton))
        self.householdButton.bind('<Button-1>', self.activate_household)
        self.transportationButton.bind('<Enter>', partial(self.onEnter, self.transportationButton))
        self.transportationButton.bind('<Leave>', partial(self.onLeave, self.transportationButton))
        self.transportationButton.bind('<Button-1>', self.activate_transportation)
        self.activitiesButton.bind('<Enter>', partial(self.onEnter, self.activitiesButton))
        self.activitiesButton.bind('<Leave>', partial(self.onLeave, self.activitiesButton))
        self.activitiesButton.bind('<Button-1>', self.activate_activities)
        self.signoutButton.bind('<Enter>', partial(self.onEnter, self.signoutButton))
        self.signoutButton.bind('<Leave>', partial(self.onLeave, self.signoutButton))
        self.signoutButton.bind('<Button-1>', self.askForSignOutConfirmation)

    def setMainComponent(self):
        colors = {"fg_color":"white", "bg_color":"white"}
        colors2 = {"fg_color":"#F6F6F6","bg_color":"#F6F6F6"}
        self.right_frame = CTk.CTkFrame(self,width=1064,height=900, corner_radius=0, **colors)
        self.right_frame.place(x=376,y=0)
        self.welcome = CTk.CTkLabel(self, text="Welcome back, John!",font=("Poppins",43), text_color="#383838",**colors)
        self.welcome.place(x=406, y=70)

        self.namelessFrame = CTk.CTkFrame(self,width=1005,height=693, corner_radius=17, fg_color="#F6F6F6", bg_color="white", border_color="black",border_width=3)
        self.namelessFrame.place(x=406,y=185)
        self.householdPageName = CTk.CTkLabel(self, text="Household", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.transportationPageName = CTk.CTkLabel(self, text="Transportation", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.activitiesPageName = CTk.CTkLabel(self, text="Activities", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.householdScrollable_frame = CTk.CTkScrollableFrame(self,width=320, height=580, corner_radius=15,**colors2)
        self.transportationScrollable_frame = CTk.CTkScrollableFrame(self, width=320, height=580, corner_radius=15,**colors2)
        self.activitiesScrollable_frame = CTk.CTkScrollableFrame(self, width=320, height=580, corner_radius=15,**colors2)
        self.mode = {}
        self.resultsFrame = CTk.CTkFrame(self,width=610,height=600, corner_radius=17, fg_color="#C9C9C9", bg_color="#F6F6F6", border_color="black",border_width=3)
        self.resultsFrame.place(x=775, y=240)
        self.addButtonIcon = Image.open("assets/addButton.png")
        self.addButtonImage = CTk.CTkImage(self.addButtonIcon, size=(50,50))
        self.addButton = CTk.CTkLabel(self,width=50, height=50, text="", image=self.addButtonImage,fg_color="#F6F6F6", cursor="hand2")
        self.addIsActive = False
        self.addButton.bind("<Button-1>", self.setNewItemFrame)
        self.addButton.place(x=700, y= 188)
        self.newItemFrame=CTk.CTkFrame(self,width=320, height=300, corner_radius=15, border_color="black",border_width=2, **colors2)
        self.activate_household(None)
    def addItem(self, name = "", top=0, down=0):
        self.setNewItemFrame()
        newcard = Card(master=self.selected, name=name,top=top, down=down, **self.mode)
        newcard.pack(side = CTk.TOP, anchor = CTk.W, padx=0)
        self.destroyModal()
        match self.selected:
            case self.householdScrollable_frame:
                self.household_cards[newcard]=[newcard.emissionsPerHour, newcard.evaluation]
            case self.transportationScrollable_frame:
                self.transportation_cards[newcard]=[newcard.emissionsPerHour, newcard.evaluation]
            case self.activitiesScrollable_frame:
                self.activities_cards[newcard]=[newcard.emissionsPerHour, newcard.evaluation]
        print(self.household_cards)
        print(self.transportation_cards)
        print(self.activities_cards)
    def destroyModal(self):
        try:
            modal_components = [self.name_label.destroy, 
            self.name_entry.destroy, 
            self.top_label.destroy, 
            self.top_entry.destroy, 
            self.down_label.destroy, 
            self.down_entry.destroy, 
            self.submit_button.destroy, 
            self.newItemFrame.place_forget]

            for component in modal_components:
                try:
                    component()
                except:
                    continue
        except:
            pass
        finally:
            self.addIsActive = False
    def setNewItemFrame(self, _ = None):
        if self.addIsActive:
            self.destroyModal()
            return
        else:
            self.addIsActive = True

        values = []
        daysInAWeek = ["1","2","3","4","5","6","7"]
        self.down_entry=None

        colors2 = {"fg_color":"#F6F6F6","bg_color":"#F6F6F6"}
        self.newItemFrame=CTk.CTkFrame(self,width=320, height=300, corner_radius=15, border_color="black",border_width=2, **colors2)
        self.newItemFrame.place(x=430, y=240)

        match self.selectedLabel:
            case self.householdButton:
                values = HOUSEHOLD
                self.down_entry = CTk.CTkEntry(self.newItemFrame)
            case self.transportationButton:
                values = list(VEHICLES.keys())
                self.down_entry = CTk.CTkComboBox(self.newItemFrame, values=daysInAWeek)
            case self.activitiesButton:
                values = list(ACTIVITIES.keys())
                self.down_entry = CTk.CTkComboBox(self.newItemFrame, values=daysInAWeek)

        self.name_label = CTk.CTkLabel(self.newItemFrame, text="Name:", text_color="#383838")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = CTk.CTkComboBox(self.newItemFrame, values=values)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.top_label = CTk.CTkLabel(self.newItemFrame, text=self.mode["topText"], text_color="#383838")
        self.top_label.grid(row=1, column=0, padx=10, pady=5)
        self.top_entry = CTk.CTkEntry(self.newItemFrame)
        self.top_entry.grid(row=1, column=1, padx=10, pady=5)
        self.down_label = CTk.CTkLabel(self.newItemFrame, text=self.mode["bottomText"], text_color="#383838")
        self.down_label.grid(row=2, column=0, padx=10, pady=5)
        self.down_entry.grid(row=2, column=1, padx=10, pady=5)
        self.submit_button = CTk.CTkButton(self.newItemFrame, text="Submit", state=CTk.DISABLED,
                                           command=lambda: self.addItem(self.name_entry.get(),self.top_entry.get(),self.down_entry.get()))
        self.top_entry.bind("<KeyPress>",command=lambda event: self.validate_entry(
                event=event,
                entry=self.top_entry,
                button=self.submit_button,
            ))
        self.submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    def validate_entry(self, event, entry: CTk.CTkEntry, button: CTk.CTkButton, command=None):
        value = event.char
        try:
            float(entry.get())
            isFloat = True
        except ValueError:
            isFloat = False

        # if value.isalpha() and value != "\x0D":
        #     button.configure(state=CTk.DISABLED)
        # elif isFloat and command is not None:
        #     command()
        if isFloat:
            button.configure(require_redraw=True, state=CTk.NORMAL)
        else:
            button.configure(state=CTk.DISABLED)

    def activate_household(self, _):
        self.selected = self.householdScrollable_frame
        self.selectedLabel = self.householdButton
        self.destroyModal()
        self.mode = {"mode": "household", "topText": "Hours used per day: ", "bottomText": "Rated Wattage: ", "exitCommand": lambda x: self.household_cards.pop(x) }
        self.householdButton.configure(text="\u2192  Household", font=("Poppins", 20, "bold"), text_color="black")
        self.transportationButton.configure(text="Transportation", font=("Poppins", 12, "bold"), text_color="white")
        self.activitiesButton.configure(text="Activities", font=("Poppins", 12, "bold"), text_color="white")
        
        self.householdPageName.place(x=430, y=200)
        self.transportationPageName.place_forget()
        self.activitiesPageName.place_forget()

        self.householdScrollable_frame.place(x=410, y=240)
        self.transportationScrollable_frame.place_forget()
        self.activitiesScrollable_frame.place_forget()

    def activate_transportation(self, _):
        self.selected=self.transportationScrollable_frame
        self.selectedLabel=self.transportationButton
        self.destroyModal()
        self.mode = {"mode": "transportation", "topText": "Distance travelled per day: ", "bottomText": "Travel days per week: ", "exitCommand": lambda x: self.transportation_cards.pop(x)}

        self.householdButton.configure(text="Household", font=("Poppins", 12, "bold"), text_color="white")
        self.transportationButton.configure(text="\u2192  Transportation", font=("Poppins", 20, "bold"), text_color="black")
        self.activitiesButton.configure(text="Activities", font=("Poppins", 12, "bold"), text_color="white")

        self.householdPageName.place_forget()
        self.transportationPageName.place(x=430, y=200)
        self.activitiesPageName.place_forget()

        self.householdScrollable_frame.place_forget()
        self.transportationScrollable_frame.place(x=410, y=240)
        self.activitiesScrollable_frame.place_forget()
        
    def activate_activities(self, _):
        self.selected=self.activitiesScrollable_frame
        self.selectedLabel=self.activitiesButton
        self.destroyModal()
        self.mode = {"mode": "activities", "topText": "Consumed per day: ", "bottomText": "Days per Week: ", "exitCommand": lambda x: self.activities_cards.pop(x)}
        self.householdButton.configure(text="Household", font=("Poppins", 12, "bold"), text_color="white")
        self.transportationButton.configure(text="Transportation", font=("Poppins", 12, "bold"), text_color="white")
        self.activitiesButton.configure(text="\u2192  Activities", font=("Poppins", 20, "bold"), text_color="black")

        self.householdPageName.place_forget()
        self.transportationPageName.place_forget()
        self.activitiesPageName.place(x=430, y=200)

        self.householdScrollable_frame.place_forget()
        self.transportationScrollable_frame.place_forget()
        self.activitiesScrollable_frame.place(x=410, y=240)

    def onEnter(self, label: CTk.CTkLabel, _):
        if label == self.selectedLabel:
            return
        label.configure(text_color="yellow", font=("poppins",20, "bold"))     
    def onLeave(self, label: CTk.CTkLabel, _):
        if label == self.selectedLabel:
            return
        label.configure(text_color="white", font=("poppins",12 ))

    def askForSignOutConfirmation(self, _=None):
        if not self.setupLoginScreen(event=True):
            return
        self.household_cards = {}
        self.transportation_cards = {}
        self.activities_cards = {}
        commands = [self.namelessFrame.destroy,
        self.householdButton.destroy,
        self.transportationButton.destroy,
        self.activitiesButton.destroy,
        self.signoutButton.destroy,
        self.right_frame.destroy,
        self.welcome.destroy,
        self.householdPageName.destroy,
        self.transportationPageName.destroy,
        self.activitiesPageName.destroy,
        self.householdScrollable_frame.destroy,
        self.transportationScrollable_frame.destroy,
        self.activitiesScrollable_frame.destroy,
        self.resultsFrame.destroy,
        self.addButton.destroy,
        self.destroyModal,
        self.newItemFrame.destroy]

        for command in commands:
            try:
                command()
            except: pass
    
    def dataProcessing(self):
        self.dataProcesor=DataProcessor()

if __name__ == '__main__':
    auth = UserAuthentication()
    app = Login(auth.login, auth.register)
    app.mainloop()