# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 18:09:01 2017

@author: rochus

          aftype

          a class for an aftype (atomtype and fragmenttype)

"""

# generates the missing rich comparison methods
from functools import total_ordering

@total_ordering
class aftype(object):

    def __init__(self, atype, fragtype):
        self.atype = atype
        self.fragtype = fragtype
        return

    @property
    def atype(self):
        return self._atype

    @atype.setter
    def atype(self, at):
        self._atype = at
        if not "_" in at:
            self._truncated = True
            self._atype_trunc = at
        else:
            self._truncated = False
            self._atype_trunc = at.split("_")[0]
        return

    @property
    def fragtype(self):
        return self._fragtype

    @fragtype.setter
    def fragtype(self, ft):
        self._fragtype = ft

    def __repr__(self):
        return "%s@%s" % (self._atype, self._fragtype)

    def __eq__(self, other):
        assert type(other) is aftype
        if self._truncated or other._truncated:
            return (self._atype_trunc == other._atype_trunc) and (self._fragtype == other._fragtype)
        else:
            return (self._atype == other._atype) and (self._fragtype == other._fragtype)

    def __lt__(self, other):
        assert type(other) is aftype
        return ("%s@%s" % (self._atype, self._fragtype)) < ("%s@%s" % (other._atype, other._fragtype))

    def __gt__(self, other):
        assert type(other) is aftype
        return ("%s@%s" % (self._atype, self._fragtype)) > ("%s@%s" % (other._atype, other._fragtype))



def aftype_sort(afl, ic):
    """
    helper function to sort a list of aftype objects according to the type (ic)
    """
    if ic == "bnd":
        afl.sort()
    elif ic == "ang":
        if afl[0] > afl[2]: afl.reverse()
    elif ic == "dih":
        if afl[1] > afl[2]:
            afl.reverse()
        elif afl[1] == afl[2]:
            if afl[0] > afl[3]: l.reverse()
    elif ic == "oop":
        plane = afl[1:]
        plane.sort()
        afl[1:] = plane
    else:
        raise ValueError, "Unknown ic %s in aftype_sort" % ic
    return afl


if __name__ == "__main__":
    a = aftype("c3_c3", "ph")
    b = aftype("c3_c2h1", "ph")
    c = aftype("c3", "ph")
    d = aftype("c3", "co2")

    print a == b
    print a == c
    print a == d

    l = [a,b,c,d]
    l.sort
    print l

    print aftype_sort(l, "oop")
