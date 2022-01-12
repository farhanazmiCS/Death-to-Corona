import csv
import sys
from cs50 import SQL

db = SQL("sqlite:///vaccine.db")

if len(sys.argv) != 2:
    print("Incorrect no. of command-line arguments.")
    exit(0)

else:
    with open(sys.argv[1]) as vaccine_csv:
        vaxLocations = csv.reader(vaccine_csv)
        next(vaxLocations)
        for col in vaxLocations:
            var = [None] * 7
            var[0] = col[0]
            var[1] = col[1]
            var[2] = col[2]
            var[3] = col[3]
            var[4] = col[4]
            var[5] = col[5]
            var[6] = col[6]

            insert = db.execute("INSERT INTO locations (name, address, x, y, longitude, latitude, zone) VALUES (?, ?, ?, ?, ?, ?, ?)", var[0], var[1], var[2], var[3], var[4], var[5], var[6])


