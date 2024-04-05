# Todo

- [ ] dans le mouvement, faire en sorte que l'agent vert n'aille pas sur un déchet jaune, que l'agent jaune n'aille pas sur un déchet rouge (à coordonner avec la tache suivante)
- [ ] donner un mouvement plus intelligent aux agents (quadrillage?)
- [ ] gérer le cas où la grille n'est pas divisible par 3
- [ ] demander si le modèle à le droit de modifier la knowledge de l'agent : NON à mettre dans le percepts et l'agent fait sa propre MAJ
--> position dans une sous clé du percept et new_clé avec action effectuée (et on détaille les conséquences par action dans update)

--> faire des agents chefs de chaque couleur pour coordonner les autres (pas abimé)
--> si chef abimé il previent et un autre devient chef ou election d'un nouveau chef


