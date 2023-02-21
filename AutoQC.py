from wodpy import wod
import pickle, sys, os, calendar, time, ast, getopt
import numpy as np
import util.main as main
from multiprocessing import Pool

from db_buddy_finder import DbBuddyFinder
from db_test_data_store import DbTestDataStore

def run(test, profiles, parameters, data_store):
  '''
  run <test> on a list of <profiles>, return an array summarizing when exceptions were raised
  '''

  verbose = []
  exec('from qctests import ' + test)
  for profile in profiles:
    exec('verbose.append(' + test + '.test(profile, parameters, data_store))')

  return verbose

def process_row(uid, logdir, table='iquod', targetdb='iquod.db'):
  '''run all tests on the indicated database row'''

  # reroute stdout, stderr to separate files for each profile to preserve logs
  sys.stdout = open(logdir + "/" + str(uid) + ".stdout", "w")
  sys.stderr = open(logdir + "/" + str(uid) + ".stderr", "w")

  # extract profile
  profile = main.get_profile_from_db(uid, table, targetdb)

  # mask out error codes in temperature data
  main.catchFlags(profile)

  # run tests
  for itest, test in enumerate(testNames):
    try:
      result = run(test, [profile], parameterStore)[0]
    except:
      print(test, 'exception', sys.exc_info())
      result = np.zeros(profile.n_levels(), dtype=bool)

    try:
      query = "UPDATE " + table + " SET " + test.lower() + "=? WHERE uid=" + str(profile.uid()) + ";"
      main.dbinteract(query, [main.pack_array(result)], targetdb=targetdb)
    except:
      print('db exception', sys.exc_info())


########################################
# main
########################################

# parse options
options, remainder = getopt.getopt(sys.argv[1:], 't:d:b:n:p:l:h')
cores=1
targetdb = 'iquod.db'
dbtable = 'iquod'
logdir = '/AutoQClogs'
batchnumber = None
nperbatch = None
for opt, arg in options:
    if opt == '-b':
        batchnumber = ast.literal_eval(arg)
    if opt == '-d':
        dbtable = arg
    if opt == '-l':
        logdir = arg
    if opt == '-n':
        cores = ast.literal_eval(arg)
    if opt == '-p':
        nperbatch = ast.literal_eval(arg)
    if opt == '-t':
        targetdb = arg
    if opt == '-h':
        print('usage:')
        print('-b <batch number to process>')
        print('-d <db table name to create and write to>')
        print('-l <directory to write logfiles to>')
        print('-n <number of cores to use>')
        print('-p <how many profiles to process per batch>')
        print('-t <name of db file>')
        print('-h print this help message and quit')

# Identify and import tests
testNames = main.importQC('qctests')
testNames.sort()
print('{} quality control checks have been found'.format(len(testNames)))
testNames = main.checkQCTestRequirements(testNames)
print('{} quality control checks are able to be run:'.format(len(testNames)))
for testName in testNames:
  print('  {}'.format(testName))

# set up a directory for logging
logdir = logdir + "/autoqc-logs-" + str(calendar.timegm(time.gmtime()))
os.makedirs(logdir)

# Parallel processing.
print('\nPlease wait while QC is performed\n')

# set up global parmaeter store
parameterStore = {
  "table": dbtable,
  "db": targetdb,
  "buddy_finder": DbBuddyFinder()
}

data_store = DbTestDataStore(targetdb)

for test in testNames:
  exec('from qctests import ' + test)
  exec(test + '.loadParameters(parameterStore)')
  exec(test + '.prepare_data_store(data_store)')

# connect to database & fetch list of all uids
query = 'SELECT uid FROM ' + dbtable + ' ORDER BY uid;'
uids = main.dbinteract(query, targetdb=targetdb)

# launch async processes
if batchnumber is not None and nperbatch is not None:
  batchnumber = int(batchnumber)
  nperbatch   = int(nperbatch)
  startindex  = batchnumber*nperbatch
  endindex    = min((batchnumber+1)*nperbatch,len(uids))
else:
  startindex  = 0
  endindex    = len(uids)
pool = Pool(processes=int(cores))
for i in range(startindex, endindex):
  pool.apply_async(process_row, (uids[i][0], logdir, dbtable, targetdb))
pool.close()
pool.join()


