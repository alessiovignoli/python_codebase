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


    def ExtractAllButField(self, position, return_type='STR'):
        """
        extracts the whole line except the field asked, is basically a special case of slice.
        It can return a string (default) or a list as output. (more if implemnted)
        """

        #usefull for debug
        if self.check_type:
            err_mssg_pos = IntTypeErr(position)
            err_mssg_pos.Asses_Type()
        
        allowed_return_types = ['STR', 'STRING', 'LIST']
        if return_type.upper() not in allowed_return_types:
            print('the return_type argument is not allowed, given :', return_type.upper(), '  allowed values', allowed_return_types, "\n", file=stderr)
            raise TypeError("Argument not allowed.")
        
        l = self.string.split(self.delimiter)
        l.pop(position)
        if return_type.upper() == 'LIST':
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

    def __init__(self, file_name, delimiter, header_flag=True, header_lines=1):
        super().__init__(file_name)
        self.delimiter = delimiter

        # Set header related variables  
        self.header_flag = header_flag
        if header_flag:
            self.header_lines = header_lines
        else:
            self.header_lines = 0
        

    
    def IntersectTables(self, table_object2, out_filename, pos1=0, pos2=0,  check_type=False):
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

            #Initialize a tabular line object to perform the merge later
            tabline_obj = TabularLine(line1, self.delimiter, check_type)

            for line2 in file2:
                
                # Line2 also needs to be an instance of class tabular line
                tabline2_obj = TabularLine(line2, table_object2.delimiter,  check_type)
                merged_lines = tabline_obj.MergeByKeyPos(tabline2_obj, pos1, pos2)

                # Since the merga return None value when it did not find a match this if is necessary 
                if merged_lines:
                    out.write(merged_lines)

            # Need to close file2 so it can be re-opened and have all flines again
            file2.close()
    

    def CountUniqueIDs(self, pos, check_type=False):
        """
        this function computes how many values of given field/column are unique, aka not identical, using exact string matching.
        Header lines are not considered by this function.
        """

        seen_ids = []    
        infile = self.OpenRead()
        self.RemoveHeader(infile, self.header_lines)
        for line in infile:
            tabline_obj = TabularLine(line, self.delimiter, check_type)
            id_value = tabline_obj.ExtractField(pos)
            if id_value not in seen_ids:
                seen_ids.append(id_value)
        return len(seen_ids)
    

    def GrepLine(self, keyword):
        """
        Returns lines that have a given field in them, (substring). Using the in built in function of python.
        Input is a list or a string. Output is a list , empty if nothing is found.
        """

        # First check if the file exist before attemping anything else
        self.CheckExists()

        # Second thing is to check if the keyword is a string or a list and unify to list for the for loop
        keyword_list = None
        try:
            err_message1 = StrTypeErr(keyword, no_print=True)
            err_message1.Asses_Type()
        except TypeError:
            err_message2 = ListTypeErr(keyword, custom_print='Variable must be string or list type')
            err_message2.Asses_Type()
            keyword_list = keyword
        else:
            keyword_list = [keyword]
        
        # open the input file and scroll through it
        infile = self.OpenRead()
        grepped_lines = []
        for line in infile:
            for word in keyword_list:
                if word in line:
                    grepped_lines.append(line)
                    break
        return grepped_lines


    def ExtractColumn(self, pos, return_type='LIST', strip=True, check_type=False):
        """
        This function extracts specific columns from a tabular file.
        The output can be of ?two? types list or set (more can be implemented). Default list.
        Set has the property to not have identical/repeated elements in it.
        It is basically a list of unique elements.
        Fields values are stripped by default, but this can be changed.
        If this function is asked to return a list, it will have all the values found at that position. 
        If some lines in the file do not have the column asked no error will be raised, for this reason
        If the column position asked for is higher than the number of columns an empty list is returned.
        """

        # First check if the file exist and pos is an integer
        self.CheckExists()
        err_mssg_pos = IntTypeErr(pos)
        err_mssg_pos.Asses_Type()

        # open the input file and scroll through it
        infile = self.OpenRead()

        # Check if the correct word is passed for output type
        allowed_return_types = ['SET', 'LIST']
        if return_type.upper() not in allowed_return_types:
            print('the return_type argument is not allowed, given :', return_type.upper(), '  allowed values', allowed_return_types, "\n", file=stderr)
            raise TypeError("Argument not allowed.")
        
        # Extract the fields or trying to and strip in case
        col_list = []
        for line in infile:
            try:
                tabline_obj = TabularLine(line, self.delimiter, check_type)
                field_value = tabline_obj.ExtractField(pos)
            except IndexError:
                continue
            else:
                if strip:
                    col_list.append(field_value.strip())
                else:
                    col_list.append(field_value)

        # Define the output type
        if return_type.upper() == 'LIST':
            return col_list
        
        # PUT HERE THE OTHER TYPE OF OUTPUTS AND CONVERSION LINES

        # THe else is reserved to set type
        else:
            return set(col_list)





class TSV(TabularFile):
    """
    Still to implement remember it must not open the file on start
    """

    def __init__(self, file_name, header_flag=True, header_lines=1):
        self.delimiter = '\t'
        super().__init__(file_name, delimiter=self.delimiter, header_flag=header_flag, header_lines=header_lines)



class CSV(TabularFile):
    """
    Still to implement remember it must not open the file on start
    """

    def __init__(self, file_name, header_flag=True, header_lines=1):
        self.delimiter = ','
        super().__init__(file_name, delimiter=self.delimiter, header_flag=header_flag, header_lines=header_lines)