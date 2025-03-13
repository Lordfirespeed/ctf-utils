from enum import ReprEnum


class BytesEnum(bytes, ReprEnum):
    """
    Enum where members are also (and must be) bytes
    """

    def __new__(cls, *values):
        """values must already be of type `bytes`"""
        if len(values) > 3:
            pass
        if len(values) == 1:
            # it must be bytes
            if not isinstance(values[0], bytes):
                raise TypeError("%r is not bytes" % (values[0], ))
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError("encoding must be a string, not %r" % (values[1], ))
        if len(values) == 3:
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError('errors must be a string, not %r' % (values[2]))
        value = bytes(*values)
        member = bytes.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        Non-ASCII member names are unsupported.
        """
        return name.lower().encode("ascii")


__all__ = ("BytesEnum",)
