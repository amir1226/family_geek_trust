from unittest import TestCase
from src.member import Member, Gender


class TestMember(TestCase):

    def setUp(self) -> None:
        self.member = Member(1, "Pepe", "Male")

    def test_initialization(self):
        # Check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # Check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Pepe")
        self.assertEqual(self.member.gender, Gender.male)
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # Edge case for gender
        self.assertRaises(ValueError, Member, 2, "OtherPepe", "Nogender")

    def test_set_mother(self):
        mother_demo_a = "mother_demo_a"
        mother_demo_b = Member(2, "MotherMale", "Male")
        mother_demo_c = Member(3, "Mom", "Female")

        # failure cases
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_a)
        self.assertRaises(ValueError, self.member.set_mother, mother_demo_b)

        # success case
        self.member.set_mother(mother_demo_c)
        self.assertEqual(self.member.mother.name, "Mom")
        self.assertEqual(self.member.mother.gender, Gender.female)


    def test_set_father(self):
        father_demo_a = "father_demo_a"
        father_demo_b = Member(2, "FatherFemale", "Female")
        father_demo_c = Member(3, "Dad", "Male")

        # failure cases
        self.assertRaises(ValueError, self.member.set_father, father_demo_a)
        self.assertRaises(ValueError, self.member.set_father, father_demo_b)

        # success case
        self.member.set_father(father_demo_c)
        self.assertEqual(self.member.father.name, "Dad")
        self.assertEqual(self.member.father.gender, Gender.male)

    def test_set_spouse(self):
        spouse_demo_a = "spouse_demo_a"
        spouse_demo_b = Member(2, "Hector", "Male")
        spouse_demo_c = Member(3, "Wife", "Female")

        # failure cases
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_a)
        self.assertRaises(ValueError, self.member.set_spouse, spouse_demo_b)

        # success case
        self.member.set_spouse(spouse_demo_c)
        self.assertEqual(self.member.spouse.name, "Wife")
        self.assertEqual(self.member.spouse.gender, Gender.female)

    def test_add_child(self):
        child_demo_a = "child_demo_a"
        child_demo_b = Member(2, "Daughter", "Female")

        # failure cases
        self.assertRaises(ValueError, self.member.add_child, child_demo_a)

        # success case
        self.member.add_child(child_demo_b)
        self.assertEqual(self.member.children[0], child_demo_b)
        self.assertEqual(len(self.member.children), 1)
