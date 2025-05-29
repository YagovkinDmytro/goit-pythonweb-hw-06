from sqlalchemy import func, desc
from connect import Session
from models import Student, Teacher, Group, Grade, Subject


# Find the 5 students with the highest grade point average across all subjects.
def select_1():
     with Session() as session:
        top_students = (
        session.query(
            Student.name,
            func.round(func.avg(Grade.value), 2).label("average_grade")
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )

        print("Top 5 students with highest average grade:")
        for student in top_students:
            print(f"{student.name}: {student.average_grade}")


# Find the student with the highest grade point average in a particular subject.
def select_2(subject_name: str):
    with Session() as session:
        result = (
        session.query(
            Student.name,
            func.round(func.avg(Grade.value), 2).label("average_grade")
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
        .first()
    )

        if result:
            print(f"Student: {result.name}, Average Grade in {subject_name}: {result.average_grade}")
        else:
            print(f"No grades found for subject: {subject_name}")


# Find the average score across groups in a particular subject.
def select_3(subject_name: str):
    with Session() as session:
        results = (
            session.query(
                Group.name.label("group_name"),
                func.round(func.avg(Grade.value), 2).label("average_grade")
            )
            .join(Student, Student.group_id == Group.id)
            .join(Grade, Grade.student_id == Student.id)
            .join(Subject, Subject.id == Grade.subject_id)
            .filter(Subject.name == subject_name)
            .group_by(Group.name)
            .order_by(("group_name"))
            .all()
        )

        for row in results:
            print(f"Group: {row.group_name}, Avg Grade: {row.average_grade}")


# Find the average score across a stream (across the entire grade table).
def select_4():
    with Session() as session:
        result = session.query(func.round(func.avg(Grade.value), 2).label("average_grade")).scalar()
        print(f"Average grade for all students: {result}")


# Find which courses a particular teacher teaches.
def select_5(teacher_name: str):
    with Session() as session:
        result = (
            session.query(Subject.name.label("subject_name"))
            .join(Teacher)
            .filter(Teacher.name == teacher_name)
            .all()
        )

        for row in result:
            print(f"Course: {row.subject_name}")


# Find a list of students in a particular group.
def select_6(group_name: str):
    with Session() as session:
        result = (
            session.query(Student.name.label("student_name"))
            .join(Group)
            .filter(Group.name == group_name)
            .all()
        )

        for row in result:
            print(f"{group_name}: {row.student_name}")


# Find the grades of students in a particular group in a particular subject.
def select_7(group_name: str, subject_name: str):
    with Session() as session:
        result = (
            session.query(
                Student.name.label("student_name"), 
                Grade.value.label("grade"))
            .join(Student, Grade.student_id == Student.id)
            .join(Group, Student.group_id == Group.id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Group.name == group_name)
            .filter(Subject.name == subject_name)
            .all()
        )

        for row in result:
            print(f"Student: {row.student_name}, Grade: {row.grade}")


# Find the average score that a particular teacher gives in his/her subjects.
def select_8(teacher_name: str):
    with Session() as session:
        result = (
            session.query(
                func.round(func.avg(Grade.value), 2).label("average_grade")
            )
            .join(Subject, Grade.subject_id == Subject.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Teacher.name == teacher_name)
            .one_or_none()
        )

        if result:
            print(f"Average grade set by {teacher_name}: {result.average_grade}")
        else:
            print(f"No grades found for teacher: {teacher_name}")


# Find a list of courses that a particular student takes.
def select_9(student_name: str):
    with Session() as session:
        result = (
            session.query(
                Subject.name.label("course_name")
            )
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .filter(Student.name == student_name)
            .distinct()
            .all()
        )

        for row in result:
            print(f"Course: {row.course_name}")


# List of courses that a particular teacher teaches to a particular student.
def select_10(student_name: str, teacher_name: str):
    with Session() as session:
        result = (
            session.query(
                Subject.name.label("course_name")
            )
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Student.name == student_name)
            .filter(Teacher.name == teacher_name)
            .distinct()
            .all()
        )

        for row in result:
            print(f"Course: {row.course_name}")
  


if __name__ == "__main__":
    select_1()
    select_2("Mathematics")
    select_3("Physics")
    select_4()
    select_5("Jason Rodriguez")
    select_6("Group 1")
    select_7("Group 1", "Biology")
    select_8("Scott Campbell")
    select_9("Ronald Mclaughlin")
    select_10("Shawn Crawford", "Calvin Mckenzie")

    