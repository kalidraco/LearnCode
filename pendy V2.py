mot_a_deviner = str(input("Entrez le mot a deviner : "))
lettres = []
for lettre in mot_a_deviner:
    lettres.append(lettre)

mot_cacher = ['_' for lettre in mot_a_deviner]
print(mot_cacher)
   

lettres_utilisees = []
chances = 7

while chances > 0:
    entree = input("Entrez une lettre : ")
    print("Mot actuel:", ' '.join(mot_cacher))
    print("Lettres déjà utilisées:", ', '.join(lettres_utilisees))
    print("Chances restantes:", chances)
    
    if len(entree) == 1 and entree in lettres and entree not in lettres_utilisees:
        print("Bonne lettre, continuez !")
        for i in range(len(mot_a_deviner)):
            if mot_a_deviner[i] == entree:
                mot_cacher[i] = entree
                print(mot_cacher)
        if '_' not in mot_cacher:
            print("Félicitations ! Vous avez deviné le mot :", mot_a_deviner)
            break

    elif len(entree) != 1:
        continue

    else:
        chances -= 1
        if chances == 0:
            print("Perdu !")
        lettres_utilisees.append(entree)
        print("Mauvaise réponse, il vous reste", chances, "vies")
        print(mot_cacher)

    

