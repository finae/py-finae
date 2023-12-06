from ..core import Attribute, Concept


@Concept
class Float:

    @Attribute
    def value(self):
        return float(self.text())


@Concept
class Integer:

    @Attribute
    def value(self):
        return int(self.text())



def test_parse():
    a = Integer('123124')
    print(a.value())
