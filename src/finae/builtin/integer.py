from ..core import Attribute, Concept


@Concept
class Float:

    @Attribute
    def value(self):
        return float(self.__finae_text__())


@Concept
class Integer:

    @Attribute
    def value(self):
        return int(self.__finae_text__())



def test_parse():
    a = Integer('123124')
    print(a.value())
