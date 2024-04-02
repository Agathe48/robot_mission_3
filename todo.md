# Todo

- [ ] gérer quand on pose un waste dans la waste disposal zone, qu'il disparaisse : self.grid.remove_agent(agent: Agent)
- [ ] gérer quand on transforme un un déchet et qu'on le pose pour qu'il existe bien
- [x] gérer dans la perception le fait que ce soit une case dans laquelle il ne peut pas aller (pour vert et jaune)
- [ ] corriger ce bug dans l'init des déchets :   File "D:\Data\Agathe\CentraleSupelec\3A\SMA\Projet\robot_mission_3\model.py", line 63, in __init__
    self.init_wastes()
  File "D:\Data\Agathe\CentraleSupelec\3A\SMA\Projet\robot_mission_3\model.py", line 122, in init_wastes
    self.nb_wastes_yellow = rd.randint(
  File "C:\Software\Dev\Python_396\lib\random.py", line 338, in randint
    return self.randrange(a, b+1)
