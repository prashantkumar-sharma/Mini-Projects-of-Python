def add_student(student_id, name, marks):
    if name == "" or student_id == "" or len(marks) == 0:
        return None

    for mark in marks:
        if not isinstance(mark, (int, float)) or mark < 0 or mark > 100:
            return None

    return {"id": student_id, "name": name, "marks": marks}


def calculate_total(marks):
    return sum(marks)


def calculate_average(marks):
    return sum(marks) / len(marks)


def get_grade(average):
    if average >= 75:
        return "Distinction"
    elif average >= 60:
        return "First Division"
    elif average >= 40:
        return "Pass"
    else:
        return "Fail"


def get_top_students(records, minimum=75):
    top = filter(lambda s: calculate_average(s["marks"]) >= minimum, records)
    names = map(lambda s: s["name"], top)
    return list(names)


def marks_average(*marks):
    if len(marks) == 0:
        return 0
    return sum(marks) / len(marks)


def recursive_sum(n):
    if n == 0:
        return 0
    return n + recursive_sum(n - 1)


def scope_example():
    message = "This is a local variable"
    print(message)
