class EmptyRoomException(Exception):
    def __init__(self, error_msg="Empty room"):
        super().__init__(error_msg)


class SingletoneException(Exception):
    def __init__(self, error_msg="Singletone Exception"):
        super().__init__(error_msg)

