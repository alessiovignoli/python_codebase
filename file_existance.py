#!/usr/bin/env python3

from abc import ABC
from os import path
from type_error_messages import StrTypeErr
from sys import stderr

class FileExists(ABC):

    """
    Simple class for checking existance of file and reporting an error message in case it is not.
    The file is given as input as string
    """
    
    def __init__(self, file_name):

        #Check if variable given is string
        variable_obj = StrTypeErr(file_name)
        variable_obj.Asses_Type()
        self.file_name = file_name

    def Check(self):
        if not path.isfile(self.file_name):
            print(self.file_name, '  file does not exist or path is incorrect\n', file=stderr)
            raise TypeError("File does not exists")
