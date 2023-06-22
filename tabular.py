#!/usr/bin/env python3

from type_error_messages import StrTypeErr
from type_error_messages import IntTypeErr
from type_error_messages import ListTypeErr\

class TabularLine():
    """
    tabular specific helper functions are stored in this class, it is meant to work on strings instead of files.
    The idea behind is to work on files line by line to decreas memory usage.
    It by default checks if the two input are of the correct type -> both string type
    """

    def __init__(self, string, delimiter='\t', check_type=False) -> None:
        self.string = string
        self.delimiter = delimiter

        #usefull for debug
        if check_type:
            err_message1 = StrTypeErr(self.string)
            err_message1.Asses_Type()
            err_message2 = StrTypeErr(self.delimiter)
            err_message2.Asses_Type()



class Extract(TabularLine):
    """
    subclass parent to all extract types functions
    """

    def __init__(self, string,  delimiter='\t', check_type=False) -> None:
        super().__init__(string, delimiter, check_type)


  
class ExtractField(Extract):
    """
    extracts and returns the requested field from the line
    """

    def __init__(self, string, position, delimiter='\t', check_type=False) -> None:
        super().__init__(string, delimiter, check_type)
        self.position = position

        #usefull for debug
        if check_type:
            err_mssg_pos = IntTypeErr(self.position)
            err_mssg_pos.Asses_Type()


    def Get_Field(self):
        return (self.string.split(self.delimiter)[self.position])
    


class ExtractNFields(Extract):
    """
    extracts more than one field. The variable position in this case refers to a list of integers that are
    all the fields/column of interest to be extracted
    """

    def __init__(self, string, position, delimiter='\t', check_type=False) -> None:
        super().__init__(string, delimiter, check_type)
        self.position = position

        #usefull for debug
        if check_type:
            err_mssg_pos = ListTypeErr(self.position)
            err_mssg_pos.Asses_Type()


    def Get_Fields(self):
        out_list = []
        for i in self.position:
            out_list.append(self.string.split(self.delimiter)[i])
        return out_list


class ExtractAllButField(Extract):
    """
    extracts the whole line except the field asked, is basically a special case of slice.
    It can return a string (default) or a list as output.
    """

    def __init__(self, string, position, delimiter='\t', check_type=False) -> None:
        super().__init__(string, delimiter, check_type)
        self.position = position

        #usefull for debug
        if check_type:
            err_mssg_pos = IntTypeErr(self.position)
            err_mssg_pos.Asses_Type()

    # return the string
    def Remove_str(self):
        l = self.string.split(self.delimiter)
        l.pop(self.position)
        return self.delimiter.join(l)
    
    # returns the list
    def Remove_element(self):
        l = self.string.split(self.delimiter)
        l.pop(self.position)
        return l
