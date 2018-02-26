from soccersimulator import SoccerTeam
from .strats import *
from .tools import *

def get_team(nb_players):
	myteam = SoccerTeam(name="SebOuss")
	if nb_players == 1:
		myteam.add("Versatile " ,MultipurposeStrategy())
	if nb_players == 2:
		myteam.add("Versatile 1", MultipurposeStrategy())
		myteam.add("Versalite 2", MultipurposeStrategy())
	if nb_players == 4:
		myteam.add("Versatile 1",MultipurposeStrategy())
		myteam.add("Goal",GoalStrategy())
		myteam.add("Versatile 2",MultipurposeStrategy())
		myteam.add("DribleurNaif",DribleStrategy())
	return myteam	

def get_team_challenge(num):
	myteam = SoccerTeam(name="MaTeamChallenge")
	if num == 1:
		myteam.add("Joueur Chal "+str(num),RandomStrategy())
	return myteam
