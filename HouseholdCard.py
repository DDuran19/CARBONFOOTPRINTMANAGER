import customtkinter as CTk

class Card(CTk.CTkFrame):
    """
    This is designed to be used as a front end.
    this defaults to emission computation for Household appliances.
    Pass down the function to `command` parameter. This will call the function to maually compute for the value.
    """
    def __init__(self, name, top, down, constant=0.6032, command = None, mode="household", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode=mode
        self.color="red"
        self.evaluation = ""
        self.name=name
        self.top=top
        self.down=down
        self.value= constant*top*down*7 if command is None else command(top, down)
        self.evaluate()
        self.configure(width=290, height=105, border_color="#383838",
                 border_width=2, corner_radius=17, fg_color="#ebebeb", bg_color="white")
        self.setName()

    def setName(self):
        match self.mode:
            case "household":
                topText = 'Hours used per day:'
                bottomText = 'Rated Wattage:'
                topUnit = ""
                bottomUnit = "KWh"
            case "transportation":
                topText = 'Distance travelled per day:'
                bottomText = 'Travel days per week:'
                topUnit = "Km"
                bottomUnit = ""
            case "activities":
                topText = 'Consumed per day:'
                bottomText = ''
                topUnit = ""
                bottomUnit = ""

        textColor = "black"
        colors = {"fg_color":"#ebebeb", "bg_color":"white"}
        CTk.CTkLabel(self,width=188, height=20, font=("Poppins",16,"bold"), text_color=textColor,
                      text=self.name, anchor=CTk.W, **colors).place(x=20,y=15)
        CTk.CTkLabel(self,width=150, height=20, font=("Poppins",16), text_color=textColor,
                      text=topText, anchor=CTk.W, **colors).place(x=20,y=50)
        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color=textColor,
                      text=f'{self.top} {topUnit}', anchor=CTk.W, **colors).place(x=220,y=50)
        CTk.CTkLabel(self,width=150, height=20, font=("Poppins",16), text_color=textColor,
                      text=bottomText, anchor=CTk.W, **colors).place(x=20,y=70)
        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color=textColor,
                      text=f'{self.down} {bottomUnit}', anchor=CTk.W, **colors).place(x=220,y=70)
        CTk.CTkLabel(self,width=50, height=20, font=("Poppins",16, "bold"), text_color="black",
                      text=self.evaluation, anchor=CTk.W, fg_color=self.color,bg_color="#ebebeb", corner_radius=8).place(x=230,y=15)
        
    def evaluate(self):
        good_threshold = 5.0
        average_threshold = 10.0
        high_threshold = 20.0

        emissions = self.value/(7 if self.mode == "household" else 1)
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
    card = Card(master = app, name = "Motorcycle",top=24,down=0.4, mode="transportation")
    card.pack(side=CTk.TOP, anchor=CTk.W)
    Card(master = app, name = "Motorcycle",top=24,down=0.4, mode="household").pack(side=CTk.TOP, anchor=CTk.W)
    Card(master = app, name = "Motorcycle",top=24,down=0.4, mode="activities").pack(side=CTk.TOP, anchor=CTk.W)
    print(card.value)
    print(card.evaluation)
    app.mainloop()