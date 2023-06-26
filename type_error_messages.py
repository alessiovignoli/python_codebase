#!/usr/bin/env python3

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

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, str):
            if self.no_print:
                raise TypeError("Variable is not string.")
            else:
                print('Variable is not string,   given :', self.variable, '  type:', type(self.variable), "\n", file=stderr)
                raise TypeError("Variable is not string.")
            

class BytesTypeErr(TypeErrorMessage):

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, bytes):
            if self.no_print:
                raise TypeError("Variable is not bytes.")
            else:
                print('Variable is not bytes,   given :', self.variable, '  type:', type(self.variable), "\n", file=stderr)
                raise TypeError("Variable is not bytes.")
            

class BytesStrErr(TypeErrorMessage):

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, str) and not isinstance(self.variable, bytes):
            if self.no_print:
                raise TypeError("Variable is nor string nor bytes.")
            else:
                print('Variable is nor string nor bytes,   given :', self.variable, '  type:', type(self.variable), "\n", file=stderr)
                raise TypeError("Variable is nor string nor bytes.")


class IntTypeErr(TypeErrorMessage):

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, int):
            if self.no_print:
                raise TypeError("Variable is not int.")
            else:        
                print('Variable is not integer,    given :', self.variable, '  type:', type(self.variable),  "\n",  file=stderr)
                raise TypeError("Variable is not int.")


class ListTypeErr(TypeErrorMessage):

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, list):
            if self.no_print:
                raise TypeError("Variable is not a list.")
            else:
                print('Variable is not a list,   given :', self.variable, '  type:', type(self.variable), "\n", file=stderr)
                raise TypeError("Variable is not a list.")



class FileTypeErr(TypeErrorMessage):

    def __init__(self, variable, no_print=False) -> None:
        self.variable = variable
        self.no_print = no_print

    def Asses_Type(self):
        if not isinstance(self.variable, io.TextIOBase):
            if self.no_print:
                raise TypeError("Invalid file object.")
            else:
                print("Invalid file object. Please pass an opened file object,   given :", self.variable, '  type:', type(self.variable), "\n", file=stderr)
                raise TypeError("Invalid file object.")


### IMplement if needed file byte file or compressed because is a different data type than the above
