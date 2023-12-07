"""Useful primitive concepts."""

from ..core import Attribute, Concept


@Concept
class Yes:

    @Attribute(key='answer')
    def contain_yes(self):
        text = self.text().lower().strip()
        if text.startswith('yes') or text.startswith('positive'):
            return True
        return False
    
    @Attribute(key='answer')
    def keep_asking(self):
        yes = Yes('Is it a positive or negative answer? Can you give one word?')
        return yes


@Concept
class No:

    @Attribute(key='answer')
    def contain_no(self):
        text = self.text().lower().strip()
        if text.startswith('no') or text.startswith('negative'):
            return True
        return False

    @Attribute(key='answer')
    def keep_asking(self):
        no = No('Is it a positive or negative answer? Can you give one word?')
        return no


def test_yes():
    a = Yes("""Answer: Yes, red is a color. It is one of the primary colors and is often associated with emotions such as love, passion, and anger.
                 
Is it a positive or negative answer? Can you give one word?""")
    print(a)
    
    
def test_no():
    a = No("""No, Aconcagua is not in Europe.

Aconcagua is the highest mountain in the Americas and the highest peak outside Asia. It is located in the Andes mountain range, in Argentina, South America. Europe, on the other hand, is a continent located to the north and east of the Atlantic Ocean, and is separated from South America by the Southeast Atlantic Ocean. Therefore, Aconcagua is not in Europe.
                 
Is it a positive or negative answer? Can you give one word?""")
    print(a)

