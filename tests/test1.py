class Guy:
    def __init__(self, name, job):
        self._name = name
        self._job = job

    def fck_off(self, other):
        other._name += self._name

    @property
    def name(self):
        return self._name


bob = Guy("Bob", "blow")
boba = Guy("Boba", "job")

bob.fck_off(boba)

print(boba.name)
