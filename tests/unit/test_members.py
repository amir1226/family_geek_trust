from unittest import TestCase
from src.member import Member


class TestMember(TestCase):

    def setUp(self) -> None:
        self.member = Member(1, "Pepe", "Male")

    def test_initialization(self):
        # Check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # Check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Pepe")
        self.assertEqual(self.member.gender.value, "Male")
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # Edge case for gender
        self.assertRaises(ValueError, Member, 2, "OtherPepe", "Nogender")

        #
