"""Useful primitive concepts."""

from ..core import Attribute, Concept


@Concept
class Yes:

    @Attribute
    def contain_yes(self):
        text = self.text().lower().strip()
        if text.startswith('yes') or text.startswith('positive'):
            return True
        return False
    
    @Attribute
    def keep_asking(self):
        yes = Yes('Is it a positive or negative answer? Can you give one word?')
        return yes


@Concept
class No:

    @Attribute
    def contain_no(self):
        text = self.text().lower().strip()
        if text.startswith('no') or text.startswith('negative'):
            return True
        return False

    @Attribute
    def keep_asking(self):
        no = No('Is it a positive or negative answer? Can you give one word?')
        return no

