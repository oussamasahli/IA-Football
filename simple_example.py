from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from footIA.strats  import GoalStrategy, DribleStrategy, FonceurStrategy, MultipurposeStrategy, RandomStrategy
from soccersimulator import SoccerTeam, Simulation, show_simu,KeyboardStrategy,DTreeStrategy,load_jsonz,dump_jsonz
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot
from footIA import MultipurposeStrategy,GoalStrategy,ToolBox,DribleStrategy,DefenseurStrategy
import sklearn
import numpy as np
import pickle
from arbre import my_get_features


dic_strategy = {MultipurposeStrategy().name:MultipurposeStrategy(),GoalStrategy().name:GoalStrategy(),DribleStrategy().name:DribleStrategy(),DefenseurStrategy().name:DefenseurStrategy()}

with open("tree_test.pkl","rb") as f:
        dt = pickle.load(f)
  
treeStrat1 = DTreeStrategy(dt,dic_strategy,my_get_features)
 

## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
control = SoccerTeam(name="controlStratTeam")
pyteam.add("verstile", MultipurposeStrategy())
control.add("control", treeStrat1)

#pyteam.add("dVersatile2", MultipurposeStrategy())
#Creation d'une partie
simu = Simulation(pyteam,control)
#Jouer et afficher la partie
show_simu(simu)
