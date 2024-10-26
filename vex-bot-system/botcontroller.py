
class Controller:

    def __init__(self,vexbot):

        self.bot = vexbot

        #V = self.Kp * (theta(t)-theta(t-1)) + self.Kd * (theta(t))
        self.Kp = 0.1
        self.Kd = 0.1
        self.Ki = 0.1

        self.target = 0 #the target angle you want the bot to reach

        #self.theta = 0

        self.previous_step = self.bot.gyro
        self.current_step = self.bot.gyro
        self.advanced_step = self.target
        self.all_steps = 0

    def updateMotors(self):

        self.previous_step = self.current_step
        self.current_step = self.target - self.bot.gyro
        self.advanced_step = self.target
        self.all_steps += self.current_step

        dV =(self.Kp * (self.current_step) 
           + self.Ki * (self.all_steps) 
           + self.Kd * (self.current_step-self.previous_step))
        
        if dV > 0:
            self.bot.V[0] += (dV)
            self.bot.V[1] -= (dV)
        elif dV < 0:
            self.bot.V[0] += (dV)
            self.bot.V[1] -= (dV)