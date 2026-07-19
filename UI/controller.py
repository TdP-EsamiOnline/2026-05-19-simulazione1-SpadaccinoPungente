import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillDDGenre(self):
        all_genres = self._model.getAllGenres()
        all_genres_dd_options = [ft.dropdown.Option(key=str(g.GenreId), text=g.Name, data=g) for g in all_genres]
        self._view._ddGenre.options = all_genres_dd_options
        self._view.update_page()

    def handleCreaGrafo(self, e):
        nodes_artists = self._model.buildGraph(self._view._ddGenre.value)
        n_nodes, n_edges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        if not n_nodes or not n_edges:
            self._view.txt_result.controls.append(ft.Text(value="Errore durante la creazione del grafo.", color="red"))
            return
        self._view._ddArtist.options = [ft.dropdown.Option(key=str(na.ArtistId), text=na.Name, data=na) for na in nodes_artists]
        self._view.txt_result.controls.append(ft.Text(value="Grafo creato correttamente!", color="green"))
        self._view.txt_result.controls.append(ft.Text(value=f"Numero di nodi: {n_nodes}\nNumero di archi: {n_edges}"))
        best_artist, max_influence = self._model.getMostInfluentialArtist()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {best_artist.Name}, con influenza: {max_influence}"))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for e in self._model.getTop5Edges():
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} -> {e[1]}: {e[2]['weight']}"))
        self._view.update_page()

    def handleSelectionArtist(self, e):
        self._view._btnTrovaCammino.disabled = False
        self._view.update_page()

    def handleCammino(self,e):
        pass

