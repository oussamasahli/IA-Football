from footIA.optimization import ParamSearch
from footIA.strats import DribleStrategy, MultipurposeStrategy
from numpy import arange

expe = ParamSearch(strategy1=DribleStrategy(),strategy2=MultipurposeStrategy(),
                   params={'drible': arange(0.5,1,0.15),'run': arange(0.8,1.5,0.1)})
expe.start()
print(expe.get_res())
	



# for all distance [......]:
#    for toutes les puissances : 
		# calculer proba de marquer.
# distance -> (meilleur puis, proba).
