import json
import customtkinter as CTk

from calculations import VEHICLES
from PIL import Image
with open("activities.json", "r") as file:
    ACTIVITIES = json.load(file)
class Card(CTk.CTkFrame):
    """
    This is designed to be used as a front end.
    this defaults to emission computation for Household appliances.
    Pass down the function to `command` parameter. This will call the function to maually compute for the value.
    """
    def __init__(self, name, top, down, exitCommand = lambda _ :print("Supply exit command parameter!"), mode="household", 
                 topText = 'Hours used per day:', bottomText = 'Rated Wattage:', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode=mode
        self.color="red"
        self.evaluation = ""
        self.name=name
        self.topValue = float(top) if top is not None else 0.0
        self.downValue = float(down) if down is not None else 0.0
        self.topText=topText
        self.downText=bottomText
        self.exitCommand = exitCommand
        self.multiplier = self.topValue * self.downValue 


        match mode:
            case "household":
                self.setHousehold()
            case "transportation":
                self.setTransportation()
            case "activities":
                self.setActivities()
        
        self.evaluate()
        self.configure(width=300, height=105, border_color="#383838",
                 border_width=2, corner_radius=17, fg_color="#ebebeb", bg_color="white")
        self.setName()
    def setHousehold(self):
        wattHourToKiloWattHour = 1000
        emissionFactor = 0.6032
        hoursPerDays = 24

        totalEmissionsPerDay = (self.multiplier / wattHourToKiloWattHour) * emissionFactor
        self.emissionsPerHour = totalEmissionsPerDay / hoursPerDays
    
    def setTransportation(self):
        vehicle = VEHICLES[self.name]
        hoursPerWeek = 168
        emissionPerKm = vehicle["KgCO2perKm"] * self.multiplier
        emissionPerL = vehicle["KmperL"] * vehicle["defaultFuel"] * self.multiplier
        totalEmissionsPerWeek = emissionPerKm + emissionPerL 
        self.emissionsPerHour = totalEmissionsPerWeek / hoursPerWeek
    
    def setActivities(self):
        hoursPerWeek = 168
        emissionFactor = ACTIVITIES[self.name]
        totalEmissionsPerWeek = emissionFactor * self.multiplier
        self.emissionsPerHour = totalEmissionsPerWeek / hoursPerWeek

    def setName(self):
        match self.mode:
            case "household":
                topUnit = ""
                bottomUnit = "KWh"
            case "transportation":
                topUnit = "Km"
                bottomUnit = ""
            case "activities":
                topUnit = ""
                bottomUnit = ""

        textColor = "black"
        colors = {"fg_color":"#ebebeb", "bg_color":"#F6F6F6"}
        self.x_image = Image.open("assets/X.png")
        self.close = CTk.CTkImage(self.x_image, size=(20,20))
        self.close_button = CTk.CTkLabel(self, width=22, height=22, fg_color="#ebebeb", bg_color="white", 
                                         image=self.close, text="", cursor = "hand2")
        self.close_button.place(x=273, y=3)
        self.close_button.bind("<Button-1>", self.exit)
        CTk.CTkLabel(self,width=188, height=20, font=("Poppins",16,"bold"), text_color=textColor,
                      text=self.name, anchor=CTk.W, **colors).place(x=20,y=15)
        CTk.CTkLabel(self,width=150, height=20, font=("Poppins",16), text_color=textColor,
                      text=self.topText, anchor=CTk.W, **colors).place(x=20,y=50)
        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color=textColor,
                      text=f'{self.topValue} {topUnit}', anchor=CTk.W, **colors).place(x=220,y=50)
        CTk.CTkLabel(self,width=150, height=20, font=("Poppins",16), text_color=textColor,
                      text=self.downText, anchor=CTk.W, **colors).place(x=20,y=70)
        result = self.downValue / (1000 if self.mode == "household" else 1)
        formatted_result = round(result, 2)
        formatted_string = f'{formatted_result} {bottomUnit}'

        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color=textColor,
                      text=formatted_string, anchor=CTk.W, **colors).place(x=210,y=70)
        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color="black",
                      text=self.evaluation, anchor=CTk.W, fg_color=self.color,bg_color="#ebebeb", corner_radius=8).place(x=210,y=15)
    def exit(self, _=None):
        self.exitCommand(self)
        self.destroy()     
    def evaluate(self):
        good_threshold = 5.0
        average_threshold = 10.0
        high_threshold = 20.0

        emissions = self.emissionsPerHour
        if emissions < good_threshold:
            self.color="green"
            self.evaluation = "Good"
            return self.evaluation
        
        elif emissions < average_threshold:
            self.color="yellow"
            self.evaluation = "Aver"
            return 
        
        elif emissions < high_threshold:
            self.color="orange"
            self.evaluation = "High"
            return 
        
        else:
            self.color="red"
            self.evaluation = "Extr"
            return self.evaluation
        
        
if __name__ == "__main__":
    app = CTk.CTk()
    app.geometry("300x200")
    c = {}

    card = Card(master = app, name = "Motorcycle",top=24,down=0.4, mode="transportation", exitCommand=lambda x: c.pop(x))
    card.pack(side=CTk.TOP, anchor=CTk.W)
    c[card] = "Card"
    a=Card(master = app, name = "Motorcycle",top=24,down=0.4, mode="household", exitCommand=lambda x: c.pop(x))
    a.pack(side=CTk.TOP, anchor=CTk.W)
    c[a]="A"
    b=Card(master = app, name = "Cigarette Smoking",top=24,down=0.4, mode="activities", exitCommand=lambda x: c.pop(x))
    b.pack(side=CTk.TOP, anchor=CTk.W)
    c[b]="B"


    print(card.evaluation)
    print(card.evaluation)
    print(c)
    app.mainloop()