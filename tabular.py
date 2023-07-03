#!/usr/bin/env python3

from .file_main import File
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
        
        allowed_return_types = ['str', 'string', 'list', 'List']
        if return_type not in allowed_return_types:
            print('the return_type argument is not allowed, given :', return_type, '  allowed values', allowed_return_types, "\n", file=stderr)
            raise TypeError("Argument not allowed.")
        
        l = self.string.split(self.delimiter)
        l.pop(position)
        if return_type == 'list' or return_type == 'List':
            return l
        
        # in the elif implement other cases

        # return the string
        else:
            return self.delimiter.join(l)

    def MergeByKeyPos(self, tabline_onject2, pos1=0, pos2=0):
        """
        This function takes two strings/lines and merges them if the key positions provided point to a substring that
        is identical in both lines.
        otherwise it return None variable.
        The idea is that we want to merge toghether two lines if they share a common key/substring 
        outputing one single line. that is the concatenation of the two lines without the repeated substring, like this:
        line1 -> a,b,c\n        line2  ->  d,b,e,f\n
        pos1 = 1                pos2 = 1
        output -> a,b,c,d,e,f 
        By default the script will match by the first position -> 0
        The script will also return the final line with the delimitator of the first line, this is done so that when for example
        a tsv and a csv files are joined all line will have the same spatiatior.
        """


        # Calling of other functions inside this class
        key1 = self.ExtractField(pos1)
        key2 = tabline_onject2.ExtractField(pos2)
        line2_minus_key = tabline_onject2.ExtractAllButField(pos2, return_type='List')

        # strip just in case
        if (key1.strip()) == (key2.strip()):
            return (self.string.rstrip() + self.delimiter + ( self.delimiter.join(line2_minus_key) ))
        else:
            return None


        

        


        

class TabularFile(File):
    """
    Abstract class parent for all types of tabular file, like tsv csv ecc..
    Child of the very general File class
    """

    def __init__(self, file_name):
        super().__init__(file_name)

    
    def IntersectTables(self, table_object2, out_filename, pos1=0, pos2=0):
        """
        This function takes two tabular files objects and writes to out_filename the intersection of them.
        By intersection is meant all lines that have a matching position. Given the example:
        line1 in file1 -> a,b,c\n    line2 in file2 ->  d,b,e,f\n      pos1 in file1 = 1      pos2 in file2 = 1
        in the output file will be written -> a,b,c,d,e,f\n
        All lines in file1 are checked against all lines in file2, in a line by line fashion.
        Non-matching pairs of lines will not be written, as well as lines that do not have a match in the other file.
        """


        # First check if the two files exist before attemping intersection
        self.CheckExists()
        table_object2.CheckExists()

        # Open the first file an go line by line, second file will be opened number_of_line_in_file1
        file1 = self.OpenRead()
        out = open(out_filename, 'w')
        for line1 in file1:
            file2 = table_object2.OpenRead()
            for line2 in file2:
                tabline_obj = TabularLine(line1, pos1)
                matched_lines = MatchByKeyPos(line1, line2, pos1, pos2, del1, del2, check)
                    matched_line = matched_lines.Match()
                    if matched_line:
                        out.write(matched_line)

            

    

class TSV(TabularFile):
    """
    Still to implement remember it must not open the file on start
    """

    def __init__(self, file_name):
        super().__init__(file_name)


class CSV(TabularFile):
    """
    Still to implement remember it must not open the file on start
    """

    def __init__(self, file_name):
        super().__init__(file_name)