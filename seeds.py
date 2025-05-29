from connect import Session
from models import Student, Teacher, Group, Grade, Subject
from faker import Faker
import random

fake = Faker()
subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Literature"]

if __name__ == "__main__":
    # with Session() as session:
    #     for name in range(1, 6):
    #         new_group = Group(name=f"Group {name}")
    #         session.add(new_group)
    #     session.commit()

    # with Session() as session:
    #     for group_id in range(1, 6):
    #         for _ in range(10):
    #             new_student = Student(name=fake.name(), group_id=group_id)
    #             session.add(new_student)
    #     session.commit()

    # with Session() as session:
    #     for _ in range(5):
    #         new_teacher = Teacher(name=fake.name())
    #         session.add(new_teacher)
    #     session.commit()
       
    # with Session() as session:
    #     teachers = session.query(Teacher).all()
    #     for i, subject_name in enumerate(subjects):
    #         teacher = teachers[i % len(teachers)]
    #         new_subject = Subject(name=subject_name, teacher_id=teacher.id)
    #         session.add(new_subject)
    #     session.commit()

    # with Session() as session:
    #     subjects = session.query(Subject).all()
    #     students = session.query(Student).all()
    #     for subject  in subjects:
    #             for student in students:
    #                 new_grade = Grade(
    #                     value=random.randint(60, 101), 
    #                     student_id=student.id, 
    #                     subject_id=subject.id)
    #                 session.add(new_grade)
    #     session.commit()

    # # Delete
    # with Session() as session:
    #     subjects = session.query(Subject).all()
    #     for subject in subjects:
    #         session.delete(subject)
    #     session.commit()

    # # Delete
    # with Session() as session:
    #     grades = session.query(Grade).all()
    #     for grade in grades:
    #         session.delete(grade)
    #     session.commit()

    with Session() as session:
        subjects = session.query(Subject).all()
        groups = session.query(Group).all()

        for subject in subjects:
            selected = random.sample(groups, k=random.randint(1, 3))
            subject.groups = selected
        session.commit()

    