#!/usr/bin/env python3

from .type_error_messages import StrTypeErr
from .type_error_messages import IntTypeErr
from .type_error_messages import ListTypeErr
from sys import stderr

class TabularLine(object):
    """
    tabular specific helper functions are stored in this class, it is meant to work on strings instead of files.
    The idea behind is to work on files line by line to decreas memory usage.
    """

    def __init__(self, string, delimiter='\t', check_type=False) -> None:
        self.string = string
        self.delimiter = delimiter
        self.check_type = check_type

        #usefull for debug
        if self.check_type:
            err_message1 = StrTypeErr(self.string)
            err_message1.Asses_Type()
            err_message2 = StrTypeErr(self.delimiter)
            err_message2.Asses_Type()
    

    def ExtractField(self, position):
        """
        extracts and returns the requested field from the line
        """

        #usefull for debug
        if self.check_type:
            err_mssg_pos = IntTypeErr(position)
            err_mssg_pos.Asses_Type()

        return (self.string.split(self.delimiter)[position])
    

    def ExtractNFields(self, positions):
        """
        extracts more than one field. The variable position in this case refers to a list of integers that are
        all the fields/column of interest to be extracted
        """

        #usefull for debug
        if self.check_type:
            err_mssg_pos = ListTypeErr(positions)
            err_mssg_pos.Asses_Type()

        out_list = []
        for i in positions:
            out_list.append(self.string.split(self.delimiter)[i])
        return out_list
    

    def ExtractAllFields(self):
        """
        simple function that returns all the fields of the line as elements in a list.
        """

        l = self.string.split(self.delimiter)
        return l


    def ExtractAllButField(self, position, return_type='str'):
        """
        extracts the whole line except the field asked, is basically a special case of slice.
        It can return a string (default) or a list as output. (more if implemnted)
        """

        #usefull for debug
        if self.check_type:
            err_mssg_pos = IntTypeErr(position)
            err_mssg_pos.Asses_Type()
        
        allowed_return_types = ['str', 'string', 'list']
        if return_type not in allowed_return_types:
            print('the return_type argument is not allowed, given :', return_type, '  allowed values', allowed_return_types, "\n", file=stderr)
            raise TypeError("Argument not allowed.")
        
        l = self.string.split(self.delimiter)
        l.pop(position)
        if return_type == 'list':
            return l
        
        # in the elif implement other cases

        # return the string
        else:
            return self.delimiter.join(l)


        

