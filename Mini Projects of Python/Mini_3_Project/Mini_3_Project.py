subjects = ("Python", "Maths", "DBMS")  # Tuple
students = []                         # List

print("Subjects:", subjects)
count = int(input("How many students? "))

for i in range(count):
    print()
    student_id = input("Student ID: ")
    name = input("Name: ")

    marks = {}  
    for subject in subjects:
        marks[subject] = int(input(f"{subject} marks: "))

# this is giving a list of dictionary
    students.append({
        "id": student_id,
        "name": name,
        "marks": marks
    })

print("\n----- STUDENT REPORT -----")

for student in students:
    marks = student["marks"]
    total = sum(marks.values())
    average = total / len(subjects)

    if average >= 75:
        result = "Distinction"
    elif average >= 40: 
        result = "Pass"
    else:
        result = "Fail"

    print(f"\n{student['id']} | {student['name']}")
    print(", ".join(f"{subject}: {marks[subject]}" for subject in subjects))
    print(f"Total: {total} | Average: {average:.2f} | Result: {result}")

print("\nUnique subjects:", set(subjects))
print("Students recorded:", len(students))
