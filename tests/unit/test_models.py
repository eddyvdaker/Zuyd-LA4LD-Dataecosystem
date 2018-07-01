# -*- coding: utf-8 -*-
"""
    tests.unit.test_models
    ~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the SQLAlchemy models
"""
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from tests.unit.base import UnitTest

from app import db
from app.models import User, Role, Module, Result, Grade, Schedule, \
    ScheduleItem, Questionnaire, QuestionnaireScale, Question, QuestionResult, \
    Attendance, ApiKey, Group


class UserModelTest(UnitTest):

    def create_test_user(self):
        """Creates a user for testing purposes"""
        # noinspection PyArgumentList
        user = User(username='abc', email='abc@abc.com', card_number="123")
        db.session.add(user)
        db.session.commit()
        return user

    def create_test_role(self):
        """Creates a role for testing purposes"""
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()

    def create_test_module(self):
        """Creates a module for testing purposes"""
        module = Module(code='tm01')
        db.session.add(module)
        db.session.commit()
        return module

    def test_create_user(self):
        """Tests the creation of a new user"""
        self.create_test_user()

    def test_try_to_add_duplicate_user(self):
        """Tests if adding a duplicate user raises an error"""
        self.create_test_user()
        with self.assertRaises(IntegrityError):
            user = self.create_test_user()
            db.session.add(user)
            db.session.commit()

    def test_add_role_to_user(self):
        """Tests if a role can be assigned to a user"""
        user = self.create_test_user()
        self.create_test_role()
        user.role_id = 1
        db.session.commit()

    def test_password(self):
        """Tests the setting and retrieving of passwords"""
        user = self.create_test_user()
        user.set_password('cat')
        db.session.commit()
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

    def test_reset_token(self):
        """Tests the generation and validation of reset tokens"""
        user = self.create_test_user()
        token = user.get_reset_password_token()
        wrong_token = user.verify_reset_password_token('abc')
        if wrong_token:
            raise Exception('wrong token still verified')
        right_token = user.verify_reset_password_token(token)
        if not right_token:
            raise Exception('right token not verified')

    def test_add_to_module_as_student(self):
        """Tests if students can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module)
        assert user.student_of_module(module)
        assert module in user.get_modules_of_student()

    def test_add_to_module_as_teacher(self):
        """Tests if teachers can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module, module_role='teacher')
        assert user.teacher_of_module(module)
        assert module in user.get_modules_of_teacher()

    def test_add_to_module_as_examiner(self):
        """Tests if examiners can be added to modules"""
        user = self.create_test_user()
        module = self.create_test_module()
        user.add_to_module(module, module_role='examiner')
        assert user.examiner_of_module(module)
        assert module in user.get_modules_of_examiner()

    def test_add_to_group(self):
        """Tests if users can be added to groups"""
        user = self.create_test_user()
        group = Group(code='1234', active=True)
        db.session.add(group)
        db.session.commit()
        user.add_to_group(group)
        assert group in user.groups_of_student()
        assert user in group.students.all()


class RoleModelTest(UnitTest):

    def test_create_role(self):
        """Tests the creation of new roles"""
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()

    def test_try_to_add_duplicate_role(self):
        """Tests if a duplicate role raises an error"""
        role = Role(role='test_role')
        db.session.add(role)
        db.session.commit()
        with self.assertRaises(IntegrityError):
            role = Role(role='test_role')
            db.session.add(role)
            db.session.commit()


class ModuleModelTest(UnitTest):

    def test_create_module(self):
        """Test if new modules can be created"""
        module = Module(
            code='tm01',
            name='testmodule01',
            description='This is a test module',
            start=datetime(2009, 10, 1),
            end=datetime(2010, 10, 1),
            faculty='Faculteit ICT',
        )
        db.session.add(module)
        db.session.commit()


class ResultModulTest(UnitTest):

    def test_create_result(self):
        """Tests if new results can be created"""
        r = Result(identifier='alksdjfklt1034', module=1)
        db.session.add(r)
        db.session.commit()

        g = Grade(name='pi1', score=6, weight=1, result=r.id)
        db.session.add(g)
        db.session.commit()


class ScheduleModelTest(UnitTest):

    def test_create_schedule(self):
        """Tests if new schedules can be created"""
        s = Schedule(description='test desc.', module=1)
        db.session.add(s)
        db.session.commit()

        i = ScheduleItem(
            title='test title',
            description='test desc.',
            start=datetime(2009, 10, 1),
            end=datetime(2010, 10, 1),
            room='room1',
            schedule=s.id
        )
        db.session.add(i)
        db.session.commit()


class QuestionnaireModelTest(UnitTest):

    def test_create_questionnaire(self):
        q = Questionnaire(
            questionnaire_id=1,
            name="test q",
            description="test desc",
            questionnaire_type="test type",
        )
        db.session.add(q)
        db.session.commit()

        qs = QuestionnaireScale(
            scale=1,
            name="test scale",
            description="test scale desc",
        )
        db.session.add(qs)
        db.session.commit()

        q.questionnaire_scale.append(qs)
        db.session.commit()

        qst = Question(
            question_number=1,
            question="test question",
            reversed=True,
        )
        db.session.add(qst)
        db.session.commit()

        qs.scale_questions.append(qst)
        db.session.commit()

        qr = QuestionResult(
            identifier="j03g039rgj3h",
            question=qst.id,
            result=3.0,
            date=datetime.utcnow()
        )
        db.session.add(qr)
        db.session.commit()


class AttendanceModelTest(UnitTest):

    def test_create_attendance(self):
        a = Attendance(
            identifier="asdgjt84",
            schedule_item_id=1
        )
        db.session.add(a)
        db.session.commit()


class ApiKeyModelTest(UnitTest):

    def test_create_apikey(self):
        a = ApiKey(
            key="abcdefg",
            description="test desc"
        )
        db.session.add(a)
        db.session.commit()


class GroupModelTest(UnitTest):

    def test_create_group(self):
        grp = Group(
            code="tm1",
            active=True
        )
        db.session.add(grp)
        db.session.commit()
