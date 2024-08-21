"""Contains the Value class."""

from math import sqrt

class Value:
    """A Value represents a numerical measurement of some kind, with its
    associated uncertainty/error.

    For example a value of 23 ± 0.2 would be ``Value(23, 0.2)``.

    Values mostly support the same operators that numbers do - you can add them,
    divide them, raise them to powers, compare them etc. There are a few
    important differences however. Firstly, the error values of the resultant
    operations will be derived from the standard guidelines for combining
    uncertainties. Specifically, values will be assumed to be independent, and
    so errors will be summed etc. in quadrature.

    Secondly, comparing two values with ``==``, ``<`` etc. will compare the
    values only - the error values will not be taken into account. I thought it
    would be too confusing otherwise. However, all values have a
    :py:meth:`.consistent_with` method which `will` look at the error values.
    If two values are consistent, then one should not be considered larger than
    the other, regardless of what ``>`` says.

    The intention behind the Value class was that if you wanted to, you could
    forget that it was anything other than an ``int`` or ``float``, and only
    access the error associated with it if you need it.

    You can create a Value `from` a value, and the argument will be treated
    exactly like an ``int`` or ``float``. That is, unless you also supply an
    error value, the resultant Value will have an error of 0. I considered
    having the error of the Value passed in become the new error, but decided
    it would become too easy to lose track of the errors. So,
    ``Value(Value(23, 0.2))`` would produce a Value with an error of 0 (and a
    value of 23).

    One final note on terminology - I know it is confusing that the Value class
    has a property called :py:meth:`value`, but that is the terminology in use
    as of this version.

    :param value: The value.
    :param error: The uncertainty associated with the value. By default this is\
    zero.
    :raises TypeError: if either the value or its error is not numeric.
    :raises ValueError: if the error is negative."""

    def __init__(self, value, error=0):
        if isinstance(value, Value): value = value._value
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("value {} is not an int or a float".format(value))
        if not isinstance(error, (int, float)) or isinstance(error, bool):
            raise TypeError("error {} is not an int or a float".format(error))
        if error < 0:
            raise ValueError("error {} is negative".format(error))
        self._value = value
        self._error = error


    @staticmethod
    def create(value, error=0):
        """This is a static method, and serves as an alternate constructor for
        Values. It tries to convert some value to an actual Value, and if it
        can't because it is the wrong type, it just sends the object back
        unaltered.

        :param value: The value to convert.
        :param error: The error associated with the value.
        :returns: Either the converted :py:class:`.Value` or the original\
        object."""

        try:
            return Value(value, error)
        except TypeError:
            return value


    def __repr__(self):
        if self._error:
            return "{} ± {}".format(self._value, self._error)
        return str(self._value)


    def __add__(self, other):
        value = self._value + (other._value if isinstance(other, Value) else other)
        error = self._error ** 2
        other_error = (other._error if isinstance(other, Value) else 0) ** 2
        error = sqrt(error + other_error)
        return Value(value, error)


    def __radd__(self, other):
        return self + other


    def __sub__(self, other):
        value = self._value - (other._value if isinstance(other, Value) else other)
        error = self._error ** 2
        other_error = (other._error if isinstance(other, Value) else 0) ** 2
        error = sqrt(error + other_error)
        return Value(value, error)


    def __rsub__(self, other):
        value = (other._value if isinstance(other, Value) else other) - self._value
        error = self._error ** 2
        other_error = (other._error if isinstance(other, Value) else 0) ** 2
        error = sqrt(error + other_error)
        return Value(value, error)


    def __mul__(self, other):
        value = self._value
        other_value = (other._value if isinstance(other, Value) else other)
        value *= other_value
        error = self.relative_error() ** 2
        other_error = other.relative_error() if isinstance(other, Value) else 0
        other_error = other_error ** 2
        error = sqrt(error + other_error)
        return Value(value, error * abs(value))


    def __rmul__(self, other):
        return self * other


    def __truediv__(self, other):
        value = self._value
        other_value = (other._value if isinstance(other, Value) else other)
        value /= other_value
        error = self.relative_error() ** 2
        other_error = other.relative_error() if isinstance(other, Value) else 0
        other_error = other_error ** 2
        error = sqrt(error + other_error)
        return Value(value, error * abs(value))


    def __rtruediv__(self, other):
        value = (other._value if isinstance(other, Value) else other) / self._value
        error = self.relative_error() + (
         other.relative_error() if isinstance(other, Value) else 0
        )
        return Value(value, error * abs(value))


    def __pow__(self, other):
        value = self._value ** other
        error = self.relative_error() * abs(other)
        return Value(value, error * abs(value))


    def __eq__(self, other):
        return self._value == (other._value if isinstance(other, Value) else other)


    def __gt__(self, other):
        return self._value > (other._value if isinstance(other, Value) else other)


    def __lt__(self, other):
        return self._value < (other._value if isinstance(other, Value) else other)


    def __ge__(self, other):
        return self._value >= (other._value if isinstance(other, Value) else other)


    def __le__(self, other):
        return self._value <= (other._value if isinstance(other, Value) else other)


    def value(self):
        """Returns the value's... value. That is, the measurement itself,
        without its associated error.

        :rtype: ``int`` or ``float``"""

        return self._value


    def error(self):
        """Returns the value's associated error.

        :rtype: ``int`` or ``float``"""

        return self._error


    def relative_error(self):
        """Returns the value's associated error as a proportion of the value. If
        the value is 0, the relative error will be 0 too.

        :rtype: ``float``"""

        if not self._value: return 0
        return self._error / abs(self._value)


    def error_range(self):
        """Returns the range of possible values implied by the uncertainty.

        :rtype: ``tuple``"""

        return (self._value - self._error, self._value + self._error)


    def consistent_with(self, other):
        """Checks if the value is `consistent` with another value. Two values
        are considered consistent if the difference between them is less than or
        equal to the sum of their uncertainties/errors.

        If two values are consistent, there cannot be said to be a difference
        between them, whereas if they are not consistent, there is a meaningful
        difference between them.

        You can also provide an ``int`` or ``float``, which will be assumed to
        have an error of zero.

        :param Value other: The other value to check against.
        :raises TypeError: if the other value given is not a ``Value``, ``int``\
        or ``float``.
        :rtype: ``bool``"""

        if isinstance(other, (int, float)):
            return abs(self.value() - other) <= self.error()
        elif not isinstance(other, Value):
            raise TypeError(
             "Cannot get consistency with non-number {}".format(other)
            )
        return abs(self.value() - other.value()) <= self.error() + other.error()
