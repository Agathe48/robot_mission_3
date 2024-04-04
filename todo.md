# Todo

- [x] gérer quand on pose un waste dans la waste disposal zone, qu'il disparaisse : self.grid.remove_agent(agent: Agent)
- [x] gérer quand on transforme un un déchet et qu'on le pose pour qu'il existe bien
- [x] gérer dans la perception le fait que ce soit une case dans laquelle il ne peut pas aller (pour vert et jaune)
- [x] corriger ce bug dans l'init des déchets :   File "D:\Data\Agathe\CentraleSupelec\3A\SMA\Projet\robot_mission_3\model.py", line 63, in __init__
    self.init_wastes()
  File "D:\Data\Agathe\CentraleSupelec\3A\SMA\Projet\robot_mission_3\model.py", line 122, in init_wastes
    self.nb_wastes_yellow = rd.randint(
  File "C:\Software\Dev\Python_396\lib\random.py", line 338, in randint
    return self.randrange(a, b+1)
- [x] dans le mouvement, favoriser la direction où il y a un déchet
- [ ] dans le mouvement, faire en sorte que l'agent vert n'aille pas sur un déchet jaune, que l'agent jaune n'aille pas sur un déchet rouge (à coordonner avec la tache suivante)
- [ ] donner un mouvement plus intelligent aux agents (quadrillage?)
- [ ] gérer le cas où la grille n'est pas divisible par 3
- [ ] demander si le modèle à le droit de modifier la knowledge de l'agent
