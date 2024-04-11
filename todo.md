# Todo

- [ ] dans le mouvement, faire en sorte que l'agent vert n'aille pas sur un déchet jaune, que l'agent jaune n'aille pas sur un déchet rouge (à coordonner avec la tache suivante) (sauf last column quand l'agent cherche a drop)  (LATER)
- [x] gérer le cas où la grille n'est pas divisible par 3 (last ou deux last colomne de manière random dans une des trois zone) (dans init grid)  (Oumaima)
- [ ] métriques à définir et datacollector à implémenter (pour avoir des courbes, ex : suivis du nb de déchets) (Agathe Poulain)
- [ ] agent chef, qui hérite des autres classes color_agent et modifier l'init du modèle (Agathe Plu, Laure)
- [x] Changer dans affichages (rond plus, gros) pour le chef  (Agathe Poulain) 
- [ ] communication des agents qui envoient tous leur knowledge pertinente au chef + les chefs de chaque couleur qui se communique les dépots et picked up sur la frontière --> init à -1 dans la grille des déchets (comme case au contenu inconnu)  (Agathe Plu, Laure)
- [ ] mouvement de quadrillage avec sépration de la zone selon le nb d'agent sur la zone  (Agathe Plu, Laure)
- [ ] faire en sorte de drop le déchet dans les cas de fin si impossibilité de faire une paire (green and yellow pas chez le rouge) (Oumaima)

- [ ] la visualisation doit permettre de changer le nb de paramètres sans rentrer dans le code (we do it know)


--> faire des agents chefs de chaque couleur pour coordonner les autres (pas abimé)
--> si chef abimé il previent et un autre devient chef ou election d'un nouveau chef (LATER)

--> savoir quadriller 

--> envoyer la grille des déchets, les picked_up_waste, le transformed waste et si tu drops
--> les chefs communiquent entres eux

--> est-ce qu'on peut drop un déchet : OUI


