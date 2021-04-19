class AverageSpeed:
    def __init__(self,distance,time):
        self.distance = distance
        self.time = time
    
    def average_speed(self):
        return (self.distance/self.time)

x = AverageSpeed(100, 2)

y = x.average_speed()

print(f"The average speed = {y} km/h")
