from random import choice


class Goblin:
    __name = ""
    hp = 10
    attack = 2
    speed = 3
    range = 1

    def __init__(self, name, hp=10, attack=2):
        self.__name = name
        self.hp = hp
        self.attack = attack

    @property
    def name(self):
        return self.__name

    def say(self, string="пошол нах!"):
        print(f"{self.name} говорит {string}")

    def get_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"Goblin {self.name} сдох:(")
            self.hp = 10
            self.__name = "NEW"

    def make_attack(self):
        print(f"Goblin {self.name} attacks")

    def __add__(self, other):
        new_gob = Goblin(self.name + other.name, (self.hp + other.hp) // 2, self.attack + other.attack)
        print(f"{self.name} трахнул {other.name}")
        return new_gob

    def __str__(self):
        return f"Goblin {self.name} (hp: {self.hp}; attack: {self.attack})"


class DemonGoblin(Goblin):
    attacks = []
    color = 'red'

    def make_spec_attack(self):
        attack = choice(self.attacks)
        print(f"Демонический гоблин {self.name} нанес спецудар: {attack}")


class HeavenGoblin(Goblin):
    buffs = []
    wings_size = 10

    def __init__(self, buffs, name, hp=100, attack=1):
        super().__init__(name, hp, attack)
        self.buffs = buffs

    def give_buff(self, goblin):
        buff = choice(self.buffs)
        print(f"Райский гоблин {self.name} набафал {goblin.name} так : {buff}")

    def __str__(self):
        return f"Heaven Goblin {self.name} (hp: {self.hp}; attack: {self.attack} wings: {self.wings_size})"


goblin = Goblin('Duppi')

goblin2 = DemonGoblin("Bertold", 100, 10)
goblin2.attacks.append("плевок")

goblin3 = HeavenGoblin(["облизывание", "вфыапр"], "Arphist", 150, 1)
goblin3.give_buff(goblin)

goblin.get_damage(20)

print(goblin)
