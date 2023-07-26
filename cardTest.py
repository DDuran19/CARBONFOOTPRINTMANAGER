import json
import customtkinter as CTk

from calculations import VEHICLES

with open("activities.json", "r") as file:
    ACTIVITIES = json.load(file)

class Card(CTk.CTkFrame):
    """
    This is designed to be used as a front end.
    this defaults to emission computation for Household appliances.
    Pass down the function to `command` parameter. This will call the function to maually compute for the value.
    """
    
    def __init__(self, name, top, down, exitCommand, mode="household", 
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
