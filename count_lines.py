#!/usr/bin/env python3

from type_error_messages import FileTypeErr

class LineCounter:

    """
    Very simple class to count lines in file.
    """

    def __init__(self, in_file):
        variable_obj = FileTypeErr(in_file)
        variable_obj.Asses_Type()
        self.in_file = in_file

    def Count_lines(self):
        line_count = 0
        for _ in self.in_file:
            line_count += 1
        return line_count

