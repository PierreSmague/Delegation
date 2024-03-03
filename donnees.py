from display_functions import *
from countries import *

##### Taille fenêtre #####
largeur_fenetre = 1920
hauteur_fenetre = 1080

##### Gestion ouverture/fermeture des fenêtres #####
dict_ecrans = {
    "ecran_accueil": 1, "menu_principal": 0, "menu_staff": 0, "menu_training": 0, "menu_tournaments": 0,
    "menu_inscriptions": 0, "menu_race": 0, "menu_facilities": 0, "menu_scouting": 0, "menu_informations": 0,
    "menu_athlete": 0, "menu_live": 0
               }

# Fonds
fond_noir = load_image("images/fonds/fond_noir.png")
fond_accueil = load_image("images/fonds/fond_accueil.png")
fond_principal = load_image("images/fonds/fond_principal.png")
fond_athlete = load_image("images/fonds/fond_athlete.png")
fond_inscriptions = load_image("images/fonds/fond_inscriptions.png")
fond_endurance = load_image("images/fonds/fond_endurance.png")

# Menus
menu_left_side_bar = load_image("images/menus/left_side_bar.png")
menu_black_rectangle = load_image("images/menus/black_rectangle.png")
menu_black_trapeze = load_image("images/menus/black_trapeze.png")
menu_tiny_black_trapeze = load_image("images/menus/tiny_black_trapeze.png")
menu_black_progress = load_image("images/menus/black_progress.png")
menu_orange_progress = load_image("images/menus/orange_progress.png")
menu_orange_tick = load_image("images/menus/orange_tick.png")
menu_white_arrow = load_image("images/menus/white_arrow.png")
menu_enter_button = load_image("images/menus/enter_button.png")
menu_escape_button = load_image("images/menus/escape_button.png")
menu_save_icon = load_image("images/menus/save_icon.png")
menu_prestige_icon = load_image("images/menus/prestige_icon.png")
menu_squad_icon = load_image("images/menus/squad_icon.png")
menu_training_icon = load_image("images/menus/training_icon.png")
menu_competitions_icon = load_image("images/menus/competitions_icon.png")
menu_infos_icon = load_image("images/menus/infos_icon.png")
menu_scouting_icon = load_image("images/menus/scouting_icon.png")
menu_staff_icon = load_image("images/menus/staff_icon.png")
menu_stadium_icon = load_image("images/menus/stadium_icon.png")
click_cursor = load_image("images/menus/click_cursor.png")

# Live racing
running_silhouette = load_image("images/racing/running_silhouette.png")
gold_medal = load_image("images/racing/gold_medal.png")
silver_medal = load_image("images/racing/silver_medal.png")
bronze_medal = load_image("images/racing/bronze_medal.png")

# Drapeaux
flag_1 = load_image("images/flags/flag_1.png")
flag_2 = load_image("images/flags/flag_2.png")
all_fake_flags = []
for i in range(1, 13):
    all_fake_flags.append(load_image(f"images/flags/flag_{i}.png"))
all_icons_flags = {}
for country_name in [x["name"] for x in countries]:
    all_icons_flags[country_name] = load_image(f"images/flags/{country_name}.png")

# Achievements
general_achievements = [
    ["Hire your first athlete", 1000, 0],
    ["Take part in your first competition", 1000, 0],
    ["Hire your first external scout", 1500, 0],
    ["Hire your first external trainer", 1500, 0],
    ["Launch your first training", 1000, 0],
    ["Set a national record in each discipline", 2500, 0],
    ["Obtain +0.5 in one stat during training", 3000, 0],
    ["Hire two athletes in the same week (except 1st week)", 3000, 0],
    ["Have 5 athletes in your team", 2500, 0],
    ["Have 10 athletes in your team", 5000, 0],
    ["Have 20 athletes in your team", 10000, 0],
    ["Have 40 athletes in your team", 20000, 0],
    ["Keep an athlete for one year", 10000, 0],
    ["Keep an athlete for two years", 20000, 0],
    ["Keep an athlete for four years", 50000, 0],
    ["Keep an athlete for ten years", 100000, 0]
]

tournament_achievements = [
    ["Compete in a category ?? meeting", "Future scouts level : +??", 0, ["E", "D", "C", "B", "A", "S"], [2, 2, 2, 2, 2, 2]],
    ["Finish at least ?? in a category E meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]],
    ["Finish at least ?? in a category D meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]],
    ["Finish at least ?? in a category C meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]],
    ["Finish at least ?? in a category B meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]],
    ["Finish at least ?? in a category A meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]],
    ["Finish at least ?? in a category S meeting", "Future scouts level : +??", 0, ["4th", "3rd", "2nd", "1st"], [2, 2, 2, 2]]
]

performance_achievements = [
    ["Run 100m in less than ??s", "Future trainers level : +??", 0, [15, 14, 13, 12, 11, 10], [1, 1, 1, 1, 1, 1], "100m"],
    ["Run 110m hurdles in less than ??s", "Future trainers level : +??", 0, [20, 18, 16, 15, 14, 13.5], [1, 1, 1, 1, 1, 1], "110mh"],
    ["Run 200m in less than ??s", "Future trainers level : +??", 0, [30, 28, 26, 24, 22, 20], [1, 1, 1, 1, 1, 1], "200m"],
    ["Run 400m in less than ??s", "Future trainers level : +??", 0, [65, 61, 57, 53, 49, 45], [1, 1, 1, 1, 1, 1], "400m"],
    ["Run 800m in less than ??s", "Future trainers level : +??", 0, [180, 150, 135, 120, 110, 105], [1, 1, 1, 1, 1, 1], "800m"],
    ["Run 1500m in less than ??s", "Future trainers level : +??", 0, [360, 330, 300, 270, 240, 225], [1, 1, 1, 1, 1, 1], "1500m"],
    ["Run 5000m in less than ??s", "Future trainers level : +??", 0, [1200, 1100, 1000, 900, 800, 750], [1, 1, 1, 1, 1, 1], "5000m"],
    ["Run 10000m in less than ??s", "Future trainers level : +??", 0, [2500, 2300, 2100, 1900, 1800, 1700], [1, 1, 1, 1, 1, 1], "10000m"],
    ["Jump more than ??m", "Future trainers level : +??", 0, [5, 6, 7, 7.5, 8, 8.3], [1, 1, 1, 1, 1, 1], "longueur"],
    ["Triple jump more than ??m", "Future trainers level : +??", 0, [10, 12, 14, 16, 17, 17.5], [1, 1, 1, 1, 1, 1], "triplesaut"],
    ["Jump higher than ??m", "Future trainers level : +??", 0, [1.6, 1.8, 2, 2.1, 2.2, 2.3], [1, 1, 1, 1, 1, 1], "hauteur"],
    ["Jump higher than ??m (pole vault)", "Future trainers level : +??", 0, [4, 4.5, 5, 5.5, 5.7, 5.8], [1, 1, 1, 1, 1, 1], "perche"],
    ["Throw more than ??m (shot put)", "Future trainers level : +??", 0, [10, 12, 14, 16, 18, 20], [1, 1, 1, 1, 1, 1], "poids"],
    ["Throw more than ??m (discus)", "Future trainers level : +??", 0, [30, 40, 50, 55, 60, 65], [1, 1, 1, 1, 1, 1], "disque"],
    ["Throw more than ??m (javelin)", "Future trainers level : +??", 0, [40, 50, 60, 70, 80, 85], [1, 1, 1, 1, 1, 1], "javelot"],
    ["Score more than ??pts (decathlon)", "Future trainers level : +??", 0, [4000, 5000, 6000, 7000, 8000, 8500], [1, 1, 1, 1, 1, 1], "decathlon"]
]

exploits_achievements = [
    ["Become world champion in an event", "Max country talents : +1", 0],
    ["Become olympic champion in an event", "Max country talents : +1", 0],
    ["Beat a world record", "Max country talents : +1", 0],
    ["Complete a double at world championships", "Max country talents : +1", 0],
    ["Complete a double at olympics", "Max country talents : +1", 0]
]

# World records

world_records = {
    "100m": 9.58,
    "200m": 19.19,
    "400m": 43.03,
    "800m": 100.91,
    "1500m": 206,
    "5000m": 755.36,
    "10000m": 1571,
    "110mh": 12.8,
    "longueur": 8.95,
    "hauteur": 2.45,
    "perche": 6.23,
    "disque": 74.08,
    "poids": 23.56,
    "javelot": 98.48,
    "triplesaut": 18.29,
    "decathlon": 9126
}