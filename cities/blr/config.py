import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from city_config import make
MAJ = "Nadaprabhu Kempegowda Station, Majestic"
globals().update(make(os.path.dirname(os.path.abspath(__file__)),
    {"purpleline": [1798771], "greenline": [1798772], "yellowline": [19421944]},
    {MAJ + " (Green Line)": MAJ, MAJ + " (Purple Line)": MAJ, "Mysore Road": "Mysuru Road", "Yeshwantpur": "Yeshwanthpur"}))
