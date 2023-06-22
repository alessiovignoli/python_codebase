#!/usr/bin/env python3

from abc import ABC, abstractmethod
from tabular import ExtractField
from tabular import ExtractAllButField



class TabularLinesMatcher(ABC):
    """
    This "super" class takes two strings/lines and matches them if the key provided is present in both.
    Any subclass of this only follow the above principle. 
    the How, specificities and particular behaviours are subclass specific.
    """

    def __init__(self, line1, line2) -> None:
        self.line1 = line1
        self.line2 = line2

    @abstractmethod
    def Match(self):
        pass



class MatchByKeyPos(TabularLinesMatcher):
    """
    This class takes two strings/lines and matches them if the key positions provided point to a substring that
    is identical in both lines.
    otherwise it return None variable.
    The idea is that we want to match toghether two lines if they share a common key/substring 
    outputing one single line. that is the concatenation of the two lines without the repeated substring, like this:
    line1 -> a,b,c\n        line2  ->  d,b,e,f\n
    pos1 = 1                pos2 = 1
    output -> a,b,c,d,e,f 
    By default the script will match by the first position -> 0
    The script will also return the final line with the delimitator of the first line, this is done so that when for example
    a tsv and a csv files are joined all line will have the same spatiatior.
    """

    def __init__(self, line1, line2, pos1=0, pos2=0, delimiter1='\t', delimiter2='\t', check_type=False) -> None:
        super().__init__(line1, line2)
        self.pos1 = pos1
        self.pos2 = pos2
        self.delimiter1 = delimiter1
        self.delimiter2 = delimiter2

        #usefull for debug
        if check_type:
            self.line1_extract = ExtractField(line1, pos1, delimiter1, True)
            self.line2_extract = ExtractField(line2, pos2, delimiter2, True)
        else:
            self.line1_extract = ExtractField(line1, pos1, delimiter1)
            self.line2_extract = ExtractField(line2, pos2, delimiter2)

        self.line2_minnus_key = ExtractAllButField(line2, pos2, delimiter2)

    def Match(self):
        key1 = self.line1_extract.Get_Field()
        key2 = self.line2_extract.Get_Field()
        if (key1.strip()) == (key2.strip()):
            line2_modified = self.line2_minnus_key.Remove_element()
            return (self.line1.rstrip() + self.delimiter1 + ( self.delimiter1.join(line2_modified) ))
        else:
            return None
