from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

from traits.api import HasTraits, Enum
from traitsui.api import View

class A(HasTraits):
    x = Enum(["foo","bar"])

a = A()
a.configure_traits()
