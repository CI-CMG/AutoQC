import io
import pickle
import sqlite3
import numpy as np

from test_data_store import TestDataStore
import util.main as main

class DbTestDataStore(TestDataStore):

  def __init__(self, db, *args, **kw):
    super().__init__(*args, **kw)
    self.__db = db
    self.__model = {}

  def is_prepared(self, key):
    return bool(self.__model.get(key))

  def prepare(self, key, field_list):
    sql = "CREATE TABLE IF NOT EXISTS " + key + " (uid INTEGER PRIMARY KEY"
    for field in field_list:
      sql = sql + ", " + field['name'] + " " + field['type']
    sql = sql + ")"
    main.dbinteract(sql, targetdb=self.__db)
    self.__model[key] = field_list

  def __serialize(self, arr):
    out = io.BytesIO()
    if type(arr) is np.ndarray or type(arr) is np.ma.core.MaskedArray:
      arr.dump(out)
    elif type(arr) is list:
      pickle.dump(arr, out)
    out.seek(0)
    return sqlite3.Binary(out.read())

  def __deserialize(self, blob):
    result = None
    if blob:
      bytes_io = io.BytesIO(blob)
      if bytes_io.getbuffer().nbytes:
        try:
          result = np.load(bytes_io,allow_pickle=True)
        except:
          result = pickle.load(bytes_io)
    return result

  def put(self, uid, key, field_dict):
    placeholders = ["?"]
    parameters = [uid]
    for field in self.__model[key]:
      placeholders.append("?")
      if field['type'] == 'BLOB':
        parameters.append(sqlite3.Binary(self.__serialize(field_dict[field['name']])))
      else:
        parameters.append(field_dict[field['name']])
    sql = "REPLACE INTO " + key + " VALUES(" + (",".join(placeholders)) + ")"
    main.dbinteract(sql, parameters, targetdb=self.__db)


  def get(self, uid, key):
    field_list = self.__model[key]
    field_names = []
    for field in field_list:
      field_names.append(field['name'])
    sql = "SELECT " + (", ".join(field_names)) + " FROM " + key + " WHERE uid = ?"
    db_result = main.dbinteract(sql, [uid], targetdb=self.__db)
    if db_result is not None and len(db_result) > 0:
      field_dict = {}
      i = 0
      for field in field_list:
        if field['type'] == 'BLOB':
          field_dict[field['name']] = self.__deserialize(db_result[0][i])
        else:
          field_dict[field['name']] = db_result[0][i]
        i += 1
      return field_dict
    return None