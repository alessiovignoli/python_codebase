#!/usr/bin/env python3

from abc import ABC, abstractmethod
from os import path
from sys import stderr
import gzip
from .type_error_messages import StrTypeErr
from .type_error_messages import FileTypeErr
from .type_error_messages import IntTypeErr


class File(ABC):
    """
    Very broad class parent to all type of files. 
    It harbours functions that can be applied to all files.
    """

    def __init__(self, file_name):
        self.file_name = file_name
    

    def CheckExists(self):
        """
        Simple class for checking existance of file and reporting an error message in case it is not.
        The file is given as input as string
        """
        
        #Check if variable given is string
        variable_obj = StrTypeErr(self.file_name)
        variable_obj.Asses_Type()

        if not path.isfile(self.file_name):
            print(self.file_name, '  file does not exist or path is incorrect\n', file=stderr)
            raise TypeError("File does not exists")
        

    def RemoveHeader(self, file_obj, header_lines=1):
        """
        Simple function for removing header lines (since the file is already opened).
        It basically consumes the lines on an opened file.
        """

        # first check if file is open
        variable1_obj = FileTypeErr(file_obj)
        variable1_obj.Asses_Type()

        #check if header_lines is an int
        variable2_obj = IntTypeErr(header_lines)
        variable2_obj.Asses_Type()

        for _ in range(0, header_lines):
            file_obj.readline()

    
    def ReturnHeader(self, file_obj, header_lines=1):
        """
        Simple function for extracting header lines and putting them in a list variable as strings.
        It works on already opened files
        """

        # first check if file is open
        variable1_obj = FileTypeErr(file_obj)
        variable1_obj.Asses_Type()

        #check if header_lines is an int
        variable2_obj = IntTypeErr(header_lines)
        variable2_obj.Asses_Type()

        header_list = []
        for _ in range(0, header_lines):
            header_list.append(file_obj.readline())
        return header_list
    

    def CountLines(self, file_obj):
        """
        Very simple class to count lines in file.
        To not assume how to open the file, if compresse or not for example, this function works with already opened files.
        
        BE CAREFULL THIS FUNCTION WILL CONSUME FILE CONTENT

        """

        # first check if file is open
        variable1_obj = FileTypeErr(file_obj)
        variable1_obj.Asses_Type()

        line_count = 0
        for _ in file_obj:
            line_count += 1
        return line_count
    

    def OpenRead(self):
        """
        This function deals with opening the file for reading only.
        It automaticly check if file compressed and open it accordingly.
        It does so checking the extention. .gz -> gzip
        """

        #check for extention
        if self.file_name[-3:] == '.gz':
            opened_file = gzip.open(self.file_name, 'rb')
            return opened_file
        
        # Implement here other type of compression

        # if all implemented types of compression fail it is assumed not to be compressed
        else:
            opened_file = open(self.file_name, 'r')
            return opened_file
        
    
    def OpenWrite(self):
        """
        This function deals with opening the file for writing only.
        """
        
        opened_file = open(self.file_name, 'w')
        return opened_file


    def WriteGzip(self):
        """
        This function deals with opening the file for writing a gzip file.
        """

        opened_file = gzip.open(self.file_name, 'wb')
        return opened_file
    

    def OpenAppend(self):
        """
        This function deals with opening the file for appending to existing file.
         It automaticly check if file compressed and open it accordingly.
        It does so checking the extention. .gz -> gzip
        """

        #check for extention
        if self.file_name[-3:] == '.gz':
            opened_file = gzip.open(self.file_name, 'ab')
            return opened_file
        
        # Implement here other type of compression

        # if all implemented types of compression fail it is assumed not to be compressed
        else:
            opened_file = open(self.file_name, 'a')
            return opened_file