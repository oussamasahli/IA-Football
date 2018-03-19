from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from footIA.strats  import GoalStrategy, DribleStrategy, FonceurStrategy, MultipurposeStrategy, RandomStrategy


## Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
fonceur = SoccerTeam(name="fonceurStratTeam")
pyteam.add("verstile", MultipurposeStrategy())
fonceur.add("Dribleur", DribleStrategy())

#pyteam.add("dVersatile2", MultipurposeStrategy())
#Creation d'une partie
simu = Simulation(pyteam,fonceur)
#Jouer et afficher la partie
show_simu(simu)
