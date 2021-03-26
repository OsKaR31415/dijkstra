# -*- coding: utf8 -*-

# Implémentation à partir d'un dictionnaire d'adjacence

class GraphePondere:
    """
        Un graphe pondéré représenté par un dictionnaire d'adjacence,
        où les sommets sur graphe sont les clés du dictionnaire
        les valeurs associées sont des dictionnaires dont les clés sont 
        les sommets adjacents et les valeurs associées les poids des arcs (ou arêtes)
        reliant les sommets.
    """

    def __init__(self):
        self.ordre = 0
        self.adj = {}

    def get_ordre(self):
        return self.ordre

    def ajouter_sommet(self, s):
        if s not in self.adj:
            self.adj[s] = {}
            self.ordre += 1

    def ajouter_arc(self, s1, s2, poids):
        self.ajouter_sommet(s1)
        self.ajouter_sommet(s2)
        self.adj[s1][s2] = poids

    def ajouter_chemin(self, s1, s2, poids):
        self.ajouter_arc(s1, s2, poids)
        self.ajouter_arc(s2, s1, poids)

    def est_lie(self, s1, s2):
        return (s2 in self.adj[s1]) or (s1 in self.adj[s2])

    def voisins(self, s):
        return self.adj[s]

    def sommets(self):
        return (list(self.adj))

g = GraphePondere()
g.ajouter_chemin('A', 'C', 160)
g.ajouter_chemin('A', 'P', 180)
g.ajouter_chemin('C', 'P', 130)
g.ajouter_chemin('C', 'E', 140)
g.ajouter_chemin('C', 'L', 180)
g.ajouter_chemin('E', 'P', 80)
g.ajouter_chemin('E', 'L', 70)
g.ajouter_chemin('E', 'V', 100)
g.ajouter_chemin('L', 'B', 80)
g.ajouter_chemin('L', 'G', 110)
g.ajouter_chemin('L', 'V', 100)
g.ajouter_chemin('V', 'P', 100)
g.ajouter_chemin('V', 'G', 90)
g.ajouter_chemin('B', 'G', 180)

# La fonction dijkstra doit renvoyer avec l'exemple précédent
# un plus chemin pour passer de B à A de 410 km
# avec le chemin ['B', 'L', 'E', 'P', 'A']

def dijkstra(graphe, s1, s2):
    """
        Renvoie le plus court chemin pour passer de s1 à s2
        en utilisant l'algorithme de Dijkstra, 
        ainsi que le poids minimal correspondant
    """
    # sommet en cours
    courant = s1 # nom du sommet
    # +inf pour les sommets non encore visités
    # -inf pour les sommets déjà visités
    i = float('inf') # écriture de i pour +infini
    mi = -float('inf') # écriture de mi pour -infini
    # dictionnaire correspondant à la ligne en cours dans le tableau
    # clé = sommet, valeur = [poids cumulé min, sommet parent]
    sommets = {s1: [0, None]}
    dico = {s: [i, None] for s in graphe.sommets() if s != s1}
    sommets.update(dico)
    while courant != s2:
        pass # à remplacer
    long = min_val
    chemin = []
    # construction du chemin en remontant le dictionnaire sommets
    while courant != s1:
        pass # à remplacer
    return long, chemin

print(dijkstra(g, 'B', 'A'))
# La fonction dijkstra doit renvoyer avec l'exemple précédent
# un plus chemin pour passer de B à A de 410 km
# avec le chemin ['B', 'L', 'E', 'P', 'A']