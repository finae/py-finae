"""Useful concepts."""

from ..core import Attribute, Concept


@Concept
class Yes:

    @Attribute(required=False)
    def contain_yes(self):
        return 'yes' in self.__finae_text__().lower()


@Concept
class No:

    @Attribute(required=False)
    def contain_no(self):
        return 'no' in self.__finae_text__().lower()


@Concept
class Array:
    pass
