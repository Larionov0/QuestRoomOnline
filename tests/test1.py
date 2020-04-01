class Ebanavt:
    def __init__(self, name, job):
        self._name = name
        self._job = job

    def fuck_off(self, other):
        other._name += self._name

    @property
    def name(self):
        return self._name


bob = Ebanavt("Bob", "blow")
boba = Ebanavt("Boba", "job")

bob.fuck_off(boba)

print(boba.name)
