
class UnpackableMixin(object):
    """
    This mixin class provides a classmethod from_data to unpack raw data
    into a python object.

    There is some requirements:
     - child class MUST define a format string for unpack in the class
       attribute "unpack_format" (see the struct module documentation)
     - child class __init__ method MUST take his parameters in the same
       order and in the same number that when returned from unpack

    """
    @classmethod
    def get_unpack_format(cls):
        """
        This method returns the format string to be passed to unpack
        method

        Child classes MUST define cls.unpack_format or override this
        method

        """
        return cls.unpack_format

    @classmethod
    def from_data(cls, data, *extra):
        """
        This method return a tuple containing:
         - an instance of child from the raw network data
         - a string containing the remaining data

        *extra is the extra args to pass to cls.__init__ and will be
        added at the end of args returned by unpack

        """
        from struct import Struct

        st = Struct(cls.get_unpack_format())
        raw = data[0:st.size]
        data = data[st.size:len(data)]
        args = st.unpack(raw)
        args += extra
        instance = cls(*args)
        return (instance, data)

    @classmethod
    def get_cstruct_size(cls):
        """
        Returns the size of the data that will be extracted when
        unpacking.

        """
        from struct import calcsize

        return calcsize(cls.get_unpack_format())
