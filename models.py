from datetime import datetime
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    mapped_column,
    Mapped,
)


Base = declarative_base()

subject_group = Table(
    "subject_group",
    Base.metadata,
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

teacher_group = Table(
    "teacher_group",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")
    
    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name='{self.name}')>"

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")
    subjects: Mapped[list["Subject"]] = relationship("Subject", secondary=subject_group, back_populates="groups")
    teachers: Mapped[list["Teacher"]] = relationship("Teacher", secondary=teacher_group, back_populates="groups")

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name='{self.name}')>"

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="teacher")
    groups: Mapped[list["Group"]] = relationship("Group",secondary=teacher_group, back_populates="teachers")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, name='{self.name}')>"

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject", cascade="all, delete-orphan")
    groups: Mapped[list["Group"]] = relationship("Group", secondary=subject_group, back_populates="subjects")

    def __repr__(self) -> str:
        return f"<Subject(id={self.id}, name='{self.name}')>"
    
class Grade (Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)
    receiving_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")

    def __repr__(self) -> str:
        return f"<Grade(id={self.id}, value='{self.value}')>"
    
    
# # Створення таблиць у базі даних
# Base.metadata.create_all(engine)