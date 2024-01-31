#!/usr/bin/env python3

from .file_main import File
from .type_error_messages import StrTypeErr
from .type_error_messages import BytesTypeErr
from .type_error_messages import BytesStrErr
from .type_error_messages import IntTypeErr
from .type_error_messages import ListTypeErr
from .type_error_messages import ListSetErr
from sys import stderr
from math import log

class TabularLine(object):
    """
    tabular specific helper functions are stored in this class, it is meant to work on strings instead of files.
    The idea behind is to work on files line by line to decreas memory usage.
    All function will always return a string or set/list/dict etc.. of strings.
    """

    def __init__(self, string, delimiter='\t', check_type=False) -> None:
        self.string = string
        self.delimiter = delimiter
        self.check_type = check_type

        #usefull for debug
        if self.check_type:
            err_message1 = BytesStrErr(self.string)
            err_message1.Asses_Type()
            err_message2 = BytesStrErr(self.delimiter)
            err_message2.Asses_Type()

        # Omogenize string and delimiter variables in case they are bytes, aka make them both string 
        if isinstance(self.string, bytes):
            self.string = self.string.decode('utf-8')
        if isinstance(self.delimiter, bytes):
            self.delimiter = self.delimiter.decode('utf-8')
        
    

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
        

    
    def IntersectTables(self, table_object2, outfile_obj, pos1=0, pos2=0, compress=False, check_type=False):
        """
        This function takes two tabular files objects and writes to out_filename the intersection of them.
        By intersection is meant all lines that have a matching position. Given the example:
        line1 in file1 -> a,b,c\n    line2 in file2 ->  d,b,e,f\n      pos1 in file1 = 1      pos2 in file2 = 1
        in the output file will be written -> a,b,c,d,e,f\n
        All lines in file1 are checked against all lines in file2, in a line by line fashion.
        Non-matching pairs of lines will not be written, as well as lines that do not have a match in the other file.
        The function can compress the output file iff specified. The outfile_obj has to be instanciated as part of the File class.
        """


        # First check if the two files exist before attemping intersection
        self.CheckExists()
        table_object2.CheckExists()

        # Open the first file an go line by line, second file will be opened number_of_line_in_file1
        file1 = self.OpenRead()

        # add .gz extention to the out filename if not present and compression requested and viceversa
        if outfile_obj.file_name[-3:] != '.gz' and compress:
            outfile_obj.file_name += '.gz'
        elif outfile_obj.file_name[-3:] == '.gz' and not compress:
            outfile_obj.file_name = outfile_obj.file_name[:-3]
        out = outfile_obj.OpenWrite()
        
        for line1 in file1:
            file2 = table_object2.OpenRead()

            #Initialize a tabular line object to perform the merge later
            tabline_obj = TabularLine(line1, self.delimiter, check_type)
            
            for line2 in file2:
                
                # Line2 also needs to be an instance of class tabular line
                tabline2_obj = TabularLine(line2, table_object2.delimiter,  check_type)
                merged_lines = tabline_obj.MergeByKeyPos(tabline2_obj, pos1, pos2)

                # Since the merga return None value when it did not find a match this if is necessary 
                # this also deals with compression
                if merged_lines and compress:
                    compresse_merged_lines = bytes(merged_lines, 'utf-8')
                    out.write(compresse_merged_lines)
                elif merged_lines and not compress:
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
        Input is a list or a string. Output is a list of string, empty if nothing is found.
    
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
        infile = self.OpenRead(uncompress=True)
        grepped_lines_dict = {}
        for line in infile:
            for word in keyword_list:
                if word in line:
                    if word in grepped_lines_dict:
                        grepped_lines_dict[word].append(line)
                    else:
                        grepped_lines_dict[word] = [line]

        # transform the dictionary to simple list conservin g order of input keyword list
        grepped_lines = []
        for dict_key in keyword_list:
            for grepped_line in grepped_lines_dict[dict_key]:
                grepped_lines.append(grepped_line)
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
        

    def HowManyIDsFirstQueryMin(self, id_pos, query_pos, check_type=False):

        """
        This function is thought to be applied to and ordered file, in which there are multiple instances of
        same value of Column ID, so to say that there can be consecutive lines with the identical value of Column ID.
        Such lines must be consecutive for this function to work, again value bubba in Col ID can not be in line1-2-3 and 5.
        Then this functions counts how many times for a given ID the value present in query_pos/Query_Column in the first line encountered
        is the lowest of those found for that id.
        For example if id=bubba on line one has value 10 in query field/column and in all other consecutive lines such id does not have
        an lower value in Query col, that would be counted as an instance by this function, aka +1 to final count.
        """

        # First check if the file exist and positional val are integer
        self.CheckExists()
        err_mssg1 = IntTypeErr(id_pos)
        err_mssg1.Asses_Type()
        err_mssg2 = IntTypeErr(query_pos)
        err_mssg2.Asses_Type()

        # open the file and remove header
        infile = self.OpenRead()
        self.RemoveHeader(infile, self.header_lines)

        # extract first non header line info so that the if in the for loop can work right away
        tabline_obj = TabularLine(infile.readline(), self.delimiter, check_type)
        first_list = tabline_obj.ExtractNFields([id_pos, query_pos])
        buffer_id = first_list[0]
        first_encounter_query = float(first_list[1].strip())    # The first value in query column per id
        first_query_min = True                                  # Flag to know if to add a +1 to the final counter
        final_counter = 0

        for line in infile:
            tabline_obj = TabularLine(line, self.delimiter, check_type)
            list_extracted = tabline_obj.ExtractNFields([id_pos, query_pos])
            
            # The case where identical id but the query value is lower than the first line in which the id was found
            # final_counter should not be updated in this case as intended
            if list_extracted[0] == buffer_id and float(list_extracted[1].strip()) <= first_encounter_query:
                first_query_min = False

            # The case in which a deifferent id is found and all info and flags should be updated and in case final_counter increased
            if list_extracted[0] != buffer_id:
                buffer_id = list_extracted[0]
                first_encounter_query = float(list_extracted[1].strip())
                if first_query_min:
                    final_counter += 1
                first_query_min = True

        # last iteration so that last id also has a chance to be compared
        if first_query_min:
            final_counter += 1
        return final_counter
    

    def HowManyIDsFirstQueryMax(self, id_pos, query_pos, check_type=False):

        """
        This function is thought to be applied to and ordered file, in which there are multiple instances of
        same value of Column ID, so to say that there can be consecutive lines with the identical value of Column ID.
        Such lines must be consecutive for this function to work, again value bubba in Col ID can not be in line1-2-3 and 5.
        Then this functions counts how many times for a given ID the value present in query_pos/Query_Column in the first line encountered
        is the highest of those found for that id.
        For example if id=bubba on line one has value 10 in query field/column and in all other consecutive lines such id does not have
        an higher value in Query col, that would be counted as an instance by this class, aka +1 to final count.
        """

        # First check if the file exist and positional val are integer
        self.CheckExists()
        err_mssg1 = IntTypeErr(id_pos)
        err_mssg1.Asses_Type()
        err_mssg2 = IntTypeErr(query_pos)
        err_mssg2.Asses_Type()

        # open the file and remove header
        infile = self.OpenRead()
        self.RemoveHeader(infile, self.header_lines)

        # extract first non header line info so that the if in the for loop can work right away
        tabline_obj = TabularLine(infile.readline(), self.delimiter, check_type)
        first_list = tabline_obj.ExtractNFields([id_pos, query_pos])
        buffer_id = first_list[0]
        first_encounter_query = float(first_list[1].strip())    # The first value in query column per id
        first_query_min = True                                  # Flag to know if to add a +1 to the final counter
        final_counter = 0

        for line in infile:
            tabline_obj = TabularLine(line, self.delimiter, check_type)
            list_extracted = tabline_obj.ExtractNFields([id_pos, query_pos])
            
            # The case where identical id but the query value is lower than the first line in which the id was found
            # final_counter should not be updated in this case as intended
            if list_extracted[0] == buffer_id and float(list_extracted[1].strip()) >= first_encounter_query:
                first_query_min = False

            # The case in which a deifferent id is found and all info and flags should be updated and in case final_counter increased
            if list_extracted[0] != buffer_id:
                buffer_id = list_extracted[0]
                first_encounter_query = float(list_extracted[1].strip())
                if first_query_min:
                    final_counter += 1
                first_query_min = True

        # last iteration so that last id also has a chance to be compared
        if first_query_min:
            final_counter += 1
        return final_counter


    def AggregateFromList(self, id_pos, grouping_pos, grouping_rule, check_type=False):
        """
        This function will output a dict object, and can work with both list or set as input.
        The values in grouping_pos column will be checked if present on the list/set, if true then added to the dict.
        The keys of the dict will be the values found in the list (grouping_pos) and the values of each key will be all the id_pos
        of every line that have such key. Example:
        line1 ->  a,2,3,4       line2 -> a,1,2,3,4      line3 -> b,33,4     line4 -> c,22,4
        grouping_rule = ['a', 'b']     id_pos = 2
        dict_out -> {'a': '3,2', 'b': '4'}
        """

        # First check if the file exist and positional val are integer
        self.CheckExists()
        err_mssg1 = IntTypeErr(id_pos)
        err_mssg1.Asses_Type()
        err_mssg2 = IntTypeErr(grouping_pos)
        err_mssg2.Asses_Type()

        # Check if grouping_rule is either a list or set
        err_mssg3 = ListSetErr(grouping_rule)
        err_mssg3.Asses_Type()

        # open the file and remove header
        infile = self.OpenRead()
        self.RemoveHeader(infile, self.header_lines)

        grouped_dict = {}
        for line in infile:
            tabline_obj = TabularLine(line, self.delimiter, check_type)
            list_extracted = tabline_obj.ExtractNFields([id_pos, grouping_pos])

            # The following if takes care of checking if a key (list_extracted[1]) is present in the list/set
            # and adds it to the dict, either creating a new key:entry or adding to an existing one
            if list_extracted[1] in grouping_rule and list_extracted[1] in grouped_dict:
                grouped_dict[list_extracted[1]] += ( ',' + list_extracted[0] )
            elif list_extracted[1] in grouping_rule and list_extracted[1] not in grouped_dict:
                grouped_dict[list_extracted[1]] = list_extracted[0]
        return grouped_dict


    def TwoFieldRatio(self, pos1, pos2, log_it=False, number_of_decimals=7, check_type=False):
        """
        BE CAREFULL THIS FUNCTION MIGHT USE A LOT OF RAM, AS MUSH AS THE SIZE OF THE INPUT FILE.

        This function takes as input a tabular file with two or more fields/column per line.
        It writes to the same file the ratio (division) of the two fields on the same line, example:
        line1 -> 21, 7, 5       pos1 = 0, pos2 = 1
        line1 after function -> 21, 7, 5, 3.0
        log_it flag applies the log10 to the ratio before the writing.
        number_of_decimals decides how many digits does have to have at most the string before writing.
        100.45 is considered to have 6 (the points count) digits.
        Header lines are automately removed, to not devide words 
        """

        # First check if the file exist and positional val are integer
        self.CheckExists()
        err_mssg1 = IntTypeErr(pos1)
        err_mssg1.Asses_Type()
        err_mssg2 = IntTypeErr(pos2)
        err_mssg2.Asses_Type()

        # Open the file for read and return header for later use
        infile = self.OpenRead()
        header_lnes = self.ReturnHeader(infile, self.header_lines, return_type='str')
        
        # Only way to update same file 
        to_be_written = ''

        # esxtract the values and do the division
        for line in infile:
            tabline_obj = TabularLine(line, self.delimiter, check_type)
            list_extracted = tabline_obj.ExtractNFields([pos1, pos2])
            ratio = float(list_extracted[0].strip()) / float(list_extracted[1].strip())
            if log_it:
                ratio = log(ratio)

            # add to the corpus that is going to be written all at once, this is why is memory heavy
            to_be_written += (line.rstrip() + self.delimiter + str(ratio)[:number_of_decimals] + '\n' )

        # close and re-open file fopr writing    
        infile.close()
        infile = self.OpenEdit()

        # to avoid writing over the input fiole when nothing has to be written
        if to_be_written:
            infile.write(header_lnes)
            infile.write(to_be_written)



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
