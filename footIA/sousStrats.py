from soccersimulator import Vector2D, SoccerState, SoccerAction, Ball
from soccersimulator import Strategy
from soccersimulator.settings import *
from .tools import ToolBox, Comportement, ProxyObj
from math import acos 

class Comportements(Comportement):

    RUN_COEF = maxPlayerAcceleration
    GO_COEF = maxPlayerAcceleration/3.
    COEF_DRIBLE= 0.5
    BIG_SHOOT_COEF = 2
    SHOOT_COEF = maxPlayerShoot/3.
    THROW_COEF = 4
    RUN_TEST = 1
    def __init__(self,state):
        super(Comportements,self).__init__(state)

    def angle_tire(self):
	u=self.position_ennemie_plus_proche
	v=self.vecTheirGoal
	scalaire= (u.x*v.x)+(u.y*v.y)
	produit_norme= (u.norm*v.norm)
	cos_angle=(scalaire/produit_norme)
	angle= acos(cos_angle)
	return angle
     
    def esquive(self):
        Vect_ennemi_proche=self.position_ennemie_plus_proche
	   
        new=Vect_ennemi_proche.scale(1.5)
	return SoccerAction( new.normalize())
        
    
    
    def run(self,p):
        return SoccerAction(acceleration=(p-self.playerPos).normalize()*self.RUN_COEF)
    
    def go(self,p):
        return SoccerAction(acceleration=(p-self.playerPos).normalize()*self.GO_COEF)
    
    def shoot(self, acc):
        if self.canShoot:
    		return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*acc)
    	return SoccerAction()

    def bigshoot(self):
    	if self.canShoot:
    		return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*self.BIG_SHOOT_COEF)
    	return SoccerAction()

        
    def degage(self):
        if self.canShoot:
            return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos)*self.THROW_COEF)
        return SoccerAction()

    def drible (self):
        if self.canShoot:
            return SoccerAction(shoot=(self.vecTheirGoal -self.ballPos).normalize()*self.COEF_DRIBLE)
        return SoccerAction()

    def returnToGoal(self):
        return SoccerAction(self.vecMyGoal - self.playerPos) 

    def returnToCamp(self):
        mates = self.get_mate
        nbup=0
        nbdown=0
        
        for mate in mates:
            if mate!=self.playerPos:

                if mate.y > self.height/2:
                    nbup=nbup+1
                
                if mate.y < self.height/2:
                    nbdown=nbdown+1

        if nbup>nbdown:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/4, (self.height*2)/5)
                - self.playerPos).normalize()*self.RUN_COEF)
        if nbdown>nbup:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/4, (self.height*3)/5)
                - self.playerPos).normalize()*self.RUN_COEF)
        else:
            return SoccerAction(acceleration= (Vector2D((self.id_team-1)*self.width/2 + self.width/5, (self.height)/2)
                - self.playerPos).normalize()*self.RUN_COEF)

    def runBallPredicted(self, n=0):
        
        pos_ball = self.ballSpeed
        pos_ball.scale(n)
	pos_ball_2=self.ballPos + pos_ball
	return SoccerAction(pos_ball_2 - self.playerPos)
	
    def runTest(self):
        
        pos_ball = self.ballSpeed
        pos_ball.scale(self.RUN_TEST)
	pos_ball_2=self.ballPos + pos_ball
	return SoccerAction(pos_ball_2 - self.playerPos)
	
        
        


    def passToMostCloseMate(self, coop):
        mates=coop
        numDistMin = GAME_WIDTH
        i=0
        for mate in mates:
            if self.playerPos!=mate:
                if self.playerPos.distance(mate)<numDistMin:
                    numDistMin=i
            i=i+1
        print('************************PASSSSSS************************')
        return SoccerAction((mates[numDistMin]-self.playerPos)*7)


    
class ConditionGoal(ProxyObj):
    def __init__(self,state):
        super(ConditionGoal,self).__init__(state)

    def inGoalZone(self):
        return (self.myGoalBall_distance<75)

    def inGoal(self):
        coordx= self.playerPos.x
        coordy= self.playerPos.y
        target = 0 if self.id_team == 1 else 1

        return ((((target == 0)and (coordx<=10))|
                ((target == 1) and(coordx>140))) 
                and (coordy<=50 and coordy>=40))

class ConditionDribleur(ProxyObj):
    COEF_DISTMIN=45
    COEF_BALL = 0.1
    def __init__(self,state):
        super(ConditionDribleur,self).__init__(state)

    def close_opp(self):
        opp = self.get_opponent
        for players in opp:
            if (self.playerPos.distance(players)<30):
                return True
        return False

    def dribleur_peut_aller_vers_balle(self):
	return self.myGoalBall_distance > 50
	

    def close_ball(self):
        return self.playerPos.distance(self.ballPos)<self.COEF_BALL*self.width

    def close_goal(self):
        return self.playerPos.distance(self.vecTheirGoal)<self.width/2.91

    def proche_goal(self,coeff):
	return self.playerPos.distance(self.vecTheirGoal) < self.width/(coeff)
   
    def ditance_test(self):
	return self.playerPos.distance(self.ballPos) >= 30

    def dist_ennemi_ball(self):
	return self.ennemie_proche_ball >=10

class ConditionAttaque(ProxyObj):
    def __init__(self, state, COEF_DIST=1):
        super(ConditionAttaque,self).__init__(state)
        self.COEF_DIST = COEF_DIST	
    def close_goal(self):
        return self.playerPos.distance(self.vecTheirGoal) < self.width/self.COEF_DIST

    def proche_goal(self,coeff):
	return self.playerPos.distance(self.vecTheirGoal) < self.width/(coeff)

    def fonceur_peut_aller_vers_balle(self):
	return self.myGoalBall_distance > 50
	
   

class ConditionPoly(ProxyObj):
    COEF_SHOOT = 0.3

    def inCamp(self):
        return (((self.myTeam==1) and (self.ballPos.x <= self.width/2))
            | ((self.myTeam==2) and (self.ballPos.x >= self.width/2)))

    def oppCloseBall(self):
        opps= self.get_opponent
        for opp in opps:
            if self.ballPos.distance(opp)<5:
                return True
        return False 
    def close_goal(self):
        return self.playerPos.distance(self.vecTheirGoal)<self.COEF_SHOOT*self.width
        
    def mateHaveBall(self, coop):
        mates=coop
        for mate in mates:
            if mate.distance(self.ballPos)< 50:
                return True
        return False

    def canPass(self):
        if self.mateMostCloseDistance < 50:
            return True
        else:
            return False


def fonceur(I):
    
        if not I.canShoot:
            return I.run(I.ballPos)
        else:
            if I.proche_goal(2.4):
               return I.shoot(5.0)
            else:
                return I.drible()
    


   
def versatile (I):
    mates= I.get_mate
    if I.inCamp():
            if not I.canShoot:
                return I.runBallPredicted(14)
            else:
                return I.degage()
    else:
        if not I.mateHaveBall(mates):
            if I.oppCloseBall():
                return I.returnToCamp()
            else:
                if not I.canShoot:
                    return I.run(I.ballPos)
                else:

                    if I.close_goal():
                        return I.shoot(4)
                    return I.shoot(0.64)
        else: 
            return I.returnToCamp()

def dribleur(I):

    if I.dist_ennemi_ball() :
	if not I.proche_goal(2.4): 
	   if I.canShoot:
	      return I.shoot(0.5)
           else:
	      
	          return I.runBallPredicted(5)
	else:
            if I.canShoot:
               return I.shoot(5.0)
            else:
                
               return I.runBallPredicted(5) 
  

 

def goal(I):
    if I.inGoalZone():
        if I.canShoot:
               return I.degage()
        else:
            return I.runBallPredicted(4)
    else:
        if not I.inGoal():
            return I.returnToGoal()
        else:
            return None

