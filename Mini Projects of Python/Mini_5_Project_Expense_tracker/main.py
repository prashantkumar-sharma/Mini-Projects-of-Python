import student_utils as su
from report_utils import build_report, class_summary


def main():
    records = []

    # Positional arguments
    s1 = su.add_student("S101", "Aman", [78, 65, 88])

    # Keyword arguments
    s2 = su.add_student(student_id="S102", name="Riya", marks=[35, 72, 61])

    if s1 is not None:
        records.append(s1)

    if s2 is not None:
        records.append(s2)

    print("===== STUDENT PERFORMANCE REPORT =====")

    for student in records:
        print(build_report(student))
        print()

    # Default argument minimum=75
    print("High performers:", su.get_top_students(records))

    print()
    class_summary(records, title="Class Report", passing_mark=40)

    print("Recursive sum from 1 to 5:", su.recursive_sum(5))

    su.scope_example()


if __name__ == "__main__":
    main()
