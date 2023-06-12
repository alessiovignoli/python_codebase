#!/usr/bin/env python3

from sys import exit
from sys import stderr
from abc import ABC, abstractmethod


class TypeErrorMessage(ABC):
    """
    This is a helper class for error type messages that will be used by other classes for sending error type messages 
    all subclass of this one should be variable type specific and they should be composed instead of inherited
    """

    @abstractmethod
    def Asses_Type(self):
        pass


class StrTypeErr(TypeErrorMessage):

    def __init__(self, variable, variable_name) -> None:
        self.variable = variable
        self.variable_name = variable_name

    def Asses_Type(self):
        if not isinstance(self.variable, str):
            print(self.variable_name, ' variable is not the correct dataset type: string   given :', self.variable, '  type:', type(self.variable), file=stderr)
            exit(1)


class IntTypeErr(TypeErrorMessage):

    def __init__(self, variable, variable_name) -> None:
        self.variable = variable
        self.variable_name = variable_name

    def Asses_Type(self):
        if not isinstance(self.variable, int):
            print(self.variable_name, ' variable is not the correct dataset type: integer   given :', self.variable, '  type:', type(self.variable), file=stderr)
            exit(1)
