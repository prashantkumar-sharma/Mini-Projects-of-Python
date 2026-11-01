from student_utils import calculate_total, calculate_average, get_grade, marks_average


def build_report(student):
    total = calculate_total(student["marks"])
    average = calculate_average(student["marks"])
    grade = get_grade(average)

    report = f"{student['id']} | {student['name']} | Marks: {student['marks']}\n"
    report += f"Total: {total} | Average: {average:.2f} | Grade: {grade}"

    return report


def class_summary(records, **kwargs):
    title = kwargs.get("title", "Class Report")
    passing_mark = kwargs.get("passing_mark", 40)

    all_marks = []
    passed = 0

    for student in records:
        for mark in student["marks"]:
            all_marks.append(mark)

        if calculate_average(student["marks"]) >= passing_mark:
            passed += 1

    print(title)
    print("Class average:", round(marks_average(*all_marks), 2))
    print("Passing students:", passed)