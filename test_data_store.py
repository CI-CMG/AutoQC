import abc


class TestDataStore(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def is_prepared(self, key):
    pass

  @abc.abstractmethod
  def prepare(self, key, field_list):
    pass

  @abc.abstractmethod
  def put(self, uid, key, field_dict):
    pass

  @abc.abstractmethod
  def get(self, uid, key):
    pass