from unittest import TestCase
from src.member import Member, Gender
from unittest.mock import patch, Mock


def create_fake_member(id=None, name=None, gender=None, mother=None, father=None, 
                        spouse=None, children=None):
    member = Mock()
    member.id = id
    member.name = name
    member.gender = gender
    member.mother = mother
    member.father = father
    member.spouse = spouse
    member.children = children
    return member


def return_father():
    return Member(100, "Dad", Gender.male)

def return_mother():
    return Member(101, "Mom", Gender.female)

def return_spouse(member_gender: Gender):
    return Member(99, "Maria", Gender.female) if member_gender == Gender.female else Member(
            1, "Pepe", Gender.male)

class TestMember(TestCase):

    def setUp(self) -> None:  
        self.member = Member(1, "Pepe", Gender.male)
        self.member_female = Member(99, "Maria", Gender.female)

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

    def test_get_paternal_grandmother(self):
        member = Member(4, "Pepito", "Male")
        father = Member(5, "Dad", "Male")
        grandmother = Member(6, "Grandma", "Female")

        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None)

        member.father.mother = grandmother
        self.assertEqual(member.get_paternal_grandmother(), grandmother)

    def test_get_maternal_grandmother(self):
        member = Member(4, "Pepito", "Male")
        mother = Member(5, "Mom", "Female")
        grandmother = Member(6, "Grandma", "Female")

        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(), None)

        member.mother.mother = grandmother
        self.assertEqual(member.get_maternal_grandmother(), grandmother)

    def test_get_spouse_mother(self):
        member = Member(4, "Pepita", "Female")
        spouse = Member(5, "Pepito", "Male")
        mother_spouse = Member(6, "NewMom", "Female")

        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = mother_spouse
        self.assertEqual(member.get_spouse_mother(), mother_spouse)


    @patch('src.member.Member.get_paternal_grandmother', side_effect=[
            None,
            create_fake_member(),
            create_fake_member(children=[Member(3, "Dad", Gender.male)]),
            create_fake_member(children=[
                Member(3, "Dad", Gender.male),
                Member(4, "Uncle1", Gender.male),
                Member(5, "Uncle2", Gender.male)
            ]),
            create_fake_member(children=[
                Member(10, "Dad", Gender.male),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt", Gender.female)
            ]),
            create_fake_member(children=[
                Member(10, "Dad", Gender.male),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt1", Gender.female),
                Member(14, "Aunt2", Gender.female),

            ])
    ])
    def test_get_paternal_aunt(self, mock_get_paternal_grandmother):
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother,Mock), True)

        # check for None Grandmother
        self.assertEqual(self.member.get_paternal_aunt(), [])

        # check for a single member
        self.assertEqual(self.member.get_paternal_aunt(), [])

        # check for a single child
        self.assertEqual(self.member.get_paternal_aunt(), [])

        # check for only men children
        self.assertEqual(self.member.get_paternal_aunt(), [])

        # success cases
        # One aunt
        paternal_aunts = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunts), 1)
        self.assertEqual(paternal_aunts[0].name, "Aunt")
        self.assertEqual(paternal_aunts[0].gender, Gender.female)

        #Two aunts
        paternal_aunts_2 = self.member.get_paternal_aunt()
        self.assertEqual(len(paternal_aunts_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["Aunt1", "Aunt2"], paternal_aunts_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.female, paternal_aunts_2)))

    @patch('src.member.Member.get_paternal_grandmother', side_effect=[
            None,
            create_fake_member(),
            create_fake_member(children=[return_father()]),
            create_fake_member(children=[
                return_father(),
                Member(4, "Aunt1", Gender.female),
                Member(5, "Aunt2", Gender.female)
            ]),
            create_fake_member(children=[
                return_father(),
                Member(11, "Uncle", Gender.male),
                Member(12, "Aunt", Gender.female)
            ]),
            create_fake_member(children=[
                return_father(),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt1", Gender.female),
                Member(14, "Aunt2", Gender.female),
            ])
    ])
    def test_get_paternal_uncle(self, mock_get_paternal_grandmother):
        self.member.father = return_father()
        # check if get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother,Mock), True)

        # check for None Grandmother
        self.assertEqual(self.member.get_paternal_uncle(), [])

        # check for a single member
        self.assertEqual(self.member.get_paternal_uncle(), [])

        # check for a single child
        self.assertEqual(self.member.get_paternal_uncle(), [])

        # check for only sisters
        self.assertEqual(self.member.get_paternal_uncle(), [])

        # success cases
        # One uncle
        paternal_uncles = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncles), 1)
        self.assertEqual(paternal_uncles[0].name, "Uncle")
        self.assertEqual(paternal_uncles[0].gender, Gender.male)

        #Two uncles
        paternal_uncles_2 = self.member.get_paternal_uncle()
        self.assertEqual(len(paternal_uncles_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["Uncle1", "Uncle2"], paternal_uncles_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.male, paternal_uncles_2)))


    @patch('src.member.Member.get_maternal_grandmother', side_effect=[
            None,
            create_fake_member(),
            create_fake_member(children=[return_mother()]),
            create_fake_member(children=[
                return_mother(),
                Member(4, "Uncle1", Gender.male),
                Member(5, "Uncle2", Gender.male)
            ]),
            create_fake_member(children=[
                return_mother(),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt", Gender.female)
            ]),
            create_fake_member(children=[
                return_mother(),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt1", Gender.female),
                Member(14, "Aunt2", Gender.female),

            ])
    ])
    def test_get_maternal_aunt(self, mock_get_maternal_grandmother):
        self.member.mother = return_mother()

        # check if get_maternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_maternal_grandmother,Mock), True)

        # check for None Grandmother
        self.assertEqual(self.member.get_maternal_aunt(), [])

        # check for a single member
        self.assertEqual(self.member.get_maternal_aunt(), [])

        # check for a single child
        self.assertEqual(self.member.get_maternal_aunt(), [])

        # check for only men children
        self.assertEqual(self.member.get_maternal_aunt(), [])

        # success cases
        # One aunt
        maternal_aunts = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunts), 1)
        self.assertEqual(maternal_aunts[0].name, "Aunt")
        self.assertEqual(maternal_aunts[0].gender, Gender.female)

        #Two aunts
        maternal_aunts_2 = self.member.get_maternal_aunt()
        self.assertEqual(len(maternal_aunts_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["Aunt1", "Aunt2"], maternal_aunts_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.female, maternal_aunts_2)))

    @patch('src.member.Member.get_maternal_grandmother', side_effect=[
            None,
            create_fake_member(),
            create_fake_member(children=[return_mother()]),
            create_fake_member(children=[
                return_mother(),
                Member(4, "Aunt1", Gender.female),
                Member(5, "Aunt2", Gender.female)
            ]),
            create_fake_member(children=[
                return_mother(),
                Member(11, "Uncle", Gender.male),
                Member(12, "Aunt", Gender.female)
            ]),
            create_fake_member(children=[
                return_mother(),
                Member(11, "Uncle1", Gender.male),
                Member(12, "Uncle2", Gender.male),
                Member(13, "Aunt1", Gender.female),
                Member(14, "Aunt2", Gender.female),
            ])
    ])
    def test_get_maternal_uncle(self, mock_get_maternal_grandmother):
        self.member.maternal = return_mother()
        # check if get_maternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_maternal_grandmother,Mock), True)

        # check for None Grandmother
        self.assertEqual(self.member.get_maternal_uncle(), [])

        # check for a single member
        self.assertEqual(self.member.get_maternal_uncle(), [])

        # check for a single child
        self.assertEqual(self.member.get_maternal_uncle(), [])

        # check for only sisters
        self.assertEqual(self.member.get_maternal_uncle(), [])

        # success cases
        # One uncle
        maternal_uncles = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncles), 1)
        self.assertEqual(maternal_uncles[0].name, "Uncle")
        self.assertEqual(maternal_uncles[0].gender, Gender.male)

        #Two uncles
        maternal_uncles_2 = self.member.get_maternal_uncle()
        self.assertEqual(len(maternal_uncles_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["Uncle1", "Uncle2"], maternal_uncles_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.male, maternal_uncles_2)))

    @patch('src.member.Member.get_spouse_mother', side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[return_spouse(Gender.male)]),
        create_fake_member(children=[
                return_spouse(Gender.male),
                Member(4, "daughter1", Gender.female),
                Member(5, "daughter2", Gender.female)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.male),
            Member(11, "son", Gender.male),
            Member(12, "daughter", Gender.female)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.male),
            Member(11, "son1", Gender.male),
            Member(12, "son2", Gender.male),
            Member(13, "daughter1", Gender.female),
            Member(14, "daughter2", Gender.female),
        ]),
        create_fake_member(children=[
            return_spouse(Gender.female),
            Member(11, "son", Gender.male),
            Member(12, "daughter", Gender.female)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.female),
            Member(11, "son1", Gender.male),
            Member(12, "son2", Gender.male),
            Member(13, "daughter1", Gender.female),
            Member(14, "daughter1", Gender.female),
        ])
    ])
    def test_get_brother_in_law(self, mock_get_spouse_mother):

        self.member.spouse = return_spouse(self.member.gender)
        
        self.member_female.spouse = return_spouse(self.member_female.gender)
        
        self.assertEqual(isinstance(self.member.get_spouse_mother,Mock), True)

        self.assertEqual(self.member.get_brother_in_law(), [])

        self.assertEqual(self.member.get_brother_in_law(), [])

        self.assertEqual(self.member.get_brother_in_law(), [])

        self.assertEqual(self.member.get_brother_in_law(), [])

        # success cases
        spouse_brothers = self.member.get_brother_in_law()
        self.assertEqual(len(spouse_brothers), 1)
        self.assertEqual(spouse_brothers[0].name, "son")
        self.assertEqual(spouse_brothers[0].gender, Gender.male)

        spouse_brothers_2 = self.member.get_brother_in_law()
        self.assertEqual(len(spouse_brothers_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["son1", "son2"], spouse_brothers_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.male, spouse_brothers_2)))

        female_spouse_brothers = self.member_female.get_brother_in_law()
        self.assertEqual(len(female_spouse_brothers), 1)
        self.assertEqual(female_spouse_brothers[0].name, "son")
        self.assertEqual(female_spouse_brothers[0].gender, Gender.male)

        female_spouse_brothers_2 = self.member_female.get_brother_in_law()
        self.assertEqual(len(female_spouse_brothers_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["son1", "son2"], female_spouse_brothers_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.male, female_spouse_brothers_2)))

    @patch('src.member.Member.get_spouse_mother', side_effect=[ 
        None,
        create_fake_member(),
        create_fake_member(children=[return_spouse(Gender.male)]),
        create_fake_member(children=[
                return_spouse(Gender.male),
                Member(4, "son1", Gender.male),
                Member(5, "son2", Gender.male)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.male),
            Member(11, "son", Gender.male),
            Member(12, "daughter", Gender.female)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.male),
            Member(11, "son1", Gender.male),
            Member(12, "son2", Gender.male),
            Member(13, "daughter1", Gender.female),
            Member(14, "daughter1", Gender.female),
        ]),
        create_fake_member(children=[
            return_spouse(Gender.female),
            Member(11, "son", Gender.male),
            Member(12, "daughter", Gender.female)
        ]),
        create_fake_member(children=[
            return_spouse(Gender.female),
            Member(11, "son1", Gender.male),
            Member(12, "son2", Gender.male),
            Member(13, "daughter1", Gender.female),
            Member(14, "daughter1", Gender.female),
        ])
    ])
    def test_get_sister_in_law(self, mock_get_spouse_mother):

        self.member.spouse = return_spouse(self.member.gender)
        
        self.member_female.spouse = return_spouse(self.member_female.gender)
        
        self.assertEqual(isinstance(self.member.get_spouse_mother,Mock), True)

        self.assertEqual(self.member.get_sister_in_law(), [])

        self.assertEqual(self.member.get_sister_in_law(), [])

        self.assertEqual(self.member.get_sister_in_law(), [])

        self.assertEqual(self.member.get_sister_in_law(), [])

        # success cases
        spouse_sisters = self.member.get_sister_in_law()
        self.assertEqual(len(spouse_sisters), 1)
        self.assertEqual(spouse_sisters[0].name, "daughter")
        self.assertEqual(spouse_sisters[0].gender, Gender.female)

        spouse_sisters_2 = self.member.get_sister_in_law()
        self.assertEqual(len(spouse_sisters_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["daughter1", "daughter2"], spouse_sisters_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.female, spouse_sisters_2)))

        female_spouse_sisters = self.member_female.get_sister_in_law()
        self.assertEqual(len(spouse_sisters), 1)
        self.assertEqual(spouse_sisters[0].name, "daughter")
        self.assertEqual(spouse_sisters[0].gender, Gender.female)

        female_spouse_sisters_2 = self.member_female.get_sister_in_law()
        self.assertEqual(len(spouse_sisters_2), 2)
        self.assertTrue(all(map(lambda m: m.name in ["daughter1", "daughter2"], female_spouse_sisters_2)))
        self.assertTrue(all(map(lambda m: m.gender == Gender.female, female_spouse_sisters_2)))

    def test_get_son(self):
        member = Member(5, "Dummy", "Male")
        son = Member(7, "Son", "Male")
        daughter = Member(7, "Daughter", "Female")

        self.assertEqual(member.get_son(), [])
        member.children.append(daughter)
        self.assertEqual(member.get_son(), [])
        member.children.append(son)
        sons = member.get_son()
        self.assertEqual(len(sons), 1)
        self.assertEqual(sons[0].name, "Son")
        self.assertEqual(sons[0].gender, Gender.male)

    def test_get_daughter(self):
        member = Member(5, "Dummy", "Male")
        son = Member(7, "Son", "Male")
        daughter = Member(7, "Daughter", "Female")

        self.assertEqual(member.get_daughter(), [])
        member.children.append(son)
        self.assertEqual(member.get_daughter(), [])
        member.children.append(daughter)
        daughters = member.get_daughter()
        self.assertEqual(len(daughters), 1)
        self.assertEqual(daughters[0].name, "Daughter")
        self.assertEqual(daughters[0].gender, Gender.female)
    

    def test_get_siblings(self):
        member = Member(5, "Dummy", "Male")
        mother = return_mother()
        son = Member(7, "Son", "Male")
        daughter = Member(7, "Daughter", "Female")

        self.assertEqual(member.get_siblings(), [])
        member.mother = mother
        self.assertEqual(member.get_siblings(), [])
        mother.children.extend([member, son, daughter])
        member.mother = mother
        siblings = member.get_siblings()
        self.assertEqual(len(siblings), 2)

    @patch('src.member.Member.get_siblings')
    @patch('src.member.Member.get_daughter')
    @patch('src.member.Member.get_son')
    @patch('src.member.Member.get_sister_in_law')
    @patch('src.member.Member.get_brother_in_law')
    @patch('src.member.Member.get_maternal_uncle')
    @patch('src.member.Member.get_maternal_aunt')
    @patch('src.member.Member.get_paternal_uncle')
    @patch('src.member.Member.get_paternal_aunt')
    def test_get_relationship(self, mock_get_paternal_aunt,
                              mock_get_paternal_uncle,
                              mock_get_maternal_aunt, mock_get_maternal_uncle,
                              mock_get_brother_in_law, mock_get_sister_in_law,
                              mock_get_son, mock_get_daughter,
                              mock_get_siblings):
        self.assertEqual(self.member.get_relationship('invalid_relation'), [])

        self.member.get_relationship('paternal_aunt')
        mock_get_paternal_aunt.assert_called_with()

        self.member.get_relationship('paternal_uncle')
        mock_get_paternal_uncle.assert_called_with()

        self.member.get_relationship('maternal_aunt')
        mock_get_maternal_aunt.assert_called_with()

        self.member.get_relationship('maternal_uncle')
        mock_get_maternal_uncle.assert_called_with()

        self.member.get_relationship('brother_in_law')
        mock_get_brother_in_law.assert_called_with()

        self.member.get_relationship('sister_in_law')
        mock_get_sister_in_law.assert_called_with()

        self.member.get_relationship('son')
        mock_get_son.assert_called_with()

        self.member.get_relationship('daughter')
        mock_get_daughter.assert_called_with()

        self.member.get_relationship('siblings')
        mock_get_siblings.assert_called_with()