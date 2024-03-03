import numpy as np
import pandas as pd
import math
import time as tm
import names
import random
from countries import *

prenoms = pd.read_csv("names/prenoms.csv", sep=";")
noms = pd.read_csv("names/noms.csv", sep=";")

all_stats = ["acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force", "technique_saut",
                 "technique_lancer", "technique_perche", "technique_haies"]
conversion_training_table = {
        "sprint" : [0.6, 0.6, 0.6, 0.2, 0, 0, 0, 0, 0, 0, 0],
        "middle distance" : [0.3, 0.5, 0.1, 0.8, 0.3, 0, 0, 0, 0, 0, 0],
        "long distance" : [0.1, 0.1, 0, 0.8, 1, 0, 0, 0, 0, 0, 0],
        "hurdles" : [0.4, 0.4, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 1],
        "throwing" : [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        "jumping" : [0, 0.2, 0, 0, 0, 0.8, 0, 1, 0, 0, 0],
        "pole vault" : [0, 0.5, 0, 0, 0, 0.25, 0.25, 0, 0, 1, 0]
    }
all_epreuves = ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "poids", "disque", "javelot",
                "longueur", "triplesaut", "hauteur", "perche", "decathlon"]
country_mapping = {
    "Sprintistan": "France",
    "American Samoa": "New Zealand",
    "Andorra": "Spain",
    "Antigua and Barbuda": "United States",
    "Aruba": "Netherlands",
    "Barbados": "United States",
    "Bhutan": "Nepal",
    "Botswana": "Zimbabwe",
    "British Virgin Islands": "United Kingdom",
    "Brunei": "Malaysia",
    "Cambodia": "India",
    "Cayman Islands": "United States",
    "Central African Republic": "Republic of the Congo",
    "Chad": "Sudan",
    "Comoros": "Mayotte",
    "Zaire": "Republic of the Congo",
    "Cook Islands": "United States",
    "Djibouti": "Somalia",
    "Dominica": "United Kingdom",
    "Equatorial Guinea": "Spain",
    "Eritrea": "Ethiopia",
    "Eswatini": "Zimbabwe",
    "Fiji": "New Zealand",
    "Gabon": "Senegal",
    "Gambia": "Senegal",
    "Great Britain": "United Kingdom",
    "Grenada": "United States",
    "Guam": "Australia",
    "Guinea Bissau": "Portugal",
    "Guyana": "Jamaica",
    "Kiribati": "New Zealand",
    "North Korea": "South Korea",
    "Kyrgyzstan": "Uzbekistan",
    "Laos": "India",
    "Lesotho": "Zimbabwe",
    "Liechtenstein": "Austria",
    "Madagascar": "Mayotte",
    "Malawi": "Zambia",
    "Maldives": "Mayotte",
    "Marshall Islands": "New Zealand",
    "Mauritania": "Mali",
    "Mauritius": "Haiti",
    "Micronesia": "Jamaica",
    "Monaco": "France",
    "Mongolia": "Kazakhstan",
    "Montenegro": "Serbia",
    "Myanmar": "India",
    "Namibia": "Zambia",
    "Nauru": "New Zealand",
    "Niger": "Nigeria",
    "Palau": "New Zealand",
    "Puerto Rico": "Cuba",
    "Saint Kitts and Nevis": "United States",
    "Saint Lucia": "Haiti",
    "Saint Vincent and the Grenadines": "United States",
    "Samoa": "New Zealand",
    "San Marino": "Italy",
    "Sao Tome and Principe": "Cape Verde",
    "Seychelles": "Mayotte",
    "Sierra Leone": "Guinea",
    "Solomon Islands": "United States",
    "South Africa": "Zimbabwe",
    "South Sudan": "Sudan",
    "Suriname": "Netherlands",
    "Tajikistan": "Uzbekistan",
    "East Timor": "Papua New Guinea",
    "Togo": "Benin",
    "Tonga": "New Zealand",
    "Turkmenistan": "Uzbekistan",
    "Tuvalu": "New Zealand",
    "Vanuatu": "New Zealand",
    "Virgin Islands": "United States",
    "Yemen": "Oman"
}

def transform_athlete(athlete):
    transformed_athlete = {
            "name": athlete["name"],
            "country": athlete["country"],
            "acceleration": max(0, round(np.random.normal(0.05 + athlete["acceleration"]/133, 0.01), 3)),
            "speed": round(np.random.normal(8 + athlete["speed"]/23, 0.06), 3),
            "reaction": round(np.random.normal(0.11 + 0.002 * (100 - athlete["reaction"]), 0.005), 3),
            "resistance": round(np.random.normal(2 + athlete["resistance"]/50, 0.04), 3),
            "endurance": round(np.random.normal(10 + athlete["endurance"]/5, 0.15), 3),
            "detente": round(np.random.normal(2 + athlete["detente"]/50, 0.04), 3),
            "technique_saut": round(np.random.normal(athlete["technique_saut"], 1), 3),
            "technique_lancer": round(np.random.normal(athlete["technique_lancer"], 1), 3),
            "technique_perche": round(np.random.normal(athlete["technique_perche"], 1), 3),
            "technique_haies": round(np.random.normal(athlete["technique_haies"], 1), 3),
            "force": round(100 + np.random.normal(athlete["force"], 2), 3)
        }
    return transformed_athlete


def cent_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 100]:
        time += 0.001
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 100:
                if fullspeed_times[i] < athletes_today[i]["resistance"]:
                    speed[i] = athletes_today[i]["speed"] * (
                                1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.8 * athletes_today[i]["speed"], 0.99995 * speed[i])
                meters_ran[i] = min(100, meters_ran[i] + speed[i] * 0.001)
                if (athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
            if not times_race[i] and meters_ran[i] == 100:
                times_race[i] = round(time, 3)
        if print_race:
            print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def cent_dix_metres_haies(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran, last_hurdle = meters_ran.copy(), meters_ran.copy()
    times_race, fullspeed_times, speed, last_hurdle_time, reset_time = meters_ran.copy(), meters_ran.copy(), meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    time= 0
    while [x for x in meters_ran if x < 110]:
        time += 0.001
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_at_hurdle = (0.4 + athletes_today[i]["technique_haies"]/357) * athletes_today[i]["speed"]
            if time < reaction_time:
                pass
            elif meters_ran[i] < 13.7:
                speed[i] = athletes_today[i]["speed"] * (1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                if fullspeed_times[i] >= 2 * athletes_today[i]["resistance"]:
                    speed[i] *= 1 - (fullspeed_times[i] - 2 * athletes_today[i]["resistance"]) * 0.09
                if speed[i] < speed_at_hurdle:
                    last_hurdle_time[i] = time - reaction_time
                meters_ran[i] = min(110, meters_ran[i] + speed[i] * 0.001)
                if (0.8 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
                if meters_ran[i] >= 13.7:
                    reset_time[i] = time
            elif meters_ran[i] < 96:
                last_hurdle[i] = int((meters_ran[i] - 13.72)/9.14) if (meters_ran[i] - 13.72)/9.14 >= 0 else int((meters_ran[i] - 13.72)/9.14) - 1
                speed[i] = athletes_today[i]["speed"] * (1 - math.exp(-(time - reset_time[i] + last_hurdle_time[i]) * athletes_today[i]["acceleration"]))
                if fullspeed_times[i] >= 2 * athletes_today[i]["resistance"]:
                    speed[i] *= 1 - (fullspeed_times[i] - 2 * athletes_today[i]["resistance"]) * 0.09
                meters_ran[i] = min(110, meters_ran[i] + speed[i] * 0.001)
                if (0.8 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
                if last_hurdle[i] != int((meters_ran[i] - 13.72)/9.14):
                    reset_time[i] = time
            else:
                speed[i] = athletes_today[i]["speed"] * (1 - math.exp(-(time - reset_time[i] + last_hurdle_time[i]) * athletes_today[i]["acceleration"]))
                if fullspeed_times[i] >= 2 * athletes_today[i]["resistance"]:
                    speed[i] *= 1 - (fullspeed_times[i] - 2 * athletes_today[i]["resistance"]) * 0.09
                meters_ran[i] = min(110, meters_ran[i] + speed[i] * 0.001)
                if (0.8 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
            if not times_race[i] and meters_ran[i] == 110:
                times_race[i] = round(time, 3)
        if print_race:
            print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def deux_cent_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 200]:
        time += 0.001
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 200:
                if fullspeed_times[i] < 2 * athletes_today[i]["resistance"]:
                    speed[i] = 0.93 * athletes_today[i]["speed"] * (
                                1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.8 * athletes_today[i]["speed"], 0.999982 * speed[i])
                meters_ran[i] = min(200, meters_ran[i] + speed[i] * 0.001)
                if (0.93 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
            if not times_race[i] and meters_ran[i] == 200:
                times_race[i] = round(time, 3)
        if print_race:
            print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def quatre_cent_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 400]:
        time += 0.001
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 400:
                if fullspeed_times[i] < 4 * athletes_today[i]["resistance"]:
                    speed[i] = 0.82 * athletes_today[i]["speed"] * (
                                1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.6 * athletes_today[i]["speed"], speed[i] * (0.99995 + 0.0000115 * athletes_today[i]["resistance"]))
                meters_ran[i] = min(400, meters_ran[i] + speed[i] * 0.001)
                if (0.82 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
            if not times_race[i] and meters_ran[i] == 400:
                times_race[i] = round(time, 3)
        if print_race:
            if int(1000 * time) % 2:
                print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def huit_cent_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 800]:
        time += 0.001
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 750:
                if fullspeed_times[i] < 4 * athletes_today[i]["resistance"] + 1.13 * athletes_today[i]["endurance"]:
                    speed[i] = (0.55 * athletes_today[i]["speed"] + 0.5 * athletes_today[i]["resistance"]) * (1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.4 * athletes_today[i]["speed"], speed[i] * (0.99993 + 0.00001 * athletes_today[i]["resistance"] + 0.000001 * athletes_today[i]["endurance"]))
                meters_ran[i] = min(800, meters_ran[i] + speed[i] * 0.001)
                if ((0.55 * athletes_today[i]["speed"] + 0.5 * athletes_today[i]["resistance"]) - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
                if meters_ran[i] >= 750:
                    fullspeed_times[i] = 0
            else:
                if fullspeed_times[i] < 0.8 * athletes_today[i]["resistance"]:
                    speed[i] = 0.85 * athletes_today[i]["speed"] * (
                            1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.7 * athletes_today[i]["speed"], 0.99992 * speed[i])
                meters_ran[i] = min(800, meters_ran[i] + speed[i] * 0.001)
                if (0.85 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.001
            if not times_race[i] and meters_ran[i] == 800:
                times_race[i] = round(time, 3)
        if print_race:
            if int(1000 * time) % 4 == 0:
                print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def quinze_cent_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 1500]:
        time += 0.01
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 1450:
                if fullspeed_times[i] < 5.5 * athletes_today[i]["resistance"] + 2.8 * athletes_today[i]["endurance"]:
                    speed[i] = (0.35 * athletes_today[i]["speed"] + 0.7 * athletes_today[i]["resistance"] + 0.04 * athletes_today[i]["endurance"]) * (1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.4 * athletes_today[i]["speed"], speed[i] * (0.99965 + 0.000018 * athletes_today[i]["resistance"] + 0.0000085 * athletes_today[i]["endurance"]))
                meters_ran[i] = min(1500, meters_ran[i] + speed[i] * 0.01)
                if ((0.35 * athletes_today[i]["speed"] + 0.7 * athletes_today[i]["resistance"] + 0.04 * athletes_today[i]["endurance"]) - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
                if meters_ran[i] >= 1450:
                    fullspeed_times[i] = 0
            else:
                if fullspeed_times[i] < 0.8 * athletes_today[i]["resistance"]:
                    speed[i] = 0.83 * athletes_today[i]["speed"] * (
                            1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.6 * athletes_today[i]["speed"], 0.99988 * speed[i])
                meters_ran[i] = min(1500, meters_ran[i] + speed[i] * 0.01)
                if (0.83 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
            if not times_race[i] and meters_ran[i] == 1500:
                times_race[i] = round(time, 3)
        if print_race:
            if int(100 * time) % 2 == 0:
                print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def cinq_mille_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 5000]:
        time += 0.01
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 4900:
                if fullspeed_times[i] < 5 * athletes_today[i]["resistance"] + 13 * athletes_today[i]["endurance"]:
                    speed[i] = (3 + 0.05 * athletes_today[i]["speed"] + 0.22 * athletes_today[i]["resistance"] + 0.1 * athletes_today[i]["endurance"]) * (1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(3 + 0.05 * athletes_today[i]["endurance"], speed[i] * (0.99995 + 0.000001 * athletes_today[i]["resistance"] + 0.000001 * athletes_today[i]["endurance"]))
                meters_ran[i] = min(5000, meters_ran[i] + speed[i] * 0.01)
                if ((3 + 0.05 * athletes_today[i]["speed"] + 0.22 * athletes_today[i]["resistance"] + 0.1 * athletes_today[i]["endurance"]) - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
                if meters_ran[i] >= 4900:
                    fullspeed_times[i] = 0
            else:
                if fullspeed_times[i] < 0.8 * athletes_today[i]["resistance"]:
                    speed[i] = 0.83 * athletes_today[i]["speed"] * (
                            1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.6 * athletes_today[i]["speed"], 0.99988 * speed[i])
                meters_ran[i] = min(5000, meters_ran[i] + speed[i] * 0.01)
                if (0.83 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
            if not times_race[i] and meters_ran[i] == 5000:
                times_race[i] = round(time, 3)
        if print_race:
            if int(100 * time) % 3 == 0:
                print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def dix_mille_metres(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    meters_ran = [0] * len(athletes_today)
    print_meters_ran = []
    truncated_meters_ran = meters_ran.copy()
    times_race, fullspeed_times, speed = meters_ran.copy(), meters_ran.copy(), meters_ran.copy()
    speed_tracking = [[]] * len(athletes_today)
    time = 0
    while [x for x in meters_ran if x < 10000]:
        time += 0.01
        speed_tracking[-1].append(time)
        for i in range(len(athletes_today)):
            reaction_time = athletes_today[i]["reaction"]
            speed_tracking[i].append(speed[i])
            if time < reaction_time:
                pass
            elif meters_ran[i] < 9800:
                if fullspeed_times[i] < 7 * athletes_today[i]["resistance"] + 26 * athletes_today[i]["endurance"]:
                    speed[i] = (2.5 + 0.2 * athletes_today[i]["resistance"] + 0.13 * athletes_today[i]["endurance"]) * (1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(3 + 0.05 * athletes_today[i]["endurance"], speed[i] * (0.99995 + 0.000001 * athletes_today[i]["resistance"] + 0.0000013 * athletes_today[i]["endurance"]))
                meters_ran[i] = min(10000, meters_ran[i] + speed[i] * 0.01)
                if ((2.5 + 0.2 * athletes_today[i]["resistance"] + 0.13 * athletes_today[i]["endurance"]) - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
                if meters_ran[i] >= 9800:
                    fullspeed_times[i] = 0
            else:
                if fullspeed_times[i] < 2 * athletes_today[i]["resistance"]:
                    speed[i] = 0.83 * athletes_today[i]["speed"] * (
                            1 - math.exp(-(time - reaction_time) * athletes_today[i]["acceleration"]))
                else:
                    speed[i] = max(0.6 * athletes_today[i]["speed"], 0.99988 * speed[i])
                meters_ran[i] = min(10000, meters_ran[i] + speed[i] * 0.01)
                if (0.83 * athletes_today[i]["speed"] - speed[i]) < 0.02 * athletes_today[i]["speed"]:
                    fullspeed_times[i] += 0.01
            if not times_race[i] and meters_ran[i] == 10000:
                times_race[i] = round(time, 3)
        if print_race:
            if int(100 * time) % 5 == 0:
                print_meters_ran.append([10 * round(x, 3) for x in meters_ran])
    if print_race:
        return [times_race, print_meters_ran]
    else:
        return times_race


def saut_en_longueur(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    longueur_sauts = [0] * len(athletes_today)
    trajectory = [0] * len(athletes_today)
    g = 9.81
    for i in range(len(athletes_today)):
        initial_height = 1
        final_height = 0.1
        theta = math.radians(14 + athletes_today[i]["technique_saut"]/10)
        horizontal_speed = 0.74 * athletes_today[i]["speed"]
        vertical_speed = athletes_today[i]["detente"]
        initial_speed = math.sqrt(math.pow(horizontal_speed, 2) + math.pow(vertical_speed, 2))
        term1 = math.pow(initial_speed, 2) * math.sin(2*theta) / (2 * g)
        term2 = (1 + math.sqrt(1 + (2 * g * (initial_height - final_height) / math.pow(initial_speed * math.sin(theta), 2))))
        longueur_sauts[i] = round(term1 * term2, 2)
        if print_race:
            trajectory[i] = []
            x = 0
            while x < longueur_sauts[i]:
                z = (initial_height - final_height) + (x * math.tan(theta)) - (g * math.pow(x, 2)) / (2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
    if print_race:
        return [longueur_sauts, trajectory]
    else:
        return longueur_sauts


def triple_saut(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    longueur_sauts = [0] * len(athletes_today)
    trajectory = [0] * len(athletes_today)
    g = 9.81
    for i in range(len(athletes_today)):
        theta = math.radians(14 + athletes_today[i]["technique_saut"]/10)
        horizontal_speed = 0.74 * athletes_today[i]["speed"]
        vertical_speed = athletes_today[i]["detente"]
        ### Premier saut
        initial_speed = math.sqrt(math.pow(horizontal_speed, 2) + math.pow(vertical_speed, 2))
        term1 = math.pow(initial_speed, 2) * math.sin(2 * theta) / g
        longueur_sauts[i] += term1
        premier_saut = longueur_sauts[i]
        if print_race:
            trajectory[i] = []
            x = 0
            while x < longueur_sauts[i]:
                z = 0.9 + (x * math.tan(theta)) - (g * math.pow(x, 2)) / (2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
        ### Deuxième saut
        initial_speed = math.sqrt(math.pow(0.83 * horizontal_speed, 2) + math.pow(vertical_speed, 2))
        term1 = math.pow(initial_speed, 2) * math.sin(2 * theta) / g
        longueur_sauts[i] += term1
        second_saut = longueur_sauts[i]
        if print_race:
            while x < longueur_sauts[i]:
                z = 0.9 + ((x - premier_saut) * math.tan(theta)) - (g * math.pow((x - premier_saut), 2)) / (2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
        ### Dernier saut
        initial_speed = math.sqrt(math.pow(0.74 * horizontal_speed, 2) + math.pow(vertical_speed, 2))
        term1 = math.pow(initial_speed, 2) * math.sin(2*theta) / (2 * g)
        term2 = (1 + math.sqrt(1 + (2 * g * 0.9 / math.pow(initial_speed * math.sin(theta), 2))))
        longueur_sauts[i] += term1 * term2
        longueur_sauts[i] = round(longueur_sauts[i], 2)
        if print_race:
            while x < longueur_sauts[i]:
                z = 0.9 + ((x - second_saut) * math.tan(theta)) - (g * math.pow((x - second_saut), 2)) / (2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
    if print_race:
        return [longueur_sauts, trajectory]
    else:
        return longueur_sauts


def saut_en_hauteur(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    hauteur_sauts = [0] * len(athletes_today)
    g, h_init = 9.81, 0.95
    for i in range(len(athletes_today)):
        theta = math.radians(20 + athletes_today[i]["technique_saut"]/7.15)
        horizontal_speed = 5 + athletes_today[i]["speed"]/4
        vertical_speed = 1.3 * athletes_today[i]["detente"]
        initial_speed = math.sqrt(math.pow(horizontal_speed, 2) + math.pow(vertical_speed, 2)) * math.sin(theta)
        hauteur_sauts[i] = round(h_init + math.pow(initial_speed, 2)/(2*g) + athletes_today[i]["technique_saut"]/1000, 2)
    return hauteur_sauts


def saut_perche(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    hauteur_sauts = [0] * len(athletes_today)
    g, h_init = 9.81, 0.95
    for i in range(len(athletes_today)):
        horizontal_speed = 0.81 * athletes_today[i]["speed"]
        vertical_speed = 0.3 * athletes_today[i]["detente"]
        initial_speed = math.sqrt(math.pow(horizontal_speed, 2) + math.pow(vertical_speed, 2))
        kinetic_energy = 0.5 * math.pow(initial_speed, 2) + 0.5 * athletes_today[i]["force"]/75
        hauteur_sauts[i] = round(h_init + kinetic_energy/g - 0.01 * (100 - athletes_today[i]["technique_perche"]), 2)
    return hauteur_sauts


def lancer_poids(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    longueur_lancers = [0] * len(athletes_today)
    trajectory = [0] * len(athletes_today)
    g = 9.81
    for i in range(len(athletes_today)):
        initial_height = 1.7
        final_height = 0.02
        initial_speed = 2 + athletes_today[i]["technique_lancer"]/30 + athletes_today[i]["force"]/21
        theta = math.radians(24 + athletes_today[i]["technique_lancer"]/5)
        term1 = math.pow(initial_speed, 2) * math.sin(2*theta) / (2 * g)
        term2 = (1 + math.sqrt(1 + (2 * g * (initial_height - final_height) / math.pow(initial_speed * math.sin(theta), 2))))
        longueur_lancers[i] = round(term1 * term2, 2)
        if print_race:
            trajectory[i] = []
            x = 0
            while x < longueur_lancers[i]:
                z = (initial_height - final_height) + (x * math.tan(theta)) - (g * math.pow(x, 2)) / (
                            2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
    if print_race:
        return [longueur_lancers, trajectory]
    else:
        return longueur_lancers


def lancer_disque(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    longueur_lancers = [0] * len(athletes_today)
    trajectory = [0] * len(athletes_today)
    g = 9.81
    for i in range(len(athletes_today)):
        initial_height = 1.7
        final_height = 0.02
        initial_speed = 5 + athletes_today[i]["force"]/16.5 + athletes_today[i]["technique_lancer"]/10
        theta = math.radians(24 + athletes_today[i]["technique_lancer"]/5)
        term1 = math.pow(initial_speed, 2) * math.sin(2*theta) / (2 * g)
        term2 = (1 + math.sqrt(1 + (2 * g * (initial_height - final_height) / math.pow(initial_speed * math.sin(theta), 2))))
        longueur_lancers[i] = round(term1 * term2, 2)
        if print_race:
            trajectory[i] = []
            x = 0
            while x < longueur_lancers[i]:
                z = (initial_height - final_height) + (x * math.tan(theta)) - (g * math.pow(x, 2)) / (
                        2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
    if print_race:
        return [longueur_lancers, trajectory]
    else:
        return longueur_lancers


def lancer_javelot(athletes_today, print_race=False):
    athletes_today = [transform_athlete(x) for x in athletes_today]
    longueur_lancers = [0] * len(athletes_today)
    trajectory = [0] * len(athletes_today)
    g = 9.81
    for i in range(len(athletes_today)):
        initial_height = 2
        final_height = 0.02
        initial_speed = 5 + athletes_today[i]["force"]/15 + athletes_today[i]["technique_lancer"]/12 + 0.4 * athletes_today[i]["speed"]
        theta = math.radians(24 + athletes_today[i]["technique_lancer"]/5)
        term1 = math.pow(initial_speed, 2) * math.sin(2*theta) / (2 * g)
        term2 = (1 + math.sqrt(1 + (2 * g * (initial_height - final_height) / math.pow(initial_speed * math.sin(theta), 2))))
        longueur_lancers[i] = round(term1 * term2, 2)
        if print_race:
            trajectory[i] = []
            x = 0
            while x < longueur_lancers[i]:
                z = (initial_height - final_height) + (x * math.tan(theta)) - (g * math.pow(x, 2)) / (2 * math.pow(math.cos(theta) * initial_speed, 2))
                trajectory[i].append([x, z])
                x += 0.01
    if print_race:
        return [longueur_lancers, trajectory]
    else:
        return longueur_lancers


def eval_potentiel(athlete, pot=False, scout=False):
    if not pot:
        eval_sprint = round(0.55 * athlete["speed"] + 0.3 * athlete["acceleration"] + 0.1 * athlete["reaction"] + 0.05 * athlete["resistance"], 2)
        eval_demifond = round(0.3 * athlete["speed"] + 0.09 * athlete["acceleration"] + 0.01 * athlete["reaction"] + 0.3 * athlete["resistance"] + 0.3 * athlete["endurance"], 2)
        eval_fond = round(0.005 * athlete["speed"] + 0.005 * athlete["acceleration"] + 0.23 * athlete["resistance"] + 0.76 * athlete["endurance"], 2)
        eval_haies = round(0.4 * athlete["speed"] + 0.2 * athlete["acceleration"] + 0.05 * athlete["reaction"] + 0.05 * athlete["resistance"] + 0.3 * athlete["technique_haies"], 2)
        eval_lancer = round(0.5 * athlete["force"] + 0.5 * athlete["technique_lancer"], 2)
        eval_saut = round(0.45 * athlete["speed"] + 0.4 * athlete["technique_saut"] + 0.15 * athlete["detente"], 2)
        eval_perche = round(0.45 * athlete["speed"] + 0.4 * athlete["technique_perche"] + 0.075 * athlete["detente"] + 0.075 * athlete["force"], 2)
        eval_combine = round(0.3 * athlete["speed"] + 0.04 * athlete["acceleration"] + 0.11 * athlete["technique_saut"] + 0.05 * athlete["technique_perche"]\
                       + 0.04 * athlete["technique_haies"] + 0.17 * athlete["technique_lancer"] + 0.16 * athlete["force"]\
                       + 0.03 * athlete["detente"] + 0.01 * athlete["reaction"] + 0.05 * athlete["resistance"] + 0.04 * athlete["endurance"], 2)

    else:
        eval_sprint = round(0.55 * athlete["pot_speed"] + 0.3 * athlete["pot_acceleration"] + 0.1 * athlete["pot_reaction"] + 0.05 * athlete["pot_resistance"], 2)
        eval_demifond = round(0.3 * athlete["pot_speed"] + 0.09 * athlete["pot_acceleration"] + 0.01 * athlete["pot_reaction"] + 0.3 * athlete["pot_resistance"] + 0.3 * athlete["pot_endurance"], 2)
        eval_fond = round(0.005 * athlete["pot_speed"] + 0.005 * athlete["pot_acceleration"] + 0.23 * athlete["pot_resistance"] + 0.76 * athlete["pot_endurance"], 2)
        eval_haies = round(0.4 * athlete["pot_speed"] + 0.2 * athlete["pot_acceleration"] + 0.05 * athlete["pot_reaction"] + 0.05 * athlete["pot_resistance"] + 0.3 * athlete["pot_technique_haies"], 2)
        eval_lancer = round(0.5 * athlete["pot_force"] + 0.5 * athlete["pot_technique_lancer"], 2)
        eval_saut = round(0.45 * athlete["pot_speed"] + 0.4 * athlete["pot_technique_saut"] + 0.15 * athlete["pot_detente"], 2)
        eval_perche = round(0.45 * athlete["pot_speed"] + 0.4 * athlete["pot_technique_perche"] + 0.075 * athlete["pot_detente"] + 0.075 * athlete["pot_force"], 2)
        eval_combine = round(0.3 * athlete["pot_speed"] + 0.04 * athlete["pot_acceleration"] + 0.11 * athlete["pot_technique_saut"] + 0.05 * athlete["pot_technique_perche"] \
            + 0.04 * athlete["pot_technique_haies"] + 0.17 * athlete["technique_lancer"] + 0.16 * athlete["pot_force"] \
            + 0.03 * athlete["pot_detente"] + 0.01 * athlete["pot_reaction"] + 0.05 * athlete["pot_resistance"] + 0.04 * athlete["pot_endurance"], 2)


    evaluation = {
        "sprinteur": eval_sprint,
        "demi fond": eval_demifond,
        "fond": eval_fond,
        "hurdler": eval_haies,
        "lanceur": eval_lancer,
        "sauteur": eval_saut,
        "perchiste": eval_perche,
        "combine": eval_combine,
            }

    if scout:
        if not pot:
            for key, value in evaluation.items():
                evaluation[key] = max(0, round(value + np.random.normal(0, (100 - scout["level_detection"])/5), 2))
        else:
            for key, value in evaluation.items():
                evaluation[key] = round(value + np.random.normal(0, (100 - scout["potential_detection"])/5), 2)


    return evaluation


def eval_epreuve(athlete, epreuve):
    eval_cent = round(0.45 * athlete["speed"] + 0.4 * athlete["acceleration"] + 0.1 * athlete["reaction"] + 0.05 * athlete["resistance"], 2)
    eval_deuxcent = round(0.55 * athlete["speed"] + 0.3 * athlete["acceleration"] + 0.05 * athlete["reaction"] + 0.1 * athlete["resistance"], 2)
    eval_quatrecent = round(0.38 * athlete["speed"] + 0.15 * athlete["acceleration"] + 0.02 * athlete["reaction"] + 0.45 * athlete["resistance"], 2)
    eval_huitcent = round(0.3 * athlete["speed"] + 0.09 * athlete["acceleration"] + 0.01 * athlete["reaction"] + 0.4 * athlete["resistance"] + 0.2 * athlete["endurance"], 2)
    eval_quinzecent = round(0.25 * athlete["speed"] + 0.05 * athlete["acceleration"] + 0.3 * athlete["resistance"] + 0.4 * athlete["endurance"], 2)
    eval_cinqmille = round(0.03 * athlete["speed"] + 0.02 * athlete["acceleration"] + 0.3 * athlete["resistance"] + 0.65 * athlete["endurance"], 2)
    eval_dixmille = round(0.01 * athlete["speed"] + 0.01 * athlete["acceleration"] + 0.18 * athlete["resistance"] + 0.8 * athlete["endurance"], 2)
    eval_centdixhaies = round(0.4 * athlete["speed"] + 0.2 * athlete["acceleration"] + 0.05 * athlete["reaction"] + 0.05 * athlete["resistance"] + 0.3 * athlete["technique_haies"], 2)
    eval_lancer = round(0.5 * athlete["force"] + 0.5 * athlete["technique_lancer"], 2)
    eval_lancerjavelot = round(0.1 * athlete["speed"] + 0.45 * athlete["force"] + 0.45 * athlete["technique_lancer"], 2)
    eval_longueur = round(0.5 * athlete["speed"] + 0.4 * athlete["technique_saut"] + 0.1 * athlete["detente"], 2)
    eval_triplesaut = round(0.5 * athlete["speed"] + 0.4 * athlete["technique_saut"] + 0.1 * athlete["detente"], 2)
    eval_hauteur = round(0.3 * athlete["speed"] + 0.4 * athlete["technique_saut"] + 0.3 * athlete["detente"], 2)
    eval_perche = round(0.45 * athlete["speed"] + 0.4 * athlete["technique_perche"] + 0.075 * athlete["detente"] + 0.075 * athlete["force"], 2)
    eval_combine = round(0.3 * athlete["speed"] + 0.04 * athlete["acceleration"] + 0.11 * athlete["technique_saut"] + 0.05 * athlete["technique_perche"] \
        + 0.04 * athlete["technique_haies"] + 0.17 * athlete["technique_lancer"] + 0.16 * athlete["force"] \
        + 0.03 * athlete["detente"] + 0.01 * athlete["reaction"] + 0.05 * athlete["resistance"] + 0.04 * athlete["endurance"], 2)

    dict_epreuves = {
        "100m": eval_cent,
        "200m": eval_deuxcent,
        "400m": eval_quatrecent,
        "800m": eval_huitcent,
        "1500m": eval_quinzecent,
        "5000m": eval_cinqmille,
        "10000m": eval_dixmille,
        "110mh": eval_centdixhaies,
        "poids": eval_lancer,
        "disque": eval_lancer,
        "javelot": eval_lancerjavelot,
        "longueur": eval_longueur,
        "triplesaut": eval_triplesaut,
        "hauteur": eval_hauteur,
        "perche": eval_perche,
        "decathlon": eval_combine/0.8
            }

    return dict_epreuves[epreuve]


def generate_athlete(level, potential_level, job):
    athlete = {
        "name": "",
        "country": "",
        "trainer": "",
        "scout": "",
        "arrival_date": "",
        "detection_level": "",
        "detection_potential_level": "",
        "salary": 0,
        "session": "REST",
        "age": 0,
        "birthday": 0,
        "progression": [0] * 11,
        "acceleration": 0,
        "speed": 0,
        "reaction": 0,
        "resistance": 0,
        "endurance": 0,
        "detente": 0,
        "technique_saut": 0,
        "technique_lancer": 0,
        "technique_perche": 0,
        "technique_haies": 0,
        "force": 0,
        "pot_acceleration": 0,
        "pot_speed": 0,
        "pot_reaction": 0,
        "pot_resistance": 0,
        "pot_endurance": 0,
        "pot_detente": 0,
        "pot_technique_saut": 0,
        "pot_technique_lancer": 0,
        "pot_technique_perche": 0,
        "pot_technique_haies": 0,
        "pot_force": 0,
        "personal_best": {
            "100m": "",
            "200m": "",
            "400m": "",
            "800m": "",
            "1500m": "",
            "5000m": "",
            "10000m": "",
            "110mh": "",
            "longueur": "",
            "hauteur": "",
            "perche": "",
            "disque": "",
            "poids": "",
            "javelot": "",
            "triplesaut": "",
            "decathlon": ""
        }
    }
    global all_stats

    if job == "sprinteur":
        while eval_potentiel(athlete)["sprinteur"] < level - 2 or eval_potentiel(athlete)["sprinteur"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["acceleration"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["reaction"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["resistance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        athlete["technique_saut"] = max(0, min(100, round(np.random.normal(0.8 * level, 15), 1)))
        for stat in ["endurance", "detente", "technique_lancer", "technique_perche", "technique_haies","force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["sprinteur"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["sprinteur"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_reaction"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_resistance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        athlete["pot_technique_saut"] = max(0, min(100, round(np.random.normal(0.8 * potential_level, 15), 1)))
        for stat in ["pot_endurance", "pot_detente", "pot_technique_lancer", "pot_technique_perche", "pot_technique_haies","pot_force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level/3, potential_level/6), 1)))

    elif job == "demi fond":
        while eval_potentiel(athlete)["demi fond"] < level - 2 or eval_potentiel(athlete)["demi fond"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["acceleration"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["reaction"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["resistance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["endurance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        for stat in ["technique_saut", "detente", "technique_lancer", "technique_perche", "technique_haies", "force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["demi fond"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["demi fond"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_reaction"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_resistance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_endurance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        for stat in ["pot_technique_saut", "pot_detente", "pot_technique_lancer", "pot_technique_perche", "pot_technique_haies", "pot_force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level / 3, potential_level / 6), 1)))

    elif job == "fond":
        while eval_potentiel(athlete)["fond"] < level - 2 or eval_potentiel(athlete)["fond"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["acceleration"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["resistance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["endurance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        for stat in ["technique_saut", "detente", "technique_lancer", "technique_perche", "technique_haies", "force", "reaction"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["fond"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["fond"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_resistance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_endurance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        for stat in ["pot_technique_saut", "pot_detente", "pot_technique_lancer", "pot_technique_perche", "pot_technique_haies", "pot_force", "pot_reaction"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level / 3, potential_level / 6), 1)))

    elif job == "hurdler":
        while eval_potentiel(athlete)["hurdler"] < level - 2 or eval_potentiel(athlete)["hurdler"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["acceleration"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["reaction"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["resistance"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["technique_haies"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        for stat in ["technique_saut", "detente", "technique_lancer", "technique_perche", "endurance", "force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["hurdler"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["hurdler"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_reaction"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_resistance"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_technique_haies"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        for stat in ["pot_technique_saut", "pot_detente", "pot_technique_lancer", "pot_technique_perche", "pot_endurance", "pot_force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level / 3, potential_level / 6), 1)))

    elif job == "lanceur":
        while eval_potentiel(athlete)["lanceur"] < level - 2 or eval_potentiel(athlete)["lanceur"] > level + 2:
            athlete["force"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["technique_lancer"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        athlete["speed"] = max(0, min(100, round(np.random.normal(level/3, 25))))
        for stat in ["technique_saut", "detente", "acceleration", "technique_perche", "endurance", "resistance", "technique_haies", "reaction"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/4, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["lanceur"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["lanceur"] > potential_level + 2:
            athlete["pot_force"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_technique_lancer"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level/3, 30), 1)))
        for stat in ["pot_technique_saut", "pot_detente", "pot_acceleration", "pot_technique_perche", "pot_endurance", "pot_resistance", "pot_technique_haies", "pot_reaction"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level / 3, potential_level / 6), 1)))

    elif job == "sauteur":
        while eval_potentiel(athlete)["sauteur"] < level - 2 or eval_potentiel(athlete)["sauteur"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["detente"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["technique_saut"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        athlete["acceleration"] = max(0, min(100, round(np.random.normal(0.8 * level, 15), 1)))
        for stat in ["technique_haies", "reaction", "technique_lancer", "technique_perche", "endurance", "force", "resistance"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["sauteur"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["sauteur"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_detente"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_technique_saut"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(0.8 * potential_level, 15), 1)))
        for stat in ["pot_technique_haies", "pot_reaction", "pot_technique_lancer", "pot_technique_perche", "pot_endurance", "pot_force", "pot_resistance"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level/3, potential_level/6), 1)))

    elif job == "perchiste":
        while eval_potentiel(athlete)["perchiste"] < level - 2 or eval_potentiel(athlete)["perchiste"] > level + 2:
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["detente"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["force"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
            athlete["technique_perche"] = max(0, min(100, round(np.random.normal(level, 15), 1)))
        athlete["acceleration"] = max(0, min(100, round(np.random.normal(0.8 * level, 15), 1)))
        for stat in ["technique_saut", "resistance", "technique_lancer", "reaction", "endurance", "force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(level/3, level/6), 1)))

        while eval_potentiel(athlete, pot=True)["perchiste"] < potential_level - 2 or eval_potentiel(athlete, pot=True)["perchiste"] > potential_level + 2:
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_detente"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_force"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
            athlete["pot_technique_perche"] = max(0, min(100, round(np.random.normal(potential_level, 15), 1)))
        athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(0.8 * potential_level, 15), 1)))
        for stat in ["pot_technique_saut", "pot_resistance", "pot_technique_lancer", "pot_reaction", "pot_endurance", "pot_force"]:
            athlete[stat] = max(0, min(100, round(np.random.normal(potential_level/3, potential_level/6), 1)))

    elif job == "combine":
        while (eval_potentiel(athlete)["combine"] < 0.8 * level - 2 or eval_potentiel(athlete)["combine"] > 0.8 * level + 2 or
               max(eval_potentiel(athlete)["sprinteur"], eval_potentiel(athlete)["demi fond"],eval_potentiel(athlete)["fond"], eval_potentiel(athlete)["hurdler"], \
               eval_potentiel(athlete)["lanceur"], eval_potentiel(athlete)["sauteur"],eval_potentiel(athlete)["perchiste"]) > 1.15 * level):
            athlete["speed"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["acceleration"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["reaction"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["resistance"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["technique_haies"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["technique_saut"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["detente"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["technique_lancer"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["technique_perche"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["endurance"] = max(0, min(100, round(np.random.normal(level, 20), 1)))
            athlete["force"] = max(0, min(100, round(np.random.normal(level, 20), 1)))

        while (eval_potentiel(athlete, pot=True)["combine"] < 0.8 * potential_level - 1 or eval_potentiel(athlete, pot=True)["combine"] > 0.8 * potential_level + 1\
               or max(eval_potentiel(athlete, pot=True)["sprinteur"], eval_potentiel(athlete, pot=True)["demi fond"],
                   eval_potentiel(athlete, pot=True)["fond"], eval_potentiel(athlete, pot=True)["hurdler"], \
                   eval_potentiel(athlete, pot=True)["lanceur"], eval_potentiel(athlete, pot=True)["sauteur"],
                   eval_potentiel(athlete, pot=True)["perchiste"]) > 1.15 * potential_level):
            athlete["pot_speed"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_acceleration"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_reaction"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_resistance"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_technique_haies"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_technique_saut"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_detente"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_technique_lancer"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_technique_perche"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_endurance"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))
            athlete["pot_force"] = max(0, min(100, round(np.random.normal(potential_level, 20), 1)))

    if potential_level == level:
        for stat in all_stats:
            athlete["pot_" + stat] = athlete[stat]
        athlete["age"] = random.randint(27, 36)
    else:
        for stat in all_stats:
            athlete["pot_" + stat] = max(athlete["pot_" + stat], athlete[stat])
        athlete["age"] = round(16 + max(np.random.normal(15 * (level/potential_level - 0.45), 1), 0))

    athlete["birthday"] = random.randint(1, 52)

    return athlete


def eval_salary(athlete, scout=False):
    if scout:
        salary_base = max(athlete["detection_level"].values())
        if salary_base == athlete["detection_level"]["combine"]:
            salary_base *= 0.85
    else:
        print(eval_potentiel(athlete))
        salary_base = max(eval_potentiel(athlete).values())
    if salary_base < 30:
        salary = 500
    else:
        salary = 100 * round(0.01 * (500 + pow(3.5 * (salary_base - 30), 2)))
    return salary


def generate_trainer(level):
    trainer = {
        "name": names.get_full_name(),
        "country": "",
        "sprint": 0,
        "middle distance": 0,
        "long distance": 0,
        "hurdles": 0,
        "throwing": 0,
        "jumping": 0,
        "pole vault": 0
    }
    all_stats = ["sprint", "middle distance", "long distance", "hurdles", "throwing", "jumping", "pole vault"]
    speciality = random.choice(all_stats)
    for stat in all_stats:
        if stat == speciality:
            trainer[stat] = round(level)
        else:
            trainer[stat] = round(random.uniform(0, level))

    return trainer


def generate_scout(level):
    scout = {
        "name": names.get_full_name(),
        "country": "",
        "level_detection": 0,
        "potential_detection": 0,
        "efficiency": 0,
        "flair": 0,
        "profile": "various",
    }
    all_stats = ["level_detection", "potential_detection", "efficiency", "flair"]
    for stat in all_stats:
        scout[stat] = max(0, min(100, round(np.random.normal(0.8 * level, 0.5 * level))))
    scout["weeks_before_detect"] = round(4 + (100 - scout["efficiency"]) / 12.5, 2)

    return scout


def generate_name(country):
    global country_mapping
    if country in country_mapping.keys():
        country = country_mapping[country]
    try:
        prenom = prenoms[prenoms.country == country]["name"].sample().iloc[0].capitalize()
    except:
        prenom = prenoms[prenoms.country == "United States"]["name"].sample().iloc[0].capitalize()
    try:
        nom = noms[noms.country == country]["name"].sample().iloc[0].capitalize()
    except:
        nom = noms[noms.country == "United States"]["name"].sample().iloc[0].capitalize()
    return f"{prenom} {nom}"


def generate_athlete_country(country, number, profile="all"):
    all_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
    if profile != "all":
        if profile == "random":
            all_profiles = random.sample(all_profiles, number)
            number = 1
        else:
            all_profiles = [profile]
    all_athletes = []
    for profile in all_profiles:
        actual_profile = country[dict_profiles[profile]]
        for _ in range(0, number):
            potential_level = 0
            while not 0 < potential_level < 100:
                if country["name"] in [x["name"] for x in real_countries]:
                    potential_level = np.random.normal(actual_profile, 2 + (100 - actual_profile) / 10)
                    potential_level = max(10, potential_level)
                else:
                    own_country_profile = random.randint(max(10, round(0.33 * actual_profile)), actual_profile)
                    potential_level = np.random.normal(own_country_profile, 2 + (100 - actual_profile) / 10)
            actual_level = max(0, min(potential_level, np.random.normal(0.8 * potential_level, 0.2 * potential_level)))
            new_athlete = generate_athlete(actual_level, potential_level, job=profile)
            new_athlete["country"] = country
            if country["name"] not in [x["name"] for x in real_countries]:
                new_athlete["name"] = generate_name(random.choice([x["name"] for x in countries]))
            else:
                new_athlete["name"] = generate_name(country["name"])

            all_athletes.append(new_athlete)
    return all_athletes


def generate_rewards(category, position):
    money, prestige = 0, 0
    if category == "E":
        if position == 5:
            money, prestige = 50, 2
        elif position == 4:
            money, prestige = 150, 5
        elif position == 3:
            money, prestige = 250, 10
        elif position == 2:
            money, prestige = 500, 15
        elif position == 1:
            money, prestige = 1250, 25
    elif category == "D":
        if position == 5:
            money, prestige = 150, 5
        elif position == 4:
            money, prestige = 250, 10
        elif position == 3:
            money, prestige = 750, 20
        elif position == 2:
            money, prestige = 1500, 40
        elif position == 1:
            money, prestige = 5000, 75
    elif category == "C":
        if position == 5:
            money, prestige = 500, 10
        elif position == 4:
            money, prestige = 2500, 30
        elif position == 3:
            money, prestige = 5000, 50
        elif position == 2:
            money, prestige = 15000, 100
        elif position == 1:
            money, prestige = 50000, 250
    elif category == "B":
        if position == 5:
            money, prestige = 2500, 20
        elif position == 4:
            money, prestige = 7500, 60
        elif position == 3:
            money, prestige = 20000, 100
        elif position == 2:
            money, prestige = 50000, 300
        elif position == 1:
            money, prestige = 100000, 750
    elif category == "A":
        if position == 5:
            money, prestige = 5000, 35
        elif position == 4:
            money, prestige = 12500, 100
        elif position == 3:
            money, prestige = 35000, 250
        elif position == 2:
            money, prestige = 80000, 500
        elif position == 1:
            money, prestige = 175000, 1500
    elif category == "S":
        if position == 5:
            money, prestige = 15000, 100
        elif position == 4:
            money, prestige = 50000, 250
        elif position == 3:
            money, prestige = 150000, 1000
        elif position == 2:
            money, prestige = 300000, 2000
        elif position == 1:
            money, prestige = 500000, 3500
    elif category == "WC":
        if position == 5:
            money, prestige = 50000, 5000
        elif position == 4:
            money, prestige = 100000, 10000
        elif position == 3:
            money, prestige = 150000, 15000
        elif position == 2:
            money, prestige = 300000, 30000
        elif position == 1:
            money, prestige = 1000000, 100000
    elif category == "O":
        if position == 5:
            money, prestige = 100000, 10000
        elif position == 4:
            money, prestige = 250000, 25000
        elif position == 3:
            money, prestige = 500000, 50000
        elif position == 2:
            money, prestige = 1000000, 100000
        elif position == 1:
            money, prestige = 3000000, 300000
    return (money, prestige)


def training_athlete(athlete, session, installs=0):
    global all_stats, conversion_training_table
    progression = []
    session = session.lower()

    if session != "rest":
        for i in range(len(all_stats)):
            stat = all_stats[i]
            progression.append(athlete[stat])

            natural_gain = 0.1
            if athlete["age"] < 25:
                natural_gain += np.random.normal(0.01 * (26 - athlete["age"]), 0.02)
            elif athlete["age"] < 29:
                natural_gain += np.random.normal(0, 0.02)
            else:
                natural_gain += np.random.normal(0.03 * (athlete["age"] - 29), 0.02)
            trainer_gain = 0.005 * athlete["trainer"][session] if athlete["trainer"] else 0
            caracs_gain = conversion_training_table[session][i]
            total_gain = np.random.normal(caracs_gain * (natural_gain + trainer_gain), 0.04)
            if total_gain > 0:
                total_gain *= (1 + installs/20)
            athlete[stat] = max(0, round(min(athlete["pot_"+stat], athlete[stat] + total_gain), 1))

            if athlete[stat] == athlete["pot_"+stat]:
                progression[i] = -99
            else:
                progression[i] = round(athlete[stat] - progression[i], 1)
        athlete["progression"] = progression
    return athlete


def add_contestants(current_contestants, all_athletes, epreuve, category):
    min_eval, max_eval = 0, 0
    if category == "E":
        min_eval = 10
        max_eval = 30
    elif category == "D":
        min_eval = 25
        max_eval = 45
    elif category == "C":
        min_eval = 40
        max_eval = 60
    elif category == "B":
        min_eval = 55
        max_eval = 75
    elif category == "A":
        min_eval = 70
        max_eval = 85
    elif category in ["S", "WC", "O"]:
        min_eval = 80
        max_eval = 100
    potential_additions = [x for x in all_athletes if min_eval <= eval_epreuve(x, epreuve) <= max_eval and eval_epreuve(x, epreuve) >= 0.85 * max([eval_epreuve(x, epr) for epr in all_epreuves])]
    to_add = min(8 - len(current_contestants), len(potential_additions))
    if category in ["WC", "O"]:
        potential_additions = sorted(potential_additions, key=lambda athlete: eval_epreuve(athlete, epreuve), reverse=True)[:to_add]
    athletes_to_add = random.sample(potential_additions, to_add) + current_contestants
    random.shuffle(athletes_to_add)
    return athletes_to_add


def decathlon_points(event, perf):
    if event == "100m":
        a = 25.4347
        b = 18
        c = 1.81
    elif event == "longueur":
        a = 0.14354
        b = 220
        c = 1.4
        perf *= 100
    elif event == "poids":
        a = 51.39
        b = 1.5
        c = 1.05
    elif event == "hauteur":
        a = 0.8465
        b = 75
        c = 1.42
        perf *= 100
    elif event == "400m":
        a = 1.53775
        b = 82
        c = 1.81
    elif event == "110mh":
        a = 5.74352
        b = 28.5
        c = 1.92
    elif event == "disque":
        a = 12.91
        b = 4
        c = 1.1
    elif event == "perche":
        a = 0.2797
        b = 100
        c = 1.35
        perf *= 100
    elif event == "javelot":
        a = 10.14
        b = 7
        c = 1.08
    elif event == "1500m":
        a = 0.03768
        b = 480
        c = 1.85
    if event in ["100m", "400m", "1500m", "110mh"]:
        return int(a * pow(max(0, b - perf), c))
    else:
        return int(a * pow(max(0, perf - b), c))


def decathlon_quick(athletes_today):
    points = [0] * len(athletes_today)
    cent_metres_points = [decathlon_points("100m", x) for x in cent_metres(athletes_today)]
    longueur_points = [decathlon_points("longueur", x) for x in saut_en_longueur(athletes_today)]
    poids_points = [decathlon_points("poids", x) for x in lancer_poids(athletes_today)]
    hauteur_points = [decathlon_points("hauteur", x) for x in saut_en_hauteur(athletes_today)]
    haies_points = [decathlon_points("110mh", x) for x in cent_dix_metres_haies(athletes_today)]
    quatre_cents_points = [decathlon_points("400m", x) for x in quatre_cent_metres(athletes_today)]
    disque_points = [decathlon_points("disque", x) for x in lancer_disque(athletes_today)]
    perche_points = [decathlon_points("perche", x) for x in saut_perche(athletes_today)]
    javelot_points = [decathlon_points("javelot", x) for x in lancer_javelot(athletes_today)]
    quinze_cent_points = [decathlon_points("1500m", x) for x in quinze_cent_metres(athletes_today)]

    points = [cent_metres_points[i] + longueur_points[i] + poids_points[i] + hauteur_points[i] + haies_points[i]\
               + quatre_cents_points[i] + disque_points[i] + perche_points[i] + javelot_points[i] + quinze_cent_points[i] for i in range(len(points))]

    return points


def time_gap(times):
    return [round(1000 * (times[i + 1] - times[i]), 3) for i in range(len(times) - 1)]


def get_caracs(athlete):
    stats_athlete = []
    for stat in ["acceleration", "speed", "reaction", "resistance", "endurance", "detente", "force", "technique_saut",
                 "technique_lancer", "technique_perche", "technique_haies"]:
        stats_athlete.append(athlete[stat])
    return stats_athlete
