#!/usr/bin/env python3

from sys import exit
from sys import stderr
from abc import ABC, abstractmethod
import io


class TypeErrorMessage(ABC):
    """
    This is a helper class for error type messages that will be used by other classes for sending error type messages 
    all subclass of this one should be variable type specific and they should be composed instead of inherited
    """

    @abstractmethod
    def Asses_Type(self):
        pass


class StrTypeErr(TypeErrorMessage):

    def __init__(self, variable) -> None:
        self.variable = variable

    def Asses_Type(self):
        if not isinstance(self.variable, str):
            print(self.variable_name, ' variable is not the correct dataset type: string   given :', self.variable, '  type:', type(self.variable), file=stderr)
            raise TypeError("Variable is not string.")


class IntTypeErr(TypeErrorMessage):

    def __init__(self, variable) -> None:
        self.variable = variable

    def Asses_Type(self):
        if not isinstance(self.variable, int):
            print(self.variable_name, ' variable is not the correct dataset type: integer   given :', self.variable, '  type:', type(self.variable), file=stderr)
            raise TypeError("Variable is not int.")
        

class FileTypeErr(TypeErrorMessage):

    def __init__(self, variable) -> None:
        self.variable = variable

    def Asses_Type(self):
        if not isinstance(self.variable, io.TextIOBase):
            print("Invalid file object. Please pass an opened file object. value given :", self.variable, '  type:', type(self.variable), "\n", file=stderr)
            raise TypeError("Invalid file object.")


### IMplement if needed file byte file or compressed because is a different data type than the above