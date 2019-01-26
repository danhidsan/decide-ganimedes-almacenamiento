import datetime


class Logger:

    def __init__(self):
        """ Constructor.
        """

    @staticmethod
    def __msg__(kind, value):
        """ Print messages in console.
        """
        print('[{:%Y-%m-%d %H:%M:%S}] {} -- {}'.format(
            datetime.datetime.now(), kind, value))

    def msg_info(self, value):
        """ INFO Log.
        """
        self.__msg__('INFO', value)

    def msg_warn(self, value):
        """ WARNING Log.
        """
        self.__msg__('WARN', value)

    def msg_error(self, value):
        """ ERROR Log.
        """
        self.__msg__('ERROR', value)
