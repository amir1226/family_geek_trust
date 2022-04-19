from unittest import TestCase
from src.family_tree import FamilyTree
from unittest.mock import patch, Mock
from src.member import Gender
from tests.unit.test_members import create_fake_member
from src import constants

class TestFamilyTree(TestCase):
    def setUp(self):
        self.ftree = FamilyTree()

    def test_initialization(self):
        self.assertEqual(self.ftree.family_tree, {})

    @patch('src.family_tree.Member', return_value=create_fake_member(
        id=1, name="Pepe", gender=Gender.male))
    def test_add_child(self, mock_member):
        # if tree is empty
        result = self.ftree.add_child("Pepe", "Male", "Mother")
        mock_member.assert_called_with(1, "Pepe", "Male")

        self.assertEqual(
            isinstance(self.ftree.family_tree.get("Pepe", None), Mock),
            True
        )
        self.assertEqual(result, constants.CHILD_ADDITION_SUCCEEDED)

        # if either mother/ father do not exist
        mother = create_fake_member(id=2, name="Mother", gender=Gender.female)
        fakemother = create_fake_member(
            id=4, name="Fakemother", gender=Gender.male)
        father = create_fake_member(id=3, name="Father", gender=Gender.male)

        # Mother doesn't exist in the tree
        self.assertEqual(
            self.ftree.add_child("Pepe2", "Male", "Mother"),
            constants.PERSON_NOT_FOUND
        )

        # Mother is a male
        self.ftree.family_tree['Fakemother'] = fakemother
        self.assertEqual(
            self.ftree.add_child("Pepe2", "Male", "Fakemother"),
            constants.CHILD_ADDITION_FAILED
        )

        # Mother doesn't have a spouse
        self.ftree.family_tree['Mother'] = mother
        self.assertEqual(
            self.ftree.add_child("Pepe2", "Male", "Mother"),
            constants.CHILD_ADDITION_FAILED
        )

        # Mother and father in the tree - Succed
        self.ftree.family_tree['Father'] = father
        self.ftree.family_tree['Mother'].spouse = father
        self.ftree.family_tree['Father'].spouse = mother

        self.assertEqual(
            self.ftree.add_child("Pepe2", "Male", "Mother"),
            constants.CHILD_ADDITION_SUCCEEDED
        )

        # Name can´t be duplicated in family tree
        self.assertEqual(
            self.ftree.add_child("Pepe2", "Male", "Mother"),
            constants.CHILD_ADDITION_FAILED
        )
        self.assertTrue(
            isinstance(
                self.ftree.family_tree.get("Pepe2", None),
                Mock
            )
        )
