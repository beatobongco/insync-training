class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, '_inst'):
      cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
    return cls._inst

# Subclassing is a problem
class Foo(Singleton):
  def hello(self):
    pass

class Bar(Foo):
  def hello_bar(self):
    pass

f = Foo()
b = Bar()

print isinstance(b, Bar)
print isinstance(b, Foo)
print isinstance(f, Foo)

