import os
import json
import csv
from datetime import datetime



# Keep the data files in the same folder as this Python file.
PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(PROJECT_FOLDER, "students.json")
CSV_FILE = os.path.join(PROJECT_FOLDER, "students.csv")
LOG_FILE = os.path.join(PROJECT_FOLDER, "activity_log.txt")

SUBJECTS = ["Python", "Maths", "DBMS"]


# ------------------------------------------------------------
# 1. LOAD OLD STUDENT RECORDS FROM students.json
# ------------------------------------------------------------
def load_students():
    # First check whether the JSON file exists.
    if not os.path.exists(JSON_FILE):
        print("No old records found. Starting with an empty record book.")
        return {}

    try:
        # 'r' means read mode. json.load() reads JSON and makes a Python object.
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            students = json.load(file)

        # In this project, all students are stored in a dictionary.
        if not isinstance(students, dict):
            print("ERROR: students.json must contain a dictionary.")
            print("The old file has been kept unchanged. Program will stop.")
            return None

        print("Loaded", len(students), "student record(s).")
        return students

    except json.JSONDecodeError:
        # Do not continue with empty data. That could overwrite a damaged file.
        print("ERROR: students.json contains invalid JSON.")
        print("The existing file has NOT been changed. Program will stop.")
        return None

    except OSError as error:
        print("Could not read students.json:", error)
        print("Program will stop so that saved data is protected.")
        return None


# ------------------------------------------------------------
# 2. SAVE ALL STUDENT RECORDS TO students.json
# ------------------------------------------------------------
def save_students(students):
    try:
        # 'w' means write mode. It replaces the old file contents with new data.
        # We use it only after successfully loading the old records.
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)

        print("Student records saved successfully.")
        return True

    except OSError as error:
        print("Could not save student records:", error)
        return False


# ------------------------------------------------------------
# 3. CREATE THE ACTIVITY LOG AND ADD NEW LOG MESSAGES
# ------------------------------------------------------------
def create_log_file():
    # Create the log file only when it does not already exist.
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            # writelines() writes more than one string to a text file.
            file.writelines([
                "STUDENT RECORDS ACTIVITY LOG\n",
                "-----------------------------\n"
            ])


def add_log_message(message):
    # datetime.now() gets the current date and time.
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = time_now + " - " + message + "\n"

    try:
        # 'a' means append mode. It adds the new line and keeps old lines.
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            # write() writes one string to the file.
            file.write(log_line)
    except OSError as error:
        print("Could not update activity_log.txt:", error)


# ------------------------------------------------------------
# 4. TAKE STUDENT DETAILS AND CHECK THE MARKS
# ------------------------------------------------------------
def get_mark(subject_name):
    # Keep asking until the user enters a number between 0 and 100.
    while True:
        entered_value = input(subject_name + " marks (0-100): ").strip()

        try:
            mark = float(entered_value)
        except ValueError:
            print("Please enter a number, for example 78 or 85.5.")
            continue

        if mark < 0 or mark > 100:
            print("Marks must be between 0 and 100.")
            continue

        # If the mark is a whole number, store it as an integer (e.g. 78).
        if mark.is_integer():
            return int(mark)
        return mark


def get_student_details():
    # Get the student's name.
    name = input("Name: ").strip()
    while name == "":
        print("Name cannot be empty.")
        name = input("Name: ").strip()

    # Get the student's department.
    department = input("Department: ").strip()
    while department == "":
        print("Department cannot be empty.")
        department = input("Department: ").strip()

    # Store the three subject marks in a dictionary.
    marks = {}
    for subject in SUBJECTS:
        marks[subject] = get_mark(subject)

    # Return one student's details as a dictionary.
    return {
        "name": name,
        "department": department,
        "marks": marks
    }


# ------------------------------------------------------------
# 5. ADD A NEW STUDENT
# ------------------------------------------------------------
def add_student(students):
    print("\n--- ADD STUDENT ---")
    student_id = input("Student ID: ").strip()

    if student_id == "":
        print("Student ID cannot be empty.")
        return

    # Do not allow the same ID to be used twice.
    if student_id in students:
        print("This Student ID already exists. Use a different ID.")
        return

    student = get_student_details()

    # Store the student's details using the ID as the dictionary key.
    students[student_id] = student

    # Save the complete collection. If saving fails, undo this new record.
    if save_students(students):
        add_log_message("Student " + student_id + " added")
    else:
        del students[student_id]
        print("The new record was not kept because saving failed.")


# ------------------------------------------------------------
# 6. UPDATE AN EXISTING STUDENT
# ------------------------------------------------------------
def update_student(students):
    print("\n--- UPDATE STUDENT ---")
    student_id = input("Enter Student ID to update: ").strip()

    if student_id not in students:
        print("Student record not found.")
        return

    print("Enter the new details below:")
    updated_student = get_student_details()

    # Keep a copy of the old details in case saving the update fails.
    old_student = students[student_id]
    students[student_id] = updated_student

    if save_students(students):
        add_log_message("Student " + student_id + " updated")
    else:
        students[student_id] = old_student
        print("The old record has been restored because saving failed.")


# ------------------------------------------------------------
# 7. DISPLAY ONE STUDENT AND SEARCH BY ID
# ------------------------------------------------------------
def display_student(student_id, student):
    print("\nStudent ID :", student_id)
    print("Name       :", student["name"])
    print("Department :", student["department"])

    # Display each subject and its marks.
    for subject in SUBJECTS:
        print(subject + " marks :", student["marks"][subject])


def search_student(students):
    print("\n--- SEARCH STUDENT ---")
    student_id = input("Enter Student ID: ").strip()

    if student_id in students:
        display_student(student_id, students[student_id])
    else:
        print("Student record not found.")

# ------------------------------------------------------------
# 8. DISPLAY ALL STUDENT RECORDS
# ------------------------------------------------------------
def view_all_students(students):
    print("\n--- ALL STUDENT RECORDS ---")

    if len(students) == 0:
        print("No student records are available.")
        return

    for student_id, student in students.items():
        display_student(student_id, student)
        print("-" * 30)


# ------------------------------------------------------------
# 9. EXPORT ALL RECORDS TO students.csv
# ------------------------------------------------------------
def export_to_csv(students):
    try:
        # newline='' is recommended when writing CSV files.
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # First write the column headings.
            writer.writerow([
                "Student ID", "Name", "Department",
                "Python", "Maths", "DBMS"
            ])

            # Then write one row for every student.
            for student_id, student in students.items():
                writer.writerow([
                    student_id,
                    student["name"],
                    student["department"],
                    student["marks"]["Python"],
                    student["marks"]["Maths"],
                    student["marks"]["DBMS"]
                ])

        print("CSV export completed. Check students.csv.")
        add_log_message("Student records exported to students.csv")

    except OSError as error:
        print("Could not create students.csv:", error)


# ------------------------------------------------------------
# 10. READ THE ACTIVITY LOG USING read(), readline(), readlines()
# ------------------------------------------------------------
def show_log_with_read():
    print("\n--- USING read(): COMPLETE FILE ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            log_text = file.read()

        print(log_text, end="")
    except FileNotFoundError:
        print("The activity log does not exist yet.")


def show_log_with_readline():
    print("\n--- USING readline(): ONE LINE AT A TIME ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            line = file.readline()

            while line != "":
                print(line, end="")
                line = file.readline()
    except FileNotFoundError:
        print("The activity log does not exist yet.")


def show_log_with_readlines():
    print("\n--- USING readlines(): ALL LINES AS A LIST ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            all_lines = file.readlines()

        for line in all_lines:
            print(line, end="")
    except FileNotFoundError:
        print("The activity log does not exist yet.")


def view_log_menu():
    print("\n1. Read complete file (read)")
    print("2. Read one line at a time (readline)")
    print("3. Read all lines into a list (readlines)")

    choice = input("Choose a method: ").strip()

    if choice == "1":
        show_log_with_read()
    elif choice == "2":
        show_log_with_readline()
    elif choice == "3":
        show_log_with_readlines()
    else:
        print("Invalid choice.")


# ------------------------------------------------------------
# 11. DEMONSTRATE json.dumps() AND json.loads()
# ------------------------------------------------------------
def demonstrate_json_strings(students):
    print("\n--- JSON STRING DEMONSTRATION ---")
    student_id = input("Enter Student ID: ").strip()

    if student_id not in students:
        print("Student record not found.")
        return

    # dumps() converts a Python dictionary into a JSON string.
    student = students[student_id]
    json_text = json.dumps(student, indent=4)

    print("\nPython dictionary converted into a JSON string:")
    print(json_text)

    # loads() converts the JSON string back into a Python dictionary.
    student_again = json.loads(json_text)
    print("\nAfter json.loads(), the student's name is:", student_again["name"])


# ------------------------------------------------------------
# 12. MAIN MENU - STARTS AND CONTROLS THE PROGRAM
# ------------------------------------------------------------
def main():
    # Make sure the activity log is ready before using it.
    create_log_file()

    # Load the records saved during the previous run.
    students = load_students()

    # None means there was a loading problem. Stop to protect old data.
    if students is None:
        print("Program stopped. Fix students.json before running again.")
        return

    # Keep showing the menu until the user chooses Exit.
    while True:
        print("\n========== STUDENT RECORDS SYSTEM ==========")
        print("1. Add student")
        print("2. Update student")
        print("3. Search student")
        print("4. View all students")
        print("5. Export records to CSV")
        print("6. View activity log")
        print("7. Demonstrate JSON string methods")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            view_all_students(students)
        elif choice == "5":
            export_to_csv(students)
        elif choice == "6":
            view_log_menu()
        elif choice == "7":
            demonstrate_json_strings(students)
        elif choice == "0":
            print("Thank you for using the Student Records System.")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


# This line runs main() only when this file is executed directly.The main guard controls when the main function should execute.
if __name__ == "__main__":
    main()
