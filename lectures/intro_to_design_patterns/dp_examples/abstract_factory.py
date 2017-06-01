from abc import ABCMeta, abstractmethod
import os

# Abstract factory
class ClientPlatform (object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def create_app_dialog(self):
    # Abstract factory method
    pass

  @abstractmethod
  def create_setup_dialog(self):
    # Abstract factory method
    pass

  @abstractmethod
  def create_icon_menu(self):
    # Abstract factory method
    pass

# Abstract Product Interfaces
class BaseAppDialog(object):
  @abstractmethod
  def show(self):
    pass

class BaseSetupDialog(object):
  @abstractmethod
  def show(self):
    pass

class BaseIconMenu(object):
  @abstractmethod
  def add_menuitem(self, text, action_cb):
    pass

# Concrete Classes implementing product interace
class WinAppDialog(BaseAppDialog):
  def __init__(self):
    print "Created Win App Dialog"

  def show(self):
    print "Called Win API show method"


class WinSetupDialog(BaseSetupDialog):
  def __init__(self):
    print "Created Win Setup Dialog"

  def show(self):
    print "Showing Win Setup Dialog"

class WinIconMenu(BaseIconMenu):
  def __init__(self):
    print "Created Win Icon Menu"

  def add_menuitem(self, text, action_cb):
    print "Called Win API add menu item with text = %r, action_cb = %r" % (text, action_cb)

"""
Other concrete classes/products

LinuxAppDialog
....
....
MacIconMenu
"""


# Concrete factory
class WinClientPlatform(ClientPlatform):
  def create_app_dialog(self):
    # factory method
    return WinAppDialog()

  def create_setup_dialog(self):
    # factory method
    return WinSetupDialog()

  def create_icon_menu(self):
    # factory method
    return WinIconMenu()

def client(concrete_factory):
  # Create and consume a product from dialog family
  app_dialog = concrete_factory.create_app_dialog()
  app_dialog.show()
  """
  app_dialog.draw()
  app_dialog.close()
  """
  # Create and consume a product from menu family
  icon_menu = concrete_factory.create_icon_menu()
  icon_menu.add_menuitem("hello", "PlayAdele")

if os.name == 'nt':
  concrete_factory = WinClientPlatform()
"""
elif os.name = 'linux':
  # Linux Concrete factory
else:
  # MAC concrete factory
"""

client(concrete_factory)