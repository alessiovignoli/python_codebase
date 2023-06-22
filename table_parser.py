#!/usr/bin/env python3

from file_existance import FileExists
from count_lines import LineCounter
from file_header import FileHeader
from type_error_messages import IntTypeErr
from tabular import ExtractField
from tabular import ExtractNFields


class TableParser():

    """
    Very general and broad class for parsing a tabular format file. This time the input is the whole file in itself. (as string).
    Evrey line should have one or more fields, all separated by an unique separator, 
    files that abide to this concepts are tsv and csv for example.
    It is not thought to write the input file just to read and do stuff based on reading.
    The values intialized are the opened file object, theeparator aka delimiter,
    total number of lines in file and the header presence flag + the nuber of header lines.
    """

    def __init__(self, infile, delimiter='\t', header=True, header_lines=1) -> None:
        self.infile = infile
        self.delimiter = delimiter
        
        # Set header related variables  
        self.header = header
        if header:
            self.header_lines = header_lines
        else:
            self.header_lines = 0
        
        # Check if file exists before doing anything
        exists = FileExists(infile)
        exists.Check()

    
    def TotalLines(self):

        """
        simple function for counting total number of lines in file
        """

        with open(self.infile, 'r') as intab:
            line_counter = LineCounter(intab)
            total_count = line_counter.Count_lines()
        return total_count




class PercentageIDs(TableParser):

    """
    This class has function related to a single field, all info that can be computed extracting just one column.
    """

    def __init__(self, infile, id_pos, delimiter='\t', header=True, header_lines=1) -> None:
        super().__init__(infile, delimiter, header, header_lines)
        self.id_pos = id_pos


    def CountUniqueIDs(self):
        
        """
        this function computes how many values of given field/column are unique, aka not identical, using exact string matching
        """

        seen_ids = []
        with open(self.infile, 'r') as in_file:
            header_obj = FileHeader(in_file, self.header_lines)
            header_obj.RemoveHeader()
            for line in in_file:
                extract_obj = ExtractField(line, self.id_pos, self.delimiter)
                id_value = extract_obj.Get_Field()
                if id_value not in seen_ids:
                    seen_ids.append(id_value)
        return len(seen_ids)



class TwoColumnStats(PercentageIDs):

    """
    This class is thought to contain all the functiones that have to scroll throught the file and count how many
    of a given field IDs have a certain property.
    For example The id bubba is found on one or many lines (ex. field one), field one has also many others IDs (unique or not),
    this class will answer questions like: how many IDs in field one have given value in field 3? ecc..
    The column to use as reference is identified by id_pos while the second column associated with it is query_pos.
    """

    def __init__(self, infile, id_pos, query_pos, delimiter='\t', header=True, header_lines=1) -> None:
        super().__init__(infile, id_pos, delimiter, header, header_lines)
        self.query_pos = query_pos
    
        # check if the value given for the query pos is an int
        int_obj = IntTypeErr(query_pos)
        int_obj.Asses_Type()

    def HowManyIDsFirstQueryMin(self):

        """
        This function is thought to be applied to and ordered file, in which there are multiple instances of
        same value of Column ID, so to say that there can be consecutive lines with the identical value of Column ID.
        Such lines must be consecutive for this function to work, again value bubba in Col ID can not be in line1-2-3 and 5.
        Then this functions counts how many times for a given ID the value present in query_pos/Query_Column in the first line encountered
        is the lowest of those found for that id.
        For example if id=bubba on line one has value 10 in query field/column and in all other consecutive lines such id does not have
        an lower value in Query col, that would be counted as an instance by this class, aka +1 to final count.
        """

        with open(self.infile, 'r') as in_file:
            header_obj = FileHeader(in_file, self.header_lines)
            header_obj.RemoveHeader()

            # extract first non header line info so that the if in the for loop can work right away
            ext_obj = ExtractNFields(in_file.readline(), [self.id_pos, self.query_pos], self.delimiter)
            first_list = ext_obj.Get_Fields()
            buffer_id = first_list[0]
            first_encounter_query = float(first_list[1].strip())    # The first value in query column per id
            first_query_min = True                                  # Flag to know if to add a +1 to the final counter
            final_counter = 0

            for line in in_file:
                extract_obj = ExtractNFields(line, [self.id_pos, self.query_pos], self.delimiter)
                list_extracted = extract_obj.Get_Fields()
               
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
            last_obj = ExtractNFields(in_file.readline(), [self.id_pos, self.query_pos], self.delimiter)
            last_list = ext_obj.Get_Fields()
            if last_list[0] != buffer_id and first_query_min:
                final_counter += 1
            return final_counter


    def HowManyIDsFirstQueryMax(self):

        """
        This function is thought to be applied to and ordered file, in which there are multiple instances of
        same value of Column ID, so to say that there can be consecutive lines with the identical value of Column ID.
        Such lines must be consecutive for this function to work, again value bubba in Col ID can not be in line1-2-3 and 5.
        Then this functions counts how many times for a given ID the value present in query_pos/Query_Column in the first line encountered
        is the highest of those found for that id.
        For example if id=bubba on line one has value 10 in query field/column and in all other consecutive lines such id does not have
        an higher value in Query col, that would be counted as an instance by this class, aka +1 to final count.
        """

        with open(self.infile, 'r') as in_file:
            header_obj = FileHeader(in_file, self.header_lines)
            header_obj.RemoveHeader()

            # extract first non header line info so that the if in the for loop can work right away
            ext_obj = ExtractNFields(in_file.readline(), [self.id_pos, self.query_pos], self.delimiter)
            first_list = ext_obj.Get_Fields()
            buffer_id = first_list[0]
            first_encounter_query = float(first_list[1].strip())    # The first value in query column per id
            first_query_max = True                                  # Flag to know if to add a +1 to the final counter
            final_counter = 0

            for line in in_file:
                extract_obj = ExtractNFields(line, [self.id_pos, self.query_pos], self.delimiter)
                list_extracted = extract_obj.Get_Fields()

                # The case where identical id but the query value is lower than the first line in which the id was found
                # final_counter should not be updated in this case as intended
                if list_extracted[0] == buffer_id and float(list_extracted[1].strip()) >= first_encounter_query:
                    first_query_max = False

                # The case in which a deifferent id is found and all info and flags should be updated and in case final_counter increased
                if list_extracted[0] != buffer_id:
                    buffer_id = list_extracted[0]
                    first_encounter_query = float(list_extracted[1].strip())

                    if first_query_max:
                        final_counter += 1

                    first_query_max = True

            # last iteration so that last id also has a chance to be compared
            last_obj = ExtractNFields(in_file.readline(), [self.id_pos, self.query_pos], self.delimiter)
            last_list = ext_obj.Get_Fields()
            if last_list[0] != buffer_id and first_query_max:
                final_counter += 1
            return final_counter
