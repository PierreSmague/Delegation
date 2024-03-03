import random
import time

from functions import *
from donnees import *
from competitions import *
from pygame.locals import *

largeur_fenetre, hauteur_fenetre = 1500, 1000

athletes_today = []

##### Initialisation affichage #####
pygame.init()
pygame.font.init()
pygame.key.set_repeat(500, 150)

fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
first_init = 1
test = False

##### Lancement du jeu #####

while dict_ecrans["ecran_accueil"]:

    if first_init:
        display_new_game = 0
        active = False
        text = ''
        flag_chosen = 0
        first_init = 0

    # Gestion de la position du curseur
    pos_curseur = pygame.mouse.get_pos()

    # Fond
    fenetre.blit(fond_accueil, (0, 0))

    if not display_new_game:
        box_0 = write(fenetre, "NEW GAME", 750, 680, 'light grey', 50, box=True)
        box_load = write(fenetre, "LOAD LAST GAME", 100, 680, 'light grey', 50, box=True)
    else:
        box_start = write(fenetre, "START GAME", 1200, 50, 'light grey', 40, box=True)
        write(fenetre, "COUNTRY NAME", 105, 58, 'light grey', 25)
        font = pygame.font.Font('fonts/lato.ttf', 36)
        input_box = [100, 100, 500, 50]
        rect_text = pygame.Rect(input_box)
        color_inactive = [0, 0, 0, 60]
        color_active = [0, 0, 0, 150]
        color = color_active if active else color_inactive
        # Blit the input_box rect.
        draw_rect_alpha(fenetre, color, rect_text)
        # Render the current text.
        txt_surface = font.render(text.upper(), True, [220, 220, 220])
        # Blit the text.
        fenetre.blit(txt_surface, (rect_text.x + 5, rect_text.y + 5))

        write(fenetre, "FLAG", 105, 250, 'light grey', 25)
        flags_box = []
        for i in range(len(all_fake_flags)):
            if flag_chosen and i == index_flag:
                blit_alpha(fenetre, all_fake_flags[i], 100 + 320 * (i % 4), 325 + 200 * (i // 4), 255)
            elif flag_chosen and not i == index_flag:
                blit_alpha(fenetre, all_fake_flags[i], 100 + 320 * (i % 4), 325 + 200 * (i // 4), 100)
            else:
                blit_alpha(fenetre, all_fake_flags[i], 100 + 320 * (i % 4), 325 + 200 * (i // 4), 230)
            flags_box.append([100 + 320 * (i % 4), 320 + 320 * (i % 4), 325 + 200 * (i // 4), 489 + 200 * (i // 4)])

    # Rafraichissement de l'écran
    pygame.display.flip()

    # Gestion des évènements
    for event in pygame.event.get():
        # Gestion de la fermeture du jeu
        if not active:
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                dict_ecrans["ecran_accueil"] = 0
        else:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == K_ESCAPE:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        ## Nouvelle partie
        if event.type == MOUSEBUTTONUP:
            races = ["100m", "200m", "400m", "800m", "1500m", "5000m", "10000m", "110mh"]
            if box_0[0] < pos_curseur[0] < box_0[1] and box_0[2] < pos_curseur[1] < box_0[3]:
                display_new_game = 1
                box_0 = [0, 0, 0, 0]
            elif box_load[0] < pos_curseur[0] < box_load[1] and box_load[2] < pos_curseur[1] < box_load[3]:
                # Initialisation de la partie
                facilities_own = [0, 0, 0, 0, 0, 0]
                facilities_max = [10, 10, 5, 10, 10, 10]
                with open('save.pickle', 'rb') as handle:
                    loadfile = pickle.load(handle)
                savefile = loadfile
                own_country = loadfile[0]
                trainers_own = loadfile[1]
                scouts_own = loadfile[2]
                athletes_own = loadfile[3]
                prospects_own = loadfile[4]
                trainers_prospects = loadfile[5]
                scouts_prospects = loadfile[6]
                facilities_own = loadfile[7]
                all_athletes = loadfile[8]
                semaine = loadfile[9]
                annee = loadfile[10]
                launched_training, hired_this_week = loadfile[11][0], loadfile[11][1]
                tournament_achievements = loadfile[12]
                performance_achievements = loadfile[13]
                tournaments = loadfile[14]
                general_achievements = loadfile[15]
                for tournament in tournaments:
                    tournament["contestants"] = [[] for _ in range(len(tournament["epreuves"]))]
                if not test:
                    dict_ecrans["menu_principal"] = 1
                    init = 1
                else:
                    bests = [(x["name"], x["country"]["name"], get_caracs(x)) for x in all_athletes if eval_epreuve(x, "100m") > 90]
                    for athlete in bests:
                        print(athlete)

            elif display_new_game:
                if input_box[0] < pos_curseur[0] < input_box[0] + input_box[2] and input_box[1] < pos_curseur[1] < input_box[1] + input_box[3]:
                    active = True
                elif [i for i in range(len(flags_box)) if flags_box[i][0] < pos_curseur[0] < flags_box[i][1] and flags_box[i][2] < pos_curseur[1] < flags_box[i][3]]:
                    index_flag = [i for i in range(len(flags_box)) if flags_box[i][0] < pos_curseur[0] < flags_box[i][1] and flags_box[i][2] < pos_curseur[1] < flags_box[i][3]][0]
                    flag_chosen = all_fake_flags[index_flag]
                elif box_start[0] < pos_curseur[0] < box_start[1] and box_start[2] < pos_curseur[1] < box_start[3]:
                    # Initialisation de la partie
                    all_athletes = []
                    own_country = [x for x in countries if x["name"] == "Sprintistan"][0]
                    own_country["name"] = text.capitalize()
                    own_country["index_flag"] = index_flag
                    athletes_own, savefile = [], []
                    type_profiles = ["sprinteur", "demi fond", "fond", "lanceur", "sauteur", "perchiste", "hurdler",
                                     "combine"]
                    real_countries = [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]
        
                    rect_to_update = pygame.Rect(100, 400, 1000, 80)
                    for country in real_countries:
                        for athlete in generate_athlete_country(country, 4):
                            all_athletes.append(athlete)
                            fenetre.blit(fond_noir, (0, 0))
                            write(fenetre, f"Generating new athletes : {round((100 * len(all_athletes))/(32 * len(real_countries)), 1)}%", 100,
                                  400, 'light grey', 50)
                            pygame.display.update(rect_to_update)
        
                    trainers_own = [generate_trainer(40)]
                    scouts_own = [generate_scout(40)]
                    trainers_prospects, scouts_prospects = [], []
                    facilities_own = [0, 0, 0, 0, 0, 0]
                    facilities_max = [10, 10, 5, 10, 10, 10]
                    launched_training, hired_this_week = 0, 0
                    own_country["money"] = 25000
                    own_country["prestige"], own_country["hidden_prestige"] = 10, 10
                    own_country["max_people"] = [10, 1, 1]
                    prospects_own = generate_athlete_country(own_country, 6, profile="random")
                    for prospect in prospects_own:
                        prospect["scout"] = scouts_own[0]
                    semaine, annee = 1, 2024
                    for tournament in tournaments:
                        tournament["contestants"] = [[] for _ in range(len(tournament["epreuves"]))]
                    dict_ecrans["menu_principal"] = 1
                    init = 1

    while dict_ecrans["menu_principal"]:

        if init:
            display_quit = 0
            page = 0
            to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
            box_fire = []
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 280, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 280, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 280, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 335, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 350, 15, 1))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)
        box_left = write(fenetre, "<", 300, 255, 'light grey', 20, box=True)
        box_right = write(fenetre, ">", 340, 255, 'light grey', 20, box=True)
        stats = ["AGE", "ACC", "SPD", "REA", "RES", "END", "VER", "STR", "JMP", "THW", "P.VLT", "HRDL"]
        stats_athlete = ["age", "acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force", "technique_saut",
                 "technique_lancer", "technique_perche", "technique_haies"]
        box_fire, box_names = [], []
        box_order_stats = []
        for i in range(len(stats)):
            box_order_stats.append(write(fenetre, stats[i], 500 + 70 * i, 260, 'light grey', 15, box=True))
        for i in range(len(to_display)):
            if i % 2 == 0:
                pygame.draw.rect(fenetre, [20, 20, 20], (290, 295 + 25 * i, 1200, 25))
            if 52 * (annee - to_display[i]["arrival_date"][1]) + (semaine - to_display[i]["arrival_date"][0]) >= 8:
                box_names.append(write(fenetre, to_display[i]["name"], 300, 300 + 25 * i, 'light grey', 13, box=True))
            else:
                box_names.append(write(fenetre, to_display[i]["name"], 300, 300 + 25 * i, [0, 171, 240], 13, box=True))
            box_fire.append(write(fenetre, f"Dismiss", 1400, 299 + 25 * i, 'light grey', 15, box=True))
            for j in range(len(stats)):
                stat_athlete = to_display[i][stats_athlete[j]]
                if stats_athlete[j] != "age":
                    color_stat_athlete = color_stats(stat_athlete)
                else:
                    color_stat_athlete = "light grey"
                write(fenetre, str(round(stat_athlete)), 505 + 70 * j, 300 + 25 * i, color_stat_athlete, 13)

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_principal"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                    for athlete in athletes_own:
                        athlete["salary"] = eval_salary(athlete)
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif [i for i in range(len(box_fire)) if box_fire[i][0] < pos_curseur[0] < box_fire[i][1] and box_fire[i][2] < pos_curseur[1] < box_fire[i][3]]:
                    index_fire = [i for i in range(len(box_fire)) if box_fire[i][0] < pos_curseur[0] < box_fire[i][1] and box_fire[i][2] < pos_curseur[1] < box_fire[i][3]][0]
                    own_country["money"] -= to_display[index_fire]["salary"]
                    athletes_own.remove(to_display[index_fire])
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif [i for i in range(len(box_names)) if box_names[i][0] < pos_curseur[0] < box_names[i][1] and box_names[i][2] < pos_curseur[1] < box_names[i][3]]:
                    index_name = [i for i in range(len(box_names)) if box_names[i][0] < pos_curseur[0] < box_names[i][1] and box_names[i][2] < pos_curseur[1] < box_names[i][3]][0]
                    athlete_to_observe = to_display[index_name]
                    dict_ecrans["menu_principal"] = 0
                    init = 1
                    dict_ecrans["menu_athlete"] = 1
                elif [x for x in box_order_stats if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                    index_order_stat = [i for i in range(len(box_order_stats)) if box_order_stats[i][0] < pos_curseur[0] < box_order_stats[i][1] and box_order_stats[i][2] < pos_curseur[1] < box_order_stats[i][3]][0]
                    stat_selected = stats_athlete[index_order_stat]
                    if stat_selected == "age":
                        athletes_own.sort(key=lambda a: a[stat_selected])
                    elif stat_selected and stat_selected not in races:
                        athletes_own.sort(key=lambda a: a[stat_selected], reverse=True)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_right[0] < pos_curseur[0] < box_right[1] and box_right[2] < pos_curseur[1] < box_right[3]:
                    page = min(page + 1, len(athletes_own) // 20)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_left[0] < pos_curseur[0] < box_left[1] and box_left[2] < pos_curseur[1] < box_left[3]:
                    page = max(0, page - 1)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    while dict_ecrans["menu_staff"]:

        if init:
            display_quit = 0
            display_trainers = 1
            display_scouts = 0
            display_recruit = 0
            box_hire_trainers, box_hire_scouts, box_fire = [], [], []
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 350, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 350, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 350, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 405, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 420, 15, 1))

        blit_alpha(fenetre, menu_black_trapeze, 325, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 575, 245, 100)
        if display_trainers:
            pygame.draw.rect(fenetre, [226, 121, 0], (388, 278, 125, 2))
        elif display_scouts:
            pygame.draw.rect(fenetre, [226, 121, 0], (638, 278, 125, 2))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)
        trainers_box = write(fenetre, "TRAINERS", 400, 250, 'light grey', 20, box=True)
        scouts_box = write(fenetre, "SCOUTS", 660, 250, 'light grey', 20, box=True)
        if display_trainers:
            box_fire, box_hire = [], []
            stats = ["SPR", "MID", "LON", "THR", "JMP", "P.VT", "HRD"]
            stats_trainer = ["sprint", "middle distance", "long distance", "throwing", "jumping", "pole vault", "hurdles"]
            for i in range(len(stats)):
                write(fenetre, stats[i], 600 + 100 * i, 350, 'light grey', 20)
            for i in range(len(trainers_own)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (290, 405 + 25 * i, 1200, 25))
                write(fenetre, trainers_own[i]["name"], 300, 410 + 25 * i, 'light grey', 13)
                box_fire.append(write(fenetre, f"Dismiss", 1400, 407 + 25 * i, 'light grey', 15, box=True))
                for j in range(len(stats)):
                    write(fenetre, str(trainers_own[i][stats_trainer[j]]), 612 + 100 * j, 410 + 25 * i, 'light grey', 13)
            if trainers_prospects:
                write(fenetre, f"RECRUIT", 300, 750, 'light grey', 25)
                for i in range(len(trainers_prospects)):
                    write(fenetre, trainers_prospects[i]["name"], 300, 800 + 25 * i, 'light grey', 15)
                    box_hire.append(write(fenetre, f"HIRE", 1400, 800 + 25 * i, 'light grey', 17, box=True))
                    for j in range(len(stats)):
                        write(fenetre, str(trainers_prospects[i][stats_trainer[j]]), 612 + 100 * j, 800 + 25 * i, 'light grey', 13)
        elif display_scouts:
            box_fire = []
            stats = ["EVAL LVL", "EVAL POT", "EFFICIENCY", "    FLAIR"]
            stats_scout = ["level_detection", "potential_detection", "efficiency", "flair"]
            for i in range(len(stats)):
                write(fenetre, stats[i], 600 + 150 * i, 350, 'light grey', 20)
            for i in range(len(scouts_own)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (290, 405 + 25 * i, 1200, 25))
                write(fenetre, scouts_own[i]["name"], 300, 410 + 25 * i, 'light grey', 13)
                box_fire.append(write(fenetre, f"Dismiss", 1400, 407 + 25 * i, 'light grey', 15, box=True))
                for j in range(len(stats)):
                    write(fenetre, str(scouts_own[i][stats_scout[j]]), 635 + 150 * j, 410 + 25 * i, 'light grey', 13)
            if scouts_prospects:
                write(fenetre, f"RECRUIT", 300, 750, 'light grey', 25)
                for i in range(len(scouts_prospects)):
                    write(fenetre, scouts_prospects[i]["name"], 300, 800 + 25 * i, 'light grey', 15)
                    box_hire.append(write(fenetre, f"HIRE", 1400, 800 + 25 * i, 'light grey', 17, box=True))
                    for j in range(len(stats)):
                        write(fenetre, str(scouts_prospects[i][stats_scout[j]]), 635 + 150 * j, 800 + 25 * i, 'light grey', 13)
        else:
            box_hire_trainers = []
            box_hire_scouts = []
            write(fenetre, "TRAINERS", 300, 350, 'light grey', 25)
            write(fenetre, "SCOUTS", 300, 550, 'light grey', 25)
            stats_1 = ["SPR", "MID", "LON", "THR", "JMP", "P.VT", "HRD"]
            stats_trainer = ["sprint", "middle distance", "long distance", "throwing", "jumping", "pole vault", "hurdles"]
            stats_2 = ["EVAL LVL", "EVAL POT", "EFFICIENCY", "    FLAIR"]
            stats_scout = ["level_detection", "potential_detection", "efficiency", "flair"]
            for i in range(len(stats_1)):
                write(fenetre, stats_1[i], 600 + 80 * i, 350, 'light grey', 20)
            for i in range(len(stats_2)):
                write(fenetre, stats_2[i], 600 + 150 * i, 550, 'light grey', 20)
            for i in range(len(trainers_prospects)):
                write(fenetre, trainers_prospects[i]["name"], 300, 410 + 25 * i, 'light grey', 15)
                box_hire_trainers.append(write(fenetre, f"HIRE", 1400, 410 + 25 * i, 'light grey', 17, box=True))
                for j in range(len(stats_1)):
                    write(fenetre, str(trainers_prospects[i][stats_trainer[j]]), 612 + 80 * j, 410 + 25 * i, 'light grey', 13)
            for i in range(len(scouts_prospects)):
                write(fenetre, scouts_prospects[i]["name"], 300, 610 + 25 * i, 'light grey', 15)
                box_hire_scouts.append(write(fenetre, f"HIRE", 1400, 610 + 25 * i, 'light grey', 17, box=True))
                for j in range(len(stats_2)):
                    write(fenetre, str(scouts_prospects[i][stats_scout[j]]), 640 + 150 * j, 610 + 25 * i, 'light grey', 17)

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_staff"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_staff"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif [i for i in range(len(box_hire)) if box_hire[i][0] < pos_curseur[0] < box_hire[i][1] and box_hire[i][2] < pos_curseur[1] < box_hire[i][3]]:
                    if display_trainers:
                        if own_country["money"] >= 0 and len(trainers_own) < own_country["max_people"][1]:
                            index_hire = [i for i in range(len(box_hire)) if box_hire[i][0] < pos_curseur[0] < box_hire[i][1] and box_hire[i][2] < pos_curseur[1] < box_hire[i][3]][0]
                            trainers_own.append(trainers_prospects[index_hire].copy())
                            trainers_prospects.pop(index_hire)
                            if general_achievements[3][2] == 0:
                                general_achievements[3][2] = 1
                    elif display_scouts:
                        if own_country["money"] >= 0 and len(scouts_own) < own_country["max_people"][2]:
                            index_hire = [i for i in range(len(box_hire)) if box_hire[i][0] < pos_curseur[0] < box_hire[i][1] and box_hire[i][2] < pos_curseur[1] < box_hire[i][3]][0]
                            scouts_own.append(scouts_prospects[index_hire].copy())
                            scouts_prospects.pop(index_hire)
                            if general_achievements[2][2] == 0:
                                general_achievements[2][2] = 1
                elif [i for i in range(len(box_fire)) if box_fire[i][0] < pos_curseur[0] < box_fire[i][1] and box_fire[i][2] < pos_curseur[1] < box_fire[i][3]]:
                    index_fire = [i for i in range(len(box_fire)) if box_fire[i][0] < pos_curseur[0] < box_fire[i][1] and box_fire[i][2] < pos_curseur[1] < box_fire[i][3]][0]
                    if display_trainers:
                        trainers_own.pop(index_fire)
                    else:
                        scouts_own.pop(index_fire)
                elif trainers_box[0] < pos_curseur[0] < trainers_box[1] and trainers_box[2] < pos_curseur[1] < trainers_box[3]:
                    display_trainers = 1
                    display_scouts = 0
                    display_recruit = 0
                elif scouts_box[0] < pos_curseur[0] < scouts_box[1] and scouts_box[2] < pos_curseur[1] < scouts_box[3]:
                    display_trainers = 0
                    display_scouts = 1
                    display_recruit = 0
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    while dict_ecrans["menu_training"]:

        if init:
            display_quit = 0
            trainer = 0
            session = 0
            athlete_to_train = 0
            page = 0
            to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 420, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 420, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 420, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 475, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 490, 15, 1))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)
        box_training = write(fenetre, "LAUNCH TRAINING", 1100, 850, 'light grey', 40, box=True)
        box_left = write(fenetre, "<", 300, 240, 'light grey', 20, box=True)
        box_right = write(fenetre, ">", 340, 240, 'light grey', 20, box=True)
        stats = ["ACC", "SPD", "REA", "RES", "END", "VER", "STR", "JMP", "THW", "P.VLT", "HRDL"]
        training_options = ["REST", "SPRINT", "MIDDLE DISTANCE", "LONG DISTANCE", "HURDLES", "THROWING", "JUMPING", "POLE VAULT"]
        box_names = []
        for i in range(len(stats)):
            write(fenetre, stats[i], 500 + 50 * i, 270, 'light grey', 15)
        for i in range(len(to_display)):
            if i % 2 == 0:
                pygame.draw.rect(fenetre, [20, 20, 20], (290, 295 + 25 * i, 1200, 25))
            box_names.append(write(fenetre, to_display[i]["name"], 300, 300 + 25 * i, 'light grey', 13, box=True))
            write(fenetre, "" if type(to_display[i]["trainer"]) == str else to_display[i]["trainer"]["name"], 1080, 300 + 25 * i, 'light grey', 13)
            write(fenetre, to_display[i]["session"], 1250, 300 + 25 * i, 'light grey', 13)
            for j in range(len(stats)):
                if not launched_training:
                    write(fenetre, f"+ 0", 500 + 50 * j, 300 + 25 * i, 'light grey', 10)
                else:
                    if to_display[i]['progression'][j] > 0:
                        write(fenetre, f"+{to_display[i]['progression'][j]}", 500 + 50 * j, 300 + 25 * i, 'green', 10)
                        if general_achievements[6][2] == 0 and to_display[i]['progression'][j] >= 0.5:
                            general_achievements[6][2] = 1
                    elif to_display[i]['progression'][j] == -99:
                        write(fenetre, "0.0", 500 + 50 * j, 300 + 25 * i, 'grey', 10)
                    elif to_display[i]['progression'][j] == 0:
                        write(fenetre, "0.0", 500 + 50 * j, 300 + 25 * i, 'light grey', 10)
                    else:
                        write(fenetre, f"{to_display[i]['progression'][j]}", 500 + 50 * j, 300 + 25 * i, 'brown', 10)
        write(fenetre, "TRAINER", 1080, 265, 'light grey', 18)
        trainer_box, session_box = [], []
        if trainer:
            pygame.draw.rect(fenetre, [20, 20, 20], (1080, 300 + 25 * athlete_to_train, 150, 25 * (len(trainers_own) + 1)))
            for i in range(len(trainers_own) + 1):
                if not i:
                    trainer_box.append(write(fenetre, "...", 1080, 300 + 25 * athlete_to_train, 'light grey', 13, box=True))
                else:
                    trainer_box.append(write(fenetre, trainers_own[i-1]["name"], 1080, 300 + 25 * (i + athlete_to_train), 'light grey', 13, box=True))
        write(fenetre, "TRAINING SESSION", 1250, 265, 'light grey', 18)
        if session:
            pygame.draw.rect(fenetre, [20, 20, 20], (1250, 300 + 25 * athlete_to_train, 150, 25 * len(training_options)))
            for i in range(len(training_options)):
                session_box.append(write(fenetre, training_options[i], 1250, 300 + 25 * (i + athlete_to_train), 'light grey', 13, box=True))

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_training"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_training"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif box_right[0] < pos_curseur[0] < box_right[1] and box_right[2] < pos_curseur[1] < box_right[3]:
                    page = min(page + 1, len(athletes_own) // 20)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_left[0] < pos_curseur[0] < box_left[1] and box_left[2] < pos_curseur[1] < box_left[3]:
                    page = max(0, page - 1)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif 1000 < pos_curseur[0] < 1250 and 300 < pos_curseur[1] < max(300 + 25 * len(to_display), 300 + 25 * athlete_to_train + 25 * (1 + len(trainers_own))):
                    if trainer and [x for x in trainer_box if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                        trainer_selected = [i for i in range(len(trainer_box)) if trainer_box[i][0] < pos_curseur[0] < trainer_box[i][1] and trainer_box[i][2] < pos_curseur[1] < trainer_box[i][3]][0]
                        if not trainer_selected:
                            to_display[athlete_to_train]["trainer"] = ""
                        else:
                            to_display[athlete_to_train]["trainer"] = trainers_own[trainer_selected - 1]
                        trainer = 0
                        athlete_to_train = 0
                    elif (pos_curseur[1] - 300) // 25 <= len(to_display):
                        trainer = 1
                        athlete_to_train = (pos_curseur[1] - 300) // 25
                    else:
                        init = 1
                elif 1250 < pos_curseur[0] < 1500 and 300 < pos_curseur[1] < max(300 + 25 * len(to_display), 300 + 25 * athlete_to_train + 25 * len(training_options)):
                    if session and [x for x in session_box if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                        training_selected = [i for i in range(len(session_box)) if session_box[i][0] < pos_curseur[0] < session_box[i][1] and session_box[i][2] < pos_curseur[1] < session_box[i][3]][0]
                        to_display[athlete_to_train]["session"] = training_options[training_selected]
                        session = 0
                        athlete_to_train = 0
                    elif (pos_curseur[1] - 300) // 25 <= len(to_display):
                        session = 1
                        athlete_to_train = (pos_curseur[1] - 300) // 25
                    else:
                        init = 1
                elif [i for i in range(len(box_names)) if box_names[i][0] < pos_curseur[0] < box_names[i][1] and box_names[i][2] < pos_curseur[1] < box_names[i][3]]:
                    index_name = [i for i in range(len(box_names)) if box_names[i][0] < pos_curseur[0] < box_names[i][1] and box_names[i][2] < pos_curseur[1] < box_names[i][3]][0]
                    athlete_to_observe = to_display[index_name]
                    dict_ecrans["menu_training"] = 0
                    init = 2
                    dict_ecrans["menu_athlete"] = 1
                elif box_training[0] < pos_curseur[0] < box_training[1] and box_training[2] < pos_curseur[1] < box_training[3] and not launched_training:
                    for athlete in athletes_own:
                        athlete = training_athlete(athlete, athlete["session"], installs=facilities_own[0])
                    launched_training = 1
                    if general_achievements[4][2] == 0:
                        general_achievements[4][2] = 1
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    while dict_ecrans["menu_tournaments"]:

        if init:
            display_quit = 0
            page = 0
            to_come = sorted([x for x in tournaments if x["semaine"] >= semaine and not x["over"]], key=lambda a: a["semaine"])
            to_display = to_come[10 * page: min(len(to_come) - 10 * page, 10 * (page + 1))].copy()
            init = 0


        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 490, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 490, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 490, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 545, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 560, 15, 1))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)

        box_left = write(fenetre, "<", 300, 250, 'light grey', 30, box=True)
        box_right = write(fenetre, ">", 340, 250, 'light grey', 30, box=True)
        write(fenetre, "WEEK", 575, 250, 'light grey', 25)
        write(fenetre, "CAT", 685, 250, 'light grey', 25)
        write(fenetre, "EVENTS", 800, 250, 'light grey', 25)
        write(fenetre, "PARTICIPATION", 1200, 250, 'light grey', 25)
        tournament_box = []
        for i in range(len(to_display)):
            if i % 2 == 0:
                pygame.draw.rect(fenetre, [20, 20, 20], (290, 340 + 50 * i, 1200, 50))
            write(fenetre, f"{to_display[i]['name']}", 300, 350 + 50 * i, 'light grey', 20)
            write(fenetre, f"{to_display[i]['semaine']}", 600, 350 + 50 * i, 'light grey', 20)
            write(fenetre, f"{to_display[i]['category']}", 700, 350 + 50 * i, 'light grey', 20)
            write(fenetre, f"{to_display[i]['tag']}", 800, 350 + 50 * i, 'light grey', 20)
            if semaine == to_display[i]['semaine']:
                tournament_box.append(write(fenetre, "GO !", 1200, 350 + 50 * i, 'orange', 20, box=True))
            else:
                write(fenetre, "NOT YET", 1200, 350 + 50 * i, 'light grey', 20)

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_tournaments"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)
                to_come = sorted([x for x in tournaments if x["semaine"] >= semaine and not x["over"]], key=lambda a: a["semaine"])
                to_display = to_come[10 * page: min(len(to_come) - 10 * page, 10 * (page + 1))].copy()

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_0[0] < pos_curseur[0] < box_0[1] and box_0[2] < pos_curseur[1] < box_0[3]:
                    dict_ecrans["menu_tournaments"] = 0
                elif box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif box_right[0] < pos_curseur[0] < box_right[1] and box_right[2] < pos_curseur[1] < box_right[3]:
                    page = min(page + 1, len(to_come) // 10)
                    to_display = to_come[10 * page: min(len(to_come), 10 * (page + 1))].copy()
                elif box_left[0] < pos_curseur[0] < box_left[1] and box_left[2] < pos_curseur[1] < box_left[3]:
                    page = max(0, page - 1)
                    to_display = to_come[10 * page: min(len(to_come), 10 * (page + 1))].copy()
                elif [x for x in tournament_box if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                    index_tournament = [i for i in range(len(tournament_box)) if tournament_box[i][0] < pos_curseur[0] < tournament_box[i][1] and tournament_box[i][2] < pos_curseur[1] < tournament_box[i][3]][0]
                    tournament_selected = to_come[index_tournament]
                    dict_ecrans["menu_tournaments"] = 0
                    init = 1
                    dict_ecrans["menu_inscriptions"] = 1
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    while dict_ecrans["menu_facilities"]:

        if init:
            display_quit = 0
            page = 0
            box_left = [0, 0, 0, 0, 0, 0]
            box_right = [0, 0, 0, 0, 0, 0]
            init = 0


        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 560, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 560, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 560, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 615, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 630, 15, 1))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)

        write(fenetre, "TRAINING CENTRE", 350, 280, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[0]}", 350, 330, 'light grey', 15)
        box_right[0] = write(fenetre, "+", 410, 330, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {10000 + 20000 * facilities_own[0]} €", 350, 360, 'light grey', 15)
        write(fenetre, f"Training bonus : +{5*facilities_own[0]}%", 350, 400, 'light grey', 20)
        
        write(fenetre, "MEDICAL CENTRE", 950, 280, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[1]}", 950, 330, 'light grey', 15)
        box_right[1] = write(fenetre, "+", 1010, 330, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {5000 + 15000 * facilities_own[1]} €", 950, 360, 'light grey', 15)
        write(fenetre, f"Recuperation bonus : +{5 * facilities_own[1]}%", 950, 400, 'light grey', 20)

        write(fenetre, "DETECTION CENTRE", 350, 480, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[2]}", 350, 530, 'light grey', 15)
        box_right[2] = write(fenetre, "+", 410, 530, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {20000 + 40000 * facilities_own[2]} €", 350, 560, 'light grey', 15)
        write(fenetre, f"Nb max scouts : {1 + facilities_own[2]}", 350, 600, 'light grey', 20)
        
        write(fenetre, "TECHNICAL CENTRE", 950, 480, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[3]}", 950, 530, 'light grey', 15)
        box_right[3] = write(fenetre, "+", 1010, 530, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {10000 + 20000 * facilities_own[3]} €", 950, 560, 'light grey', 15)
        write(fenetre, f"Nb max trainers : {1 + facilities_own[3]}", 950, 600, 'light grey', 20)
        
        write(fenetre, "RESIDENCES", 350, 680, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[4]}", 350, 730, 'light grey', 15)
        box_right[4] = write(fenetre, "+", 410, 730, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {15000 + 25000 * facilities_own[4]} €", 350, 760, 'light grey', 15)
        write(fenetre, f"Nb max athletes : {10 + 7 * facilities_own[4]}", 350, 800, 'light grey', 20)
        
        write(fenetre, "MERCHANDISING", 950, 680, 'light grey', 30)
        write(fenetre, f"Lvl {facilities_own[5]}", 950, 730, 'light grey', 15)
        box_right[5] = write(fenetre, "+", 1010, 730, 'light grey', 20, box=True)
        write(fenetre, f"Cost : {4 * max(0, -5000 + 10000 * (facilities_own[5] + 1))} €", 950, 760, 'light grey', 15)
        write(fenetre, f"Weekly income : {max(0, -5000 + 10000 * facilities_own[5])}€", 950, 800, 'light grey', 20)

        own_country["max_people"] = [10 + 7 * facilities_own[4], 1 + facilities_own[3], 1 + facilities_own[2]]

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_facilities"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_facilities"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif [i for i in range(len(box_right)) if box_right[i][0] < pos_curseur[0] < box_right[i][1] and box_right[i][2] < pos_curseur[1] < box_right[i][3]]:
                    index_facility = [i for i in range(len(box_right)) if box_right[i][0] < pos_curseur[0] < box_right[i][1] and box_right[i][2] < pos_curseur[1] < box_right[i][3]][0]
                    if index_facility == 0:
                        cost = 10000 + 20000 * facilities_own[0]
                    elif index_facility == 1:
                        cost = 5000 + 15000 * facilities_own[1]
                    elif index_facility == 2:
                        cost = 20000 + 40000 * facilities_own[2]
                    elif index_facility == 3:
                        cost = 10000 + 20000 * facilities_own[3]
                    elif index_facility == 4:
                        cost = 15000 + 25000 * facilities_own[4]
                    elif index_facility == 5:
                        cost = 4 * max(0, -5000 + 10000 * (facilities_own[5] + 1))
                    if facilities_own[index_facility] < facilities_max[index_facility] and own_country["money"] >= cost:
                        own_country["money"] -= cost
                        facilities_own[index_facility] += 1
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    
    while dict_ecrans["menu_scouting"]:

        if init:
            display_quit = 0
            display_prospects = 1
            display_scouts = 0
            display_talents = 0
            box_upgrade = [0, 0, 0, 0, 0, 0, 0, 0]
            profile_box = []
            choose_profile = 0
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 630, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 630, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 630, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 685, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 700, 15, 1))

        blit_alpha(fenetre, menu_black_trapeze, 325, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 575, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 825, 245, 100)
        if display_prospects:
            pygame.draw.rect(fenetre, [226, 121, 0], (388, 278, 125, 2))
        elif display_talents:
            pygame.draw.rect(fenetre, [226, 121, 0], (638, 278, 125, 2))
        else:
            pygame.draw.rect(fenetre, [226, 121, 0], (888, 278, 125, 2))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)

        prospects_box = write(fenetre, "NEW PROSPECTS", 370, 250, 'light grey', 20, box=True)
        talents_box = write(fenetre, "PROSPECT QUALITY", 605, 250, 'light grey', 20, box=True)
        scouts_box = write(fenetre, "POLICIES", 905, 250, 'light grey', 20, box=True)
        if display_prospects:
            stats = ["AGE", "SPR", "MID", "LON", "THR", "JMP", "P.VT", "HRD"]
            stats_trainer = ["sprinteur", "demi fond", "fond", "lanceur", "sauteur", "perchiste", "hurdler"]
            write(fenetre, "DETECTED BY", 1100, 330, 'light grey', 20)
            write(fenetre, "SALARY", 1270, 330, 'light grey', 20)
            write(fenetre, "(p/week)", 1270, 355, 'light grey', 12)
            for i in range(len(stats)):
                write(fenetre, stats[i], 500 + 75 * i, 330, 'light grey', 20)
            box_hire = []
            for i in range(len(prospects_own)):
                write(fenetre, prospects_own[i]["name"], 300, 400 + 40 * i, 'light grey', 15)
                write(fenetre, str(prospects_own[i]["age"]), 500, 400 + 40 * i, 'light grey', 15)
                write(fenetre, prospects_own[i]["scout"]["name"], 1100, 400 + 40 * i, 'light grey', 13)
                box_hire.append(write(fenetre, f"HIRE", 1400, 400 + 40 * i, 'light grey', 20, box=True))
                if not prospects_own[i]["detection_level"]:
                    prospects_own[i]["detection_level"] = eval_potentiel(prospects_own[i], scout=prospects_own[i]["scout"])
                    prospects_own[i]["detection_potentiel_level"] = eval_potentiel(prospects_own[i], pot=True, scout=prospects_own[i]["scout"])
                    prospects_own[i]["salary"] = eval_salary(prospects_own[i], scout=True)
                    for key in prospects_own[i]["detection_potentiel_level"]:
                        prospects_own[i]["detection_potentiel_level"][key] = max(prospects_own[i]["detection_potentiel_level"][key], prospects_own[i]["detection_level"][key])
                write(fenetre, str(prospects_own[i]["salary"]), 1270, 400 + 40 * i, 'light grey', 15)
                for j in range(len(stats_trainer)):
                    write(fenetre, f"{str(round(prospects_own[i]['detection_level'][stats_trainer[j]]))} ({str(round(prospects_own[i]['detection_potentiel_level'][stats_trainer[j]]))})", 580 + 75 * j, 400 + 40 * i, 'light grey', 13)
        elif display_talents:
            stats_country = ["sprinteur", "demi fond", "fond", "lanceur", "sauteur", "perchiste", "hurdler", "combine"]
            for i in range(len(stats_country)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (290, 385 + 60 * i, 1200, 60))
                for j in range(own_country[stats_country[i]] - 10, 80):
                    blit_alpha(fenetre, menu_black_progress, 460 + 10 * j, 403 + 60 * i, 250)
                for j in range(0, own_country[stats_country[i]] - 10):
                    blit_alpha(fenetre, menu_orange_progress, 460 + 10 * j, 403 + 60 * i, 250)
                write(fenetre, stats_country[i].capitalize(), 300, 400 + 60 * i, 'light grey', 20)
                write(fenetre, str(own_country[stats_country[i]]), 420, 400 + 60 * i, 'light grey', 20)
                box_upgrade[i] = write(fenetre, "+", 1280, 393 + 60 * i, 'light grey', 30, box=True)
                cost_talent = str(10 * (1 + round((math.pow(1.25 * (own_country[stats_country[i]] - 9), 2)/10))))
                write(fenetre, "   " * (5 - len(cost_talent)) + cost_talent, 1360, 400 + 60 * i, 'light grey', 20)
                blit_alpha(fenetre, menu_prestige_icon, 1430, 396 + 60 * i, 240)
        else:
            profile_box = []
            stats = ["EVAL LVL", "EVAL POT", "EFFICIENCY", "    FLAIR"]
            stats_scout = ["level_detection", "potential_detection", "efficiency", "flair"]
            type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
            for i in range(len(stats)):
                write(fenetre, stats[i], 600 + 150 * i, 350, 'light grey', 20)
            write(fenetre, "MAIN FOCUS", 1250, 350, 'light grey', 20)
            for i in range(len(scouts_own)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (290, 405 + 25 * i, 1200, 25))
                write(fenetre, scouts_own[i]["name"], 300, 410 + 25 * i, 'light grey', 13)
                for j in range(len(stats)):
                    write(fenetre, str(scouts_own[i][stats_scout[j]]), 640 + 150 * j, 410 + 25 * i, 'light grey', 13)
                if not choose_profile:
                    profile_box.append(write(fenetre, scouts_own[i]["profile"].capitalize(), 1250, 408 + 25 * i, 'light grey', 15, box=True))
                else:
                    write(fenetre, scouts_own[i]["profile"].capitalize(), 1250, 408 + 25 * i, 'light grey', 15)
            if choose_profile:
                pygame.draw.rect(fenetre, [20, 20, 20], (1245, 408 + 25 * index_scout, 150, 25 * len(type_profiles)))
                for i in range(len(type_profiles)):
                    profile_box.append(write(fenetre, type_profiles[i].capitalize(), 1250, 408 + 25 * (index_scout + i), 'light grey', 15, box=True))

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_scouting"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)

            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_7[0] < pos_curseur[0] < box_7[1] and box_7[2] < pos_curseur[1] < box_7[3]:
                    dict_ecrans["menu_scouting"] = 0
                    init = 1
                    dict_ecrans["menu_informations"] = 1
                elif box_upgrade != [0, 0, 0, 0, 0, 0, 0, 0] and [i for i in range(len(box_upgrade)) if box_upgrade[i][0] < pos_curseur[0] < box_upgrade[i][1] and box_upgrade[i][2] < pos_curseur[1] < box_upgrade[i][3]]:
                    index_upgrade = [i for i in range(len(box_upgrade)) if box_upgrade[i][0] < pos_curseur[0] < box_upgrade[i][1] and box_upgrade[i][2] < pos_curseur[1] < box_upgrade[i][3]][0]
                    if own_country[stats_country[index_upgrade]] == 90:
                        pass
                    else:
                        cost_upgrade = 10 * (1 + round((math.pow(1.25 * (own_country[stats_country[index_upgrade]] - 9), 2)/10)))
                        if cost_upgrade <= own_country["prestige"]:
                            own_country[stats_country[index_upgrade]] += 1
                            own_country["prestige"] -= cost_upgrade
                        else:
                            pass
                elif [i for i in range(len(profile_box)) if profile_box[i][0] < pos_curseur[0] < profile_box[i][1] and profile_box[i][2] < pos_curseur[1] < profile_box[i][3]]:
                    index_scout = [i for i in range(len(profile_box)) if profile_box[i][0] < pos_curseur[0] < profile_box[i][1] and profile_box[i][2] < pos_curseur[1] < profile_box[i][3]][0]
                    if choose_profile:
                        scout_selected["profile"] = type_profiles[index_scout]
                        choose_profile = 0
                    else:
                        scout_selected = scouts_own[index_scout]
                        choose_profile = 1
                elif [i for i in range(len(box_hire)) if box_hire[i][0] < pos_curseur[0] < box_hire[i][1] and box_hire[i][2] < pos_curseur[1] < box_hire[i][3]]:
                    index_hire = [i for i in range(len(box_hire)) if box_hire[i][0] < pos_curseur[0] < box_hire[i][1] and box_hire[i][2] < pos_curseur[1] < box_hire[i][3]][0]
                    if own_country["money"] >= prospects_own[index_hire]["salary"] and len(athletes_own) < own_country["max_people"][0]:
                        prospects_own[index_hire]["arrival_date"] = [semaine, annee]
                        athletes_own.append(prospects_own[index_hire].copy())
                        own_country["money"] -= prospects_own[index_hire]["salary"]
                        prospects_own.pop(index_hire)
                        hired_this_week += 1
                        if general_achievements[7][2] == 0 and hired_this_week >= 2 and not (semaine == 1 and annee == 2024):
                            general_achievements[7][2] = 1
                        if general_achievements[0][2] == 0:
                            general_achievements[0][2] = 1
                        if general_achievements[8][2] == 0 and len(athletes_own) >= 5:
                            general_achievements[8][2] = 1
                        if general_achievements[9][2] == 0 and len(athletes_own) >= 10:
                            general_achievements[9][2] = 1
                        if general_achievements[10][2] == 0 and len(athletes_own) >= 20:
                            general_achievements[10][2] = 1
                        if general_achievements[11][2] == 0 and len(athletes_own) >= 40:
                            general_achievements[11][2] = 1
                elif prospects_box[0] < pos_curseur[0] < prospects_box[1] and prospects_box[2] < pos_curseur[1] < prospects_box[3]:
                    display_prospects = 1
                    display_scouts = 0
                    display_talents = 0
                elif scouts_box[0] < pos_curseur[0] < scouts_box[1] and scouts_box[2] < pos_curseur[1] < scouts_box[3]:
                    display_prospects = 0
                    display_scouts = 1
                    display_talents = 0
                elif talents_box[0] < pos_curseur[0] < talents_box[1] and talents_box[2] < pos_curseur[1] < talents_box[3]:
                    display_prospects = 0
                    display_scouts = 0
                    display_talents = 1
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    
    while dict_ecrans["menu_informations"]:

        if init:
            display_quit = 0
            display_general = 1
            display_records = 0
            display_finances = 0
            display_exploits = 0
            display_general_2 = 1
            display_tournaments_2 = 0
            display_performances_2 = 0
            display_exploits_2 = 0
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_principal, 250, 0, 50)
        blit_alpha(fenetre, all_fake_flags[own_country["index_flag"]], 300, 20, 200)
        blit_alpha(fenetre, menu_left_side_bar, 0, 0, 100)

        # Chevrons menu sélectionné
        blit_alpha(fenetre, menu_black_rectangle, 3, 700, 150)
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 700, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (3, 700, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (249, 755, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (235, 770, 15, 1))

        blit_alpha(fenetre, menu_black_trapeze, 325, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 575, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 825, 245, 100)
        blit_alpha(fenetre, menu_black_trapeze, 1075, 245, 100)
        if display_general:
            pygame.draw.rect(fenetre, [226, 121, 0], (388, 278, 125, 2))
        elif display_records:
            pygame.draw.rect(fenetre, [226, 121, 0], (638, 278, 125, 2))
        elif display_finances:
            pygame.draw.rect(fenetre, [226, 121, 0], (888, 278, 125, 2))
        else:
            pygame.draw.rect(fenetre, [226, 121, 0], (1138, 278, 125, 2))

        blit_alpha(fenetre, menu_save_icon, 20, 50, 240)
        blit_alpha(fenetre, menu_white_arrow, 1450, 30, 240)
        blit_alpha(fenetre, menu_squad_icon, 26, 290, 220)
        blit_alpha(fenetre, menu_staff_icon, 22, 372, 240)
        blit_alpha(fenetre, menu_training_icon, 22, 447, 240)
        blit_alpha(fenetre, menu_competitions_icon, 24, 507, 240)
        blit_alpha(fenetre, menu_stadium_icon, 22, 585, 240)
        blit_alpha(fenetre, menu_scouting_icon, 22, 655, 240)
        blit_alpha(fenetre, menu_infos_icon, 24, 722, 240)

        # Texte
        box_save = write(fenetre, "Save  Game", 75, 55, 'light grey', 28, box=True)
        if savefile:
            write(fenetre, f"(Last save : {savefile[9]}/{savefile[10]})", 75, 90, 'light grey', 15)
        write(fenetre, own_country["name"], 560, 20, 'light grey', 30)
        blit_alpha(fenetre, menu_prestige_icon, 555, 133, 240)
        write(fenetre, f"€    {own_country['money']}", 560, 90, 'light grey', 30)
        write(fenetre, f"{own_country['prestige']}", 601, 130, 'light grey', 30)

        # Date et bouton continuer
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        box_continue = write(fenetre, "CONTINUE", 1280, 25, 'light grey', 30, box=True)

        box_1 = write(fenetre, "Athletes", 75, 300, 'light grey', 22, box=True)
        box_2 = write(fenetre, "Staff", 75, 370, 'light grey', 22, box=True)
        if trainers_prospects or scouts_prospects:
            write(fenetre, f"({len(trainers_prospects) + len(scouts_prospects)})", 130, 370, 'light grey', 20)
        box_3 = write(fenetre, "Training", 75, 440, 'light grey', 22, box=True)
        box_4 = write(fenetre, "Competitions", 75, 510, 'light grey', 22, box=True)
        box_5 = write(fenetre, "Facilities", 75, 580, 'light grey', 22, box=True)
        box_6 = write(fenetre, "Scouting", 75, 650, 'light grey', 22, box=True)
        if prospects_own:
            write(fenetre, f"({len(prospects_own)})", 165, 650, 'light grey', 20)
        box_7 = write(fenetre, "Informations", 75, 720, 'light grey', 22, box=True)
        general_box = write(fenetre, "GENERAL", 405, 250, 'light grey', 20, box=True)
        records_box = write(fenetre, "RECORDS", 652, 250, 'light grey', 20, box=True)
        finances_box = write(fenetre, "FINANCES", 902, 250, 'light grey', 20, box=True)
        exploits_box = write(fenetre, "ACHIEVEMENTS", 1125, 250, 'light grey', 20, box=True)
        if display_general:
            pygame.draw.rect(fenetre, [20, 20, 20], (290, 465, 1200, 100))
            pygame.draw.rect(fenetre, [20, 20, 20], (290, 665, 1200, 100))
            write(fenetre, "ACTUAL", 700, 400, 'light grey', 20)
            write(fenetre, "MAX", 1000, 400, 'light grey', 20)
            write(fenetre, "ATHLETES", 300, 500, 'light grey', 20)
            write(fenetre, str(len(athletes_own)), 730, 500, 'light grey', 20)
            write(fenetre, str(own_country["max_people"][0]), 1010, 500, 'light grey', 20)
            write(fenetre, "TRAINERS", 300, 600, 'light grey', 20)
            write(fenetre, str(len(trainers_own)), 730, 600, 'light grey', 20)
            write(fenetre, str(own_country["max_people"][1]), 1010, 600, 'light grey', 20)
            write(fenetre, "SCOUTS", 300, 700, 'light grey', 20)
            write(fenetre, str(len(scouts_own)), 730, 700, 'light grey', 20)
            write(fenetre, str(own_country["max_people"][2]), 1010, 700, 'light grey', 20)
        elif display_records:
            i = 0
            real_countries = [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]
            write(fenetre, "EPREUVE", 300, 320, 'light grey', 22)
            write(fenetre, "RECORD", 500, 320, 'light grey', 22)
            write(fenetre, "ATHLETE", 700, 320, 'light grey', 22)
            write(fenetre, "DATE", 900, 320, 'light grey', 22)
            write(fenetre, "WORLD RANKING", 1150, 320, 'light grey', 22)
            for epreuve in own_country["national_best"]:
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (290, 375 + 35 * i, 1200, 35))
                write(fenetre, epreuve.capitalize(), 300, 380 + 35 * i, 'light grey', 20)
                unit = "s" if epreuve in races else "pts" if epreuve == "decathlon" else "m"
                if unit == "s" and own_country["national_best"][epreuve][0] and own_country["national_best"][epreuve][0] >= 60:
                    minutes, seconds = divmod(own_country["national_best"][epreuve][0], 60)
                    write(fenetre, f"{round(minutes)}:{0 if int(seconds) < 10 else ''}{int(seconds)}:{round(100 * (seconds - int(seconds)))}", 500, 380 + 35 * i, 'light grey', 20)
                    world_rankings = sorted([x["national_best"][epreuve] for x in real_countries])
                    better_countries = [x for x in world_rankings if x < own_country["national_best"][epreuve][0]]
                    country_rank = 1 if not better_countries else len(better_countries) + 1
                elif unit == "s" and own_country["national_best"][epreuve][0]:
                    write(fenetre, str(own_country["national_best"][epreuve][0]) + " " + unit, 500, 380 + 35 * i, 'light grey', 20)
                    world_rankings = sorted([x["national_best"][epreuve] for x in real_countries])
                    better_countries = [x for x in world_rankings if x < own_country["national_best"][epreuve][0]]
                    country_rank = 1 if not better_countries else len(better_countries) + 1
                elif own_country["national_best"][epreuve][0]:
                    write(fenetre, str(own_country["national_best"][epreuve][0]) + " " + unit, 500, 380 + 35 * i, 'light grey', 20)
                    world_rankings = sorted([x["national_best"][epreuve] for x in real_countries])
                    better_countries = [x for x in world_rankings if x > own_country["national_best"][epreuve][0]]
                    country_rank = 1 if not better_countries else len(better_countries) + 1
                write(fenetre, str(own_country["national_best"][epreuve][1]), 700, 380 + 35 * i, 'light grey', 20)
                write(fenetre, own_country["national_best"][epreuve][2], 900, 380 + 35 * i, 'light grey', 20)
                write(fenetre, f"{country_rank}/{len(real_countries) + 1}", 1200, 380 + 35 * i, 'light grey', 20)
                i += 1
        elif display_finances:
            total = 0
            write(fenetre, "EXPENSES", 300, 380, 'light grey', 30)
            write(fenetre, "Athletes", 300, 450, 'light grey', 18)
            write(fenetre, "-" + str(sum([x["salary"] for x in athletes_own])) + " €", 800, 450, 'light grey', 18)
            total -= sum([x["salary"] for x in athletes_own])
            write(fenetre, "---------------------------------------------------------", 300, 480, 'light grey', 20)
            write(fenetre, "INCOME", 300, 505, 'light grey', 30)
            write(fenetre, "Merchandising", 300, 580, 'light grey', 18)
            write(fenetre, "+" + str(max(0, -5000 + 10000 * facilities_own[5])) + " €", 800, 580, 'light grey', 18)
            total += max(0, -5000 + 10000 * facilities_own[5])
            write(fenetre, "Achievements", 300, 610, 'light grey', 18)
            write(fenetre, "+" + str(sum([x[1] for x in general_achievements if x[2] == 1])) + " €", 800, 610, 'light grey', 18)
            total += sum([x[1] for x in general_achievements if x[2] == 1])
            write(fenetre, "---------------------------------------------------------", 300, 640, 'light grey', 20)
            write(fenetre, "WEEKLY TOTAL BALANCE", 300, 675, 'light grey', 30)
            write(fenetre, str(total) + " €", 800, 680, 'light grey', 24)
        else:
            blit_alpha(fenetre, menu_tiny_black_trapeze, 325, 315, 100)
            blit_alpha(fenetre, menu_tiny_black_trapeze, 525, 315, 100)
            blit_alpha(fenetre, menu_tiny_black_trapeze, 725, 315, 100)
            blit_alpha(fenetre, menu_tiny_black_trapeze, 925, 315, 100)
            if display_general_2:
                pygame.draw.rect(fenetre, [226, 121, 0], (375, 340, 100, 2))
            elif display_tournaments_2:
                pygame.draw.rect(fenetre, [226, 121, 0], (575, 340, 100, 2))
            elif display_performances_2:
                pygame.draw.rect(fenetre, [226, 121, 0], (775, 340, 100, 2))
            else:
                pygame.draw.rect(fenetre, [226, 121, 0], (975, 340, 100, 2))
            general_box_2 = write(fenetre, "GENERAL", 393, 320, 'light grey', 15, box=True)
            if display_general_2:
                for i in range(len(general_achievements)):
                    if i % 2 == 0:
                        pygame.draw.rect(fenetre, [20, 20, 20], (315, 422 + 25 * i, 1200, 25))
                    if general_achievements[i][2]:
                        blit_alpha(fenetre, menu_orange_tick, 900, 425 + 25 * i, 170)
                        write(fenetre, general_achievements[i][0], 325, 425 + 25 * i, 'orange', 15)
                    else:
                        write(fenetre, general_achievements[i][0], 325, 425 + 25 * i, 'light grey', 15)
                    write(fenetre, f"+{general_achievements[i][1]}€/w", 1100, 425 + 25 * i, 'light grey', 15)
            tournaments_box_2 = write(fenetre, "TOURNAMENTS", 570, 320, 'light grey', 15, box=True)
            if display_tournaments_2:
                for i in range(len(tournament_achievements)):
                    if i % 2 == 0:
                        pygame.draw.rect(fenetre, [20, 20, 20], (315, 422 + 25 * i, 1200, 25))
                    current_step = tournament_achievements[i]
                    if current_step[2] == len(current_step[3]):
                        write(fenetre, current_step[0].replace("??", str(current_step[3][current_step[2] - 1])), 325, 425 + 25 * i, 'orange', 15)
                        write(fenetre, current_step[1].replace("??", str(sum(current_step[4][0:current_step[2]]))), 1100, 425 + 25 * i, 'light grey', 15, box=True)
                    else:
                        write(fenetre, current_step[0].replace("??", str(current_step[3][current_step[2]])), 325, 425 + 25 * i, 'light grey', 15)
                        write(fenetre, current_step[1].replace("??", str(sum(current_step[4][0:current_step[2]]))), 1100, 425 + 25 * i, 'light grey', 15, box=True)
                    for j in range(current_step[2]):
                        blit_alpha(fenetre, menu_orange_tick, 650 + 70 * j, 425 + 25 * i, 170)
                write(fenetre, f"Total bonus : {sum([sum(x[4][0:x[2]]) for x in tournament_achievements])}", 400, 800, 'light grey', 25)
            performances_box_2 = write(fenetre, "PERFORMANCES", 765, 320, 'light grey', 15, box=True)
            if display_performances_2:
                for i in range(len(performance_achievements)):
                    if i % 2 == 0:
                        pygame.draw.rect(fenetre, [20, 20, 20], (315, 422 + 25 * i, 1200, 25))
                    current_step = performance_achievements[i]
                    if current_step[2] == 6:
                        write(fenetre, current_step[0].replace("??", str(current_step[3][min(5, current_step[2])])), 325, 425 + 25 * i, 'orange', 15, box=True)
                        write(fenetre, current_step[1].replace("??", str(sum(current_step[4][0:current_step[2] - 1]))), 1025, 425 + 25 * i, 'light grey', 15, box=True)
                    else:
                        write(fenetre, current_step[0].replace("??", str(current_step[3][min(5, current_step[2])])), 325, 425 + 25 * i, 'light grey', 15, box=True)
                        write(fenetre, current_step[1].replace("??", str(sum(current_step[4][0:current_step[2]]))), 1025, 425 + 25 * i, 'light grey', 15, box=True)
                    for j in range(current_step[2]):
                        blit_alpha(fenetre, menu_orange_tick, 650 + 70 * j, 425 + 25 * i, 170)
                write(fenetre, f"Total bonus : {sum([sum(x[4][0:x[2]]) for x in performance_achievements])}", 400, 900, 'light grey', 25, box=True)
            exploits_box_2 = write(fenetre, "EXPLOITS", 990, 320, 'light grey', 15, box=True)
            if display_exploits_2:
                for i in range(len(exploits_achievements)):
                    if i % 2 == 0:
                        pygame.draw.rect(fenetre, [20, 20, 20], (315, 422 + 25 * i, 1200, 25))
                    if exploits_achievements[i][2]:
                        blit_alpha(fenetre, menu_orange_tick, 900, 425 + 25 * i, 170)
                        write(fenetre, exploits_achievements[i][0], 325, 425 + 25 * i, 'orange', 15)
                    else:
                        write(fenetre, exploits_achievements[i][0], 325, 425 + 25 * i, 'light grey', 15)
                    write(fenetre, exploits_achievements[i][1], 1100, 425 + 25 * i, 'light grey', 15)

        if display_quit:
            draw_rect_alpha(fenetre, [0, 0, 0, 200], (400, 350, 600, 250))
            write(fenetre, "QUIT GAME", 585, 360, 'light grey', 40)
            blit_alpha(fenetre, menu_enter_button, 420, 525, 220)
            blit_alpha(fenetre, menu_escape_button, 840, 525, 220)
            write(fenetre, "YES", 500, 520, 'light grey', 35)
            write(fenetre, "NO", 895, 520, 'light grey', 35)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                display_quit = 1 - display_quit
            elif event.type == KEYUP and event.key == K_RETURN and display_quit:
                dict_ecrans["menu_informations"] = 0
                dict_ecrans["ecran_accueil"] = 0

            if ((event.type == KEYUP and event.key == K_SPACE) or
                    (event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3])):
                if semaine < 52:
                    semaine += 1
                    for athlete in [x for x in athletes_own + all_athletes if x["birthday"] == semaine]:
                        athlete["age"] += 1
                        if athlete["age"] == 37:
                            if athlete in athletes_own:
                                athletes_own.remove(athlete)
                            else:
                                all_athletes.remove(athlete)
                    for athlete in all_athletes:
                        if athlete["age"] < 25:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = min(athlete[stat] + 0.15, athlete["pot_" + stat])
                        elif 33 > athlete["age"] > 29:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.05, athlete["pot_" + stat]))
                        elif athlete["age"] >= 33:
                            for stat in [x for x in all_stats if athlete[x] < athlete["pot_" + x]]:
                                athlete[stat] = max(0, min(athlete[stat] - 0.15, athlete["pot_" + stat]))
                else:
                    semaine = 1
                    annee += 1
                    if annee % 2 == 1:
                        worlds = {
                            "name": "World Championship",
                            "category": "WC",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(worlds)
                    else:
                        try:
                            worlds = [x for x in tournaments if x["category"] == "WC"][0]
                            tournaments.remove(worlds)
                        except:
                            pass
                    if annee % 4 == 0:
                        olympics = {
                            "name": "Olympics",
                            "category": "O",
                            "semaine": 30,
                            "epreuves": all_epreuves,
                            "tag": "All",
                            "over": False
                        }
                        tournaments.append(olympics)
                    else:
                        try:
                            tournaments.remove(olympics)
                        except:
                            pass
                    for country in [x for x in countries if x["name"] != own_country["name"] and x["name"] != "Sprintistan"]:
                        for athlete in generate_athlete_country(country, 1):
                            all_athletes.append(athlete)
                    for tournament in tournaments:
                        tournament["over"] = False
                launched_training, hired_this_week = 0, 0
                if general_achievements[12][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 2) or (annee - x["arrival_date"][1] == 1 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[12][2] = 1
                if general_achievements[13][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 3) or (annee - x["arrival_date"][1] == 2 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[13][2] = 1
                if general_achievements[14][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 6) or (annee - x["arrival_date"][1] == 5 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[14][2] = 1
                if general_achievements[15][2] == 0:
                    if [x for x in athletes_own if (annee - x["arrival_date"][1] >= 11) or (annee - x["arrival_date"][1] == 10 and semaine - x["arrival_date"][0] >= 0)]:
                        general_achievements[15][2] = 1
                own_country["money"] -= sum([x["salary"] for x in athletes_own])
                own_country["money"] += max(0, -5000 + 10000 * facilities_own[5])
                own_country["money"] += sum([x[1] for x in general_achievements if x[2] == 1])
                prospects_own, trainers_prospects, scouts_prospects = [], [], []
                total_scout_bonus = sum([sum(x[4][0:x[2]]) for x in tournament_achievements])
                ## Calcul des perfs
                for achievement in performance_achievements:
                    i = 0
                    if achievement[5] in races:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] < achievement[3][i]:
                            i += 1
                        achievement[2] = i
                    else:
                        while own_country["national_best"][achievement[5]][0] and i < len(achievement[3]) and own_country["national_best"][achievement[5]][0] > achievement[3][i]:
                            i += 1
                        achievement[2] = i
                total_trainer_bonus = sum([sum(x[4][0:x[2]]) for x in performance_achievements])
                for scout in scouts_own:
                    scout["weeks_before_detect"] -= 1
                    if scout["weeks_before_detect"] <= 0:
                        type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
                        scout["weeks_before_detect"] += round(4 + (100 - scout["efficiency"]) / 12.5, 2)
                        if scout["profile"] == "various":
                            new_profile = "random"
                        else:
                            proba_profile = random.uniform(0, 1)
                            if 0.2 + 0.008 * scout["flair"] > proba_profile:
                                new_profile = scout["profile"]
                            else:
                                other_profiles = type_profiles.copy()
                                other_profiles.remove(scout["profile"])
                                new_profile = random.choice(other_profiles)
                        new_prospect = generate_athlete_country(own_country, 1, profile=new_profile)[0]
                        prospects_own.append(new_prospect)
                        new_prospect["scout"] = scout
                proba_new_trainer = random.uniform(0, 1)
                proba_new_scout = random.uniform(0, 1)
                if proba_new_trainer >= 0.75:
                    new_trainer = generate_trainer(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_trainer_bonus, 15))))
                    trainers_prospects.append(new_trainer)
                if proba_new_scout >= 0.75:
                    new_scout = generate_scout(max(0, min(100, np.random.normal(own_country["hidden_prestige"] + total_scout_bonus, 15))))
                    scouts_prospects.append(new_scout)
            ## Nouvelle partie
            elif event.type == MOUSEBUTTONUP:
                if display_exploits:
                    if general_box_2[0] < pos_curseur[0] < general_box_2[1] and general_box_2[2] < pos_curseur[1] < general_box_2[3]:
                        display_general_2 = 1
                        display_tournaments_2 = 0
                        display_performances_2 = 0
                        display_exploits_2 = 0
                    elif tournaments_box_2[0] < pos_curseur[0] < tournaments_box_2[1] and tournaments_box_2[2] < pos_curseur[1] < tournaments_box_2[3]:
                        display_general_2 = 0
                        display_tournaments_2 = 1
                        display_performances_2 = 0
                        display_exploits_2 = 0
                    elif performances_box_2[0] < pos_curseur[0] < performances_box_2[1] and performances_box_2[2] < pos_curseur[1] < performances_box_2[3]:
                        display_general_2 = 0
                        display_tournaments_2 = 0
                        display_performances_2 = 1
                        display_exploits_2 = 0
                    elif exploits_box_2[0] < pos_curseur[0] < exploits_box_2[1] and exploits_box_2[2] < pos_curseur[1] < exploits_box_2[3]:
                        display_general_2 = 0
                        display_tournaments_2 = 0
                        display_performances_2 = 0
                        display_exploits_2 = 1
                if box_1[0] < pos_curseur[0] < box_1[1] and box_1[2] < pos_curseur[1] < box_1[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_principal"] = 1
                elif box_2[0] < pos_curseur[0] < box_2[1] and box_2[2] < pos_curseur[1] < box_2[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_staff"] = 1
                elif box_3[0] < pos_curseur[0] < box_3[1] and box_3[2] < pos_curseur[1] < box_3[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_training"] = 1
                elif box_4[0] < pos_curseur[0] < box_4[1] and box_4[2] < pos_curseur[1] < box_4[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_tournaments"] = 1
                elif box_5[0] < pos_curseur[0] < box_5[1] and box_5[2] < pos_curseur[1] < box_5[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_facilities"] = 1
                elif box_6[0] < pos_curseur[0] < box_6[1] and box_6[2] < pos_curseur[1] < box_6[3]:
                    dict_ecrans["menu_informations"] = 0
                    init = 1
                    dict_ecrans["menu_scouting"] = 1
                elif general_box[0] < pos_curseur[0] < general_box[1] and general_box[2] < pos_curseur[1] < general_box[3]:
                    display_general = 1
                    display_records = 0
                    display_finances = 0
                    display_exploits = 0
                elif records_box[0] < pos_curseur[0] < records_box[1] and records_box[2] < pos_curseur[1] < records_box[3]:
                    display_general = 0
                    display_records = 1
                    display_finances = 0
                    display_exploits = 0
                elif finances_box[0] < pos_curseur[0] < finances_box[1] and finances_box[2] < pos_curseur[1] < finances_box[3]:
                    display_general = 0
                    display_records = 0
                    display_finances = 1
                    display_exploits = 0
                elif exploits_box[0] < pos_curseur[0] < exploits_box[1] and exploits_box[2] < pos_curseur[1] < exploits_box[3]:
                    display_general = 0
                    display_records = 0
                    display_finances = 0
                    display_exploits = 1
                elif box_save[0] < pos_curseur[0] < box_save[1] and box_save[2] < pos_curseur[1] < box_save[3]:
                    savefile = [own_country, trainers_own, scouts_own, athletes_own, prospects_own, trainers_prospects,
                                scouts_prospects, facilities_own, all_athletes, semaine, annee, [launched_training, hired_this_week],
                                tournament_achievements, performance_achievements, tournaments, general_achievements]
                    with open('save.pickle', 'wb') as handle:
                        pickle.dump(savefile, handle, protocol=pickle.HIGHEST_PROTOCOL)

    while dict_ecrans["menu_inscriptions"]:

        if init:
            epreuve_selected = 0
            athlete_selected = 0
            page = 0
            to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_inscriptions, 0, 0, 50)
        fenetre.blit(all_fake_flags[own_country["index_flag"]], (300, 50))

        # Texte
        write(fenetre, own_country["name"], 650, 50, 'light grey', 30)
        write(fenetre, f"Balance  :  {own_country['money']} €", 650, 150, 'light grey', 20)
        write(fenetre, f"Prestige  :  {own_country['prestige']}", 650, 170, 'light grey', 20)
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1090, 18, 15, 1))
        pygame.draw.rect(fenetre, [226, 121, 0], (1229, 58, 1, 15))
        pygame.draw.rect(fenetre, [226, 121, 0], (1215, 73, 15, 1))
        write(fenetre, f"WEEK {semaine}", 1100, 20, 'orange', 25)
        write(fenetre, f"{annee}", 1100, 50, 'orange', 20)
        write(fenetre, "ELIGIBLE ATHLETES", 300, 215, 'light grey', 25)
        write(fenetre, "SELECTION", 1350, 268, 'light grey', 15)
        box_auto = write(fenetre, "AUTO SELECTION", 1200, 200, 'light grey', 30, box=True)
        box_left = write(fenetre, "<", 300, 265, 'light grey', 18, box=True)
        box_right = write(fenetre, ">", 330, 265, 'light grey', 18, box=True)
        box_continue = write(fenetre, "LAUNCH", 1320, 20, 'light grey', 25, box=True)
        box_launch = write(fenetre, "COMPETITION", 1320, 50, 'light grey', 25, box=True)

        box_epreuves = []
        box_order_stats = []
        selection_box = [1370, 1500, 310, 310 + 25 * len(to_display)]
        stats = ["ACC", "SPD", "REA", "RES", "END", "VER", "STR", "JMP", "THW", "P.VLT", "HRDL"]
        stats_athlete = ["acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force",
                         "technique_saut",
                         "technique_lancer", "technique_perche", "technique_haies"]
        for i in range(len(tournament_selected["epreuves"])):
            if epreuve_selected == tournament_selected['epreuves'][i]:
                draw_rect_alpha(fenetre, [0, 0, 0, 150], (40, 45 + 75 * i, 140, 50))
                pygame.draw.rect(fenetre, [226, 121, 0], (40, 45 + 75 * i, 1, 15))
                pygame.draw.rect(fenetre, [226, 121, 0], (40, 45 + 75 * i, 15, 1))
                pygame.draw.rect(fenetre, [226, 121, 0], (180, 80 + 75 * i, 1, 15))
                pygame.draw.rect(fenetre, [226, 121, 0], (166, 94 + 75 * i, 15, 1))
                box_epreuves.append(write(fenetre, f"{tournament_selected['epreuves'][i]}", 50, 50 + 75 * i, 'orange', 25, box=True))
            else:
                box_epreuves.append(write(fenetre, f"{tournament_selected['epreuves'][i]}", 50, 50 + 75 * i, 'light grey', 25, box=True))
        for i in range(len(stats)):
            box_order_stats.append(write(fenetre, stats[i], 500 + 60 * i, 270, 'light grey', 15, box=True))
        box_order_stats.append(write(fenetre, "PB", 1230, 270, 'light grey', 15, box=True))
        for i in range(len(to_display)):
            if i % 2 == 0:
                pygame.draw.rect(fenetre, [20, 20, 20], (290, 305 + 25 * i, 1200, 25))
            write(fenetre, to_display[i]["name"], 300, 310 + 25 * i, 'light grey', 13)
            write(fenetre, to_display[i]["name"], 300, 310 + 25 * i, 'light grey', 13)
            for j in range(len(stats)):
                color_stat_athlete = color_stats(to_display[i][stats_athlete[j]])
                write(fenetre, str(round(to_display[i][stats_athlete[j]])), 503 + 60 * j, 310 + 25 * i, color_stat_athlete, 13)
            if epreuve_selected:
                write(fenetre, str(to_display[i]["personal_best"][epreuve_selected]), 1220, 310 + 25 * i, 'light grey', 13)
                if to_display[i] in tournament_selected["contestants"][index_epreuve]:
                    write(fenetre, "OK", 1375, 310 + 25 * i, 'light grey', 12)
        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                dict_ecrans["menu_inscriptions"] = 0
                init = 1
                dict_ecrans["menu_tournaments"] = 1

            elif event.type == MOUSEBUTTONUP:
                if [x for x in box_epreuves if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                    index_epreuve = [i for i in range(len(box_epreuves)) if box_epreuves[i][0] < pos_curseur[0] < box_epreuves[i][1] and box_epreuves[i][2] < pos_curseur[1] < box_epreuves[i][3]][0]
                    epreuve_selected = tournament_selected['epreuves'][index_epreuve]
                    if tournament_selected["category"] not in  ["E", "WC", "O"]:
                        if epreuve_selected in races:
                            eligible_athletes = [x for x in athletes_own if x["personal_best"][epreuve_selected] and x["personal_best"][epreuve_selected] <= minimas[tournament_selected["category"]][epreuve_selected]]
                        else:
                            eligible_athletes = [x for x in athletes_own if x["personal_best"][epreuve_selected] and x["personal_best"][epreuve_selected] >= minimas[tournament_selected["category"]][epreuve_selected]]
                    else:
                        eligible_athletes = athletes_own
                    if epreuve_selected and epreuve_selected in races:
                        eligible_athletes.sort(key=lambda a: a["personal_best"][epreuve_selected] if a["personal_best"][
                            epreuve_selected] else 100000)
                    elif epreuve_selected and epreuve_selected not in races:
                        eligible_athletes.sort(key=lambda a: a["personal_best"][epreuve_selected] if a["personal_best"][
                            epreuve_selected] else 0, reverse=True)
                    to_display = eligible_athletes[20 * page: min(len(eligible_athletes), 20 * (page + 1))].copy()
                if [x for x in box_order_stats if x[0] < pos_curseur[0] < x[1] and x[2] < pos_curseur[1] < x[3]]:
                    index_order_stat = [i for i in range(len(box_order_stats)) if box_order_stats[i][0] < pos_curseur[0] < box_order_stats[i][1] and box_order_stats[i][2] < pos_curseur[1] < box_order_stats[i][3]][0]
                    if index_order_stat == len(box_order_stats) - 1:
                        if epreuve_selected and epreuve_selected in races:
                            athletes_own.sort(key=lambda a: a["personal_best"][epreuve_selected] if a["personal_best"][epreuve_selected] else 100000)
                        elif epreuve_selected and epreuve_selected not in races:
                            athletes_own.sort(key=lambda a: a["personal_best"][epreuve_selected] if a["personal_best"][epreuve_selected] else 0, reverse=True)
                    else:
                        stat_selected = stats_athlete[index_order_stat]
                        athletes_own.sort(key=lambda a: a[stat_selected], reverse=True)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_auto[0] < pos_curseur[0] < box_auto[1] and box_auto[2] < pos_curseur[1] < box_auto[3]:
                    for i in range(len(tournament_selected["epreuves"])):
                        if not tournament_selected['contestants'][i]:
                            epreuve = tournament_selected['epreuves'][i]
                            if tournament_selected["category"] not in ["E", "WC", "O"]:
                                if epreuve in races:
                                    eligible_athletes = [x for x in athletes_own if x["personal_best"][epreuve] and x["personal_best"][epreuve] <= minimas[tournament_selected["category"]][epreuve]]
                                else:
                                    eligible_athletes = [x for x in athletes_own if x["personal_best"][epreuve] and x["personal_best"][epreuve] >= minimas[tournament_selected["category"]][epreuve]]
                            else:
                                eligible_athletes = athletes_own
                            if eligible_athletes:
                                if epreuve in races:
                                    eligible_athletes.sort(key=lambda a: a["personal_best"][epreuve] if a["personal_best"][epreuve] else 100000)
                                else:
                                    eligible_athletes.sort(key=lambda a: a["personal_best"][epreuve] if a["personal_best"][epreuve] else 0, reverse=True)
                                auto_selection = eligible_athletes[0:min(2, len(eligible_athletes))]
                                for athlete in auto_selection:
                                    tournament_selected['contestants'][i].append(athlete)
                elif selection_box[0] < pos_curseur[0] < selection_box[1] and selection_box[2] < pos_curseur[1] < selection_box[3] and epreuve_selected:
                    athlete_selected = to_display[(pos_curseur[1] - 310) // 25]
                    if athlete_selected in tournament_selected["contestants"][index_epreuve]:
                        tournament_selected["contestants"][index_epreuve].remove(athlete_selected)
                    elif len(tournament_selected["contestants"][index_epreuve]) < 2:
                        tournament_selected["contestants"][index_epreuve].append(athlete_selected)
                    athlete_selected = 0
                elif box_launch[0] < pos_curseur[0] < box_launch[1] and [x for x in tournament_selected["contestants"] if x]:
                    if box_launch[2] < pos_curseur[1] < box_launch[3] or box_continue[2] < pos_curseur[1] < box_continue[3]:
                        dict_ecrans["menu_inscriptions"] = 0
                        init = 1
                        dict_ecrans["menu_race"] = 1
                elif box_right[0] < pos_curseur[0] < box_right[1] and box_right[2] < pos_curseur[1] < box_right[3]:
                    page = min(page + 1, len(athletes_own) // 20)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()
                elif box_left[0] < pos_curseur[0] < box_left[1] and box_left[2] < pos_curseur[1] < box_left[3]:
                    page = max(0, page - 1)
                    to_display = athletes_own[20 * page: min(len(athletes_own), 20 * (page + 1))].copy()

    while dict_ecrans["menu_race"]:

        if init:
            index_selected = [i for i in range(len(tournament_selected["epreuves"])) if tournament_selected["contestants"][i]][0]
            epreuve_selected = tournament_selected["epreuves"][index_selected]
            # current_contestants = tournament_selected["contestants"][index_selected]
            current_contestants = add_contestants(tournament_selected["contestants"][index_selected], all_athletes, epreuve_selected,
                                                  tournament_selected["category"])
            results, box_live = [], [0, 0, 0, 0]
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_endurance, 0, 0, 50)

        # Texte
        write(fenetre, f"{tournament_selected['name']}", 50, 50, 'light grey', 30)
        write(fenetre, f"{epreuve_selected}", 50, 100, 'light grey', 30)
        write(fenetre, f"WEEK {semaine}", 1180, 20, 'light grey', 25)
        write(fenetre, f"{annee}", 1180, 50, 'light grey', 20)
        pygame.draw.rect(fenetre, [220, 220, 220], (90, 238 + 60 * len(current_contestants), 1300, 2))
        pygame.draw.rect(fenetre, [220, 220, 220], (88, 238, 2, 60 * len(current_contestants)))
        pygame.draw.rect(fenetre, [220, 220, 220], (1390, 238, 2, 60 * len(current_contestants)))
        if results:
            for i in range(len(results)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (90, 238 + 60 * i, 1300, 60))
                pygame.draw.rect(fenetre, [220, 220, 220], (90, 238 + 60 * i, 1300, 2))
                unit = "s" if epreuve_selected in races else "pts" if epreuve_selected == "decathlon" else "m"
                if results[i][0]["country"]["name"] == own_country["name"]:
                    color_display = "orange"
                else:
                    color_display = "light grey"
                if results[i][0]["country"]["name"] == own_country["name"]:
                    fenetre.blit(pygame.transform.scale(all_fake_flags[own_country["index_flag"]], (48, 36)), (175, 250 + 60 * i))
                else:
                    fenetre.blit(all_icons_flags[results[i][0]["country"]["name"]], (175, 250 + 60 * i))
                write(fenetre, str(i + 1), 100, 250 + 60 * i, color_display, 30)
                write(fenetre, f"{results[i][0]['name']}", 250, 250 + 60 * i, color_display, 30)
                if unit == "s" and results[i][1] >= 60:
                    minutes, seconds = divmod(results[i][1], 60)
                    write(fenetre, f"{round(minutes)}:{0 if int(seconds) < 10 else ''}{int(seconds)}:{round(100 * (seconds - int(seconds)))}", 650, 250 + 60 * i, color_display, 30)
                else:
                    write(fenetre, f"{results[i][1]} {unit}", 650, 250 + 60 * i, color_display, 30)
                if results[i][0]["personal_best"][epreuve_selected] == results[i][1]:
                    write(fenetre, "PB", 950, 250 + 60 * i, color_display, 30)
                if world_records[epreuve_selected] == results[i][1]:
                    write(fenetre, "WR", 880, 245 + 60 * i, "orange", 35)
                else:
                    if results[i][0]["country"] == own_country:
                        if results[i][0]["country"]["national_best"][epreuve_selected][0] == results[i][1]:
                            write(fenetre, "NR", 900, 250 + 60 * i, color_display, 30)
                    else:
                        if results[i][0]["country"]["national_best"][epreuve_selected] == results[i][1]:
                            write(fenetre, "NR", 900, 250 + 60 * i, color_display, 30)
                if results[i][0]["country"]["name"] == own_country["name"]:
                    write(fenetre, f"+{results[i][2]}€", 1100, 250 + 60 * i, 'light grey', 30)
                    write(fenetre, f"+{results[i][3]}P", 1300, 250 + 60 * i, 'light grey', 30)
            if index_selected == -1:
                box_continue = write(fenetre, "RETURN", 1340, 20, 'light grey', 25, box=True)
                box_launch = write(fenetre, "TO MENU", 1340, 50, 'light grey', 25, box=True)
                tournament_selected["over"] = True
            else:
                box_continue = write(fenetre, "NEXT", 1340, 20, 'light grey', 25, box=True)
                box_launch = write(fenetre, "EVENT", 1340, 50, 'light grey', 25, box=True)
        else:
            stats = ["ACC", "SPD", "REA", "RES", "END", "VER", "STR", "JMP", "THW", "PVLT", "HRD"]
            stats_athlete = ["acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force",
                             "technique_saut", "technique_lancer", "technique_perche", "technique_haies"]
            for i in range(len(stats)):
                write(fenetre, stats[i], 600 + 70 * i, 200, 'light grey', 20)
            for i in range(len(current_contestants)):
                if i % 2 == 0:
                    pygame.draw.rect(fenetre, [20, 20, 20], (90, 238 + 60 * i, 1300, 60))
                pygame.draw.rect(fenetre, [220, 220, 220], (90, 238 + 60 * i, 1300, 2))
                if current_contestants[i]["country"]["name"] == own_country["name"]:
                    color_display = "orange"
                else:
                    color_display = "light grey"
                write(fenetre, str(i + 1), 100, 250 + 60 * i, color_display, 30)
                write(fenetre, f"{current_contestants[i]['name']}", 235, 252 + 60 * i, color_display, 25)
                if current_contestants[i]["country"]["name"] == own_country["name"]:
                    fenetre.blit(pygame.transform.scale(all_fake_flags[own_country["index_flag"]], (48, 36)), (175, 250 + 60 * i))
                else:
                    fenetre.blit(all_icons_flags[current_contestants[i]["country"]["name"]], (175, 250 + 60 * i))
                for j in range(len(stats_athlete)):
                    stat_athlete = current_contestants[i][stats_athlete[j]]
                    color_stat_athlete = color_stats(stat_athlete)
                    write(fenetre, str(round(stat_athlete)), 600 + 70 * j, 255 + 60 * i, color_stat_athlete, 20)
            box_continue = write(fenetre, "QUICK", 1320, 20, 'light grey', 25, box=True)
            box_launch = write(fenetre, "SIMULATION", 1320, 50, 'light grey', 25, box=True)
            if epreuve_selected in ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "longueur", "triplesaut", "javelot", "poids", "disque"]:
                box_live = write(fenetre, "LIVE EVENT", 1320, 150, 'light grey', 25, box=True)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            if (event.type == KEYUP and event.key == K_SPACE) or\
                (event.type == MOUSEBUTTONUP and (box_launch[0] < pos_curseur[0] < box_launch[1] and (box_launch[2] < pos_curseur[1] < box_launch[3] or box_continue[2] < pos_curseur[1] < box_continue[3]))):
                if results:
                    if index_selected == -1:
                        dict_ecrans["menu_race"] = 0
                        init = 1
                        dict_ecrans["menu_principal"] = 1
                    else:
                        init = 1
                else:
                    # current_contestants = add_contestants(current_contestants, all_athletes, epreuve_selected, tournament_selected["category"])
                    if epreuve_selected == "100m":
                        results = cent_metres(current_contestants)
                    elif epreuve_selected == "110mh":
                        results = cent_dix_metres_haies(current_contestants)
                    elif epreuve_selected == "200m":
                        results = deux_cent_metres(current_contestants)
                    elif epreuve_selected == "400m":
                        results = quatre_cent_metres(current_contestants)
                    elif epreuve_selected == "800m":
                        results = huit_cent_metres(current_contestants)
                    elif epreuve_selected == "1500m":
                        results = quinze_cent_metres(current_contestants)
                    elif epreuve_selected == "5000m":
                        results = cinq_mille_metres(current_contestants)
                    elif epreuve_selected == "10000m":
                        results = dix_mille_metres(current_contestants)
                    elif epreuve_selected == "longueur":
                        results = saut_en_longueur(current_contestants)
                    elif epreuve_selected == "triplesaut":
                        results = triple_saut(current_contestants)
                    elif epreuve_selected == "hauteur":
                        results = saut_en_hauteur(current_contestants)
                    elif epreuve_selected == "perche":
                        results = saut_perche(current_contestants)
                    elif epreuve_selected == "poids":
                        results = lancer_poids(current_contestants)
                    elif epreuve_selected == "disque":
                        results = lancer_disque(current_contestants)
                    elif epreuve_selected == "javelot":
                        results = lancer_javelot(current_contestants)
                    elif epreuve_selected == "decathlon":
                        results = decathlon_quick(current_contestants)
                    results = [[current_contestants[i], results[i], 0, 0] for i in range(len(results))]
                    results.sort(key=lambda a: a[1])
                    if epreuve_selected not in races:
                        results.reverse()
                    for i in range(len(results)):
                        if results[i][0]["country"]["name"] == own_country["name"]:
                            rewards = generate_rewards(tournament_selected["category"], i + 1)
                            results[i][2], results[i][3] = rewards
                            own_country["money"] += rewards[0]
                            own_country["prestige"] += rewards[1]
                            if tournament_selected["category"] in tournament_achievements[0][3]:
                                if i <= 3 - tournament_achievements[tournament_achievements[0][3].index(tournament_selected["category"]) + 1][2]:
                                    tournament_achievements[tournament_achievements[0][3].index(tournament_selected["category"]) + 1][2] = 4 - i
                        # Personal Best
                        if epreuve_selected in races and (not results[i][0]["personal_best"][epreuve_selected] or results[i][1] < results[i][0]["personal_best"][epreuve_selected]):
                            results[i][0]["personal_best"][epreuve_selected] = results[i][1]
                        elif epreuve_selected not in races and (not results[i][0]["personal_best"][epreuve_selected] or results[i][1] > results[i][0]["personal_best"][epreuve_selected]):
                            results[i][0]["personal_best"][epreuve_selected] = results[i][1]

                        # National record
                        if results[i][0]["country"]["name"] == own_country["name"]:
                            if epreuve_selected in races and (not own_country["national_best"][epreuve_selected][0] or results[i][1] < own_country["national_best"][epreuve_selected][0]):
                                own_country["national_best"][epreuve_selected][0] = results[i][1]
                                own_country["national_best"][epreuve_selected][1] = results[i][0]["name"]
                                own_country["national_best"][epreuve_selected][2] = f"Week {semaine} - {annee}"
                            elif epreuve_selected not in races and (not own_country["national_best"][epreuve_selected][0] or results[i][1] > own_country["national_best"][epreuve_selected][0]):
                                own_country["national_best"][epreuve_selected][0] = results[i][1]
                                own_country["national_best"][epreuve_selected][1] = results[i][0]["name"]
                                own_country["national_best"][epreuve_selected][2] = f"Week {semaine} - {annee}"
                        else:
                            if epreuve_selected in races and (not results[i][0]["country"]["national_best"][epreuve_selected] or results[i][1] < results[i][0]["country"]["national_best"][epreuve_selected]):
                                results[i][0]["country"]["national_best"][epreuve_selected] = results[i][1]
                            elif epreuve_selected not in races and (not results[i][0]["country"]["national_best"][epreuve_selected] or results[i][1] > results[i][0]["country"]["national_best"][epreuve_selected]):
                                results[i][0]["country"]["national_best"][epreuve_selected] = results[i][1]

                        # World record
                        if epreuve_selected in races and results[i][1] < world_records[epreuve_selected]:
                            world_records[epreuve_selected] = results[i][1]
                        elif epreuve_selected not in races and results[i][1] > world_records[epreuve_selected]:
                            world_records[epreuve_selected] = results[i][1]
                    if general_achievements[1][2] == 0:
                        general_achievements[1][2] = 1
                    if general_achievements[5][2] == 0 and not [x for x in own_country["national_best"].values() if x[0] == ""]:
                        general_achievements[5][2] = 1
                    if tournament_selected["category"] in tournament_achievements[0][3]:
                        if tournament_achievements[0][2] <= tournament_achievements[0][3].index(tournament_selected["category"]):
                            tournament_achievements[0][2] = tournament_achievements[0][3].index(tournament_selected["category"]) + 1
                    tournament_selected["contestants"][index_selected] = []
                    if not [i for i in range(len(tournament_selected["epreuves"])) if tournament_selected["contestants"][i]]:
                        index_selected = -1
            elif event.type == MOUSEBUTTONUP and box_live[0] < pos_curseur[0] < box_live[1] and box_live[2] < pos_curseur[1] < box_live[3]:
                dict_ecrans["menu_race"] = 0
                init = 1
                dict_ecrans["menu_live"] = 1

    while dict_ecrans["menu_live"]:

        if init:
            launch = 0
            if epreuve_selected == "100m":
                results_live = cent_metres(current_contestants, print_race=True)
            elif epreuve_selected == "110mh":
                results_live = cent_dix_metres_haies(current_contestants, print_race=True)
            elif epreuve_selected == "200m":
                results_live = deux_cent_metres(current_contestants, print_race=True)
            elif epreuve_selected == "400m":
                results_live = quatre_cent_metres(current_contestants, print_race=True)
            elif epreuve_selected == "800m":
                results_live = huit_cent_metres(current_contestants, print_race=True)
            elif epreuve_selected == "1500m":
                results_live = quinze_cent_metres(current_contestants, print_race=True)
            elif epreuve_selected == "5000m":
                results_live = cinq_mille_metres(current_contestants, print_race=True)
            elif epreuve_selected == "10000m":
                results_live = dix_mille_metres(current_contestants, print_race=True)
            elif epreuve_selected == "longueur":
                results_live = saut_en_longueur(current_contestants, print_race=True)
            elif epreuve_selected == "triplesaut":
                results_live = triple_saut(current_contestants, print_race=True)
            elif epreuve_selected == "javelot":
                results_live = lancer_javelot(current_contestants, print_race=True)
            elif epreuve_selected == "poids":
                results_live = lancer_poids(current_contestants, print_race=True)
            elif epreuve_selected == "disque":
                results_live = lancer_disque(current_contestants, print_race=True)
            box_continue = [0, 0, 0, 0]
            race_step, temp_step, current_athlete = 0, 0, 0
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_endurance, 0, 0, 50)

        # Texte
        write(fenetre, f"{tournament_selected['name']}", 50, 50, 'light grey', 30)
        write(fenetre, f"{epreuve_selected}", 50, 100, 'light grey', 30)

        box_live = write(fenetre, "LAUNCH EVENT", 700, 150, 'light grey', 25, box=True)
        if race_step == len(results_live[1]) or temp_step == -1:
            box_continue = write(fenetre, "TO RESULTS", 1200, 150, 'light grey', 30, box=True)

        if epreuve_selected in races:
            # Piste
            pygame.draw.rect(fenetre, [200, 75, 60], (300, 250, 1050, 640))
            for i in range(len(current_contestants) + 1):
                pygame.draw.rect(fenetre, [220, 220, 220], (300, 250 + 80 * i, 1050, 2))
                if i != len(current_contestants):
                    pygame.draw.rect(fenetre, [220, 220, 220], (1275, 260 + 80 * i, 2, 60))
            pygame.draw.rect(fenetre, [220, 220, 220], (1350, 250, 2, 640))
        else:
            if epreuve_selected == "javelot":
                pygame.draw.rect(fenetre, [17, 124, 19], (100, 600, 1315, 350))
                pygame.draw.rect(fenetre, [200, 75, 60], (100, 850, 300, 100))
                pygame.draw.rect(fenetre, [220, 220, 220], (400, 950, 1015, 2))
                pygame.draw.rect(fenetre, [220, 220, 220], (100, 850, 300, 2))
                pygame.draw.rect(fenetre, [220, 220, 220], (100, 950, 300, 2))
                pygame.draw.rect(fenetre, [220, 220, 220], (400, 850, 2, 102))
                for i in range(3, 11):
                    pygame.draw.rect(fenetre, [220, 220, 220], (415 + 100 * i, 950, 2, 10))
                    write(fenetre, f"{10 * i}m", 400 + 100 * i, 962, 'light grey', 15)
            elif epreuve_selected in ["poids", "disque"]:
                pygame.draw.rect(fenetre, [17, 124, 19], (200, 600, 1315, 350))
                pygame.draw.circle(fenetre, [200, 75, 60], (300, 850), 98)
                pygame.draw.circle(fenetre, [220, 220, 220], (300, 850), 100, width=2)
                pygame.draw.rect(fenetre, [220, 220, 220], (200, 950, 1315, 2))
                if epreuve_selected == "poids":
                    for i in range(3, 14):
                        pygame.draw.rect(fenetre, [220, 220, 220], (400 + 80 * i, 950, 2, 10))
                        write(fenetre, f"{2 * i}m", 390 + 80 * i, 962, 'light grey', 15)
                else:
                    for i in range(3, 16):
                        pygame.draw.rect(fenetre, [220, 220, 220], (400 + 70 * i, 950, 2, 10))
                        write(fenetre, f"{5 * i}m", 390 + 70 * i, 962, 'light grey', 15)
            elif epreuve_selected in ["longueur", "triplesaut"]:
                # Sautoir
                pygame.draw.rect(fenetre, [200, 75, 60], (100, 735, 600, 100))
                pygame.draw.rect(fenetre, [174, 155, 119], (700, 670, 750, 230))
                pygame.draw.rect(fenetre, [220, 220, 220], (700, 900, 750, 2))
                pygame.draw.rect(fenetre, [220, 220, 220], (100, 735, 600, 2))
                pygame.draw.rect(fenetre, [220, 220, 220], (100, 835, 600, 2))
                if epreuve_selected == "longueur":
                    pygame.draw.rect(fenetre, [220, 220, 220], (700, 735, 2, 102))
                    for i in range(3, 11):
                        pygame.draw.rect(fenetre, [220, 220, 220], (650 + 75 * i, 900, 2, 10))
                        write(fenetre, f"{i}m", 635 + 75 * i, 912, 'light grey', 15)
                else:
                    pygame.draw.rect(fenetre, [220, 220, 220], (350, 735, 2, 102))
                    for i in range(3, 20):
                        pygame.draw.rect(fenetre, [220, 220, 220], (300 + 60 * i, 900, 2, 10))
                        write(fenetre, f"{i}m", 285 + 60 * i, 912, 'light grey', 15)
        silhouettes = []

        # Athlètes
        for i in range(len(current_contestants)):
            if epreuve_selected in races:
                if current_contestants[i]["country"]["name"] == own_country["name"]:
                    fenetre.blit(pygame.transform.scale(all_fake_flags[own_country["index_flag"]], (48, 36)),
                                 (25, 280 + 80 * i))
                else:
                    fenetre.blit(all_icons_flags[current_contestants[i]["country"]["name"]], (25, 280 + 80 * i))
                write(fenetre, f"{current_contestants[i]['name']}", 100, 280 + 80 * i, 'light grey', 20)
                write(fenetre, f"{i + 1}", 1305, 275 + 80 * i, 'light grey', 30)
            else:
                if current_contestants[i]["country"]["name"] == own_country["name"]:
                    fenetre.blit(pygame.transform.scale(all_fake_flags[own_country["index_flag"]], (48, 36)),
                                 (25 + 350 * (i % 4), 250 + 200 * (i // 4)))
                else:
                    fenetre.blit(all_icons_flags[current_contestants[i]["country"]["name"]], (25 + 350 * (i % 4), 250 + 200 * (i // 4)))
                write(fenetre, f"{current_contestants[i]['name']}", 100 + 350 * (i % 4), 250 + 200 * (i // 4), 'light grey', 20)
            if race_step == len(results_live[1]) or temp_step == -1:
                if epreuve_selected in races:
                    write(fenetre, f"{results_live[0][i]}s", 1385, 275 + 80 * i, 'light grey', 20)
                    sorted_results = [results_live[0][i] for i in range(len(current_contestants))].copy()
                    sorted_results = sorted(sorted_results)
                    if results_live[0][i] == sorted_results[0]:
                        fenetre.blit(gold_medal, (1200, 265 + 80 * i))
                    elif results_live[0][i] == sorted_results[1]:
                        fenetre.blit(silver_medal, (1200, 265 + 80 * i))
                    elif results_live[0][i] == sorted_results[2]:
                        fenetre.blit(bronze_medal, (1200, 265 + 80 * i))
                else:
                    write(fenetre, f"{results_live[0][i]}m", 100 + 350 * (i % 4), 310 + 200 * (i // 4), 'light grey', 25)
                    sorted_results = [results_live[0][i] for i in range(len(current_contestants))].copy()
                    sorted_results = sorted(sorted_results, reverse=True)
                    if results_live[0][i] == sorted_results[0]:
                        fenetre.blit(gold_medal, (30 + 350 * (i % 4), 300 + 200 * (i // 4)))
                    elif results_live[0][i] == sorted_results[1]:
                        fenetre.blit(silver_medal, (30 + 350 * (i % 4), 300 + 200 * (i // 4)))
                    elif results_live[0][i] == sorted_results[2]:
                        fenetre.blit(bronze_medal, (30 + 350 * (i % 4), 300 + 200 * (i // 4)))
            if not launch and not race_step == len(results_live[1]):
                if epreuve_selected in races:
                    rect_silhouette = running_silhouette.get_rect()
                    rect_silhouette.topleft = (300, 265 + 80 * i)
                    fenetre.blit(running_silhouette, rect_silhouette)
                    silhouettes.append(rect_silhouette)
        if epreuve_selected not in races:
            if epreuve_selected in ["longueur", "triplesaut"]:
                rect_silhouette = running_silhouette.get_rect()
                rect_silhouette.topleft = (100, 760)
                fenetre.blit(running_silhouette, rect_silhouette)
                silhouettes.append(rect_silhouette)
            elif epreuve_selected == "javelot":
                rect_silhouette = running_silhouette.get_rect()
                rect_silhouette.topleft = (100, 875)
                fenetre.blit(running_silhouette, rect_silhouette)
                silhouettes.append(rect_silhouette)
                rect_javelot = pygame.draw.line(fenetre, [220, 220, 220], (115, 890), (165, 870), width=2)
                silhouettes.append(rect_javelot)
            elif epreuve_selected in ["poids", "disque"]:
                rect_silhouette = running_silhouette.get_rect()
                rect_silhouette.topleft = (250, 843)
                fenetre.blit(running_silhouette, rect_silhouette)
                silhouettes.append(rect_silhouette)
                if epreuve_selected == "poids":
                    rect_poids = pygame.draw.circle(fenetre, [230, 230, 230], (295, 850), 8)
                    silhouettes.append(rect_poids)
                else:
                    rect_disque = pygame.draw.ellipse(fenetre, [230, 230, 230], (290, 850, 20, 5))
                    silhouettes.append(rect_disque)

        while launch:
            silhouettes = []
            if epreuve_selected in races:
                pygame.draw.rect(fenetre, [200, 75, 60], (300, 250, 1050, 640))
                for i in range(len(current_contestants) + 1):
                    pygame.draw.rect(fenetre, [220, 220, 220], (300, 250 + 80 * i, 1050, 2))
                    if i != len(current_contestants):
                        pygame.draw.rect(fenetre, [220, 220, 220], (1275, 260 + 80 * i, 2, 60))
                pygame.draw.rect(fenetre, [220, 220, 220], (1350, 250, 2, 640))
                for i in range(len(current_contestants)):
                    rect_silhouette = running_silhouette.get_rect()
                    if epreuve_selected == "100m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i], 265 + 80 * i)
                    elif epreuve_selected == "110mh":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/1.1, 265 + 80 * i)
                    elif epreuve_selected == "200m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/2, 265 + 80 * i)
                    elif epreuve_selected == "400m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/4, 265 + 80 * i)
                    elif epreuve_selected == "800m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/8, 265 + 80 * i)
                    elif epreuve_selected == "1500m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/15, 265 + 80 * i)
                    elif epreuve_selected == "5000m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/50, 265 + 80 * i)
                    elif epreuve_selected == "10000m":
                        rect_silhouette.topleft = (300 + results_live[1][race_step][i]/100, 265 + 80 * i)
                    fenetre.blit(running_silhouette, rect_silhouette)
                    silhouettes.append(rect_silhouette)
                race_step += 1
                tm.sleep(0.00025)
                if race_step == len(results_live[1]):
                    launch = 0
                pygame.display.update(silhouettes)
            else:
                if epreuve_selected in ["longueur", "triplesaut"]:
                    pygame.draw.rect(fenetre, [200, 75, 60], (100, 735, 600, 100))
                    pygame.draw.rect(fenetre, [174, 155, 119], (700, 670, 750, 230))
                    pygame.draw.rect(fenetre, [220, 220, 220], (700, 900, 750, 2))
                    pygame.draw.rect(fenetre, [220, 220, 220], (100, 735, 600, 2))
                    pygame.draw.rect(fenetre, [220, 220, 220], (100, 835, 600, 2))
                elif epreuve_selected == "javelot":
                    pygame.draw.rect(fenetre, [200, 75, 60], (100, 850, 300, 100))
                    pygame.draw.rect(fenetre, [17, 124, 19], (300, 600, 100, 250))
                    pygame.draw.rect(fenetre, [17, 124, 19], (400, 600, 1015, 350))
                    pygame.draw.rect(fenetre, [220, 220, 220], (400, 950, 1015, 2))
                    pygame.draw.rect(fenetre, [220, 220, 220], (100, 850, 300, 2))
                    pygame.draw.rect(fenetre, [220, 220, 220], (100, 950, 300, 2))
                    pygame.draw.rect(fenetre, [220, 220, 220], (400, 850, 2, 102))
                elif epreuve_selected in ["poids", "disque"]:
                    pygame.draw.rect(fenetre, [17, 124, 19], (200, 600, 1315, 350))
                    pygame.draw.circle(fenetre, [200, 75, 60], (300, 850), 98)
                    pygame.draw.circle(fenetre, [220, 220, 220], (300, 850), 100, width=2)
                if epreuve_selected == "longueur":
                    pygame.draw.rect(fenetre, [220, 220, 220], (700, 735, 2, 102))
                elif epreuve_selected == "triplesaut":
                    pygame.draw.rect(fenetre, [220, 220, 220], (350, 735, 2, 102))
                rect_silhouette = running_silhouette.get_rect()
                if launch == 1:
                    if epreuve_selected == "javelot":
                        athlete_x = 100 + (0.4 + current_contestants[current_athlete]["speed"] / 200) * temp_step
                        rect_silhouette.topleft = (athlete_x, 875)
                        fenetre.blit(running_silhouette, rect_silhouette)
                        silhouettes.append(rect_silhouette)
                        rect_javelot = pygame.draw.line(fenetre, [220, 220, 220], (athlete_x + 15, 890), (athlete_x + 65, 870), width=2)
                        silhouettes.append(rect_javelot)
                    elif epreuve_selected in ["poids", "disque"]:
                        athlete_x = 250 + 0.012 * temp_step
                        rect_silhouette.topleft = (athlete_x, 843)
                        fenetre.blit(running_silhouette, rect_silhouette)
                        silhouettes.append(rect_silhouette)
                        if epreuve_selected == "poids":
                            rect_poids = pygame.draw.circle(fenetre, [230, 230, 230], (athlete_x + 45, 850), 8)
                            silhouettes.append(rect_poids)
                        else:
                            rect_disque = pygame.draw.ellipse(fenetre, [230, 230, 230], (athlete_x + 40, 850, 20, 5))
                            silhouettes.append(rect_disque)
                    else:
                        athlete_x = 100 + (0.8 + current_contestants[current_athlete]["speed"] / 200) * temp_step
                        rect_silhouette.topleft = (athlete_x, 760)
                        fenetre.blit(running_silhouette, rect_silhouette)
                        silhouettes.append(rect_silhouette)
                    temp_step += 1
                    if epreuve_selected == "longueur":
                        if athlete_x >= 650:
                            launch = 2
                            temp_step = 0
                    elif epreuve_selected == "javelot":
                        if athlete_x >= 350:
                            launch = 2
                            temp_step = 0
                    elif epreuve_selected == "poids":
                        if athlete_x >= 355:
                            launch = 2
                            temp_step = 0
                    elif epreuve_selected == "disque":
                        if athlete_x >= 360:
                            launch = 2
                            temp_step = 0
                    else:
                        if athlete_x >= 300:
                            launch = 2
                            temp_step = 0
                else:
                    if epreuve_selected == "longueur":
                        rect_silhouette.topleft = (650 + 75 * results_live[1][current_athlete][race_step][0], 850 - 100 * results_live[1][current_athlete][race_step][1])
                    elif epreuve_selected == "triplesaut":
                        rect_silhouette.topleft = (300 + 60 * results_live[1][current_athlete][race_step][0], 850 - 100 * results_live[1][current_athlete][race_step][1])
                    elif epreuve_selected == "javelot":
                        abs, ord = 365 + 10 * results_live[1][current_athlete][race_step][0], 930 - 20 * results_live[1][current_athlete][race_step][1]
                        rect_silhouette.topleft = (350, 875)
                    elif epreuve_selected == "poids":
                        abs, ord = 400 + 40 * results_live[1][current_athlete][race_step][0], 950 - 56.5 * results_live[1][current_athlete][race_step][1]
                        rect_silhouette.topleft = (355, 843)
                    elif epreuve_selected == "disque":
                        abs, ord = 400 + 14 * results_live[1][current_athlete][race_step][0], 950 - 18 * results_live[1][current_athlete][race_step][1]
                        rect_silhouette.topleft = (355, 843)
                    if race_step != len(results_live[1][current_athlete]) - 1:
                        fenetre.blit(running_silhouette, rect_silhouette)
                        silhouettes.append(rect_silhouette)
                        if epreuve_selected == "javelot":
                            flight_step = results_live[1][current_athlete][race_step][0]/results_live[0][current_athlete]
                            ord_max = ord - 20 * (1 - 2 * flight_step)
                            rect_javelot = pygame.draw.line(fenetre, [220, 220, 220], (abs, ord), (abs + 50, ord_max), width=2)
                            silhouettes.append(rect_javelot)
                        elif epreuve_selected == "poids":
                            rect_poids = pygame.draw.circle(fenetre, [220, 220, 220], (abs, ord), 8)
                            silhouettes.append(rect_poids)
                        elif epreuve_selected == "disque":
                            rect_disque = pygame.draw.ellipse(fenetre, [220, 220, 220], (abs, ord, 20, 5))
                            silhouettes.append(rect_disque)
                    race_step += 1
                if epreuve_selected in ["longueur", "triplesaut"]:
                    tm.sleep(0.007)
                elif epreuve_selected == "javelot":
                    if launch == 1:
                        tm.sleep(0.003)
                    else:
                        tm.sleep(0.001)
                elif epreuve_selected == "poids" and launch == 2:
                    tm.sleep(0.003)
                elif epreuve_selected == "disque" and launch == 2:
                    tm.sleep(0.0015)
                if race_step == len(results_live[1][current_athlete]):
                    current_athlete += 1
                    if current_athlete == 8:
                        launch = 0
                        temp_step = -1
                    else:
                        write(fenetre, f"{results_live[0][current_athlete- 1]}m", 100 + 350 * ((current_athlete- 1) % 4), 310 + 200 * ((current_athlete- 1) // 4), 'light grey', 25)
                        launch = 1
                        temp_step = 0
                        race_step = 0
                        tm.sleep(0.3)
                        pygame.display.flip()
                pygame.display.update(silhouettes)

        # Rafraichissement de l'écran
        if launch:
            pygame.display.update(silhouettes)
        else:
            pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_ESCAPE:
                dict_ecrans["menu_live"] = 0
                init = 1
                dict_ecrans["menu_inscriptions"] = 1
            elif event.type == MOUSEBUTTONUP and box_live[0] < pos_curseur[0] < box_live[1] and box_live[2] < pos_curseur[1] < box_live[3]:
                if race_step != len(results_live[1]):
                    launch = 1
            elif event.type == MOUSEBUTTONUP and box_continue[0] < pos_curseur[0] < box_continue[1] and box_continue[2] < pos_curseur[1] < box_continue[3]:
                if race_step == len(results_live[1]) or temp_step == -1:
                    dict_ecrans["menu_live"] = 0
                    init = 0
                    results = [[current_contestants[i], results_live[0][i], 0, 0] for i in range(len(results_live[0]))]
                    results.sort(key=lambda a: a[1])
                    if epreuve_selected not in races:
                        results.reverse()
                    for i in range(len(results)):
                        if results[i][0]["country"]["name"] == own_country["name"]:
                            rewards = generate_rewards(tournament_selected["category"], i + 1)
                            results[i][2], results[i][3] = rewards
                            own_country["money"] += rewards[0]
                            own_country["prestige"] += rewards[1]
                            try:
                                if i <= 3 - tournament_achievements[tournament_achievements[0][3].index(tournament_selected["category"]) + 1][2]:
                                    tournament_achievements[tournament_achievements[0][3].index(tournament_selected["category"]) + 1][2] = 4 - i
                            except:
                                pass
                        # Personal Best
                        if epreuve_selected in races and (not results[i][0]["personal_best"][epreuve_selected] or results[i][1] < results[i][0]["personal_best"][epreuve_selected]):
                            results[i][0]["personal_best"][epreuve_selected] = results[i][1]
                        elif epreuve_selected not in races and (not results[i][0]["personal_best"][epreuve_selected] or results[i][1] > results[i][0]["personal_best"][epreuve_selected]):
                            results[i][0]["personal_best"][epreuve_selected] = results[i][1]

                        # National record
                        if results[i][0]["country"]["name"] == own_country["name"]:
                            if epreuve_selected in races and (not own_country["national_best"][epreuve_selected][0] or results[i][1] < own_country["national_best"][epreuve_selected][0]):
                                own_country["national_best"][epreuve_selected][0] = results[i][1]
                                own_country["national_best"][epreuve_selected][1] = results[i][0]["name"]
                                own_country["national_best"][epreuve_selected][2] = f"Week {semaine} - {annee}"
                            elif epreuve_selected not in races and (not own_country["national_best"][epreuve_selected][0] or results[i][1] > own_country["national_best"][epreuve_selected][0]):
                                own_country["national_best"][epreuve_selected][0] = results[i][1]
                                own_country["national_best"][epreuve_selected][1] = results[i][0]["name"]
                                own_country["national_best"][epreuve_selected][2] = f"Week {semaine} - {annee}"
                        else:
                            if epreuve_selected in races and (not results[i][0]["country"]["national_best"][epreuve_selected] or results[i][1] < results[i][0]["country"]["national_best"][epreuve_selected]):
                                results[i][0]["country"]["national_best"][epreuve_selected] = results[i][1]
                            elif epreuve_selected not in races and (not results[i][0]["country"]["national_best"][epreuve_selected] or results[i][1] > results[i][0]["country"]["national_best"][epreuve_selected]):
                                results[i][0]["country"]["national_best"][epreuve_selected] = results[i][1]

                        # World record
                        if epreuve_selected in races and results[i][1] < world_records[epreuve_selected]:
                            world_records[epreuve_selected] = results[i][1]
                        elif epreuve_selected not in races and results[i][1] > world_records[epreuve_selected]:
                            world_records[epreuve_selected] = results[i][1]
                    if general_achievements[1][2] == 0:
                        general_achievements[1][2] = 1
                    if general_achievements[5][2] == 0 and not [x for x in own_country["national_best"].values() if x[0] == ""]:
                        general_achievements[5][2] = 1
                    if tournament_achievements[0][2] <= tournament_achievements[0][3].index(tournament_selected["category"]):
                        tournament_achievements[0][2] = tournament_achievements[0][3].index(tournament_selected["category"]) + 1
                    tournament_selected["contestants"][index_selected] = []
                    if not [i for i in range(len(tournament_selected["epreuves"])) if tournament_selected["contestants"][i]]:
                        index_selected = -1
                    dict_ecrans["menu_race"] = 1

    while dict_ecrans["menu_athlete"]:

        if init:
            if init == 2:
                last_screen = "training"
            else:
                last_screen = "principal"
            athlete_selected = athlete_to_observe
            init = 0

        # Gestion de la position du curseur
        pos_curseur = pygame.mouse.get_pos()

        # Images fixes
        fenetre.blit(fond_noir, (0, 0))
        blit_alpha(fenetre, fond_athlete, 0, 0, 50)

        # Texte
        draw_rect_alpha(fenetre, [0, 0, 0, 70], (20, 30, 360, 650))
        write(fenetre, "GENERAL", 30, 40, 'orange', 30)
        write(fenetre, "NAME", 30, 100, 'light grey', 20)
        write(fenetre, athlete_selected['name'].upper(), 30, 125, 'light grey', 35)
        write(fenetre, "COUNTRY", 30, 250, 'light grey', 20)
        if athlete_selected["country"]["name"] == own_country["name"]:
            fenetre.blit(pygame.transform.scale(all_fake_flags[own_country["index_flag"]], (48, 36)), (30, 280))
        else:
            fenetre.blit(all_icons_flags[athlete_selected["country"]["name"]], (30, 280))
        write(fenetre, athlete_selected['country']['name'].upper(), 90, 275, 'light grey', 35)
        write(fenetre, "AGE", 30, 400, 'light grey', 20)
        write(fenetre, str(athlete_selected['age']).upper(), 30, 425, 'light grey', 35)
        write(fenetre, "SALARY", 30, 550, 'light grey', 20)
        write(fenetre, f"{str(athlete_selected['salary']).upper()}€", 30, 575, 'light grey', 35)
        write(fenetre, "(p/week)", 110, 550, 'light grey', 15)

        stats = ["acceleration", "speed", "reaction", "resistance", "endurance", "Verticality", "strength",
                         "jumping technique", "throwing technique", "pole vault technique", "hurdles technique"]
        stats_athlete = ["acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force",
                         "technique_saut", "technique_lancer", "technique_perche", "technique_haies"]

        all_profiles = ["sprinteur", "demi fond", "fond", "hurdler", "lanceur", "sauteur", "perchiste", "combine"]
        eval_actual = eval_potentiel(athlete_selected)
        eval_potential = eval_potentiel(athlete_selected, pot=True)
        eval_actual["combine"] = min(100, eval_actual["combine"] * 1.1)
        eval_potential["combine"] = min(100, eval_potential["combine"] * 1.1)

        draw_rect_alpha(fenetre, [0, 0, 0, 70], (405, 30, 1080, 650))
        write(fenetre, "ATTRIBUTES", 420, 40, 'orange', 30)
        for i in range(len(stats)):
            write(fenetre, stats[i].capitalize(), 420, 100 + 50 * i, 'light grey', 25)
            color_stat = color_stats(athlete_selected[stats_athlete[i]])
            write(fenetre, f"{athlete_selected[stats_athlete[i]]}", 690, 100 + 50 * i, color_stat, 25)

        for i in range(1, 6):
            points = [(1150, 350 + 50 * i), (1150 + 35 * i, 350 + 35 * i), (1150 + 50 * i, 350), (1150 + 35 * i, 350 - 35 * i), (1150, 350 - 50 * i), (1150 - 35 * i, 350 - 35 * i), (1150 - 50 * i, 350), (1150 - 35 * i, 350 + 35 * i)]
            pygame.draw.polygon(fenetre, [220, 220, 220], points, 1)
        points_stats = [(1150, 350 + 2.5 * eval_actual["lanceur"]), (1150 + 1.75 * eval_actual["sauteur"], 350 + 1.75 * eval_actual["sauteur"]),
                        (1150 + 2.5 * eval_actual["perchiste"], 350), (1150 + 1.75 * eval_actual["combine"], 350 - 1.75 * eval_actual["combine"]),
                        (1150, 350 - 2.5 * eval_actual["sprinteur"]), (1150 - 1.75 * eval_actual["demi fond"], 350 - 1.75 * eval_actual["demi fond"]),
                        (1150 - 2.5 * eval_actual["fond"], 350), (1150 - 1.75 * eval_actual["hurdler"], 350 + 1.75 * eval_actual["hurdler"])]
        if 52 * (annee - athlete_selected["arrival_date"][1]) + (semaine - athlete_selected["arrival_date"][0]) >= 8:
            points_potential = [(1150, 350 + 2.5 * eval_potential["lanceur"]), (1150 + 1.75 * eval_potential["sauteur"], 350 + 1.75 * eval_potential["sauteur"]),
                            (1150 + 2.5 * eval_potential["perchiste"], 350), (1150 + 1.75 * eval_potential["combine"], 350 - 1.75 * eval_potential["combine"]),
                            (1150, 350 - 2.5 * eval_potential["sprinteur"]), (1150 - 1.75 * eval_potential["demi fond"], 350 - 1.75 * eval_potential["demi fond"]),
                            (1150 - 2.5 * eval_potential["fond"], 350), (1150 - 1.75 * eval_potential["hurdler"], 350 + 1.75 * eval_potential["hurdler"])]
            draw_polygon_alpha(fenetre, [44, 117, 255, 110], points_potential)
            pygame.draw.polygon(fenetre, [44, 117, 255], points_potential, 1)
        draw_polygon_alpha(fenetre, [226, 121, 0, 160], points_stats)
        pygame.draw.polygon(fenetre, [226, 121, 0], points_stats, 1)
        write(fenetre, "THW", 1118, 610, 'light grey', 30)
        write(fenetre, "JMP", 1335, 515, 'light grey', 30)
        write(fenetre, "P VT", 1415, 335, 'light grey', 30)
        write(fenetre, "COM", 1345, 157, 'light grey', 30)
        write(fenetre, "SPR", 1122, 58, 'light grey', 30)
        write(fenetre, "MID", 895, 157, 'light grey', 30)
        write(fenetre, "LON", 828, 335, 'light grey', 30)
        write(fenetre, "HRDL", 885, 515, 'light grey', 30)

        draw_rect_alpha(fenetre, [220, 220, 220, 240], (0, 690, 1500, 2))

        draw_rect_alpha(fenetre, [0, 0, 0, 70], (20, 712, 1465, 250))
        write(fenetre, "RECORDS", 30, 722, 'orange', 30)
        for i in range(len(all_epreuves)):
            draw_rect_alpha(fenetre, [220, 220, 220, 240], (347 + 350 * (i // 4), 765, 1, 190))
            write(fenetre, all_epreuves[i].capitalize(), 30 + 350 * (i // 4), 770 + 50 * (i % 4), 'light grey', 25)
            unit = "s" if all_epreuves[i] in races else "pts" if all_epreuves[i] == "decathlon" else "m"
            if unit == "s" and athlete_selected["personal_best"][all_epreuves[i]] and athlete_selected["personal_best"][all_epreuves[i]] >= 60:
                minutes, seconds = divmod(athlete_selected["personal_best"][all_epreuves[i]], 60)
                write(fenetre, f"{round(minutes)}:{0 if int(seconds) < 10 else ''}{int(seconds)}:{round(100 * (seconds - int(seconds)))}", 150 + 360 * (i // 4), 770 + 50 * (i % 4), 'light grey', 25)
            elif unit == "s" and athlete_selected["personal_best"][all_epreuves[i]]:
                write(fenetre, str(athlete_selected["personal_best"][all_epreuves[i]]) + " " + unit, 150 + 360 * (i // 4), 770 + 50 * (i % 4), 'light grey', 25)
            elif athlete_selected["personal_best"][all_epreuves[i]]:
                write(fenetre, str(athlete_selected["personal_best"][all_epreuves[i]]) + " " + unit, 150 + 360 * (i // 4), 770 + 50 * (i % 4), 'light grey', 25)

        # Rafraichissement de l'écran
        pygame.display.flip()

        # Gestion des évènements
        for event in pygame.event.get():
            # Gestion de la fermeture du jeu
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                dict_ecrans["menu_athlete"] = 0
                if last_screen == "training":
                    dict_ecrans["menu_training"] = 1
                else:
                    dict_ecrans["menu_principal"] = 1