import customtkinter as CTk

from PIL import Image
from functools import partial

class CarbonFootprint(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center_window()
        self.title("Carbong Footprint Manager")
        self.selected = None
        self.setSideBar()
        self.setMainComponent()
        
    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - 1440) // 2
        y = (screen_height - 900) // 2
        self.geometry(f"{1440}x{900}+{x}+{y}")
        self.resizable(False,False)
    
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

    def setMainComponent(self):
        colors = {"fg_color":"white", "bg_color":"white"}

        right_frame = CTk.CTkFrame(self,width=1064,height=900, corner_radius=0, **colors)
        right_frame.place(x=376,y=0)
        self.welcome = CTk.CTkLabel(self, text="Welcome back, John!",font=("Poppins",43), text_color="#383838",**colors)
        self.welcome.place(x=406, y=70)

        CTk.CTkFrame(self,width=1005,height=693, corner_radius=17, fg_color="#F6F6F6", bg_color="white", border_color="black",border_width=3).place(x=406,y=185)
        self.householdPageName = CTk.CTkLabel(self, text="Household", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.transportationPageName = CTk.CTkLabel(self, text="Transportation", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.activitiesPageName = CTk.CTkLabel(self, text="Activities", font=("Poppins",18, "bold"), text_color="#383838", fg_color="#F6F6F6",bg_color="white")
        self.householdScrollable_frame = CTk.CTkScrollableFrame(self, width=300, height=580, corner_radius=15,fg_color="#F6F6F6",bg_color="#F6F6F6")
        self.transportationScrollable_frame = CTk.CTkScrollableFrame(self, width=300, height=580, corner_radius=15,fg_color="#F6F6F6",bg_color="#F6F6F6")
        self.activitiesScrollable_frame = CTk.CTkScrollableFrame(self, width=300, height=580, corner_radius=15,fg_color="#F6F6F6",bg_color="#F6F6F6")

        self.resultsFrame = CTk.CTkFrame(self,width=610,height=600, corner_radius=17, fg_color="#C9C9C9", bg_color="#F6F6F6", border_color="black",border_width=3)
        self.resultsFrame.place(x=775, y=240)

        self.activate_household(None)

    def activate_household(self, _):
        self.selected = self.householdButton
        self.householdButton.configure(text="\u2192  Household", font=("Poppins", 20, "bold"), text_color="black")
        self.transportationButton.configure(text="Transportation", font=("Poppins", 12, "bold"), text_color="white")
        self.activitiesButton.configure(text="Activities", font=("Poppins", 12, "bold"), text_color="white")
        
        self.householdPageName.place(x=430, y=200)
        self.transportationPageName.place_forget()
        self.activitiesPageName.place_forget()

        self.householdScrollable_frame.place(x=430, y=240)
        self.transportationScrollable_frame.place_forget(x=430, y=240)
        self.activitiesScrollable_frame.place_forget(x=430, y=240)

    def activate_transportation(self, _):
        self.selected=self.transportationButton
        self.householdButton.configure(text="Household", font=("Poppins", 12, "bold"), text_color="white")
        self.transportationButton.configure(text="\u2192  Transportation", font=("Poppins", 20, "bold"), text_color="black")
        self.activitiesButton.configure(text="Activities", font=("Poppins", 12, "bold"), text_color="white")

        self.householdPageName.place_forget()
        self.transportationPageName.place(x=430, y=200)
        self.activitiesPageName.place_forget()

        self.householdScrollable_frame.place_forget()
        self.transportationScrollable_frame.place(x=430, y=240)
        self.activitiesScrollable_frame.place_forget()
        
    def activate_activities(self, _):
        self.selected=self.activitiesButton
        self.householdButton.configure(text="Household", font=("Poppins", 12, "bold"), text_color="white")
        self.transportationButton.configure(text="Transportation", font=("Poppins", 12, "bold"), text_color="white")
        self.activitiesButton.configure(text="\u2192  Activities", font=("Poppins", 20, "bold"), text_color="black")

        self.householdPageName.place_forget()
        self.transportationPageName.place_forget()
        self.activitiesPageName.place(x=430, y=200)

        self.householdScrollable_frame.place_forget()
        self.transportationScrollable_frame.place_forget()
        self.activitiesScrollable_frame.place(x=430, y=240)


    def onEnter(self, label: CTk.CTkLabel, _):
        if label == self.selected:
            return
        label.configure(text_color="yellow", font=("poppins",20, "bold"))
        

    def onLeave(self, label: CTk.CTkLabel, _):
        if label == self.selected:
            return
        label.configure(text_color="white", font=("poppins",12 ))
        
        
    

if __name__ == '__main__':

    app = CarbonFootprint()
    app.mainloop()