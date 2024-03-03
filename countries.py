import pickle

with open('real_countries.pickle', 'rb') as handle:
    countries = pickle.load(handle)

sprintistan = {
        "name": "Sprintistan",
        "Sprinter": 10,
        "Middle-distance": 10,
        "Long-distance": 10,
        "Hurdler": 10,
        "Thrower": 10,
        "Jumper": 10,
        "Pole vaulter": 10,
        "Decathlete": 10,
        "national_best": {
            "100m": ["", "", ""],
            "200m": ["", "", ""],
            "400m": ["", "", ""],
            "800m": ["", "", ""],
            "1500m": ["", "", ""],
            "5000m": ["", "", ""],
            "10000m": ["", "", ""],
            "110mh": ["", "", ""],
            "longueur": ["", "", ""],
            "hauteur": ["", "", ""],
            "perche": ["", "", ""],
            "disque": ["", "", ""],
            "poids": ["", "", ""],
            "javelot": ["", "", ""],
            "triplesaut": ["", "", ""],
            "decathlon": ["", "", ""]
        }
    }
countries.append(sprintistan)

min_stds, max_stds = {}, {}


dict_profiles = {
    "Sprinter": "sprinteur",
    "Middle-distance": "demi fond",
    "Long-distance": "fond",
    "Thrower": "lanceur",
    "Jumper": "sauteur",
    "Pole vaulter": "perchiste",
    "Hurdler": "hurdler",
    "Decathlete": "combine"
}
type_profiles = ["Sprinter", "Middle-distance", "Long-distance", "Thrower", "Jumper", "Pole vaulter", "Hurdler", "Decathlete"]
real_countries = [x for x in countries if x["name"] != "Sprintistan"]
for profile in type_profiles:
    min_stds[profile] = min([x[dict_profiles[profile]] for x in real_countries])
    max_stds[profile] = max([x[dict_profiles[profile]] for x in real_countries])


for country in real_countries:
    for profile in type_profiles:
        country[profile] = round(85 * (country[dict_profiles[profile]] - min_stds[profile]) / (max_stds[profile] - min_stds[profile]), 1)