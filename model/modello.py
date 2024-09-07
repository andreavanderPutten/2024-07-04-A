import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.avvistamenti = DAO.get_all_sightings()
        self.idMap = {}
        self.nodi = []
        for avvistamento in self.avvistamenti :
            self.idMap[avvistamento.id] = avvistamento
        self.cammino_ottimo = []
        self.score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)

    def creaGrafo(self,anno,forma):
        for avvistamento in self.avvistamenti :
            if avvistamento.shape == forma and avvistamento.datetime.year == anno :
                self.grafo.add_node(avvistamento)
                self.nodi.append(avvistamento)

        archi = DAO.getArchi(anno,forma,self.idMap)
        for arco in archi :
            self.grafo.add_edge(arco[0],arco[1])

    def getNumeroDeboli(self):
        deboli = nx.weakly_connected_components(self.grafo)
        lista = list(deboli)
        return len(lista)
    def getStrongest(self):
        strongest = nx.weakly_connected_components(self.grafo)
        lista = list(strongest)
        lista.sort(key=lambda x : len(x), reverse=True)

        return lista[0]
    def cammino_ottimoo(self):
        self.cammino_ottimo = 0
        self.score_ottimo = 0
        self._occorrenze_mese = dict.fromkeys(range(1, 13), 0)
        for nodo in self.nodi :
            self._occorrenze_mese[nodo.datetime.month] += 1
            successivi_durata_crescente = self.calcola_successivi(nodo)
            self.ricorsione([nodo],successivi_durata_crescente)
            self._occorrenze_mese[nodo.datetime.month] -= 1
        return self.cammino_ottimo, self.score_ottimo
    def ricorsione(self,parziale : list[Sighting],successivi : list[Sighting]):
        if len(successivi) == 0 :
            score = self.calcola_score(parziale)
            if score > self.score_ottimo :
                self.score_ottimo = score
                self.cammino_ottimo = copy.deepcopy(parziale)
            else :
                for nodo in successivi :
                    parziale.append(nodo)
                    self._occorrenze_mese[nodo.datetime.month] += 1
                    nuovi_succ = self.calcola_successivi(nodo)
                    self.ricorsione(nodo,nuovi_succ)
                    self._occorrenze_mese[parziale[-1].datetime.month] -= 1
                    parziale.pop()


    def calcola_score(self,cammino : list[Sighting]):
        score = 100*len(cammino)
        for i in range(1,len(cammino)) :
            if cammino[i].datetime.month == cammino[i-1].datetime.month :
                score += 200
        return score

    def calcola_successivi(self,nodo : Sighting):
        successivi = self.grafo.neighbors(nodo)
        successivi_buoni = []
        for s in successivi :
            if s.duration > nodo.duration and self._occorrenze_mese[s.datetime.month] < 3 :
                successivi_buoni.append(s)
        return successivi_buoni
    def grafoDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)