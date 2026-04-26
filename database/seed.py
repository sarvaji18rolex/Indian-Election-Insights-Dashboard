import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "election.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS parties (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    abbr TEXT NOT NULL,
    color TEXT NOT NULL,
    alliance TEXT,
    symbol TEXT,
    founded INTEGER,
    logo TEXT,
    description TEXT
);
CREATE TABLE IF NOT EXISTS states (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    seats INTEGER,
    ruling_party_id INTEGER,
    ruling_since TEXT,
    cm TEXT,
    next_election TEXT,
    population INTEGER,
    literacy REAL,
    region TEXT,
    FOREIGN KEY(ruling_party_id) REFERENCES parties(id)
);
CREATE TABLE IF NOT EXISTS assembly_results (
    id INTEGER PRIMARY KEY,
    state_id INTEGER,
    party_id INTEGER,
    year INTEGER,
    seats_won INTEGER,
    vote_share REAL,
    FOREIGN KEY(state_id) REFERENCES states(id),
    FOREIGN KEY(party_id) REFERENCES parties(id)
);
CREATE TABLE IF NOT EXISTS lok_sabha (
    id INTEGER PRIMARY KEY,
    party_id INTEGER,
    seats_won INTEGER,
    vote_share REAL,
    year INTEGER,
    FOREIGN KEY(party_id) REFERENCES parties(id)
);
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    party_id INTEGER,
    state_id INTEGER,
    constituency TEXT,
    position TEXT,
    age INTEGER,
    education TEXT,
    image TEXT,
    is_cm INTEGER DEFAULT 0,
    is_pm INTEGER DEFAULT 0,
    FOREIGN KEY(party_id) REFERENCES parties(id),
    FOREIGN KEY(state_id) REFERENCES states(id)
);
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY,
    state_id INTEGER,
    party_id INTEGER,
    predicted_seats INTEGER,
    confidence REAL,
    election_year INTEGER,
    factors TEXT,
    FOREIGN KEY(state_id) REFERENCES states(id),
    FOREIGN KEY(party_id) REFERENCES parties(id)
);
"""

PARTIES = [
    (1,"Bharatiya Janata Party","BJP","#FF6B00","NDA","🪷",1980,"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/BJP_symbol.svg/120px-BJP_symbol.svg.png","Ruling party at centre, right-wing nationalist"),
    (2,"Indian National Congress","INC","#19A84B","INDIA","✋",1885,"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Indian_National_Congress_hand_logo.svg/120px-Indian_National_Congress_hand_logo.svg.png","Grand old party, centre-left"),
    (3,"Dravida Munnetra Kazhagam","DMK","#E60026","INDIA","☀️",1949,"https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/DMK_Flag.svg/120px-DMK_Flag.svg.png","Dravidian party ruling Tamil Nadu"),
    (4,"AIADMK","AIADMK","#006400","NDA","🎦",1972,"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/AIADMK_symbol.svg/120px-AIADMK_symbol.svg.png","Main opposition in Tamil Nadu"),
    (5,"Aam Aadmi Party","AAP","#0080FF","INDIA","🧹",2012,"https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Aam_Aadmi_Party_logo.svg/120px-Aam_Aadmi_Party_logo.svg.png","Anti-corruption party, rules Punjab"),
    (6,"Trinamool Congress","TMC","#1A9B8A","INDIA","🌸",1998,"https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/All_India_Trinamool_Congress_Flag.svg/120px-All_India_Trinamool_Congress_Flag.svg.png","Mamata Banerjee's party, rules West Bengal"),
    (7,"YSRCP","YSRCP","#00BFFF","NDA","🎯",2011,"https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/YSRCP_flag.svg/120px-YSRCP_flag.svg.png","Andhra Pradesh regional party"),
    (8,"Telugu Desam Party","TDP","#DAA520","NDA","🚲",1982,"https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Telugu_Desam_Party_logo.svg/120px-Telugu_Desam_Party_logo.svg.png","Rules Andhra Pradesh"),
    (9,"Biju Janata Dal","BJD","#00CED1","Independent","🐚",1997,"https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Biju_Janata_Dal_logo.svg/120px-Biju_Janata_Dal_logo.svg.png","Odisha regional party"),
    (10,"Shiv Sena (UBT)","SS-UBT","#FF6600","INDIA","🏹",1966,"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/ShivSena.svg/120px-ShivSena.svg.png","Maharashtra regional party"),
    (11,"NCP (Sharad Pawar)","NCP-SP","#0000CD","INDIA","⏰",1999,"https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Nationalist_Congress_Party_flag.svg/120px-Nationalist_Congress_Party_flag.svg.png","Maharashtra regional party"),
    (12,"Janata Dal (United)","JDU","#32CD32","NDA","🏺",2003,"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Janata_Dal_United.svg/120px-Janata_Dal_United.svg.png","Bihar regional party, Nitish Kumar"),
    (13,"Rashtriya Janata Dal","RJD","#CC0000","INDIA","🔦",1997,"https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Rashtriya_Janata_Dal.svg/120px-Rashtriya_Janata_Dal.svg.png","Bihar opposition party, Tejashwi Yadav"),
    (14,"Samajwadi Party","SP","#FF0000","INDIA","🚲",1992,"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Samajwadi_Party_Logo.svg/120px-Samajwadi_Party_Logo.svg.png","UP socialist party, Akhilesh Yadav"),
    (15,"Bahujan Samaj Party","BSP","#1C1C1C","None","🐘",1984,"https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/BSP_flag.svg/120px-BSP_flag.svg.png","Dalit-focused party, Mayawati"),
    (16,"CPI (Marxist)","CPI-M","#CC0000","INDIA","⭐",1964,"https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/CPIMLogo.svg/120px-CPIMLogo.svg.png","Left party, rules Kerala"),
    (17,"Jharkhand Mukti Morcha","JMM","#FF4500","INDIA","🌿",1972,"https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Jharkhand_Mukti_Morcha_logo.png/120px-Jharkhand_Mukti_Morcha_logo.png","Tribal party, rules Jharkhand"),
    (18,"National Conference","NC","#4682B4","INDIA","🌐",1932,"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/National_Conference_logo.svg/120px-National_Conference_logo.svg.png","J&K regional party, Omar Abdullah"),
    (19,"Shiv Sena (Shinde)","SS-S","#FF8C00","NDA","🔱",1966,"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/ShivSena.svg/120px-ShivSena.svg.png","Maharashtra NDA ally"),
    (20,"NCP (Ajit Pawar)","NCP-A","#4169E1","NDA","⌚",1999,"https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Nationalist_Congress_Party_flag.svg/120px-Nationalist_Congress_Party_flag.svg.png","Maharashtra NDA ally"),
]

STATES = [
    (1,"Tamil Nadu","TN",234,3,"2021-05","M.K. Stalin","2026-05-01",77841267,80.1,"South"),
    (2,"Uttar Pradesh","UP",403,1,"2022-03","Yogi Adityanath","2027-03-01",199812341,67.7,"North"),
    (3,"Maharashtra","MH",288,1,"2024-11","Devendra Fadnavis","2029-11-01",112374333,82.9,"West"),
    (4,"West Bengal","WB",294,6,"2021-05","Mamata Banerjee","2026-05-01",91276115,76.3,"East"),
    (5,"Bihar","BR",243,12,"2020-11","Nitish Kumar","2025-11-01",104099452,61.8,"East"),
    (6,"Rajasthan","RJ",200,1,"2023-12","Bhajan Lal Sharma","2028-12-01",68548437,66.1,"North"),
    (7,"Madhya Pradesh","MP",230,1,"2023-12","Mohan Yadav","2028-11-01",72626809,69.3,"Central"),
    (8,"Karnataka","KA",224,2,"2023-05","Siddaramaiah","2028-05-01",61095297,75.6,"South"),
    (9,"Gujarat","GJ",182,1,"2022-12","Bhupendrabhai Patel","2027-12-01",60439692,78.0,"West"),
    (10,"Andhra Pradesh","AP",175,8,"2024-06","N. Chandrababu Naidu","2029-05-01",49386799,67.0,"South"),
    (11,"Telangana","TS",119,2,"2023-12","A. Revanth Reddy","2028-11-01",35003674,66.5,"South"),
    (12,"Kerala","KL",140,16,"2021-05","Pinarayi Vijayan","2026-05-01",33406061,94.0,"South"),
    (13,"Odisha","OD",147,1,"2024-06","Mohan Majhi","2029-05-01",41974218,72.9,"East"),
    (14,"Jharkhand","JH",81,17,"2024-11","Hemant Soren","2029-11-01",32988134,66.4,"East"),
    (15,"Punjab","PB",117,5,"2022-03","Bhagwant Mann","2027-02-01",27743338,76.7,"North"),
    (16,"Haryana","HR",90,1,"2024-10","Nayab Singh Saini","2029-10-01",25351462,75.6,"North"),
    (17,"Chhattisgarh","CG",90,1,"2023-12","Vishnu Deo Sai","2028-11-01",25545198,70.3,"Central"),
    (18,"Himachal Pradesh","HP",68,2,"2022-12","Sukhvinder Singh Sukhu","2027-11-01",6864602,82.8,"North"),
    (19,"Uttarakhand","UK",70,1,"2022-03","Pushkar Singh Dhami","2027-02-01",10086292,78.8,"North"),
    (20,"Assam","AS",126,1,"2021-05","Himanta Biswa Sarma","2026-04-01",31205576,72.2,"Northeast"),
    (21,"Jammu & Kashmir","JK",90,18,"2024-10","Omar Abdullah","2029-09-01",12541302,67.2,"North"),
    (22,"Delhi","DL",70,1,"2025-02","Rekha Gupta","2030-02-01",16787941,86.2,"North"),
    (23,"Goa","GA",40,1,"2022-03","Pramod Sawant","2027-02-01",1458545,88.7,"West"),
    (24,"Manipur","MN",60,1,"2022-03","N. Biren Singh","2027-02-01",2855794,76.9,"Northeast"),
    (25,"Tripura","TR",60,1,"2023-02","Manik Saha","2028-02-01",3673917,87.2,"Northeast"),
    (26,"Meghalaya","ML",60,1,"2023-03","Conrad Sangma","2028-02-01",2966889,74.4,"Northeast"),
    (27,"Nagaland","NL",60,1,"2023-02","Neiphiu Rio","2028-02-01",1978502,79.6,"Northeast"),
    (28,"Arunachal Pradesh","AR",60,1,"2024-06","Pema Khandu","2029-04-01",1383727,65.4,"Northeast"),
]

ASSEMBLY = [
    # Tamil Nadu 2021
    (1,1,3,2021,159,45.4),(2,1,4,2021,66,33.3),(3,1,2,2021,18,10.2),(4,1,1,2021,4,2.6),
    # UP 2022
    (5,2,1,2022,255,41.3),(6,2,14,2022,111,32.1),(7,2,15,2022,1,12.9),(8,2,2,2022,2,2.3),
    # West Bengal 2021
    (9,4,6,2021,213,48.0),(10,4,1,2021,77,38.1),(11,4,2,2021,0,2.9),
    # Karnataka 2023
    (12,8,2,2023,135,42.9),(13,8,1,2023,66,36.0),(14,8,14,2023,19,13.3),
    # Rajasthan 2023
    (15,6,1,2023,115,41.7),(16,6,2,2023,69,39.5),
    # MP 2023
    (17,7,1,2023,163,48.6),(18,7,2,2023,66,40.4),
    # Telangana 2023
    (19,11,2,2023,64,39.4),(20,11,1,2023,8,13.9),
    # Chhattisgarh 2023
    (21,17,1,2023,54,46.2),(22,17,2,2023,35,42.2),
    # Bihar 2020
    (23,5,12,2020,43,19.5),(24,5,1,2020,74,19.5),(25,5,13,2020,75,23.1),
    # Maharashtra 2024
    (26,3,1,2024,132,26.8),(27,3,19,2024,57,12.4),(28,3,20,2024,41,10.2),
    (29,3,10,2024,20,9.9),(30,3,11,2024,10,8.1),(31,3,2,2024,16,12.5),
    # AP 2024
    (32,10,8,2024,135,45.6),(33,10,7,2024,11,40.0),
    # Odisha 2024
    (34,13,1,2024,78,40.7),(35,13,9,2024,51,32.9),
    # Jharkhand 2024
    (36,14,17,2024,34,34.3),(37,14,2,2024,16,11.1),(38,14,1,2024,21,33.2),
    # Delhi 2025
    (39,22,1,2025,48,40.6),(40,22,5,2025,22,43.5),
    # Haryana 2024
    (41,16,1,2024,48,39.9),(42,16,2,2024,37,39.1),
    # J&K 2024
    (43,21,18,2024,42,23.4),(44,21,2,2024,6,8.9),(45,21,1,2024,29,25.6),
    # Arunachal 2024
    (46,28,1,2024,46,41.1),
    # Punjab 2022
    (47,15,5,2022,92,42.0),(48,15,1,2022,2,6.6),(49,15,2,2022,18,22.9),
    # Gujarat 2022
    (50,9,1,2022,156,52.5),(51,9,2,2022,17,27.3),(52,9,5,2022,5,12.9),
]

LOK_SABHA = [
    (1,1,240,36.6,2024),(2,2,99,21.2,2024),(3,6,29,3.6,2024),
    (4,14,37,6.7,2024),(5,3,11,1.1,2024),(6,8,16,2.6,2024),
    (7,16,4,0.5,2024),(8,12,12,1.5,2024),(9,5,4,0.4,2024),
    (10,13,4,0.5,2024),(11,18,2,0.3,2024),(12,17,3,0.4,2024),
    (13,15,13,2.1,2024),(14,4,9,1.3,2024),(15,11,4,0.8,2024),
    # 2019 for comparison
    (16,1,303,37.4,2019),(17,2,52,19.5,2019),(18,6,22,4.1,2019),
    (19,14,5,2.5,2019),(20,3,18,2.1,2019),(21,16,3,1.8,2019),
]

CANDIDATES = [
    (1,"Narendra Modi",1,2,"Varanasi","Prime Minister",74,"MA (Pol. Sci.)","https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Narendra_Modi_2023.jpg/220px-Narendra_Modi_2023.jpg",0,1),
    (2,"M.K. Stalin",3,1,"Kolathur","Chief Minister — Tamil Nadu",71,"BA","https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/MK_Stalin_2023.jpg/220px-MK_Stalin_2023.jpg",1,0),
    (3,"Yogi Adityanath",1,2,"Gorakhpur Urban","Chief Minister — Uttar Pradesh",52,"BSc","https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Yogi_Adityanath_2023.jpg/220px-Yogi_Adityanath_2023.jpg",1,0),
    (4,"Mamata Banerjee",6,4,"Bhawanipore","Chief Minister — West Bengal",69,"BA LLB","https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Mamata_Banerjee_2021.jpg/220px-Mamata_Banerjee_2021.jpg",1,0),
    (5,"Siddaramaiah",2,8,"Varuna","Chief Minister — Karnataka",76,"BL","https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Siddaramaiah_2023.jpg/220px-Siddaramaiah_2023.jpg",1,0),
    (6,"Nitish Kumar",12,5,"Nalanda","Chief Minister — Bihar",73,"BE","https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Nitish_Kumar_2022.jpg/220px-Nitish_Kumar_2022.jpg",1,0),
    (7,"Pinarayi Vijayan",16,12,"Dharmadom","Chief Minister — Kerala",79,"BA","https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Pinarayi_Vijayan_2023.jpg/220px-Pinarayi_Vijayan_2023.jpg",1,0),
    (8,"Bhagwant Mann",5,15,"Dhuri","Chief Minister — Punjab",50,"BA","https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Bhagwant_Mann_2022.jpg/220px-Bhagwant_Mann_2022.jpg",1,0),
    (9,"N. Chandrababu Naidu",8,10,"Kuppam","Chief Minister — Andhra Pradesh",74,"MBA","https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nara_Chandrababu_Naidu_2022.jpg/220px-Nara_Chandrababu_Naidu_2022.jpg",1,0),
    (10,"Devendra Fadnavis",1,3,"Nagpur South West","Chief Minister — Maharashtra",54,"LLB","https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Devendra_Fadnavis.jpg/220px-Devendra_Fadnavis.jpg",1,0),
    (11,"Rahul Gandhi",2,8,"Wayanad / Rae Bareli","Leader of Opposition (Lok Sabha)",54,"MPhil","https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Rahul_Gandhi_2019.jpg/220px-Rahul_Gandhi_2019.jpg",0,0),
    (12,"Udhayanidhi Stalin",3,1,"Chepauk-Thiruvallikeni","Dy. CM — Tamil Nadu",47,"BBA","https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Udhayanidhi_Stalin_2022.jpg/220px-Udhayanidhi_Stalin_2022.jpg",0,0),
    (13,"Edappadi K. Palaniswami",4,1,"Edappadi","Leader of Opposition — Tamil Nadu",71,"BSc Agri","https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Edappadi_K._Palaniswami_2023.jpg/220px-Edappadi_K._Palaniswami_2023.jpg",0,0),
    (14,"A. Revanth Reddy",2,11,"Kodangal","Chief Minister — Telangana",55,"BA","https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Revanth_Reddy.jpg/220px-Revanth_Reddy.jpg",1,0),
    (15,"Hemant Soren",17,14,"Barhait","Chief Minister — Jharkhand",48,"12th Pass","https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Hemant_Soren.jpg/220px-Hemant_Soren.jpg",1,0),
    (16,"Omar Abdullah",18,21,"Ganderbal / Budgam","Chief Minister — J&K",54,"BSc","https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Omar_Abdullah_2022.jpg/220px-Omar_Abdullah_2022.jpg",1,0),
    (17,"Mohan Majhi",1,13,"Keonjhar","Chief Minister — Odisha",52,"BA","https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Mohan_Majhi.jpg/220px-Mohan_Majhi.jpg",1,0),
    (18,"Sukhvinder Singh Sukhu",2,18,"Nadaun","Chief Minister — Himachal Pradesh",60,"MA","https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Sukhvinder_Singh_Sukhu.jpg/220px-Sukhvinder_Singh_Sukhu.jpg",1,0),
]

PREDICTIONS = [
    (1,1,3,145,72,"2026","Strong incumbency, welfare schemes (Kalaignar Magalir Urimai), anti-NDA Tamil sentiment, Udhayanidhi factor"),
    (2,1,4,80,65,"2026","Unified AIADMK under EPS, OPS exit hurts, sympathy factor for Jayalalithaa legacy"),
    (3,1,1,5,35,"2026","NDA alliance limited in TN, BJP unlikely to gain beyond 5 seats alone"),
    (4,4,6,180,70,"2026","Mamata brand very strong, cut-money complaints declining, women voters remain loyal"),
    (5,4,1,110,62,"2026","Central schemes push, Ram Mandir benefit, strong org in north Bengal"),
    (6,5,12,80,55,"2025","JDU-NDA alliance holds, Nitish Kumar incumbency advantage"),
    (7,5,1,88,55,"2025","BJP strong in upper Bihar, NDA seat sharing critical"),
    (8,5,13,65,52,"2025","RJD-MY combine resilient, Tejashwi youth appeal"),
    (9,None,1,260,60,"2029","PM Modi popularity, NDA unity, development narrative, welfare delivery"),
    (10,None,2,115,50,"2029","INDIA bloc if united, Rahul Gandhi sustained campaign, anti-incumbency risk for BJP"),
    (11,None,14,50,57,"2029","SP strong in UP under Akhilesh, INDIA bloc coordination key"),
    (12,12,16,80,65,"2026","LDF strong on welfare, Pinarayi Vijayan competent governance image"),
    (13,12,2,55,58,"2026","UDF Congress-led alliance, anti-incumbency benefit"),
]

def seed():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.executemany("INSERT OR REPLACE INTO parties VALUES(?,?,?,?,?,?,?,?,?)", PARTIES)
    conn.executemany("INSERT OR REPLACE INTO states VALUES(?,?,?,?,?,?,?,?,?,?,?)", STATES)
    conn.executemany("INSERT OR REPLACE INTO assembly_results VALUES(?,?,?,?,?,?)", ASSEMBLY)
    conn.executemany("INSERT OR REPLACE INTO lok_sabha VALUES(?,?,?,?,?)", LOK_SABHA)
    conn.executemany("INSERT OR REPLACE INTO candidates VALUES(?,?,?,?,?,?,?,?,?,?,?)", CANDIDATES)
    conn.executemany("INSERT OR REPLACE INTO predictions VALUES(?,?,?,?,?,?,?)", PREDICTIONS)
    conn.commit()
    conn.close()
    print("✅  Database seeded →", DB_PATH)

if __name__ == "__main__":
    seed()
