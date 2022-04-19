from unittest import TestCase
from src.member import Member
from src import constants
from src.family_tree import FamilyTree


class TestFamilyTree(TestCase):

    def setUp(self):
        self.ftree = FamilyTree()

    def test_add_child(self):
        result = self.ftree.add_child("Father", "Male")
        self.assertEqual(result, constants.CHILD_ADDITION_SUCCEEDED)
        self.assertEqual(
            self.ftree.family_tree.get("Father", None) is not None,
            True
        )

        self.assertEqual(
            self.ftree.add_child("Pepe", "Male", "Mother"),
            constants.PERSON_NOT_FOUND
        )
        self.assertEqual(
            self.ftree.add_child("Pepe", "Male", "Father"),
            constants.CHILD_ADDITION_FAILED
        )

        mother = Member(2, "Mother", "Female")
        mother.spouse = self.ftree.family_tree["Father"]
        self.ftree.family_tree["Father"].set_spouse(mother)
        self.ftree.family_tree["Mother"] = mother

        self.assertEqual(
            self.ftree.add_child("Pepe", "Male", "Mother"),
            constants.CHILD_ADDITION_SUCCEEDED
        )
        self.assertEqual(
            self.ftree.add_child("Pepe", "Male", "Mother"),
            constants.CHILD_ADDITION_FAILED
        )
        self.assertTrue(
            self.ftree.family_tree.get("Pepe", None) is not None
        )
