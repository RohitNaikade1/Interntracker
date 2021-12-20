from Package import *
from datetime import *

day=datetime.today().strftime('%A')

if day == "Saturday" or day == "Sunday":
    print("Enjoy weekend")
else:
    print(day)
# Mentors=db.Mentors

# data=Mentors.find({})

# for d in data:
#  print(d['interns'])