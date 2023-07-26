import json

with open("transportation.json", "r") as file:
    VEHICLES = json.load(file)

        # self.carbonFootprint = CarbonFootprint(KM, L, KGCO2perLperWeek)

class CarbonFootprintCalculator:
    def __init__(
        self,
        household: dict,
        transportations: dict,
        activities: dict,
    ) -> None:
        self.household = household
        self.transportations = transportations
        self.activities = activities

    def get_weekly_emission(self):
        hoursInAWeek = 168
        total_household = 0
        total_transportations = 0
        total_activities = 0

        for value in self.household.values():
            total_household += value[0] 

        for value in self.transportations.values():
            total_transportations += value[0] 
        
        for value in self.activities.values():
            total_activities += value[0] 

        combined_total = total_household + total_transportations + total_activities

        return combined_total * hoursInAWeek

    def get_monthly_emission(self):
        return self.get_weekly_emission() * 4

    def get_yearly_emission(self):
        return self.get_weekly_emission() * 52
