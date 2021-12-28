import os
import glob
from Package import *
from datetime import *

day = datetime.today().strftime('%A')

if day == "Sunday":
    files = glob.glob('Package/static/Sheets/*')
    for f in files:
        os.remove(f)
else:
    print("Other days")
