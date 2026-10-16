import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from city_config import make
globals().update(make(os.path.dirname(os.path.abspath(__file__)), {"line1blue":[3808111],"line2ayellow":[13989912],"line2byellow":[20403808],"line3aqua":[7898597],"line7red":[13989915],"line9red":[20403865],"navimumbaime":[16533436]}, {}))
