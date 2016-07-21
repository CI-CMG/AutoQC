# usage: python build-db.py <wod ascii file name> <table name to append to>

import psycopg2
from wodpy import wod
import sys
import util.main as main

# connect to database and create a cursor by which to interact with it.
try:
    conn = psycopg2.connect("dbname='root' user='root'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

# Identify tests
testNames = main.importQC('qctests')
testNames.sort()

# set up our table
query = "CREATE TABLE IF NOT EXISTS " + sys.argv[2] + """(
            lat real, 
            long real, 
            uid integer,
            cruise integer,
            year integer,
            month integer,
            day integer,
            time real,
            probetype integer,
            depth real[], 
            temperature real[],
            salinity real[],
            truth boolean,
            n_levels integer,
        """
for i in range(len(testNames)):
    query += testNames[i].lower() + ' boolean'
    if i<len(testNames)-1:
        query += ','
    else:
        query += ');'

cur.execute(query)

# populate table from wod-ascii data
fid = open(sys.argv[1])
while True:
    profile = wod.WodProfile(fid)
    wodDict = profile.npdict()
    wodDict['z'] = "'{" + ",".join(map(str, wodDict['z'])) + "}'"
    wodDict['t'] = "'{" + ",".join(map(str, wodDict['t'])) + "}'"
    wodDict['s'] = "'{" + ",".join(map(str, wodDict['s'])) + "}'"
    wodDict['truth'] = sum(profile.t_level_qc(originator=True) >= 3) >= 1
    
    query = "INSERT INTO " + sys.argv[2] + " (lat, long, uid, cruise, year, month, day, time, probetype, depth, temperature, salinity, truth, n_levels) "  + """ VALUES(
                {p[latitude]}, 
                {p[longitude]}, 
                {p[uid]}, 
                {p[cruise]},
                {p[year]},
                {p[month]},
                {p[day]},
                {p[time]},
                {p[probe_type]},
                {p[z]}, 
                {p[t]},
                {p[s]},
                {p[truth]},
                {p[n_levels]}
               )""".format(p=wodDict)
    query = query.replace('--', 'NULL')
    query = query.replace('None', 'NULL')
    cur.execute(query)
    if profile.is_last_profile_in_file(fid) == True:
        break

conn.commit()
