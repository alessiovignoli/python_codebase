#!/usr/bin/env python3

from abc import ABC, abstractmethod
from .type_error_messages import StrTypeErr
import gzip

class ReadCompress(ABC):
    """
    Simple class to open  different types of compressed files. Input should be a string.
    No check will be made on the existance of the file so that the class can adapt to the cases in which have to 
    be written to scratch (created).
    There is no function close because it is something not specific to compressed files. Also if a new class is instanciated two times is 
    effectively as if the file was closed and re openeed.
    This class by itself is debatable if really necessary.
    """

    def __init__(self, infile):
        self.infile = infile

        #Check if the above variable is a string
        err_message = StrTypeErr(self.infile)
        err_message.Asses_Type()

    @abstractmethod
    def Open_Read(self):
        pass

    @abstractmethod
    def Open_Write(self):
        pass

    @abstractmethod
    def Open_Append(self):
        pass



class ReadGzip(ReadCompress):
    """
    This class deals with the reading (open closing) of gzip files .gz
    """

    def __init__(self, infile):
        super().__init__(infile)

    def Open_Read(self):
        opened_file = gzip.open(self.infile, 'rb')
        return opened_file

    def Open_Write(self):
        opened_file = gzip.open(self.infile, 'wb')
        return opened_file

    def Open_Append(self):
        opened_file = gzip.open(self.infile, 'ab')
        return opened_file

    