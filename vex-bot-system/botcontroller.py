
class Controller:

    def __init__(self,vexbot):

        self.bot = vexbot

        #V = self.Kp * (theta(t)-theta(t-1)) + self.Kd * (theta(t))
        self.Kp = 0.1
        self.Kd = 0.1
        #self.Ki = #the integral can be neglected here

        self.target = 0 #the target angle you want the bot to reach

        #self.theta = 0

        self.previous_step = self.bot.gyro
        self.current_step = self.bot.gyro #the current difference in the voltages of the bot
        self.advanced_step = self.target

    def updateMotors(self):

        self.current_step = self.bot.gyro
        V = self.Kp * (self.current_step-self.previous_step) + self.Kd * self.current_step
        self.previous_step = self.current_step

        if V > 0:
            self.bot.motor[0] -= abs(V)
        elif V < 0:
            self.bot.motor[1] -= abs(V)