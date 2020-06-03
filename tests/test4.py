
class A:
    instance = None

    def __init__(self, use_this_out_of_class=True):
        if use_this_out_of_class:
            raise Exception("Using out of Class (Singletone)")
        A.instance = self

    @staticmethod
    def get_instance():
        if A.instance is None:
            return A(use_this_out_of_class=False)
        else:
            return A.instance

    def __str__(self):
        return "LOh"


ob = A.get_instance()

ob2 = A.get_instance()

print(ob is ob2)
