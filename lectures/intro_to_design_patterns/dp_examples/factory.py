from ideskutils.collexions import namedtuplex

WorkerKind = namedtuplex('WorkerKind',
  # FS, GD, AC, FSGD
  'domain',
  # ADD, DEL, etc.
  'type',
  )

Work = namedtuplex('Work',
  'id',
  'fs_id',
  'gd_id',
  'type',
  )

class Worker(object):
  __classes = {}

  @classmethod
  def Kind(cls, domain, work_type):
    def wrapper(worker_class):
      worker_class.kind = WorkerKind(domain, work_type)
      cls.__classes[worker_class.kind] = worker_class
      return worker_class
    return wrapper

  @classmethod # Factory
  def build(cls, work):
    domain = ''
    if work.fs_id:
      domain += 'FS'
    if work.gd_id:
      domain += 'GD'
    if not domain:
      domain = 'AC'
    worker_class = cls.__classes.get((domain, work.type))
    if not worker_class:
      raise Exception("Work %r doesn't have a Worker class." % work.id)
    return worker_class(work)

  def __init__(self, work):
    self._work = work

  def __repr__(self):
    class_name = type(self).__name__
    repr_values = []
    repr_values.append("work_id=" + repr(self._work.id))
    if self.kind.domain == '-': #
      repr_values.append("type=" + repr(self._work.type))
    if self._work.fs_id:
      repr_values.append("fs_id=" + repr(self._work.fs_id))
    if self._work.gd_id:
      repr_values.append("gd_id=" + repr(self._work.gd_id))
    return class_name + "(" + ', '.join(repr_values) + ")"


# Use decorators to register with the factory
@Worker.Kind('AC', 'FSP')
class FSWorkProducer(Worker):
  """FS work producer.

  """
  pass


@Worker.Kind('FS', 'ADD_UL')
class FSAdder(Worker):
  "Upload worker"
  pass

@Worker.Kind('FSGD', 'ADD_DL')
class GDAdder(Worker):
  "Download worker"
  pass


works = []
works.append(Work(-10, None, None, type='FSP')) #AC FSWorkProducer
works.append(Work(id=1, fs_id=91, gd_id=None, type='ADD_UL')) #FS FSAdder
works.append(Work(id=2, fs_id=98, gd_id='GIBBERISH', type='ADD')) #FSGD GDAdder

for work in works:
  print Worker.build(work)
