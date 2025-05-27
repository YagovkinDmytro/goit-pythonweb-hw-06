import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    declarative_base,
    mapped_column,
    Mapped,
)


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, max_overflow=5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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
    teachers: Mapped[list["Teacher"]] = relationship("Teacher", back_populates="groups")

    def __repr__(self) -> str:
        return f"<Group(id={self.id}, name='{self.name}')>"

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="teacher")
    groups: Mapped[list["Group"]] = relationship("Group", back_populates="teachers")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, name='{self.name}')>"

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")

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
    
    

# Створення таблиць у базі даних
Base.metadata.create_all(engine)