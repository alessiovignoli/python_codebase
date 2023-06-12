#!/usr/bin/env python3

from abc import ABC, abstractmethod
from tabular import ExtractField
from count_lines import LineCounter

class TableParser(ABC):

    """
    Very general and broad class for parsing a tabular format file. This time the input is the whole file in itself. (already opened).
    Evrey line should have one or more fields, all separated by an unique separator, 
    files that abide to this concepts are tsv and csv for example.
    It is not thought to write the input file just to read and do stuff based on reading.
    """

    def __init__(self, infile) -> None:
        self.infile = infile
        line_counter = LineCounter(infile)
        self.total_lines = line_counter.Count_lines()
    



    