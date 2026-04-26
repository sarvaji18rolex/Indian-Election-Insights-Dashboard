import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'election.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # ─── TABLES ────────────────────────────────────────────────────────────────
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS parties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        abbreviation TEXT NOT NULL,
        color TEXT NOT NULL,
        alliance TEXT,
        symbol TEXT,
        founded_year INTEGER,
        logo_url TEXT,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL,
        total_seats INTEGER,
        ruling_party_id INTEGER,
        ruling_since TEXT,
        cm_name TEXT,
        next_election TEXT,
        population INTEGER,
        literacy_rate REAL,
        region TEXT,
        FOREIGN KEY(ruling_party_id) REFERENCES parties(id)
    );

    CREATE TABLE IF NOT EXISTS election_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_id INTEGER,
        party_id INTEGER,
        election_year INTEGER,
        election_type TEXT,
        seats_won INTEGER,
        vote_share REAL,
        FOREIGN KEY(state_id) REFERENCES states(id),
        FOREIGN KEY(party_id) REFERENCES parties(id)
    );

    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        party_id INTEGER,
        state_id INTEGER,
        constituency TEXT,
        position TEXT,
        age INTEGER,
        education TEXT,
        image_url TEXT,
        is_cm INTEGER DEFAULT 0,
        is_pm INTEGER DEFAULT 0,
        votes_received INTEGER,
        FOREIGN KEY(party_id) REFERENCES parties(id),
        FOREIGN KEY(state_id) REFERENCES states(id)
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_id INTEGER,
        party_id INTEGER,
        predicted_seats INTEGER,
        confidence_pct REAL,
        prediction_year INTEGER,
        factors TEXT,
        FOREIGN KEY(state_id) REFERENCES states(id),
        FOREIGN KEY(party_id) REFERENCES parties(id)
    );

    CREATE TABLE IF NOT EXISTS lok_sabha (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        party_id INTEGER,
        seats_won INTEGER,
        total_seats INTEGER,
        vote_share REAL,
        election_year INTEGER,
        FOREIGN KEY(party_id) REFERENCES parties(id)
    );
    """)

    # ─── PARTIES ───────────────────────────────────────────────────────────────
    parties = [
        (1, 'Bharatiya Janata Party', 'BJP', '#FF6B00', 'NDA', '🪷', 1980,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/BJP_symbol.svg/200px-BJP_symbol.svg.png',
         'Right-wing nationalist party, currently ruling at centre'),
        (2, 'Indian National Congress', 'INC', '#00A651', 'INDIA', '✋', 1885,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Indian_National_Congress_hand_logo.svg/200px-Indian_National_Congress_hand_logo.svg.png',
         'Grand old party of India, centre-left ideology'),
        (3, 'Dravida Munnetra Kazhagam', 'DMK', '#E60026', 'INDIA', '☀️', 1949,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/DMK_Flag.svg/200px-DMK_Flag.svg.png',
         'Dravidian party ruling Tamil Nadu'),
        (4, 'All India Anna Dravida Munnetra Kazhagam', 'AIADMK', '#006400', 'NDA', '🎦', 1972,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/AIADMK_symbol.svg/200px-AIADMK_symbol.svg.png',
         'Dravidian party, main opposition in Tamil Nadu'),
        (5, 'Aam Aadmi Party', 'AAP', '#0080FF', 'INDIA', '🧹', 2012,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Aam_Aadmi_Party_logo.svg/200px-Aam_Aadmi_Party_logo.svg.png',
         'Anti-corruption party ruling Delhi and Punjab'),
        (6, 'Trinamool Congress', 'TMC', '#20B2AA', 'INDIA', '🌸', 1998,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/All_India_Trinamool_Congress_Flag.svg/200px-All_India_Trinamool_Congress_Flag.svg.png',
         'Regional party ruling West Bengal'),
        (7, 'Yuvajana Sramika Rythu Congress Party', 'YSRCP', '#00BFFF', 'NDA', '🎯', 2011,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/YSRCP_flag.svg/200px-YSRCP_flag.svg.png',
         'Regional party of Andhra Pradesh'),
        (8, 'Telugu Desam Party', 'TDP', '#FFFF00', 'NDA', '🚲', 1982,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Telugu_Desam_Party_logo.svg/200px-Telugu_Desam_Party_logo.svg.png',
         'Regional party of Andhra Pradesh'),
        (9, 'Biju Janata Dal', 'BJD', '#00CED1', 'NDA', '🐚', 1997,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Biju_Janata_Dal_logo.svg/200px-Biju_Janata_Dal_logo.svg.png',
         'Regional party ruling Odisha'),
        (10, 'Shiv Sena (UBT)', 'SS-UBT', '#FF6600', 'INDIA', '🏹', 1966,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/ShivSena.svg/200px-ShivSena.svg.png',
         'Regional party of Maharashtra'),
        (11, 'Nationalist Congress Party (SP)', 'NCP-SP', '#0000CD', 'INDIA', '⏰', 1999,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Nationalist_Congress_Party_flag.svg/200px-Nationalist_Congress_Party_flag.svg.png',
         'Regional party of Maharashtra'),
        (12, 'Janata Dal (United)', 'JDU', '#32CD32', 'NDA', '🏺', 2003,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Janata_Dal_United.svg/200px-Janata_Dal_United.svg.png',
         'Regional party ruling Bihar'),
        (13, 'Rashtriya Janata Dal', 'RJD', '#FF0000', 'INDIA', '🔦', 1997,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Rashtriya_Janata_Dal.svg/200px-Rashtriya_Janata_Dal.svg.png',
         'Regional party of Bihar'),
        (14, 'Samajwadi Party', 'SP', '#FF0000', 'INDIA', '🚲', 1992,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Samajwadi_Party_Logo.svg/200px-Samajwadi_Party_Logo.svg.png',
         'Socialist party of Uttar Pradesh'),
        (15, 'Bahujan Samaj Party', 'BSP', '#1C1C1C', 'None', '🐘', 1984,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/BSP_flag.svg/200px-BSP_flag.svg.png',
         'Dalit-focused party of Uttar Pradesh'),
        (16, 'Communist Party of India (Marxist)', 'CPI(M)', '#CC0000', 'INDIA', '⭐', 1964,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/CPIMLogo.svg/200px-CPIMLogo.svg.png',
         'Left party ruling Kerala'),
        (17, 'Indian Union Muslim League', 'IUML', '#00875A', 'INDIA', '🌙', 1948,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Indian_Union_Muslim_League_logo.svg/200px-Indian_Union_Muslim_League_logo.svg.png',
         'Muslim minority party of Kerala'),
        (18, 'Jharkhand Mukti Morcha', 'JMM', '#FF4500', 'INDIA', '🌿', 1972,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Jharkhand_Mukti_Morcha_logo.png/200px-Jharkhand_Mukti_Morcha_logo.png',
         'Tribal party ruling Jharkhand'),
        (19, 'Shiromani Akali Dal', 'SAD', '#00008B', 'NDA', '⚖️', 1920,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/ShiromaniAkaliDal.svg/200px-ShiromaniAkaliDal.svg.png',
         'Sikh party of Punjab'),
        (20, 'National Conference', 'NC', '#4682B4', 'INDIA', '🌐', 1932,
         'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/National_Conference_logo.svg/200px-National_Conference_logo.svg.png',
         'Regional party of Jammu & Kashmir'),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO parties 
        (id,name,abbreviation,color,alliance,symbol,founded_year,logo_url,description)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, parties)

    # ─── STATES ────────────────────────────────────────────────────────────────
    states = [
        # (id, name, code, total_seats, ruling_party_id, ruling_since, cm_name, next_election, population, literacy, region)
        (1,  'Tamil Nadu',         'TN',  234, 3,  '2021', 'M.K. Stalin',          '2026-04-01', 77841267,  80.1, 'South'),
        (2,  'Uttar Pradesh',      'UP',  403, 1,  '2022', 'Yogi Adityanath',       '2027-04-01', 199812341, 67.7, 'North'),
        (3,  'Maharashtra',        'MH',  288, 1,  '2024', 'Devendra Fadnavis',     '2029-04-01', 112374333, 82.9, 'West'),
        (4,  'West Bengal',        'WB',  294, 6,  '2021', 'Mamata Banerjee',        '2026-04-01', 91276115,  76.3, 'East'),
        (5,  'Bihar',              'BR',  243, 12, '2020', 'Nitish Kumar',           '2025-11-01', 104099452, 61.8, 'East'),
        (6,  'Rajasthan',          'RJ',  200, 1,  '2023', 'Bhajan Lal Sharma',      '2028-12-01', 68548437,  66.1, 'North'),
        (7,  'Madhya Pradesh',     'MP',  230, 1,  '2023', 'Mohan Yadav',            '2028-11-01', 72626809,  69.3, 'Central'),
        (8,  'Karnataka',          'KA',  224, 2,  '2023', 'Siddaramaiah',           '2028-05-01', 61095297,  75.6, 'South'),
        (9,  'Gujarat',            'GJ',  182, 1,  '2022', 'Bhupendrabhai Patel',    '2027-12-01', 60439692,  78.0, 'West'),
        (10, 'Andhra Pradesh',     'AP',  175, 8,  '2024', 'N. Chandrababu Naidu',   '2029-05-01', 49386799,  67.0, 'South'),
        (11, 'Telangana',          'TS',  119, 2,  '2023', 'A. Revanth Reddy',       '2028-11-01', 35003674,  66.5, 'South'),
        (12, 'Kerala',             'KL',  140, 16, '2021', 'Pinarayi Vijayan',       '2026-04-01', 33406061,  94.0, 'South'),
        (13, 'Odisha',             'OD',  147, 1,  '2024', 'Mohan Majhi',            '2029-04-01', 41974218,  72.9, 'East'),
        (14, 'Jharkhand',          'JH',  81,  18, '2024', 'Hemant Soren',           '2029-11-01', 32988134,  66.4, 'East'),
        (15, 'Punjab',             'PB',  117, 5,  '2022', 'Bhagwant Mann',          '2027-02-01', 27743338,  76.7, 'North'),
        (16, 'Haryana',            'HR',  90,  1,  '2024', 'Nayab Singh Saini',      '2029-10-01', 25351462,  75.6, 'North'),
        (17, 'Chhattisgarh',       'CG',  90,  1,  '2023', 'Vishnu Deo Sai',         '2028-11-01', 25545198,  70.3, 'Central'),
        (18, 'Himachal Pradesh',   'HP',  68,  2,  '2022', 'Sukhvinder Singh Sukhu', '2027-11-01', 6864602,   82.8, 'North'),
        (19, 'Uttarakhand',        'UK',  70,  1,  '2022', 'Pushkar Singh Dhami',    '2027-02-01', 10086292,  78.8, 'North'),
        (20, 'Assam',              'AS',  126, 1,  '2021', 'Himanta Biswa Sarma',    '2026-04-01', 31205576,  72.2, 'Northeast'),
        (21, 'Jammu & Kashmir',    'JK',  90,  20, '2024', 'Omar Abdullah',          '2029-09-01', 12541302,  67.2, 'North'),
        (22, 'Delhi',              'DL',  70,  1,  '2025', 'Rekha Gupta',            '2030-02-01', 16787941,  86.2, 'North'),
        (23, 'Goa',                'GA',  40,  1,  '2022', 'Pramod Sawant',           '2027-02-01', 1458545,   88.7, 'West'),
        (24, 'Manipur',            'MN',  60,  1,  '2022', 'N. Biren Singh',          '2027-02-01', 2855794,   76.9, 'Northeast'),
        (25, 'Tripura',            'TR',  60,  1,  '2023', 'Manik Saha',              '2028-02-01', 3673917,   87.2, 'Northeast'),
        (26, 'Meghalaya',          'ML',  60,  1,  '2023', 'Conrad Sangma',           '2028-02-01', 2966889,   74.4, 'Northeast'),
        (27, 'Nagaland',           'NL',  60,  1,  '2023', 'Neiphiu Rio',             '2028-02-01', 1978502,   79.6, 'Northeast'),
        (28, 'Arunachal Pradesh',  'AR',  60,  1,  '2024', 'Pema Khandu',             '2029-04-01', 1383727,   65.4, 'Northeast'),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO states
        (id,name,code,total_seats,ruling_party_id,ruling_since,cm_name,next_election,population,literacy_rate,region)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, states)

    # ─── ELECTION RESULTS ──────────────────────────────────────────────────────
    results = [
        # Tamil Nadu 2021
        (1,1,3,2021,'State',159,45.4), (2,1,4,2021,'State',66,33.3), (3,1,2,2021,'State',18,10.2),
        (4,1,1,2021,'State',4,2.6),   (5,1,5,2021,'State',6,4.0),

        # Uttar Pradesh 2022
        (6,2,1,2022,'State',255,41.3), (7,2,14,2022,'State',111,32.1), (8,2,15,2022,'State',1,12.9),
        (9,2,2,2022,'State',2,2.3),

        # West Bengal 2021
        (10,4,6,2021,'State',213,48.0), (11,4,1,2021,'State',77,38.1), (12,4,2,2021,'State',0,2.9),

        # Karnataka 2023
        (13,8,2,2023,'State',135,42.9), (14,8,1,2023,'State',66,36.0), (15,8,14,2023,'State',19,13.3),

        # Rajasthan 2023
        (16,6,1,2023,'State',115,41.7), (17,6,2,2023,'State',69,39.5),

        # Madhya Pradesh 2023
        (18,7,1,2023,'State',163,48.6), (19,7,2,2023,'State',66,40.4),

        # Telangana 2023
        (20,11,2,2023,'State',64,39.4), (21,11,1,2023,'State',8,13.9),

        # Chhattisgarh 2023
        (22,17,1,2023,'State',54,46.2), (23,17,2,2023,'State',35,42.2),

        # Bihar 2020
        (24,5,12,2020,'State',43,19.5), (25,5,1,2020,'State',74,19.5), (26,5,13,2020,'State',75,23.1),

        # Maharashtra 2024
        (27,3,1,2024,'State',132,26.8), (28,3,10,2024,'State',20,9.9), (29,3,11,2024,'State',10,8.1),

        # Andhra Pradesh 2024
        (30,10,8,2024,'State',135,45.6), (31,10,7,2024,'State',11,40.0),

        # Odisha 2024
        (32,13,1,2024,'State',78,40.7), (33,13,9,2024,'State',51,32.9),

        # Jharkhand 2024
        (34,14,18,2024,'State',34,34.3), (35,14,2,2024,'State',16,11.1), (36,14,1,2024,'State',21,33.2),

        # Delhi 2025
        (37,22,1,2025,'State',48,40.6), (38,22,5,2025,'State',22,43.5),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO election_results
        (id,state_id,party_id,election_year,election_type,seats_won,vote_share)
        VALUES (?,?,?,?,?,?,?)
    """, results)

    # ─── LOK SABHA 2024 ────────────────────────────────────────────────────────
    ls_results = [
        (1,1,240,543,36.6,2024), (2,2,99,543,21.2,2024),
        (3,6,39,543,3.5,2024),  (4,14,37,543,6.7,2024),
        (5,3,29,543,1.1,2024),  (6,8,12,543,3.6,2024),
        (7,12,22,543,4.2,2024), (8,13,21,543,4.1,2024),
        (9,16,4,543,1.5,2024),  (10,18,4,543,0.5,2024),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO lok_sabha
        (id,party_id,seats_won,total_seats,vote_share,election_year)
        VALUES (?,?,?,?,?,?)
    """, ls_results)

    # ─── CANDIDATES ────────────────────────────────────────────────────────────
    candidates = [
        # PM
        (1,'Narendra Modi',1,9,'Varanasi','Prime Minister',74,'MA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Narendra_Modi_2023.jpg/220px-Narendra_Modi_2023.jpg',0,1,612000),

        # CMs
        (2,'M.K. Stalin',3,1,'Kolathur','Chief Minister - Tamil Nadu',71,'BA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/MK_Stalin_2023.jpg/220px-MK_Stalin_2023.jpg',1,0,142000),
        (3,'Yogi Adityanath',1,2,'Gorakhpur Urban','Chief Minister - Uttar Pradesh',52,'BSc',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Yogi_Adityanath_2023.jpg/220px-Yogi_Adityanath_2023.jpg',1,0,180000),
        (4,'Mamata Banerjee',6,4,'Bhawanipore','Chief Minister - West Bengal',69,'BA LLB',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Mamata_Banerjee_2021.jpg/220px-Mamata_Banerjee_2021.jpg',1,0,211000),
        (5,'Siddaramaiah',2,8,'Varuna','Chief Minister - Karnataka',76,'BL',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Siddaramaiah_2023.jpg/220px-Siddaramaiah_2023.jpg',1,0,122000),
        (6,'Nitish Kumar',12,5,'Nalanda','Chief Minister - Bihar',73,'BE',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Nitish_Kumar_2022.jpg/220px-Nitish_Kumar_2022.jpg',1,0,156000),
        (7,'Pinarayi Vijayan',16,12,'Dharmadom','Chief Minister - Kerala',79,'BA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Pinarayi_Vijayan_2023.jpg/220px-Pinarayi_Vijayan_2023.jpg',1,0,98000),
        (8,'Bhagwant Mann',5,15,'Dhuri','Chief Minister - Punjab',50,'BA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Bhagwant_Mann_2022.jpg/220px-Bhagwant_Mann_2022.jpg',1,0,84000),
        (9,'N. Chandrababu Naidu',8,10,'Kuppam','Chief Minister - Andhra Pradesh',74,'MBA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nara_Chandrababu_Naidu_2022.jpg/220px-Nara_Chandrababu_Naidu_2022.jpg',1,0,134000),

        # TN Key Candidates
        (10,'Edappadi K. Palaniswami',4,1,'Edappadi','Leader of Opposition - TN',71,'BSc Agri',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Edappadi_K._Palaniswami_2023.jpg/220px-Edappadi_K._Palaniswami_2023.jpg',0,0,118000),
        (11,'Udhayanidhi Stalin',3,1,'Chepauk-Thiruvallikeni','Deputy CM - TN',46,'BBA',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Udhayanidhi_Stalin_2022.jpg/220px-Udhayanidhi_Stalin_2022.jpg',0,0,98000),
        (12,'Rahul Gandhi',2,8,'Wayanad/Rae Bareli','Leader of Opposition - LoK Sabha',54,'MPhil',
         'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Rahul_Gandhi_2019.jpg/220px-Rahul_Gandhi_2019.jpg',0,0,498000),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO candidates
        (id,name,party_id,state_id,constituency,position,age,education,image_url,is_cm,is_pm,votes_received)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, candidates)

    # ─── PREDICTIONS ───────────────────────────────────────────────────────────
    predictions = [
        # TN 2026
        (1,1,3,145,72.0,2026,'Strong incumbency, welfare schemes, anti-NDA sentiment'),
        (2,1,4,80,65.0,2026,'Unified AIADMK under EPS, sympathy factor'),
        (3,1,1,5,40.0,2026,'NDA alliance limited in TN'),

        # WB 2026
        (4,4,6,175,68.0,2026,'Mamata brand, strong org, women voters'),
        (5,4,1,110,60.0,2026,'Central schemes, Ram Mandir benefit'),

        # Bihar 2025
        (6,5,12,80,55.0,2025,'JDU-BJP alliance strong'),
        (7,5,1,85,55.0,2025,'NDA umbrella seat sharing'),
        (8,5,13,65,50.0,2025,'RJD MY combine strong in north Bihar'),

        # Lok Sabha 2029
        (9,None,1,260,58.0,2029,'PM Modi, development narrative, NDA unity'),
        (10,None,2,120,52.0,2029,'INDIA bloc if united, Rahul Gandhi factor'),
        (11,None,14,45,55.0,2029,'SP strong in UP, INDIA bloc benefit'),
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO predictions
        (id,state_id,party_id,predicted_seats,confidence_pct,prediction_year,factors)
        VALUES (?,?,?,?,?,?,?)
    """, predictions)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()
