from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from footIA.strats  import GoalStrategy, DribleStrategy, FonceurStrategy, MultipurposeStrategy, RandomStrategy, DefStrategy, AttStrategy
 

## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
drible = SoccerTeam(name="dribleTeam")

drible.add("polyvalentr",DefStrategy())
pyteam.add("defenseur",DefStrategy())
drible.add("polyvalent2",FonceurStrategy())
pyteam.add("attaquant",AttStrategy())

#Creation d'une partie
simu = Simulation(pyteam,drible)
#Jouer et afficher la partie
show_simu(simu)
