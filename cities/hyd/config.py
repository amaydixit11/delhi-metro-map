import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from city_config import make
globals().update(make(os.path.dirname(os.path.abspath(__file__)), {"redlinecorri":[8297636],"bluelinecorr":[8297688],"greenlinecor":[10692235]}, {}))
