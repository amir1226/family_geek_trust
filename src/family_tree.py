from src.member import Member, Gender
from src import constants

class FamilyTree:
    def __init__(self):
        self.family_tree = {}

    
    def add_child(self, name, gender, mother_name=None):

        _id = len(self.family_tree.keys()) + 1
        member = Member(_id, name, gender)

        if not self.family_tree:
            self.family_tree[name] = member
            return constants.CHILD_ADDITION_SUCCEEDED

        if name in self.family_tree:
            return constants.CHILD_ADDITION_FAILED
            
        mother = self.family_tree.get(mother_name, None)
        if not mother:
            return constants.PERSON_NOT_FOUND
        if mother.gender != Gender.female:
            return constants.CHILD_ADDITION_FAILED

        father = mother.spouse
        if not father:
            return constants.CHILD_ADDITION_FAILED

        try:
            member.set_mother(mother)
            member.set_father(father)
            self.family_tree[mother_name].add_child(member)
            self.family_tree[father.name].add_child(member)
            self.family_tree[name] = member
            return constants.CHILD_ADDITION_SUCCEEDED
        except ValueError:
            return constants.CHILD_ADDITION_FAILED