import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from city_config import make
globals().update(make(os.path.dirname(os.path.abspath(__file__)), {"purplelineli":[13917123],"aqualineline":[13916710]}, {}))
