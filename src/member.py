import enum


class Gender(enum.Enum):
    male = "Male"
    female = "Female"


class Member:
    def __init__(self, id, name, gender):
        self.id = id
        self.name = name
        self.gender = Gender(gender)
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_mother(self, mother):
        if not isinstance(mother, Member):
            raise ValueError('Invalid value for mother')
        if not mother.gender == Gender.female:
            raise ValueError('Mother should be female')
        self.mother = mother

    def set_father(self, father):
        if not isinstance(father, Member):
            raise ValueError('Invalid value for father')
        if not father.gender == Gender.male:
            raise ValueError('Father should be male')
        self.father = father

    def set_spouse(self, spouse):
        if not isinstance(spouse, Member):
            raise ValueError('Invalid value for spouse')
        if spouse.gender == self.gender:
            raise ValueError('Spouse should be opposite gender')
        self.spouse = spouse

    def add_child(self, child):
        if not isinstance(child, Member):
            raise ValueError('Invalid value for child')
        self.children.append(child)