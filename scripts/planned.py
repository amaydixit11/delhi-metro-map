# Planned network, Phase IV -> V(C).
# Station entry: (name, lat, lon, conf) or ("@Existing Name",) to reuse an existing/earlier station's point.
# conf: "o" = named in an official/press/Wikipedia source, "p" = projected by us (name + site chosen from
# locality/density; DMRC has not published it). Coordinates of planned stations are approximate either way.

LINES = {
    "red": ("Red Line", "#E21F26"), "yellow": ("Yellow Line", "#F2B705"), "blue": ("Blue Line", "#1F63B6"),
    "green": ("Green Line", "#1E9E48"), "violet": ("Violet Line", "#6A2C91"), "airport": ("Airport Express", "#F28C28"),
    "pink": ("Pink Line", "#EE82B4"), "magenta": ("Magenta Line", "#B5267B"), "grey": ("Grey Line", "#8A8D8F"),
    "golden": ("Golden Line", "#C49A3A"),
    "cs": ("Central Secretariat–Kishangarh", "#0E9AA7"), "jm": ("Jor Bagh–Mithapur", "#8B5A2B"),
    "sm": ("Shastri Park–Mayur Vihar III", "#7CB518"), "kr": ("Keshav Puram–Rohini Sec 34", "#22408F"),
    "mk": ("Mayapuri–Kashmere Gate", "#8E1B3C"), "tn": ("Tughlakabad–Noida Sec 142", "#5B5BD6"),
    "g2": ("Gurugram Metro Line 2", "#8E7CC3"), "gpc": ("Gurugram: Sector 56–Pachgaon", "#26A69A"),
    "gew": ("Gurugram: GCER–Sector 5", "#FF8A65"), "gbh": ("Gurugram: Bhondsi–Railway Stn", "#AFB42B"),
    "gmk": ("Gurugram: Manesar–Samalkha", "#6D4C41"), "gde": ("Gurugram: Dwarka Expressway", "#0288D1"),
    "gpv": ("Palam Vihar–Dwarka link", "#FFB300"), "nbg": ("Namo Bharat: Gurugram–Faridabad–Noida", "#E8590C"),
    "rrA": ("Namo Bharat: Delhi–Gurugram–Alwar", "#9A3412"), "rrP": ("Namo Bharat: Delhi–Panipat–Karnal", "#FB923C"),
    "rrJ": ("Namo Bharat: Ghaziabad–Jewar Airport", "#C2410C"), "lrt": ("Film City light rail (YEIDA)", "#E11D48"),
    "meerut": ("Meerut Metro Line 1", "#00A86B"), "meerut2": ("Meerut Metro Line 2", "#5C6BC0"),
    "meerut3": ("Meerut Metro Line 3", "#D4A017"),
    "lite": ("Delhi Metrolite (light rail)", "#C0CA33"),
    "mvl": ("Mayur Vihar III–Loni Border", "#9575CD"), "cgs": ("CGO Complex–Surya Vihar (Faridabad)", "#A1887F"),
    "fgm": ("Faridabad–Gurugram Metro", "#00ACC1"),
    "rrF": ("Namo Bharat: Delhi–Faridabad–Palwal", "#BF360C"), "rrK": ("Namo Bharat: Ghaziabad–Khurja", "#E65100"),
    "rrR": ("Namo Bharat: Delhi–Bahadurgarh–Rohtak", "#D84315"), "rrH": ("Namo Bharat: Ghaziabad–Hapur", "#FF7043"),
    "rrB": ("Namo Bharat: Delhi–Shahdara–Baraut", "#A0522D"),
    "gfm": ("Gurugram–Faridabad Metro (on Namo Bharat track)", "#26C6DA"),
    "aqua": ("Aqua Line (NMRC)", "#2BB3C0"), "rapid": ("Rapid Metro Gurugram", "#6E7B8B"), "rrts": ("Namo Bharat RRTS", "#E8590C"),
}

SEGMENTS = [
  # ---------------- Phase IV ----------------
  dict(line="red", phase="IV", title="Rithala → Kundli → Nathupur", status="Approved Dec 2024 · target 2029", km=26.46, src="wiki-red", st=[
    ("@Rithala",), ("Rohini Sector 25", 28.7273, 77.0982, "o"), ("Rohini Sector 26", 28.7328, 77.0901, "o"),
    ("Rohini Sector 31", 28.7394, 77.0800, "o"), ("Rohini Sector 32", 28.7432, 77.0708, "o"),
    ("Rohini Sector 36", 28.7479, 77.0617, "o"), ("Barwala", 28.7607, 77.0590, "o"),
    ("Rohini Sector 35", 28.7738, 77.0558, "o"), ("Rohini Sector 34", 28.7787, 77.0495, "o"),
    ("Bawana Industrial Area-1 Sector 3,4", 28.7858, 77.0414, "o"), ("Bawana Industrial Area-1 Sector 1,2", 28.7955, 77.0421, "o"),
    ("Bawana JJ Colony", 28.8043, 77.0469, "o"), ("Sanoth", 28.8184, 77.0622, "o"), ("New Sanoth", 28.8285, 77.0730, "o"),
    ("Depot Station", 28.8320, 77.0800, "o"), ("Bhorgarh Village", 28.8345, 77.0880, "o"),
    ("Anaj Mandi Narela", 28.8364, 77.0949, "o"), ("Narela DDA Sports Complex", 28.8440, 77.1035, "o"),
    ("Narela", 28.8530, 77.1010, "o"), ("Narela Sector 5", 28.8625, 77.1080, "o"), ("Kundli", 28.8780, 77.1180, "o"),
    ("Nathupur", 28.8960, 77.1120, "o")]),
  dict(line="pink", phase="IV", title="Soorghat (infill)", status="Under construction · 2026", km=None, src="wiki-dm", st=[
    ("@Jagatpur–Wazirabad",), ("@Soorghat",), ("@Nanaksar–Sonia Vihar",)], infill=True),
  dict(line="magenta", phase="IV", title="Krishna Park Extn → Deepali Chowk", status="Under construction · 2026", km=17.53, src="wiki-magenta", st=[
    ("@Krishna Park Extension",), ("Keshopur", 28.6515, 77.0867, "o"), ("Paschim Vihar", 28.6685, 77.0928, "o"),
    ("Peeragarhi", 28.6789, 77.0946, "o"), ("Mangolpuri", 28.6873, 77.0960, "o"),
    ("Mangolpur Kalan–West Enclave", 28.6931, 77.1011, "o"), ("Pushpanjali", 28.6956, 77.1088, "o"), ("@Deepali Chowk",)]),
  dict(line="magenta", phase="IV", title="Majlis Park → R.K. Ashram Marg", status="Under construction · 2027", km=None, src="wiki-magenta", st=[
    ("@Majlis Park",), ("Azadpur", 28.7066, 77.1796, "o"), ("Ashok Vihar", 28.6995, 77.1848, "o"),
    ("Nanak Piao–Derawal Nagar", 28.6927, 77.1904, "o"), ("Ghanta Ghar", 28.6774, 77.2017, "o"), ("@Pulbangash",),
    ("Sadar Bazar", 28.6593, 77.2159, "o"), ("Nabi Karim", 28.6528, 77.2112, "o"), ("@Ramakrishna Ashram Marg",)]),
  dict(line="magenta", phase="IV", title="Indraprastha → Inderlok", status="Under construction · 2030", km=12.38, src="wiki-magenta", st=[
    ("@Indraprastha",), ("Delhi Sachivalaya–I.G. Stadium", 28.6316, 77.2468, "o"), ("Delhi Gate", 28.6399, 77.2427, "o"),
    ("New Delhi", 28.6433, 77.2256, "o"), ("@Nabi Karim",), ("Jhandewalan Mandir", 28.6475, 77.2015, "o"),
    ("Ajmal Khan Park", 28.6533, 77.1959, "o"), ("Sarai Rohilla", 28.6598, 77.1851, "o"), ("Daya Basti", 28.6676, 77.1805, "o"),
    ("@Inderlok",)]),
  dict(line="golden", phase="IV", title="Delhi Aerocity → Tughlakabad", status="Under construction · 2026", km=23.62, src="wiki-golden", st=[
    ("@Delhi Aerocity",), ("Mahipal Pur", 28.5413, 77.1299, "o"), ("Vasant Kunj", 28.5344, 77.1422, "o"),
    ("Kishangarh", 28.5220, 77.1680, "o"), ("@Chhatarpur",), ("Chhatarpur Mandir", 28.5010, 77.1830, "o"),
    ("IGNOU", 28.4990, 77.1975, "o"), ("Neb Sarai", 28.5055, 77.2075, "o"), ("Saket G Block", 28.5173, 77.2182, "o"),
    ("Ambedkar Nagar", 28.5154, 77.2278, "o"), ("Khanpur–Vayusenabad", 28.5135, 77.2355, "o"),
    ("Sangam Vihar–Tigri", 28.5122, 77.2439, "o"), ("Anandmayee Marg Jn.", 28.5042, 77.2793, "o"),
    ("Tughlakabad Railway Colony", 28.5016, 77.2908, "o"), ("@Tughlakabad",)]),
  dict(line="golden", phase="IV", title="Lajpat Nagar → Saket G Block (branch)", status="Under construction · 2029", km=8.4, src="wiki-golden", st=[
    ("@Lajpat Nagar",), ("Andrews Ganj", 28.5623, 77.2324, "o"), ("Greater Kailash-1", 28.5546, 77.2286, "o"),
    ("@Chirag Delhi",), ("Pushpa Bhawan", 28.5290, 77.2322, "o"), ("Saket District Centre", 28.5276, 77.2262, "o"),
    ("Pushp Vihar", 28.5250, 77.2215, "o"), ("@Saket G Block",)]),

  # ---------------- Gurugram Metro Line 2 (GMRL) ----------------
  dict(line="g2", phase="G1", title="Line 2 Ph-1: Millennium City Centre → Sector 9", status="Under construction · target 2029", km=15.3, n=14, src="gmrl", st=[
    ("@Millennium City Centre Gurugram",), ("Sector 45", 28.4449, 77.0664, "o"), ("Cyber Park", 28.4429, 77.0559, "o"),
    ("Sector 47", 28.4252, 77.0475, "o"), ("Subhash Chowk", 28.4277, 77.0371, "o"), ("Sector 48", 28.4185, 77.0335, "o"),
    ("Sector 33", 28.4245, 77.0250, "o"), ("Hero Honda Chowk", 28.4290, 77.0160, "o"), ("Udyog Vihar Ph-6", 28.4320, 77.0070, "o"),
    ("Sector 10", 28.4420, 77.0040, "o"), ("Sector 37", 28.4480, 76.9965, "o"), ("Basai", 28.4580, 76.9890, "o"),
    ("Sector 101", 28.4684, 76.9804, "o"), ("Sector 9", 28.4645, 77.0030, "o")]),
  dict(line="g2", phase="G1", title="Line 2 Ph-2: Sector 9 → Cyber City", status="Approved · target 2029", km=14.2, n=13, src="gmrl", st=[
    ("@Sector 9",), ("Sector 7", 28.4663, 77.0143, "o"), ("Sector 4", 28.4750, 77.0104, "o"), ("Sector 5", 28.4835, 77.0115, "o"),
    ("Ashok Vihar (Gurugram)", 28.4951, 77.0248, "o"), ("Sector 3", 28.4985, 77.0190, "o"), ("Bajghera Road", 28.5065, 77.0225, "o"),
    ("Palam Vihar Ext.", 28.5110, 77.0310, "o"), ("Palam Vihar", 28.5101, 77.0418, "o"), ("Sector 23A", 28.5057, 77.0475, "o"),
    ("Sector 22", 28.5063, 77.0655, "o"), ("Udyog Vihar Ph-4", 28.4990, 77.0790, "o"), ("Udyog Vihar Ph-5", 28.4960, 77.0860, "o"),
    ("@Cyber City",)]),

  # ---------------- Phase V(A) — Centre approved Dec 2025 ----------------
  dict(line="magenta", phase="VA", title="R.K. Ashram Marg → Indraprastha", status="Centre approved Dec 2025 · 2028", km=9.913, src="cabinet-va", st=[
    ("@Ramakrishna Ashram Marg",), ("@Shivaji Stadium",), ("Yuge Yugeen Bharat", 28.6142, 77.2052, "o"),
    ("@Central Secretariat",), ("Kartavya Bhawan", 28.6118, 77.2175, "o"), ("India Gate", 28.6135, 77.2260, "o"),
    ("War Memorial–High Court", 28.6095, 77.2350, "o"), ("Baroda House", 28.6178, 77.2310, "o"),
    ("Bharat Mandapam", 28.6172, 77.2420, "o"), ("@Indraprastha",)]),
  dict(line="golden", phase="VA", title="Delhi Aerocity → Terminal 1", status="Centre approved Dec 2025 · 2028", km=2.263, src="cabinet-va", st=[
    ("@Delhi Aerocity",), ("@Terminal 1 IGI Airport",)]),
  dict(line="golden", phase="VA", title="Tughlakabad → Kalindi Kunj", status="Centre approved Dec 2025 · 2028", km=3.9, src="cabinet-va", st=[
    ("@Tughlakabad",), ("Sarita Vihar Depot", 28.5150, 77.2990, "o"), ("Madanpur Khadar", 28.5300, 77.3020, "o"), ("@Kalindi Kunj",)]),

  # ---------------- Phase V(B) — Delhi govt approved May 2026, awaiting Union Cabinet ----------------
  dict(line="grey", phase="VB", title="Dhansa Bus Stand → Nangloi", status="State approved May 2026", km=11.859, n=9, src="vb", st=[
    ("@Dhansa Bus Stand",), ("Roshan Garden", 28.6155, 76.9945, "p"), ("Gopal Nagar", 28.6265, 77.0005, "p"),
    ("Sainik Enclave", 28.6335, 77.0070, "p"), ("Baprola", 28.6404, 77.0129, "p"), ("Bakkarwala", 28.6545, 77.0210, "p"),
    ("Ranhola", 28.6580, 77.0359, "p"), ("Nilothi Extension", 28.6650, 77.0480, "p"),
    ("Naresh Park Extension", 28.6738, 77.0575, "p"), ("@Nangloi",)]),
  dict(line="cs", phase="VB", title="Central Secretariat → Kishangarh", status="State approved May 2026", km=15.969, n=10, src="vb", st=[
    ("@Central Secretariat",), ("PM Sangrahalaya–Teen Murti", 28.6028, 77.1988, "p"), ("Chanakyapuri", 28.5947, 77.1885, "p"),
    ("@Sir M. Vishweshwaraiah Moti Bagh",), ("R.K. Puram Sector 5", 28.5660, 77.1790, "p"), ("@R. K. Puram",),
    ("JNU East Gate", 28.5455, 77.1745, "p"), ("JNU", 28.5402, 77.1646, "p"), ("Vasant Kunj Sector B", 28.5300, 77.1590, "p"),
    ("@Kishangarh",)]),
  dict(line="yellow", phase="VB", title="Samaypur Badli → Narela DDA Sports Complex", status="State approved May 2026", km=12.89, n=8, src="vb", st=[
    ("@Samaypur Badli",), ("Siraspur", 28.7581, 77.1298, "p"), ("Khera Kalan", 28.7697, 77.1159, "p"),
    ("Khera Khurd", 28.7840, 77.1200, "p"), ("Alipur", 28.7973, 77.1330, "p"), ("Bakoli", 28.8105, 77.1290, "p"),
    ("Holambi Kalan", 28.8215, 77.1150, "p"), ("Narela Sector A-9", 28.8335, 77.1100, "p"), ("@Narela DDA Sports Complex",)]),
  dict(line="green", phase="VB", title="Kirti Nagar → Palam", status="State approved May 2026", km=9.967, n=6, src="vb", st=[
    ("@Kirti Nagar",), ("Mayapuri Industrial Area", 28.6290, 77.1300, "p"), ("Hari Nagar", 28.6255, 77.1110, "p"),
    ("Janakpuri A-Block", 28.6185, 77.0975, "p"), ("Sagarpur", 28.6080, 77.0990, "p"), ("Sadh Nagar", 28.5960, 77.0905, "p"),
    ("@Palam",)]),
  dict(line="jm", phase="VB", title="Jor Bagh → Mithapur", status="State approved May 2026", km=16.991, n=12, src="vb", st=[
    ("@Jor Bagh",), ("Lodhi Colony", 28.5850, 77.2255, "p"), ("Defence Colony", 28.5735, 77.2310, "p"), ("@Lajpat Nagar",),
    ("Amar Colony", 28.5615, 77.2431, "p"), ("@Okhla NSIC",), ("Okhla Phase II", 28.5366, 77.2756, "p"), ("@Jasola Apollo",),
    ("@Madanpur Khadar",), ("Madanpur Khadar Extension", 28.5180, 77.3065, "p"), ("Jaitpur", 28.5060, 77.3105, "p"),
    ("Mithapur", 28.4935, 77.3185, "p")]),
  dict(line="sm", phase="VB", title="Shastri Park → Mayur Vihar Ph-III", status="State approved May 2026", km=13.197, n=8, src="vb", st=[
    ("@Shastri Park",), ("Gandhi Nagar", 28.6588, 77.2716, "p"), ("Geeta Colony", 28.6500, 77.2760, "p"), ("@Nirman Vihar",),
    ("Patparganj", 28.6235, 77.2960, "p"), ("@Trilokpuri–Sanjay Lake",), ("Kondli", 28.6071, 77.3243, "p"),
    ("Mayur Vihar Phase-III", 28.6020, 77.3350, "p")]),
  dict(line="kr", phase="VB", title="Keshav Puram → Rohini Sector 34", status="State approved May 2026", km=16.285, n=12, src="vb", st=[
    ("@Keshav Puram",), ("West Shalimar Bagh", 28.7040, 77.1560, "p"), ("@Uttari Pitampura–Prashant Vihar",),
    ("Rohini Sector 16", 28.7240, 77.1310, "p"), ("Rohini Sector 17", 28.7345, 77.1265, "p"), ("DTU", 28.7505, 77.1170, "p"),
    ("Shahbad Daulatpur", 28.7545, 77.1060, "p"), ("Rohini Sector 24", 28.7540, 77.0960, "p"), ("Rohini Sector 29", 28.7600, 77.0880, "p"),
    ("Rohini Sector 30", 28.7660, 77.0790, "p"), ("Rohini Sector 33", 28.7730, 77.0640, "p"), ("@Rohini Sector 34",)]),

  # ---------------- Phase V(C) — proposed ----------------
  dict(line="airport", phase="VC", title="Yashobhoomi Dwarka Sec 25 → Rajiv Chowk (Gurugram)", status="Proposed · merged DPR (DMRC, Jul 2026), fully underground", km=20, n=5, src="tribune-airport", st=[
    ("@Yashobhoomi Dwarka Sector 25",), ("Bijwasan", 28.5370, 77.0513, "o"), ("Kapashera", 28.5273, 77.0823, "o"),
    ("@Sector 22",), ("@IFFCO Chowk",), ("Rajiv Chowk (Gurugram)", 28.4475, 77.0328, "o")]),
  dict(line="red", phase="VC", title="Shaheed Sthal → Ghaziabad Railway Station", status="Proposed", km=3, n=2, src="vc", st=[
    ("@Shaheed Sthal (New Bus Adda)",), ("Ghaziabad Old Bus Stand", 28.6650, 77.4250, "p"), ("Ghaziabad Railway Station", 28.6529, 77.4282, "p")]),
  dict(line="blue", phase="VC", title="Noida Electronic City → Sahibabad", status="Proposed", km=5.1, n=5, src="wiki-blue", st=[
    ("@Noida Electronic City",), ("Vaibhav Khand", 28.6370, 77.3690, "o"), ("DPS Indirapuram", 28.6435, 77.3705, "o"),
    ("Shakti Khand", 28.6500, 77.3700, "o"), ("Vasundhara Sector 5", 28.6585, 77.3740, "o"), ("@Sahibabad",)]),
  dict(line="blue", phase="VC", title="Vaishali → Mohan Nagar", status="Proposed", km=5.04, n=5, src="vc", st=[
    ("@Vaishali",), ("Vaishali Sector 5", 28.6555, 77.3445, "p"), ("Prahladgarhi", 28.6605, 77.3520, "p"),
    ("Sahibabad Industrial Area", 28.6660, 77.3600, "p"), ("Lajpat Nagar Sahibabad", 28.6725, 77.3730, "p"), ("@Mohan Nagar",)]),
  dict(line="mk", phase="VC", title="Mayapuri → Kashmere Gate", status="Proposed", km=12, n=7, src="vc", st=[
    ("@Mayapuri",), ("Naraina Industrial Area", 28.6321, 77.1371, "p"), ("Inderpuri", 28.6287, 77.1471, "p"),
    ("Old Rajinder Nagar", 28.6395, 77.1830, "p"), ("Dev Nagar", 28.6544, 77.1835, "p"), ("@Tis Hazari",), ("@Kashmere Gate",)]),
  dict(line="blue", phase="VC", title="Dwarka Sector 21 → Udyog Vihar", status="Proposed · overlaps the merged Airport-line DPR", km=11, n=3, src="vc", st=[
    ("@Dwarka Sector 21",), ("@Bijwasan",), ("@Kapashera",), ("@Udyog Vihar Ph-4",)]),
  dict(line="pink", phase="VC", title="Gokulpuri → Arthala (via Hindon Airport)", status="Proposed · names per DMRC Sept 2024 proposal", km=12, n=8, src="wiki-pink", st=[
    ("@Gokulpuri",), ("Gol Chakkar", 28.7040, 77.3010, "o"), ("DLF", 28.7010, 77.3175, "o"), ("Tulsi Niketan", 28.6950, 77.3260, "o"),
    ("Bhopura", 28.6984, 77.3334, "o"), ("Shalimar Garden", 28.6880, 77.3420, "o"), ("Rajendra Nagar (Sahibabad)", 28.6905, 77.3540, "o"),
    ("Hindon Airport", 28.7043, 77.3648, "o"), ("Karhaira", 28.6965, 77.3790, "o"), ("New Karhaira Colony", 28.6900, 77.3840, "o"),
    ("Loni Road Industrial Area", 28.6830, 77.3885, "o"), ("@Arthala",)]),
  dict(line="tn", phase="VC", title="Tughlakabad → Noida Sector 142", status="Proposed", km=15, n=10, src="vc", st=[
    ("@Tughlakabad",), ("Molarband", 28.5000, 77.3110, "p"), ("@Mithapur",), ("Noida Sector 168", 28.4975, 77.3520, "p"),
    ("Noida Sector 133", 28.5052, 77.3715, "p"), ("Noida Sector 132", 28.5100, 77.3830, "p"), ("Noida Sector 134", 28.5020, 77.3895, "p"),
    ("Noida Sector 135", 28.4980, 77.4000, "p"), ("Noida Sector 140A", 28.5040, 77.4070, "p"), ("@Noida Sector 142",)]),
  dict(line="violet", phase="VC", title="Raja Nahar Singh → Palwal", status="Proposed · HMRTC feasibility done", km=24, n=13, src="vc", st=[
    ("@Raja Nahar Singh",), ("Sector 58-59", 28.3120, 77.3095, "o"), ("Sector 61-62", 28.3030, 77.3140, "p"), ("Jajru", 28.2935, 77.3125, "p"), ("Sikri", 28.2850, 77.3110, "o"),
    ("Sikri Industrial Area", 28.2730, 77.3100, "p"), ("Softa", 28.2600, 77.3070, "o"), ("Gadpuri", 28.2470, 77.3030, "p"),
    ("Prithla", 28.2328, 77.3000, "p"), ("Baghola", 28.2089, 77.3063, "p"), ("Rasoolpur", 28.1930, 77.3120, "p"),
    ("Alahpur", 28.1780, 77.3180, "p"), ("Palwal Bus Stand", 28.1459, 77.3348, "p"), ("Palwal Railway Station", 28.1516, 77.3418, "p")]),
  dict(line="green", phase="VC", title="Brigadier Hoshiyar Singh → Asaudha", status="Proposed · DPR May 2026", km=8, n=6, src="wiki-green", st=[
    ("@Brigadier Hoshiyar Singh",), ("Sankhol", 28.7075, 76.9120, "o"), ("Udyog Vihar Sector 16", 28.7160, 76.9020, "o"),
    ("HSIIDC Sector 17", 28.7245, 76.8945, "o"), ("Jakhoda", 28.7335, 76.8860, "o"), ("HPCL Plant", 28.7420, 76.8790, "o"),
    ("Asaudha", 28.7507, 76.8715, "o")]),
]

SEGMENTS += [
  dict(line="gpc", phase="G2", title="Sector 56 → Pachgaon (Manesar)", status="DPR ready Sept 2025 · 28 stations", km=35.5, n=28, src="ht-pachgaon", st=[
    ("@Sector 55–56",), ("Sector 61", 28.4110, 77.0964, "o"), ("Sector 62", 28.4077, 77.0824, "o"), ("Sector 63", 28.4030, 77.0690, "p"),
    ("Sector 66", 28.3974, 77.0539, "o"), ("Vatika Chowk", 28.3985, 77.0440, "o"), ("Sector 69", 28.3961, 77.0372, "o"),
    ("Sector 70", 28.3947, 77.0223, "o"), ("Sector 71", 28.3955, 77.0145, "p"), ("Sector 75", 28.3964, 77.0066, "o"),
    ("Kherki Daula", 28.4040, 76.9830, "o"), ("Sector 36A", 28.4120, 76.9740, "o"), ("Sector 88", 28.4130, 76.9660, "o"),
    ("Sector 84", 28.4095, 76.9600, "o"), ("Sector 85", 28.4060, 76.9530, "o"), ("Sector 89", 28.4075, 76.9460, "o"),
    ("Sector 86", 28.4035, 76.9400, "o"), ("Sector 90", 28.4040, 76.9320, "o"), ("Sector 91", 28.4000, 76.9230, "o"),
    ("M-15", 28.3925, 76.9160, "o"), ("M-14", 28.3840, 76.9080, "o"), ("M-10", 28.3770, 76.9150, "p"), ("M-9", 28.3700, 76.9200, "o"),
    ("IMT Manesar", 28.3610, 76.9230, "o"), ("M-7", 28.3530, 76.9150, "p"), ("M-6", 28.3450, 76.9080, "p"),
    ("P-7", 28.3390, 76.9010, "o"), ("P-4", 28.3330, 76.8950, "p"), ("Pachgaon", 28.3270, 76.8890, "o")]),
  dict(line="rrA", phase="RR", title="Namo Bharat: Sarai Kale Khan → Gurugram → Bawal → Alwar", status="Approved · construction from Aug 2026, target Nov 2031", km=164, n=22, src="rr-alwar", st=[
    ("@Sarai Kale Khan",), ("@Dilli Haat–INA",), ("@Munirka",), ("@Delhi Aerocity",), ("@Cyber City",),
    ("Gurugram Sector-17", 28.4758, 77.0608, "o"), ("@Rajiv Chowk (Gurugram)",), ("@Kherki Daula",), ("@IMT Manesar",), ("@Pachgaon",),
    ("Bilaspur Chowk", 28.2886, 76.8602, "o"), ("Dharuhera", 28.2055, 76.7953, "o"), ("MBIR", 28.1750, 76.7050, "o"),
    ("Rewari District", 28.1957, 76.6165, "o"), ("Bawal", 28.0597, 76.5766, "o"), ("Kotputli-Behror Border", 28.0150, 76.5050, "o"),
    ("Shahjahanpur", 27.9953, 76.4509, "o"), ("Neemrana", 27.9922, 76.3857, "o"), ("Behror", 27.8901, 76.2858, "o"),
    ("Sotanala", 27.8200, 76.2950, "o"), ("Khairthal", 27.7978, 76.6417, "o"), ("Alwar", 27.5605, 76.6214, "o")]),
  dict(line="gpv", phase="G2", title="Palam Vihar → Dwarka Sector 21", status="Haryana-approved 2022 · awaiting MoHUA", km=8.4, src="gpv", st=[
    ("@Palam Vihar",), ("Chauma–Sector 110A", 28.5161, 77.0376, "o"), ("Sector 111", 28.5223, 77.0336, "o"),
    ("@Yashobhoomi Dwarka Sector 25",), ("@Dwarka Sector 21",)]),
  dict(line="gew", phase="G2", title="Golf Course Ext. Road → Sector 5", status="DPR consultant tendered Mar 2025", km=14, src="dm-gurugram", st=[
    ("@Sector 61",), ("Sector 57", 28.4232, 77.0804, "p"), ("Sector 46", 28.4359, 77.0640, "p"), ("@Millennium City Centre Gurugram",),
    ("Signature Tower", 28.4664, 77.0581, "o"), ("Rana Pratap Chowk", 28.4705, 77.0470, "o"), ("Atul Kataria Chowk", 28.4770, 77.0340, "o"),
    ("@Sector 5",)]),
  dict(line="gbh", phase="G2", title="Bhondsi → Gurugram Railway Station", status="DPR underway", km=20, src="dm-gurugram", st=[
    ("Bhondsi", 28.3505, 77.0619, "p"), ("Ramgarh", 28.3720, 77.0560, "p"), ("Badshahpur", 28.3880, 77.0490, "p"), ("@Vatika Chowk",),
    ("Sector 49", 28.4129, 77.0498, "p"), ("@Subhash Chowk",), ("Medanta", 28.4390, 77.0400, "p"),
    ("@Rajiv Chowk (Gurugram)",), ("Sadar Bazar (Gurugram)", 28.4609, 77.0293, "p"), ("Sector 12", 28.4725, 77.0225, "p"), ("@Sector 5",)]),
  dict(line="gmk", phase="G2", title="Manesar → Samalkha–Kapashera Road (via Old Gurugram)", status="Planned", km=30, src="dm-gurugram", st=[
    ("Manesar", 28.3600, 76.9380, "p"), ("Sector 80", 28.3800, 76.9600, "p"), ("Narsinghpur", 28.3950, 76.9700, "p"), ("@Kherki Daula",),
    ("Sector 35", 28.4180, 76.9960, "p"), ("@Hero Honda Chowk",), ("New Colony", 28.4520, 77.0210, "p"), ("@Sadar Bazar (Gurugram)",),
    ("Sector 14", 28.4738, 77.0472, "p"), ("@Gurugram Sector-17",), ("Sector 21", 28.5144, 77.0730, "p"), ("@Kapashera",),
    ("Samalkha", 28.5319, 77.1034, "p")]),
  dict(line="gde", phase="G2", title="Kherki Daula → Sector 111 (Dwarka Expressway)", status="Ridership study by DMRC", km=25, src="dm-gurugram", st=[
    ("@Kherki Daula",), ("Sector 36", 28.4230, 76.9840, "p"), ("Sector 37D", 28.4480, 76.9700, "p"), ("Sector 99", 28.4646, 76.9629, "p"),
    ("Sector 102", 28.4730, 76.9800, "p"), ("Sector 104", 28.4795, 76.9937, "p"), ("Sector 106", 28.5061, 76.9968, "p"),
    ("Sector 109", 28.5109, 77.0066, "p"), ("Sector 110", 28.5170, 77.0170, "p"), ("@Sector 111",)]),
  dict(line="nbg", phase="RR", title="Namo Bharat: IFFCO Chowk → Faridabad → Surajpur", status="DPR submitted by NCRTC · Jun 2026", km=64, n=7, src="nbg", st=[
    ("@IFFCO Chowk",), ("@Sector 61",), ("Gwal Pahari", 28.4326, 77.1481, "o"), ("Sainik Colony (Faridabad)", 28.4290, 77.2890, "o"),
    ("@Bata Chowk",), ("Sector 87-88 (Faridabad)", 28.4000, 77.3420, "o"), ("@Noida Sector 142",), ("Surajpur", 28.5107, 77.4786, "o")]),
]

SEGMENTS += [
  # ---- Noida Metro (NMRC) ----
  dict(line="aqua", phase="G1", title="Aqua branch: Botanical Garden → Noida Sector 142", status="Union Cabinet approved · target 2030", km=11.56, n=8, src="nmrc", st=[
    ("@Botanical Garden",), ("Noida Sector 44", 28.5513, 77.3352, "o"), ("Noida Office", 28.5454, 77.3377, "o"),
    ("Noida Sector 97", 28.5405, 77.3541, "o"), ("Noida Sector 105", 28.5316, 77.3692, "o"), ("Noida Sector 108", 28.5266, 77.3768, "o"),
    ("Noida Sector 93", 28.5230, 77.3861, "o"), ("Panchsheel Balak Inter College", 28.5098, 77.3927, "o"), ("@Noida Sector 142",)]),
  dict(line="aqua", phase="G1", title="Aqua: Depot → Boraki", status="Centre approved Jul 2025 · 3-year build", km=2.6, n=2, src="nmrc", st=[
    ("@Depot",), ("MMTH–Junpat", 28.4952, 77.5548, "o"), ("Boraki", 28.5076, 77.5637, "o")]),
  dict(line="aqua", phase="G2", title="Aqua: Noida Sector 51 → Knowledge Park V", status="GNIDA approved 2018 · not yet built", km=15, n=9, src="nmrc", st=[
    ("@Noida Sector 51",), ("Noida Sector 122", 28.5929, 77.3976, "o"), ("Noida Sector 123", 28.5885, 77.4085, "o"),
    ("Greater Noida West Sector IV", 28.6075, 77.4300, "o"), ("Ecotech 12", 28.6120, 77.4420, "o"),
    ("Greater Noida West Sector II", 28.6000, 77.4440, "o"), ("Greater Noida West Sector 3", 28.5930, 77.4480, "o"),
    ("Greater Noida West Sector 10", 28.5850, 77.4520, "o"), ("Greater Noida West Sector 12", 28.5780, 77.4560, "o"),
    ("Knowledge Park V", 28.5700, 77.4610, "o")]),
  # ---- Namo Bharat (NCRTC) ----
  dict(line="rrJ", phase="RR", title="Namo Bharat: Ghaziabad → Noida Airport (Jewar)", status="DPR submitted Apr 2024 · revised Aug 2024", km=72.44, n=12, src="rr-jewar", st=[
    ("@Ghaziabad",), ("Ghaziabad South", 28.6405, 77.4113, "o"), ("@Greater Noida West Sector IV",), ("@Greater Noida West Sector II",),
    ("@Knowledge Park V",), ("@Surajpur",), ("@Pari Chowk",), ("Ecotech VI", 28.4500, 77.5300, "o"), ("Dankaur", 28.3496, 77.5540, "o"),
    ("YEIDA Sector 18", 28.3150, 77.5450, "o"), ("YEIDA Sector 21", 28.2700, 77.5570, "o"), ("Jewar Airport", 28.1717, 77.6089, "o")]),
  dict(line="lrt", phase="G2", title="Film City light rail: Noida Airport → YEIDA Sector 21", status="Proposed · 14.6 km", km=14.6, src="rr-jewar", st=[
    ("@Jewar Airport",), ("Kureb", 28.1914, 77.5985, "p"), ("YEIDA Sector 29", 28.2110, 77.5881, "p"), ("Dhanpura", 28.2307, 77.5778, "p"),
    ("YEIDA Sector 22", 28.2503, 77.5674, "p"), ("@YEIDA Sector 21",)]),
  dict(line="rrP", phase="RR", title="Namo Bharat: Sarai Kale Khan → Panipat → Karnal", status="PIB cleared Nov 2025 · pre-construction underway", km=136.3, n=22, src="rr-panipat", st=[
    ("@Sarai Kale Khan",), ("@Indraprastha",), ("@Kashmere Gate",), ("@Jharoda Majra",), ("@Bhalaswa",), ("@Alipur", "o"),
    ("@Narela",), ("@Kundli",), ("KMP", 28.9100, 77.1130, "o"), ("Bahalgarh Chowk", 28.9587, 77.0951, "o"), ("Murthal", 29.0350, 77.0750, "o"),
    ("Bahri", 29.0850, 77.0550, "o"), ("Gannaur", 29.1378, 77.0203, "o"), ("Samalkha (Panipat)", 29.2350, 77.0130, "o"),
    ("Panipat ISBT", 29.3700, 76.9790, "o"), ("Panipat City", 29.3920, 76.9700, "o"), ("Panipat Sector 18", 29.4180, 76.9580, "o"),
    ("Ganjbar-Badauli-Kohand", 29.4777, 76.9654, "o"), ("Gharunda", 29.5394, 76.9389, "o"), ("Karnal Bypass", 29.6650, 76.9850, "o"),
    ("Karnal Sector 7", 29.6920, 76.9800, "o"), ("Karnal ISBT", 29.7080, 76.9920, "o")]),
]

SEGMENTS += [
  # ---- Meerut Metro (NCRTC) ----
  dict(line="meerut2", phase="G2", title="Meerut Line 2: Shradhapuri Ph-II → Jagriti Vihar", status="Proposed · awaiting new DPR tender", km=15, n=13, src="meerut2", st=[
    ("Shradhapuri Phase II", 29.0310, 77.6720, "o"), ("Kanker Khera", 29.0233, 77.6879, "o"), ("Meerut Cantt Railway Station", 29.0165, 77.6877, "o"),
    ("Rajban Bazar", 29.0049, 77.6976, "o"), ("@Begumpul",), ("Bachcha Park", 28.9890, 77.7065, "o"), ("Shahpeer Gate", 28.9786, 77.7114, "o"),
    ("Hapur Adda", 28.9738, 77.7136, "o"), ("Gandhi Ashram", 28.9709, 77.7206, "o"), ("Mangal Pandey Nagar", 28.9725, 77.7320, "o"),
    ("Tejgarhi", 28.9641, 77.7397, "o"), ("Medical College", 28.9611, 77.7508, "o"), ("Jagriti Vihar Extension", 28.9600, 77.7620, "o")]),
  dict(line="meerut3", phase="G2", title="Meerut Line 3: CCS University → Begumpul (via Ganga Nagar)", status="Planning stage", km=9, n=6, src="meerut-wiki", st=[
    ("CCS University", 28.9670, 77.7389, "o"), ("Shastri Nagar Extension", 28.9820, 77.7480, "p"), ("Ganga Nagar", 28.9997, 77.7594, "o"),
    ("Mawana Road", 28.9995, 77.7380, "p"), ("Civil Lines (Meerut)", 28.9990, 77.7180, "p"), ("@Begumpul",)]),
]

SEGMENTS += [
  dict(line="lite", phase="G2", title="Delhi Metrolite: Kirti Nagar → Dwarka Sector 28 (Bamnoli)", status="DPR approved by DMRC board Oct 2019 · awaiting Delhi govt · listed as cancelled in Wikipedia's index", km=19.09, n=21, src="metrolite", st=[
    ("@Kirti Nagar",), ("Saraswati Garden", 28.6466, 77.1374, "o"), ("Mayapuri Bus Depot", 28.6420, 77.1330, "o"), ("@Mayapuri",),
    ("Hari Nagar Block BE", 28.6340, 77.1240, "o"), ("@Mayapuri Industrial Area", "o"), ("Mayapuri Industrial Area-II", 28.6230, 77.1235, "o"),
    ("Lajwanti Garden", 28.6133, 77.1073, "o"), ("Shivpuri", 28.6118, 77.0985, "o"), ("Dabri Village", 28.6101, 77.0889, "o"),
    ("Sitapuri Extension", 28.6131, 77.0836, "o"), ("Mahavir Enclave", 28.6000, 77.0790, "o"), ("Dwarka Sector 2", 28.5986, 77.0687, "o"),
    ("Dwarka Sector 7", 28.5874, 77.0673, "o"), ("Dwarka Sector 6", 28.5925, 77.0647, "o"), ("@Dwarka Sector 10",),
    ("Dwarka Sector 20", 28.5714, 77.0589, "o"), ("Dwarka Sector 23", 28.5620, 77.0491, "o"), ("Dhul Siras Village", 28.5560, 77.0380, "o"),
    ("@Yashobhoomi Dwarka Sector 25",), ("Dwarka Sector 28", 28.5442, 77.0250, "o")]),
]

SEGMENTS += [
  # ---- rest of DMRC's Phase V wish list (18-corridor proposal, 2025) — no station lists published ----
  dict(line="blue", phase="G2", title="Yamuna Bank → Loni", status="Phase V proposal (DMRC 2025) · stations projected", km=12, src="nbm-18", st=[
    ("@Yamuna Bank",), ("@Geeta Colony",), ("@Shastri Park",), ("Usmanpur", 28.6862, 77.2507, "p"), ("@Bhajanpura",),
    ("Loni Border", 28.7378, 77.2609, "p"), ("Loni", 28.7317, 77.2901, "o")]),
  dict(line="pink", phase="G2", title="Shiv Vihar → Loni", status="Phase V proposal · stations projected", km=3, src="dm-wiki", st=[
    ("@Shiv Vihar",), ("@Loni",)]),
  dict(line="mvl", phase="G2", title="Mayur Vihar Ph-III → Loni Border", status="Phase V proposal (DMRC 2025), 21 km · stations projected", km=21, src="nbm-18", st=[
    ("@Mayur Vihar Phase-III",), ("Ghazipur", 28.6303, 77.3203, "p"), ("@Anand Vihar",), ("Vivek Vihar", 28.6720, 77.3150, "p"),
    ("@Dilshad Garden",), ("Sunder Nagri", 28.6890, 77.3060, "p"), ("@Johri Enclave",), ("@Loni Border",)]),
  dict(line="cgs", phase="G2", title="CGO Complex → Surya Vihar (Faridabad)", status="Phase V proposal (DMRC 2025) · route and stations projected", src="nbm-18", st=[
    ("CGO Complex", 28.5863, 77.2387, "o"), ("Hazrat Nizamuddin", 28.5864, 77.2530, "p"), ("@Ashram",), ("@Sukhdev Vihar",),
    ("@Sarita Vihar",), ("@Badarpur",), ("Faridabad Sector 37", 28.4797, 77.3119, "p"), ("Surya Vihar", 28.4802, 77.2919, "o")]),
  dict(line="fgm", phase="G2", title="Faridabad–Gurugram: Bata Chowk → Vatika Chowk", status="DPR by DMRC (2020) · HMRTC asked for a revised DPR", km=34, n=12, src="fgm", st=[
    ("@Bata Chowk",), ("Piyali Chowk", 28.3950, 77.3000, "o"), ("Shaheed Bhagat Singh Marg", 28.4000, 77.2920, "o"),
    ("Badkhal Enclave", 28.4073, 77.2830, "o"), ("Pali Chowk", 28.4050, 77.2460, "o"), ("Police Chowki Mangar", 28.4150, 77.2000, "o"),
    ("@Gwal Pahari",), ("@Sector 55–56",), ("Sushant Lok", 28.4200, 77.0900, "o"), ("Sushant Lok Phase III", 28.4130, 77.0780, "o"),
    ("Rosewood City", 28.4102, 77.0545, "o"), ("@Vatika Chowk",)]),
  # ---- NCRTC future-phase Namo Bharat corridors (endpoints only published; stops projected at main towns) ----
  dict(line="rrF", phase="RR", title="Namo Bharat: Delhi → Faridabad → Ballabgarh → Palwal", status="NCRTC future phase · 60 km · stops projected", km=60, src="ncrtc", st=[
    ("@Sarai Kale Khan",), ("@Tughlakabad",), ("@Old Faridabad",), ("@Raja Nahar Singh",), ("@Palwal Railway Station",)]),
  dict(line="rrK", phase="RR", title="Namo Bharat: Ghaziabad → Bulandshahr → Khurja", status="NCRTC future phase · 83 km · stops projected", km=83, src="ncrtc", st=[
    ("@Ghaziabad",), ("Dadri", 28.5387, 77.5372, "p"), ("Sikandrabad", 28.4171, 77.7353, "p"), ("Bulandshahr", 28.3874, 77.9744, "p"),
    ("Khurja", 28.2533, 77.8539, "o")]),
  dict(line="rrR", phase="RR", title="Namo Bharat: Delhi → Bahadurgarh → Rohtak", status="NCRTC future phase · 70 km · stops projected", km=70, src="ncrtc", st=[
    ("@Inderlok",), ("@Nangloi",), ("@Mundka",), ("@Bahadurgarh City",), ("Sampla", 28.8192, 76.7609, "p"), ("Rohtak", 28.9011, 76.5802, "o")]),
  dict(line="rrH", phase="RR", title="Namo Bharat: Ghaziabad → Hapur", status="NCRTC future phase · 57 km · stops projected", km=57, src="ncrtc", st=[
    ("@Ghaziabad",), ("Masuri", 28.6919, 77.5529, "p"), ("Pilkhuwa", 28.7142, 77.6549, "p"), ("Hapur", 28.7167, 77.8904, "o")]),
  dict(line="rrB", phase="RR", title="Namo Bharat: Delhi → Shahdara → Baghpat → Baraut", status="NCRTC future phase · 56 km · stops projected", km=56, src="ncrtc", st=[
    ("@Shahdara",), ("@Loni",), ("Khekra", 28.8656, 77.2840, "p"), ("Baghpat", 29.0375, 77.3063, "p"), ("Baraut", 29.1561, 77.3064, "o")]),
]

SEGMENTS += [
  # ---- longer-range Delhi Metro extensions into Haryana (Delhi Metro article, "studies done") — stops projected ----
  dict(line="red", phase="G2", title="Red Line: Nathupur → Sonipat Sector 7", status="Proposed · studies done · stops projected (one report says it may be a Yellow Line extension instead)", km=11, src="dm-wiki", st=[
    ("@Nathupur",), ("Rai", 28.9406, 77.0962, "p"), ("@Bahalgarh Chowk",), ("Sonipat Sector 7", 28.9866, 77.0788, "o")]),
  dict(line="grey", phase="G2", title="Grey Line: Dhansa Bus Stand → Jhajjar (via Badli)", status="Proposed · DPR consultant tendered Mar 2025 · stops projected", km=33, src="dm-wiki", st=[
    ("@Dhansa Bus Stand",), ("Surakhpur", 28.6054, 76.9339, "p"), ("Rawata Mor", 28.5989, 76.8893, "p"), ("Gubhana", 28.5925, 76.8447, "p"),
    ("Badli (Jhajjar)", 28.5727, 76.8101, "o"), ("Jhajjar Bypass", 28.5960, 76.7100, "p"), ("Jhajjar", 28.6060, 76.6570, "o")]),
]

SEGMENTS += [
  # metro services proposed on the Gurugram–Faridabad Namo Bharat corridor (NCRTC/HMRTC, Mar 2026)
  dict(line="gfm", phase="G2", title="Gurugram metro on Namo Bharat track: IFFCO Chowk → Gwal Pahari", status="Proposed Mar 2026 · shares the Namo Bharat corridor", src="hmrtc", st=[
    ("@IFFCO Chowk",), ("Sector 29 (Gurugram)", 28.4669, 77.0671, "o"), ("@Millennium City Centre Gurugram",), ("Sector 52 (Gurugram)", 28.4368, 77.0795, "o"),
    ("Wazirabad (Gurugram)", 28.4338, 77.0878, "o"), ("@Sector 57", "o"), ("@Sector 61",), ("Sectors 58-61", 28.4180, 77.1150, "o"), ("@Gwal Pahari",)]),
  dict(line="gfm", phase="G2", title="Faridabad metro on Namo Bharat track: NIT-3 → Sectors 88-89", status="Proposed Mar 2026 · shares the Namo Bharat corridor", src="hmrtc", st=[
    ("NIT-3", 28.3961, 77.2903, "o"), ("NIT-1", 28.3847, 77.3026, "o"), ("@Bata Chowk",), ("Sectors 12-15", 28.3855, 77.3232, "o"),
    ("Sector 80 (Faridabad)", 28.3815, 77.3330, "o"), ("Sectors 81-82", 28.3900, 77.3400, "o"), ("Sectors 85-86", 28.4068, 77.3425, "o"),
    ("Sectors 88-89", 28.4210, 77.3668, "o")]),
]

# Phase IV/V stations on operational-line geometry that are not open yet
PENDING_EXISTING = {"Soorghat": "IV"}

SOURCES = {
  "wiki-red": ("Wikipedia: Red Line (Delhi Metro) – Phase IV station list", "https://en.wikipedia.org/wiki/Red_Line_(Delhi_Metro)"),
  "wiki-magenta": ("Wikipedia: Magenta Line (Delhi Metro)", "https://en.wikipedia.org/wiki/Magenta_Line_(Delhi_Metro)"),
  "wiki-golden": ("Wikipedia: Golden Line (Delhi Metro)", "https://en.wikipedia.org/wiki/Golden_Line_(Delhi_Metro)"),
  "wiki-dm": ("Wikipedia: Delhi Metro – Phase IV table", "https://en.wikipedia.org/wiki/Delhi_Metro"),
  "cabinet-va": ("Union Cabinet approval, Phase V(A), 24 Dec 2025", "https://www.newsonair.gov.in/cabinet-approves-delhi-metro-phase-5a-worth-%e2%82%b912015-crore"),
  "vb": ("Phase V(B): 7 corridors, 65 stations (Amar Ujala, 3 May 2026)", "https://www.amarujala.com/delhi-ncr/delhi-metro-mega-expansion-seven-new-corridors-97-km-long-network-65-stations-2026-05-03"),
  "vc": ("Wikipedia: Delhi Metro – Phase V(C) proposed table", "https://en.wikipedia.org/wiki/Delhi_Metro"),
  "wiki-blue": ("Wikipedia: Blue Line – NEC–Sahibabad proposal", "https://en.wikipedia.org/wiki/Blue_Line_(Delhi_Metro)"),
  "wiki-pink": ("Wikipedia: Pink Line – Gokulpuri–Arthala proposal (Sept 2024)", "https://en.wikipedia.org/wiki/Pink_Line_(Delhi_Metro)"),
  "gmrl": ("Wikipedia: Gurugram Metro – Line 2 station list", "https://en.wikipedia.org/wiki/Gurugram_Metro"),
  "tribune-airport": ("Tribune: merged DPR, 5 stations, Yashobhoomi–Rajiv Chowk (27 Jul 2026)", "https://www.tribuneindia.com/news/gurugram/merged-dpr-5-stations-gurugrams-airport-metro-plan-finally-takes-shape/"),
  "ht-pachgaon": ("Sector 56–Pachgaon DPR, 28 stations (India TV, Sept 2025)", "https://www.indiatvnews.com/business/markets/gurugram-sector-56-to-pachgaon-metro-dpr-prepared-check-route-length-number-of-stations-and-other-details-2025-09-16-1008451"),
  "gpv": ("Palam Vihar–Dwarka metro link (Housing.com)", "https://housing.com/news/hmrtc-plans-to-finalise-gurgaon-metros-palam-vihar-dwarka-project"),
  "dm-gurugram": ("Wikipedia: Gurugram Metro – planned lines", "https://en.wikipedia.org/wiki/Gurugram_Metro"),
  "nbg": ("Metro Rail News: Gurugram–Faridabad–Noida RRTS DPR (27 Jun 2026)", "https://metrorailnews.in/gurugram-noida-rrts-corridor-dpr-submitted/"),
  "nmrc": ("Wikipedia: Noida Metro – approved & planned extensions", "https://en.wikipedia.org/wiki/Noida_Metro"),
  "rr-alwar": ("Wikipedia: Delhi–Alwar RRTS station list", "https://en.wikipedia.org/wiki/Delhi%E2%80%93Alwar_Regional_Rapid_Transit_System"),
  "rr-jewar": ("Wikipedia: Ghaziabad–Jewar RRTS station list", "https://en.wikipedia.org/wiki/Ghaziabad%E2%80%93Jewar_Regional_Rapid_Transit_System"),
  "rr-panipat": ("Wikipedia: Delhi–Panipat RRTS station list", "https://en.wikipedia.org/wiki/Delhi%E2%80%93Panipat_Regional_Rapid_Transit_System"),
  "meerut2": ("Metro Rail News: Meerut Metro Line 2 stations", "https://metrorailnews.in/meerut-metro-information-route-maps-project-updates/"),
  "meerut-wiki": ("Wikipedia: Meerut Metro", "https://en.wikipedia.org/wiki/Meerut_Metro"),
  "metrolite": ("Wikipedia: Delhi Metrolite", "https://en.wikipedia.org/wiki/Delhi_Metrolite"),
  "nbm-18": ("NBM&CW: DMRC proposes 18 Phase-V corridors (Apr 2025)", "https://www.nbmcw.com/news/dmrc-proposes-18-new-metro-corridors-under-phase-v.html"),
  "dm-wiki": ("Wikipedia: Delhi Metro – Phase V expansion", "https://en.wikipedia.org/wiki/Delhi_Metro"),
  "fgm": ("DNA: Faridabad–Gurgaon metro, 12 stations", "https://www.dnaindia.com/india/report-faridabad-gurgaon-to-have-metro-connectivity-list-of-12-stations-route-details-3031311"),
  "ncrtc": ("NCRTC: Project details – future phases", "https://ncrtc.in/details/"),
  "hmrtc": ("HMRTC/NCRTC: metro stations on the Gurugram–Faridabad Namo Bharat corridor (2026)", "https://hmrtc.in/"),
  "wiki-green": ("Wikipedia: Green Line – Bahadurgarh–Asaudha", "https://en.wikipedia.org/wiki/Green_Line_(Delhi_Metro)"),
}
