import json


class StudentRecordError(Exception):
    pass


def check_student(student, ids):
    if not isinstance(student, dict):
        raise TypeError("record must be a dictionary")

    try:
        student_id = student["student_id"]
        name = student["name"]
        department = student["department"]
        marks = student["marks"]
    except KeyError as error:
        raise StudentRecordError(f"missing field '{error.args[0]}'")

    if not isinstance(marks, list):
        raise TypeError("marks must be a list")

    if len(marks) != 3:
        raise StudentRecordError("marks must have exactly 3 values")

    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise TypeError("marks must be numbers")

        if mark < 0 or mark > 100:
            raise StudentRecordError("marks must be between 0 and 100")

    if student_id in ids:
        raise StudentRecordError("duplicate student ID")

    ids.add(student_id)


def main():
    file_name = input("Enter file name (Enter = students_input.json): ")

    if file_name == "":
        file_name = "students_input.json"

    print("\n========== STUDENT IMPORT ==========")
    print("Import started:", file_name)

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("Error: file not found.")
        return

    except PermissionError:
        print("Error: permission denied.")
        return

    except json.JSONDecodeError:
        print("Error: invalid JSON file.")
        return

    except OSError as error:
        print("File error:", error)
        return

    else:
        print("File read successfully.")

    if not isinstance(data, list):
        print("Error: JSON must contain a list of students.")
        return

    valid = []
    errors = []
    ids = set()

    print("\nChecking records...")

    for number, student in enumerate(data, 1):

        try:
            check_student(student, ids)
            valid.append(student)

            print(f"✓ Accepted: {student['student_id']} - {student['name']}")

        except StudentRecordError as error:
            message = f"Rejected record {number}: {error}"
            errors.append(message)
            print("✗", message)

        except (TypeError, ValueError) as error:
            message = f"Rejected record {number}: {error}"
            errors.append(message)
            print("✗", message)

    with open("students_valid.json", "w", encoding="utf-8") as file:
        json.dump(valid, file, indent=4)

    with open("import_errors.txt", "w", encoding="utf-8") as file:
        for error in errors:
            file.write(error + "\n")

    print("\n========== SUMMARY ==========")
    print("Accepted :", len(valid))
    print("Rejected :", len(errors))
    print("Valid file: students_valid.json")
    print("Error log : import_errors.txt")


try:
    main()

finally:
    print("\nProgram finished.")

