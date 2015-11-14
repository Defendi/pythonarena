# -*- coding: utf-8 -*-
#
# POC to manage attributes in the Glances project
# Nicolargo (11/2015)
#

from time import time

class Attribute(object):

    def __init__(self, name, description='', history_max_size=None, is_rate=False):
        """Init the attribute
        name: Attribute name (string)
        description: Attribute human reading description (string)
        history_max_size: Maximum size of the history list (default is no limit)
        is_rate: If True then the value is manage like a rate (store timestamp in the history)
        """
        self._name = name
        self._name = description
        self._value = None
        self._history_max_size = history_max_size
        self._history = []
        self.is_rate = is_rate

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    """
    Properties for the attribute name
    """
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    """
    Properties for the attribute value
    """
    @property
    def value(self):
        if self.is_rate:
            if self.history_len() > 0:
                return (self._value[1] - self.history_value()[1]) / (self._value[0] - self.history_value()[0])
            else:
                return None
        else:
            return self._value

    @value.setter
    def value(self, new_value):
        """Set a value.
        If self.is_rate is True, store a tuple with (<timestamp>, value)
        else, store directly the value (wathever type is it)
        """
        if self.is_rate:
            new_value = (time(), new_value)
        if self._value is not None:
            self.history_add(self._value)
        self._value = new_value

    """
    Properties for the attribute history
    """
    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, new_history):
        self._history = new_history

    @history.deleter
    def history(self):
        del self._history

    def history_add(self, value):
        """Add a value in the history
        """
        if self._history_max_size is None or self.history_len() < self._history_max_size:
            self._history.append(value)
        else:
            self._history = self._history[1:] + [value]

    def history_size(self):
        """Return the history size (maximum nuber of value in the history)
        """
        return len(self._history)

    def history_len(self):
        """Return the current history lenght
        """
        return len(self._history)

    def history_value(self, pos=1):
        """Return the value in position pos in the history.
        Default is to return the latest value added to the history.
        """
        return self._history[-pos:][0]
