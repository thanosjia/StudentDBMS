import psycopg2
from psycopg2 import OperationalError

# Connect to PostgreSQL database
def create_connection():
    try:
        conn = psycopg2.connect(
            database="assignment3",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

# Retrieves and prints all student records from the database
def get_all_students():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# Adds a new student record to the database
def add_student(first_name, last_name, email, enrollment_date):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
        conn.commit()
        print("Student added successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# Updates the email address of an existing student record
def update_student_email(student_id, new_email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
        conn.commit()
        print("Email updated successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# Deletes a student record from the database
def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        print("Student deleted successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

# Helper function for adding a student record
def get_student_details():
    first_name = input("Enter student's first name: ")
    last_name = input("Enter student's last name: ")
    email = input("Enter student's email: ")
    enrollment_date = input("Enter student's enrollment date (YYYY-MM-DD): ")
    return first_name, last_name, email, enrollment_date

# Prompts user for a student ID, validating it as an integer
def get_student_id():
    student_id = input("Enter the student's ID: ")
    try:
        student_id = int(student_id)
    except ValueError:
        print("Please enter a valid integer for the student ID.")
        return None
    return student_id

# Fetches and returns a student record by ID, or None if not found
def find_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    student = None
    try:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()
    return student

# Confirms with the user before deleting a student record
def confirm_delete(student_id):
    student = find_student(student_id)
    if not student:
        print("No student found with ID:", student_id)
        return False
    else:
        print("Student Details:")
        print("ID:", student[0])
        print("First Name:", student[1])
        print("Last Name:", student[2])
        print("Email:", student[3])
        print("Enrollment Date:", student[4])
        print("You are about to delete the above student record.")
        confirm = input("Are you sure? (y/n): ").lower()
        return confirm == 'y'

# Main menu options
def main_menu():
    print("\nWelcome To The Student Management System")
    print("Please choose an option (enter the number):")
    print("1. List all students")
    print("2. Add a new student")
    print("3. Update a student's email")
    print("4. Delete a student")
    print("5. Exit")

# main
if __name__ == "__main__":
    while True:
        main_menu()
        choice = input("Your choice: ")

        if choice == '1':
            get_all_students()
        elif choice == '2':
            first_name, last_name, email, enrollment_date = get_student_details()
            add_student(first_name, last_name, email, enrollment_date)
        elif choice == '3':
            student_id = get_student_id()
            if student_id is not None:
                student = find_student(student_id)
                if student:
                    new_email = input("Enter the new email for the student: ")
                    update_student_email(student_id, new_email)
                else:
                    print("No student found with ID:", student_id)
        elif choice == '4':
            student_id = get_student_id()
            if student_id is not None:
                if confirm_delete(student_id):
                    delete_student(student_id)
        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid option. Please try again.")