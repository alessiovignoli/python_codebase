#!/usr/bin/env python3

from type_error_messages import FileTypeErr
from type_error_messages import IntTypeErr

class FileHeader():

    """
    Simple calss to handle header lines when present.
    This class takes as input an already opened file object.
    It is both usefull for removing header lines (since the file is already opened) or
    extracting them and putting them in a list variable as strings
    depending on the called function
    """

    def __init__(self, in_file, header_lines=1):
        # first check if file is open
        variable_obj = FileTypeErr(in_file)
        variable_obj.Asses_Type()

        #check if header_lines is an int
        int_obj = IntTypeErr(header_lines)
        int_obj.Asses_Type()

        self.in_file = in_file
        self.header_lines = header_lines

    def RemoveHeader(self):
        for header_line in range(0, self.header_lines):
            self.in_file.readline()

    def ReturnHeader(self):
        header_list = []
        for header_line in range(0, self.header_lines):
            header_list.append(self.in_file.readline())
        return header_list
            
