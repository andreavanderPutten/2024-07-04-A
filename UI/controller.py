import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        anno = int(self._view.ddyear.value)
        forma = self._view.ddshape.value
        if anno == None or forma == None :
            self._view.create_alert("Scegliere una forma e un anno prima di creare il grafo")
            return
        self._model.creaGrafo(anno,forma)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi : {self._model.grafoDetails()[0]}, numero di archi : {self._model.grafoDetails()[1]}"))
        numero_deboli = self._model.getNumeroDeboli()
        self._view.txt_result1.controls.append(ft.Text(f"Il numero di componenti debolmente connesse è {numero_deboli}"))
        lista = self._model.getStrongest()
        for elemento in lista :
            self._view.txt_result1.controls.append(ft.Text(elemento))
        self._view.update_page()
    def handle_path(self, e):
        cammino,valore = self._model.cammino_ottimoo()
        self._view.txt_result2.controls.append(ft.Text(f"il cammino ha valore {valore}"))
        for valore in cammino :
            self._view.txt_result2.controls.append(ft.Text(f"{valore}"))

        self._view.update_page()
    def fillDD(self):
        anni = DAO.getAnni()
        self._view.ddyear.options =  list(map(lambda x: ft.dropdown.Option(x), anni))

    def fillDDshape(self,e):
        anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None

        forme = DAO.getForme(anno)
        for forma in forme :
            if forma ==  "" or forma == None :
                forme.remove(forma)
        self._view.ddshape.options = list(map(lambda x: ft.dropdown.Option(x), forme))
        self._view.update_page()






