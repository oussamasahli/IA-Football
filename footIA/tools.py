from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import SoccerTeam, Strategy, Player, Ball
from soccersimulator.settings import *

import math

class ProxyObj(object):
    def __init__(self,state):
        self._obj = state
    def __getattr__(self,attr):
        return getattr(self._obj,attr)

class ToolBox(ProxyObj):
    
    def __init__(self, state, id_team, id_player):

        super(ToolBox,self).__init__(state)
        self.id_team = id_team
        self.id_player = id_player
    @property
    def myTeam(self):
        return self.id_team
    @property        
    def playerPos(self):
        return self.player_state(self.id_team, self.id_player).position
    @property     
    def ballPos(self):
        return self.ball.position
    @property
    def ballSpeed(self):
        return self.ball.vitesse
    @property
    def vecMyGoal(self):
        target = 0 if self.id_team == 1 else 1
        return Vector2D((target)*GAME_WIDTH, GAME_HEIGHT/2)
    @property
    def vecTheirGoal(self):
        target = 0 if self.id_team == 2 else 1
        return Vector2D((target)*GAME_WIDTH, GAME_HEIGHT/2)
    @property
    def myGoalBall_distance(self):
        return self.ballPos.distance(self.vecMyGoal)
    @property
    def playerBall_distance(self):
        return self.ballPos.distance(self.playerPos)
    @property
    def width(self):
        return GAME_WIDTH
    @property
    def height(self):
        return GAME_HEIGHT
    @property
    def get_opponent(self):
        opp = [self.player_state(idteam, idplayer).position for idteam, idplayer in self.players if idteam != self.id_team]
        return opp
    @property
    def get_mate(self):
        mate = [self.player_state(idteam,idplayer).position for idteam,idplayer in self.players if (idteam == self.id_team)]
        return mate
    @property    
    def mateMostCloseDistance(self):
        mates= self.get_mate
        DistMin = GAME_WIDTH*2
        for mate in mates:
            if self.playerPos!=mate:
                if self.playerPos.distance(mate)<DistMin:
                    DistMin=self.playerPos.distance(mate)
        return DistMin


########################################################################################################
# Boolean Function
########################################################################################################
    @property
    def canShoot(self):
        return self.ballPos.distance(self.playerPos) < PLAYER_RADIUS + BALL_RADIUS
    @property
    def isInGoal(self, norm_acc = None):
    
        coordx= self.playerPos.x
        coordy= self.playerPos.y
        target = 0 if self.id_team == 1 else 1

        if((((target == 0)and (coordx<=5))|
        ((target == 1) and(coordx>145))) 
        and (coordy<=50 and coordy>=40)):
            return True
        else:
            return False   
    @property
    def mateHaveBall(self):
        mate= self.get_mate()
        for players in mate :
            if (players.distance(self.ballPos)<=5):
                return True
        return False
    @property
    def iHaveBall(self):
        if (self.playerPos.distance(self.ballPos)<=5):
            return True
        return False
    @property
    def inCorner(self):
        if (self.id_team == 0):
            if ((self.playerPos.distance(Vector2D(GAME_WIDHT,0).position)<=10) | (self.playerPos().distance(Vector2D(GAME_WIDTH,GAME_HEIGHT).position)<=10)):
                return True
            else:
                return False
        else:
            if ((self.playerPos.distance(Vector2D(0,0).position)<=10) | (self.playerPos().distance(Vector2D(0,GAME_HEIGHT).position)<=10)):
                return True
            else:
                return False
    @property
    def isInAera(self):
        opp = self.get_opponent
        for players in opp:
            if (players.distance(self.PosJoueur)<30):
                return True
        return False


###################################################################
#COMPORTEMENTS
###################################################################

class Comportement(ProxyObj):
    def __init__(self,obj):
        super(Comportement,self).__init__(obj)
    def run(self,p):
        raise(NotImplementedError)
    def go(self,p):
        raise(NotImplementedError)
    def shoot(self):
        raise(NotImplementedError)
    def degage(self):
        raise(NotImplementedError)
    def drible(self):
        raise(NotImplementedError)
    def VecBallPredicted(self):
        raise(NotImplementedError)
    def returnToGial(self):
        raise(NotImplementedError)
    def returnToCamp(self):
        raise(NotImplementedError)
    def passToMostCloseMate(self):
        raise(NotImplementedError)

def get_random_vec():
    return Vector2D.create_random(-1,1)

def get_random_SoccerAction():
    return SoccerAction(get_random_vec(),get_random_vec())
