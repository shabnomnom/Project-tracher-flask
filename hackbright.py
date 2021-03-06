"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_all_students():
	"""Return a list of all the students"""

	QUERY= """
		SELECT first_name, last_name, github
		FROM students
	"""

	db_cursor = db.session.execute(QUERY)

	students = db_cursor.fetchall() #list of tuples ( first_name, last_name, github )

	return students


def get_all_projects():
	"""Return a list of all the projects"""

	QUERY= """
		SELECT title, description, max_grade
		FROM projects
	"""

	db_cursor = db.session.execute(QUERY) #SQL response object, 

	projects = db_cursor.fetchall() #list of tuples ( title, description, max_grade )

	return projects


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone() #tuple

    print(f"Student: {row[0]} {row[1]}\nGitHub account: {row[2]}")

    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO students (first_name, last_name, github)
          VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})
    db.session.commit()

    print(f"Successfully added student: {first_name} {last_name}")


def make_new_project(title,description,max_grade):
	"""Add a new project with title, description and max_grade"""
	
	QUERY ="""
	INSERT INTO projects (title, description, max_grade)
	VALUES (:title, :description, :max_grade)
	"""

	db.session.execute(QUERY, {'title':title, 'description': description, 'max_grade': max_grade})
	db.session.commit()

	print(f"Project {title} was added with {max_grade} max grade.")


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print(f"Title: {row[0]}\nDescription: {row[1]}\nMax Grade: {row[2]}")

    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
        SELECT grade
        FROM grades
        WHERE student_github = :github
          AND project_title = :title
        """

    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})

    row = db_cursor.fetchone()

    print(f"Student {github} in project {title} received grade of {row[0]}")

    return row


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    # QUERY = """
    #     INSERT INTO grades (student_github, project_title, grade)
    #       VALUES (:github, :title, :grade)
    #     """

    # db_cursor = db.session.execute(QUERY, {'github': github,
    #                                        'title': title,
    #                                        'grade': grade})


    # db.session.commit()

    TEST_QUERY = """
    	SELECT student_github
    	FROM grades
    	WHERE student_github = 'songcelia' AND project_title = 'Markov'
    """
    db_cursor = db.session.execute(TEST_QUERY)
    rows = db_cursor.fetchone()

    print(rows)
    # print(f"Successfully assigned grade of {grade} for {github} in {title}")


def get_grades_by_github(github):
    """Get a list of all grades for a student by their github username"""

    QUERY = """
        SELECT project_title, grade
        FROM grades
        WHERE student_github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    rows = db_cursor.fetchall()

    for row in rows:
        print(f"Student {github} received grade of {row[1]} for {row[0]}")

    return rows


def get_grades_by_title(title):
    """Get a list of all student grades for a project by its title"""

    QUERY = """
        SELECT student_github, grade
        FROM grades
        WHERE project_title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    rows = db_cursor.fetchall()

    for row in rows:
        print(f"Student {row[0]} received grade of {row[1]} for {title}")

    return rows


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "student_grades":
            github = args[0]
            get_grades_by_github(github)

        elif command == "project_grades":
            title = args[0]
            get_grades_by_title(title)


if __name__ == "__main__":
    connect_to_db(app)

    # handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db.session.close()
