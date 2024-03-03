minimas = {
    "D": {
            "100m": 16,
            "200m": 30,
            "400m": 65,
            "800m": 180,
            "1500m": 350,
            "5000m": 1200,
            "10000m": 2500,
            "110mh": 17,
            "longueur": 4.5,
            "hauteur": 1.5,
            "perche": 3.75,
            "disque": 30,
            "poids": 10,
            "javelot": 40,
            "triplesaut": 10,
            "decathlon": 3500
    },
    "C": {
            "100m": 13.5,
            "200m": 26,
            "400m": 57.5,
            "800m": 150,
            "1500m": 310,
            "5000m": 1050,
            "10000m": 2300,
            "110mh": 15.5,
            "longueur": 6,
            "hauteur": 1.8,
            "perche": 4.5,
            "disque": 40,
            "poids": 13,
            "javelot": 50,
            "triplesaut": 13,
            "decathlon": 5000
    },
    "B": {
            "100m": 12,
            "200m": 23,
            "400m": 51,
            "800m": 125,
            "1500m": 275,
            "5000m": 900,
            "10000m": 2000,
            "110mh": 14.25,
            "longueur": 7.25,
            "hauteur": 2.05,
            "perche": 5.2,
            "disque": 50,
            "poids": 16,
            "javelot": 60,
            "triplesaut": 15,
            "decathlon": 6500
    },
    "A": {
            "100m": 11,
            "200m": 21.5,
            "400m": 48,
            "800m": 112.5,
            "1500m": 250,
            "5000m": 825,
            "10000m": 1800,
            "110mh": 13.6,
            "longueur": 7.5,
            "hauteur": 2.2,
            "perche": 5.5,
            "disque": 57.5,
            "poids": 18,
            "javelot": 70,
            "triplesaut": 16,
            "decathlon": 7500
    },
    "S": {
        "100m": 10.5,
        "200m": 20.5,
        "400m": 46.5,
        "800m": 110,
        "1500m": 235,
        "5000m": 800,
        "10000m": 1700,
        "110mh": 13.3,
        "longueur": 7.8,
        "hauteur": 2.28,
        "perche": 5.7,
        "disque": 62,
        "poids": 20,
        "javelot": 78.5,
        "triplesaut": 16.75,
        "decathlon": 8000
    }
}

tournaments = [
    {
        "name": "Meeting de Jaipur",
        "category": "E",
        "semaine": 1,
        "epreuves": ["100m", "200m", "400m", "110mh"],
        "tag": "sprint",
        "over": False
    },
    {
        "name": "Meeting de Makassar",
        "category": "E",
        "semaine": 2,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Rawalpindi",
        "category": "E",
        "semaine": 3,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Rostov",
        "category": "E",
        "semaine": 4,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Alger",
        "category": "E",
        "semaine": 8,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting de Milan",
        "category": "E",
        "semaine": 9,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Quanzhou",
        "category": "E",
        "semaine": 10,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Rosario",
        "category": "E",
        "semaine": 11,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Quezon",
        "category": "E",
        "semaine": 12,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Tijuana",
        "category": "E",
        "semaine": 14,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche"],
        "tag": "jumps",
        "over": False
    },
    {
        "name": "Meeting de Yaoundé",
        "category": "E",
        "semaine": 15,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Phnom Penh",
        "category": "E",
        "semaine": 17,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Shenyang",
        "category": "E",
        "semaine": 20,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Bangkok",
        "category": "E",
        "semaine": 25,
        "epreuves": ["100m", "200m", "400m", "110mh"],
        "tag": "sprint",
        "over": False
    },
    {
        "name": "Meeting de Gujranwala",
        "category": "E",
        "semaine": 26,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Shantou",
        "category": "E",
        "semaine": 28,
        "epreuves": ["poids", "disque", "javelot", "800m", "1500m", "5000m", "10000m"],
        "tag": "throws, endurance",
        "over": False
    },
    {
        "name": "Meeting de Philadelphia",
        "category": "E",
        "semaine": 29,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Nanjing",
        "category": "E",
        "semaine": 32,
        "epreuves": ["100m", "110mh", "200m", "400m", "longueur", "hauteur", "perche", "triplesaut"],
        "tag": "sprint, jumps",
        "over": False
    },
    {
        "name": "Meeting de Ningbo",
        "category": "E",
        "semaine": 33,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Sofia",
        "category": "E",
        "semaine": 34,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Fukuoka",
        "category": "E",
        "semaine": 35,
        "epreuves": ["100m", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Birmingham",
        "category": "E",
        "semaine": 36,
        "epreuves": ["100m", "110mh", "200m", "400m", "longueur", "hauteur", "perche", "triplesaut"],
        "tag": "sprint, jumps",
        "over": False
    },
    {
        "name": "Meeting de Faisalabad",
        "category": "E",
        "semaine": 40,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Gdansk",
        "category": "E",
        "semaine": 41,
        "epreuves": ["poids", "disque", "javelot"],
        "tag": "throws",
        "over": False
    },
    {
        "name": "Meeting de Nagpur",
        "category": "E",
        "semaine": 42,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Munich",
        "category": "E",
        "semaine": 45,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting d'Ekaterinburg",
        "category": "E",
        "semaine": 46,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting d'Auckland",
        "category": "E",
        "semaine": 47,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting d'Ispahan",
        "category": "E",
        "semaine": 50,
        "epreuves": ["poids", "disque", "javelot"],
        "tag": "throws",
        "over": False
    },
    {
        "name": "Meeting de Cestas",
        "category": "E",
        "semaine": 52,
        "epreuves": ["100m", "110mh", "200m", "400m", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Lucknow",
        "category": "D",
        "semaine": 9,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Ekurhuleni",
        "category": "D",
        "semaine": 46,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Mandalay",
        "category": "D",
        "semaine": 51,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Taipei",
        "category": "D",
        "semaine": 28,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Dhaka",
        "category": "D",
        "semaine": 14,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting de Managua",
        "category": "D",
        "semaine": 3,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Budapest",
        "category": "D",
        "semaine": 43,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Guadalajara",
        "category": "D",
        "semaine": 6,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Ahvaz",
        "category": "D",
        "semaine": 37,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Brisbane",
        "category": "D",
        "semaine": 31,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Riyad",
        "category": "D",
        "semaine": 13,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Surabaya",
        "category": "D",
        "semaine": 12,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting d'Addis Abeba",
        "category": "D",
        "semaine": 32,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Tianjin",
        "category": "D",
        "semaine": 23,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting du Cap",
        "category": "D",
        "semaine": 29,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Varsovie",
        "category": "D",
        "semaine": 16,
        "epreuves": ["poids", "disque", "javelot", "800m", "1500m", "5000m", "10000m"],
        "tag": "throws, endurance",
        "over": False
    },
    {
        "name": "Meeting de New Delhi",
        "category": "D",
        "semaine": 26,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Santa Cruz",
        "category": "D",
        "semaine": 27,
        "epreuves": ["100m", "110mh", "200m", "400m", "longueur", "hauteur", "perche", "triplesaut"],
        "tag": "sprint, jumps",
        "over": False
    },
    {
        "name": "Meeting de Daegu",
        "category": "D",
        "semaine": 35,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Minsk",
        "category": "D",
        "semaine": 4,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Manille",
        "category": "D",
        "semaine": 50,
        "epreuves": ["100m", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Douala",
        "category": "D",
        "semaine": 39,
        "epreuves": ["100m", "110mh", "200m", "400m", "longueur", "hauteur", "perche", "triplesaut"],
        "tag": "sprint, jumps",
        "over": False
    },
    {
        "name": "Meeting de Bogota",
        "category": "D",
        "semaine": 10,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Tashkent",
        "category": "D",
        "semaine": 19,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Montevideo",
        "category": "D",
        "semaine": 47,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Brasilia",
        "category": "C",
        "semaine": 18,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Kano",
        "category": "C",
        "semaine": 41,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Brazzaville",
        "category": "C",
        "semaine": 33,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Kobe",
        "category": "C",
        "semaine": 20,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting d'Izmir",
        "category": "C",
        "semaine": 51,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting de Toronto",
        "category": "C",
        "semaine": 19,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Kyoto",
        "category": "C",
        "semaine": 3,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Bandung",
        "category": "C",
        "semaine": 7,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Dar es Salaam",
        "category": "C",
        "semaine": 8,
        "epreuves": ["poids", "disque", "javelot"],
        "tag": "throws",
        "over": False
    },
    {
        "name": "Meeting d'Hiroshima",
        "category": "C",
        "semaine": 17,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting d'Omsk",
        "category": "C",
        "semaine": 40,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Harare",
        "category": "C",
        "semaine": 4,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Kwangju",
        "category": "C",
        "semaine": 29,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Dubai",
        "category": "C",
        "semaine": 32,
        "epreuves": ["100m", "200m", "400m", "110mh"],
        "tag": "sprint",
        "over": False
    },
    {
        "name": "Meeting de Kuala Lumpur",
        "category": "C",
        "semaine": 48,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Novosibirsk",
        "category": "C",
        "semaine": 22,
        "epreuves": ["poids", "disque", "javelot", "800m", "1500m", "5000m", "10000m"],
        "tag": "throws, endurance",
        "over": False
    },
    {
        "name": "Meeting de Bagdad",
        "category": "C",
        "semaine": 42,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de San Diego",
        "category": "C",
        "semaine": 12,
        "epreuves": ["100m", "110mh", "200m", "400m", "longueur", "hauteur", "perche", "triplesaut"],
        "tag": "sprint, jumps",
        "over": False
    },
    {
        "name": "Meeting de Tbilissi",
        "category": "C",
        "semaine": 24,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Los Angeles",
        "category": "C",
        "semaine": 6,
        "epreuves": ["poids", "disque", "javelot"],
        "tag": "throws",
        "over": False
    },
    {
        "name": "Meeting de Jakarta",
        "category": "B",
        "semaine": 1,
        "epreuves": ["100m", "200m", "400m", "110mh"],
        "tag": "sprint",
        "over": False
    },
    {
        "name": "Meeting de La Havane",
        "category": "B",
        "semaine": 35,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Dallas",
        "category": "B",
        "semaine": 38,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Lagos",
        "category": "B",
        "semaine": 13,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Téhéran",
        "category": "B",
        "semaine": 7,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting d'Astana",
        "category": "B",
        "semaine": 14,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot"],
        "tag": "sprint, throws",
        "over": False
    },
    {
        "name": "Meeting de Kinshasa",
        "category": "B",
        "semaine": 21,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Hong Kong",
        "category": "B",
        "semaine": 46,
        "epreuves": ["800m", "1500m", "5000m", "10000m"],
        "tag": "endurance",
        "over": False
    },
    {
        "name": "Meeting de Tripoli",
        "category": "B",
        "semaine": 30,
        "epreuves": ["poids", "disque", "javelot", "decathlon"],
        "tag": "throws, combine",
        "over": False
    },
    {
        "name": "Meeting de Saint-Petersbourg",
        "category": "B",
        "semaine": 17,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche"],
        "tag": "jumps",
        "over": False
    },
    {
        "name": "Meeting de Vienne",
        "category": "B",
        "semaine": 51,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Rio de Janeiro",
        "category": "B",
        "semaine": 45,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Prague",
        "category": "B",
        "semaine": 16,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Houston",
        "category": "B",
        "semaine": 18,
        "epreuves": ["100m", "200m", "400m", "110mh", "decathlon"],
        "tag": "sprint, combine",
        "over": False
    },
    {
        "name": "Meeting de Buenos Aires",
        "category": "B",
        "semaine": 5,
        "epreuves": ["longueur", "hauteur", "perche", "triplesaut"],
        "tag": "jumps",
        "over": False
    },
    {
        "name": "Meeting de Barcelone",
        "category": "A",
        "semaine": 34,
        "epreuves": ["100m", "200m", "400m", "110mh", "800m", "1500m", "5000m", "10000m"],
        "tag": "sprint, endurance",
        "over": False
    },
    {
        "name": "Meeting de Sapporo",
        "category": "A",
        "semaine": 38,
        "epreuves": ["longueur", "triplesaut", "hauteur", "perche", "disque", "poids", "javelot"],
        "tag": "jumps, throws",
        "over": False
    },
    {
        "name": "Meeting de Seoul",
        "category": "A",
        "semaine": 12,
        "epreuves": ["poids", "disque", "javelot", "800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "throws, endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Singapour",
        "category": "A",
        "semaine": 46,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "sprint, endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Maputo",
        "category": "A",
        "semaine": 2,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "800m", "1500m", "5000m", "10000m"],
        "tag": "jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting de Ouagadougou",
        "category": "A",
        "semaine": 24,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot", "decathlon"],
        "tag": "sprint, throws, combine",
        "over": False
    },
    {
        "name": "Meeting du Caire",
        "category": "A",
        "semaine": 10,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "sprint, endurance, combine",
        "over": False
    },
    {
        "name": "Meeting d'Ankara",
        "category": "A",
        "semaine": 26,
        "epreuves": ["800m", "1500m", "5000m", "10000m", "longueur", "hauteur", "triplesaut", "perche"],
        "tag": "endurance, jumps",
        "over": False
    },
    {
        "name": "Meeting de Berlin",
        "category": "A",
        "semaine": 39,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "poids", "disque", "javelot"],
        "tag": "throws, jumps",
        "over": False
    },
    {
        "name": "Meeting de Tokyo",
        "category": "A",
        "semaine": 49,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "decathlon"],
        "tag": "jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Paris",
        "category": "S",
        "semaine": 46,
        "epreuves": ["100m", "110mh", "200m", "400m", "poids", "disque", "javelot", "longueur", "hauteur", "triplesaut", "perche", "decathlon"],
        "tag": "sprint, throws, jumps, combine",
        "over": False
    },
    {
        "name": "Meeting de Madrid",
        "category": "S",
        "semaine": 52,
        "epreuves": ["100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "longueur", "hauteur", "triplesaut", "perche"],
        "tag": "sprint, jumps, endurance",
        "over": False
    },
    {
        "name": "Meeting de Pékin",
        "category": "S",
        "semaine": 23,
        "epreuves": ["poids", "disque", "javelot", "800m", "1500m", "5000m", "10000m", "longueur", "hauteur", "triplesaut", "perche", "decathlon"],
        "tag": "throws, jumps, endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Lima",
        "category": "S",
        "semaine": 18,
        "epreuves": ["poids", "disque", "javelot", "100m", "110mh", "200m", "400m", "800m", "1500m", "5000m", "10000m", "decathlon"],
        "tag": "throws, sprint, endurance, combine",
        "over": False
    },
    {
        "name": "Meeting de Sydney",
        "category": "S",
        "semaine": 8,
        "epreuves": ["longueur", "hauteur", "triplesaut", "perche", "poids", "disque", "javelot", "100m", "110mh", "200m", "400m", "decathlon"],
        "tag": "jumps, sprint, throws, combine",
        "over": False
    }
    ]