import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.id_map_artists = {}
        self.popularity = DAO.getPopularities()

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, selected_genre_id):
        self.graph.clear()
        nodes_artists = DAO.getArtistsByGenre(selected_genre_id)
        self.graph.add_nodes_from(nodes_artists)
        self.id_map_artists = {a.ArtistId: a for a in nodes_artists}

        for a1_id, a2_id in DAO.getArtistsBySharedCostumers(selected_genre_id):
            if a1_id in self.id_map_artists and a2_id in self.id_map_artists:
                a1 = self.id_map_artists[a1_id]
                a2 = self.id_map_artists[a2_id]
                pop1 = self.popularity.get(a1_id, 0) # se l'artista non ha venduto, considero 0
                pop2 = self.popularity.get(a2_id, 0)
                weight = pop1 + pop2
                if pop1 > pop2: self.graph.add_edge(a1, a2, weight=weight)
                elif pop1 < pop2: self.graph.add_edge(a2, a1, weight=weight)
                else:
                    self.graph.add_edge(a1, a2, weight=weight)
                    self.graph.add_edge(a2, a1, weight=weight)

        return nodes_artists

    def getGraphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def getMostInfluentialArtist(self):
        best_artist, max_influence = None, -1

        for artist in self.graph.nodes:
            out_weight = sum([data['weight'] for _, _, data in self.graph.out_edges(artist, data=True)])
            in_weight = sum([data['weight'] for _, _, data in self.graph.in_edges(artist, data=True)])
            influence = out_weight - in_weight

            if best_artist is None or influence > max_influence:
                best_artist, max_influence = artist, influence

        return best_artist, max_influence

    def getTop5Edges(self):
        return sorted(self.graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]


if __name__ == '__main__':
    test_model = Model()
    genre_test_id = 1 # rock
    test_model.buildGraph(genre_test_id)
    n_nodes, n_edges = test_model.getGraphDetails()
    print(f"Nodi: {n_nodes} | Archi: {n_edges}")
    # testo: nodi 51, archi 492

    best_art, max_infl = test_model.getMostInfluentialArtist()
    if best_art:
        print(f"\nArtista più influente: {best_art.Name}, con influenza: {max_infl}")
        # testo: U2, influenza 4093

    print("\nTop 5 archi:")
    top_edges = test_model.getTop5Edges()
    for u, v, data in top_edges:
        print(f"{u.Name} -> {v.Name} (peso: {data['weight']})")

    if n_nodes > 0:
        start_node = list(test_model.graph.nodes)[0]
        print(f"Provo a lanciare la ricerca a partire da: {start_node.Name}")

        """
        path = test_model.find_longest_path(start_node)
        print(f"Cammino trovato! Lunghezza: {len(path)} nodi.")
        for p in path:
            print(p.Name)
        """