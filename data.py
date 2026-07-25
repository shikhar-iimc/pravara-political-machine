"""
Data for the Pravara sugar-bank-party network.
Everything here is a schematic reconstruction from public, cited sources.
It is meant to show the structure of control, not to be an exhaustive census.
"""

# ----- colours (chosen for contrast on a white ground, dark labels) -----
COLORS = {
    "dynasty": {"bg": "#1f3a5f", "border": "#12253c"},   # deep navy
    "factory": {"bg": "#c07b18", "border": "#7d4f0d"},   # ochre
    "bank":    {"bg": "#2a7d7d", "border": "#195050"},   # teal
    "trust":   {"bg": "#4a7c59", "border": "#2f5138"},   # muted green
    "congress":{"bg": "#5b8fb0", "border": "#3c6580"},
    "ncp":     {"bg": "#7d6aa8", "border": "#544778"},
    "bjp":     {"bg": "#cf7a2b", "border": "#8f5216"},
    "base":    {"bg": "#7a7a7a", "border": "#565656"},
    "rival":   {"bg": "#9a5b5b", "border": "#6d3d3d"},
}

DIM_NODE = {"bg": "#e2e2e2", "border": "#cccccc", "font": "#b4b4b4"}

# ----- 14 schematic nodes -----
# group drives colour; title is the hover tooltip (kept short, with a source)
NODES = [
    {"id": "vitthalrao", "label": "Vitthalrao Vikhe Patil", "group": "dynasty",
     "title": "Founder of Pravara (1950), Asia's first cooperative sugar factory. Source: official district records."},
    {"id": "balasaheb", "label": "Balasaheb Vikhe Patil", "group": "dynasty",
     "title": "Son of the founder. Seven-time MP; expanded the group into education and health."},
    {"id": "radhakrishna", "label": "Radhakrishna Vikhe Patil", "group": "dynasty",
     "title": "Chairman of the factory board and a district cooperative bank director; sitting state minister. Sources: board roster (PFR, 2021); Down To Earth (2019)."},
    {"id": "sujay", "label": "Sujay Vikhe Patil", "group": "dynasty",
     "title": "Expert Director on the factory board; former MP for Ahmednagar. Source: board roster (PFR, 2021)."},

    {"id": "factory", "label": "Pravara Sugar Factory", "group": "factory",
     "title": "Padmashri Dr. Vitthalrao Vikhe Patil SSK Ltd. Owned by roughly 100,000 farmer-members; directed by the board."},
    {"id": "bank", "label": "District Cooperative Bank", "group": "bank",
     "title": "In 2017 a district central cooperative bank sanctioned a low-interest loan of about Rs 35 crore to a Vikhe Patil sugarcane venture while R. Vikhe Patil sat on the bank board. Cited to show the interlock; the loan was for a sugarcane venture, not necessarily this factory. Source: Down To Earth (2019)."},
    {"id": "college", "label": "Medical College and Hospital", "group": "trust",
     "title": "Institution of the Vikhe Patil Foundation."},
    {"id": "ibmrd", "label": "IBMRD Management Institute", "group": "trust",
     "title": "Institution of the Vikhe Patil Foundation."},

    {"id": "congress", "label": "Congress (INC)", "group": "congress",
     "title": "The family's party from the founding era until 2019."},
    {"id": "ncp", "label": "NCP", "group": "ncp",
     "title": "Nationalist Congress Party; the family's alliance partner and local rival."},
    {"id": "bjp", "label": "BJP", "group": "bjp",
     "title": "The family's party since the 2019 switch."},

    {"id": "members", "label": "Farmer-members (~100,000)", "group": "base",
     "title": "The nominal owners of the cooperative. Source: Down To Earth (2019)."},
    {"id": "votebank", "label": "Cane-growers' vote bank", "group": "base",
     "title": "Members mobilised electorally through the cooperative's patronage."},
    {"id": "pawar", "label": "Sharad Pawar / NCP leadership", "group": "rival",
     "title": "Regional rival. The NCP's refusal to cede the Ahmednagar seat triggered the 2019 switch. Source: Deccan Herald (2019)."},
]

# nodes that form the capture loop
LOOP_NODES = {"radhakrishna", "factory", "bank"}

# ----- edges -----
# type drives styling; loop=True marks the three edges of the capture loop
# 'party' on affiliation/vote edges is resolved by period in app.py

STATIC_EDGES = [
    {"src": "vitthalrao", "dst": "balasaheb", "label": "father", "type": "family"},
    {"src": "balasaheb", "dst": "radhakrishna", "label": "father", "type": "family"},
    {"src": "radhakrishna", "dst": "sujay", "label": "father", "type": "family"},

    {"src": "vitthalrao", "dst": "factory", "label": "founded 1950", "type": "founding"},
    {"src": "balasaheb", "dst": "college", "label": "founded", "type": "founding"},
    {"src": "balasaheb", "dst": "ibmrd", "label": "founded", "type": "founding"},

    {"src": "radhakrishna", "dst": "factory", "label": "Chairman", "type": "directorship", "loop": True,
     "title": "Radhakrishna Vikhe Patil chairs the factory board. Source: board roster (PFR, 2021)."},
    {"src": "sujay", "dst": "factory", "label": "Expert Director", "type": "directorship",
     "title": "Sujay Vikhe Patil is an Expert Director on the board. Source: board roster (PFR, 2021)."},
    {"src": "radhakrishna", "dst": "bank", "label": "director", "type": "directorship", "loop": True,
     "title": "R. Vikhe Patil also sat on the cooperative bank board. Source: Down To Earth (2019)."},
    {"src": "bank", "dst": "factory", "label": "loan ~Rs 35 cr (2017)", "type": "loan", "loop": True,
     "title": "Cheap credit routed from the bank to the sugarcane venture whose board the borrower also sat on. Source: Down To Earth (2019)."},

    {"src": "members", "dst": "factory", "label": "own", "type": "ownership",
     "title": "Nominal ownership by the farmer-members."},
    {"src": "members", "dst": "votebank", "label": "mobilised as", "type": "mobilise"},
    {"src": "factory", "dst": "votebank", "label": "FRP, jobs, patronage", "type": "mobilise",
     "title": "Cane payments, employment and harvesting contracts, framed as favours."},

    {"src": "pawar", "dst": "ncp", "label": "leads", "type": "rival"},
    {"src": "pawar", "dst": "sujay", "label": "seat denied, 2019", "type": "rival",
     "title": "The NCP under Pawar refused the Ahmednagar seat, triggering the switch. Source: Deccan Herald (2019)."},
]

def party_edges(period):
    """Affiliation and vote-delivery edges that flip with the 2019 switch."""
    party = "congress" if period == "before" else "bjp"
    ptitle = ("Congress affiliation, founding era to 2019."
              if period == "before"
              else "BJP affiliation since the 2019 switch. Source: Deccan Herald (2019).")
    return [
        {"src": "radhakrishna", "dst": party, "label": "affiliation", "type": "affiliation",
         "party": party, "title": ptitle},
        {"src": "sujay", "dst": party, "label": "affiliation", "type": "affiliation",
         "party": party, "title": ptitle},
        {"src": "votebank", "dst": party, "label": "delivers votes", "type": "votes",
         "party": party,
         "title": "The mobilised membership is delivered to whichever party the family currently holds."},
    ]

# ----- legend -----
LEGEND = [
    {"label": "Vikhe Patil dynasty", "color": COLORS["dynasty"]["bg"]},
    {"label": "Sugar factory", "color": COLORS["factory"]["bg"]},
    {"label": "Cooperative bank", "color": COLORS["bank"]["bg"]},
    {"label": "Family trusts", "color": COLORS["trust"]["bg"]},
    {"label": "Congress", "color": COLORS["congress"]["bg"]},
    {"label": "NCP / rival", "color": COLORS["ncp"]["bg"]},
    {"label": "BJP", "color": COLORS["bjp"]["bg"]},
    {"label": "Farmers / vote bank", "color": COLORS["base"]["bg"]},
]

# ----- the actual 2021 board roster (transcribed from the PFR document) -----
# is_dynasty flags the two seats held by the family
BOARD = [
    (1, "Radhakrishna E. Vikhe Patil (MLA)", "Chairman", True),
    (2, "Vishwasrao Kashevrao Kadu Patil", "Vice Chairman", False),
    (3, "Kailas Suryabhan Tambe Patil", "Director", False),
    (4, "Dinkar Ganpat Gaikawad Patil", "Director", False),
    (5, "Bhanudas Lahanu Tambe Patil", "Director", False),
    (6, "Devichand Bharat Tambe Patil", "Director", False),
    (7, "Uttamrao Rambhau Dighe Patil", "Director", False),
    (8, "Sanjay Sopanrao Aher Patil", "Director", False),
    (9, "Dadasaheb Chandrabhan Ghogare Patil", "Director", False),
    (10, "Dhananjay Babasaheb Dale Patil", "Director", False),
    (11, "Swapnil Suresh Nibe Patil", "Director", False),
    (12, "Dattatraya Sahebrao Kharde Patil", "Director", False),
    (13, "Sahebrao Jijaba Mhaske Patil", "Director", False),
    (14, "Satish Shivajirao Sasane Patil", "Director", False),
    (15, "Sampatrao Bhaurao Chitalkar Patil", "Director", False),
    (16, "Rambhau Shankarrao Bhusal Patil", "Director", False),
    (17, "Babu Fakira Palghadmal Patil", "Director", False),
    (18, "Shantaram Genu Jori Patil", "Director", False),
    (19, "Subhash Namdev Antre Patil", "Director", False),
    (20, "Ujwala Ashok Gholap", "Director", False),
    (21, "Sangeeta Bhaskar Kharde", "Director", False),
    (22, "Dr. Sujay Radhakrishna Vikhe Patil (MP)", "Expert Director", True),
    (23, "Annasaheb Murlidhar Mhaska Patil", "Expert Director", False),
    (24, "Popatrao Aanadrao Wani Patil", "Functional Director", False),
    (25, "Dilip Gorakshnath Kadu Patil", "Functional Director", False),
    (26, "T. R. Dhone", "Managing Director", False),
]

# ----- sources -----
SOURCES = [
    ("Board roster (2021)", "Padmashri Dr. Vitthalrao Vikhe Patil SSK Ltd, Pre-Feasibility Report submitted to MoEF&CC, 2021."),
    ("The 2017 bank loan and the ownership figures", "Down To Earth (2019), 'Sugarcane farmers caught in a maze of brotherhood of brokers'."),
    ("The 2019 party switch and the Pawar rivalry", "Deccan Herald (2019), reporting on the Vikhe Patil move to the BJP."),
    ("FRP payment and arrears", "Sugar Commissionerate, Maharashtra (2026), Statement A, sugar season 2025-26, as on 28 February 2026."),
]

# ----- FRP snapshot (for the small data row) -----
FRP = {"paid_pct": "71.5%", "arrears": "~Rs 72 cr", "asof": "28 Feb 2026"}
