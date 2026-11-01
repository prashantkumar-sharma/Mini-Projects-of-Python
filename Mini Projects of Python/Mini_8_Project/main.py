from abc import ABC, abstractmethod
from datetime import date, timedelta
import json


# LIBRARY ITEMS 

class LibraryItem(ABC):
    library_name = "My College Library"

    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self._available = True

    @property
    def available(self):
        return self._available

    def borrow_item(self):
        if not self._available:
            raise ValueError("Item is already borrowed.")
        self._available = False

    def return_item(self):
        self._available = True

    @abstractmethod
    def loan_period_days(self):
        pass

    @classmethod
    def change_library_name(cls, name):
        cls.library_name = name


class Book(LibraryItem):
    def loan_period_days(self):
        return 14


class Magazine(LibraryItem):
    def loan_period_days(self):
        return 7


class ReferenceBook(LibraryItem):
    def loan_period_days(self):
        return 0


# MEMBERS 

class Member:
    max_loans = 3

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self._active_loans = []

    @property
    def borrowed_count(self):
        return len(self._active_loans)

    def add_loan(self, item_id):
        if self.borrowed_count >= self.max_loans:
            raise ValueError("Borrowing limit reached.")
        self._active_loans.append(item_id)

    def remove_loan(self, item_id):
        if item_id in self._active_loans:
            self._active_loans.remove(item_id)

    @classmethod
    def set_limit(cls, limit):
        cls.max_loans = limit


class StudentMember(Member):
    pass


class ResearchStudent(StudentMember):
    pass


class FacultyMember(Member):
    max_loans = 5


# MULTIPLE INHERITANCE 

class NotificationMixin:
    def send_notice(self, message):
        print("Notice:", message)


# MRO: NotifiedMember -> Member -> NotificationMixin -> object
class NotifiedMember(Member, NotificationMixin):
    pass


# LIBRARY MANAGER 

class LibraryManager:

    def __init__(self):
        self.items = {}
        self.members = {}
        self.loans = {}

    def add_item(self, item):
        if item.item_id in self.items:
            print("Item ID already exists.")
            return

        self.items[item.item_id] = item
        print("Item added successfully.")

    def add_member(self, member):
        if member.member_id in self.members:
            print("Member ID already exists.")
            return

        self.members[member.member_id] = member
        print("Member added successfully.")

    def borrow(self, member_id, item_id):
        if member_id not in self.members:
            print("Member not found.")
            return

        if item_id not in self.items:
            print("Item not found.")
            return

        member = self.members[member_id]
        item = self.items[item_id]

        try:
            if not item.available:
                raise ValueError("Item is already borrowed.")

            if item.loan_period_days() == 0:
                raise ValueError("Reference books cannot be borrowed.")

            member.add_loan(item_id)
            item.borrow_item()

            issue_date = date.today()
            due_date = issue_date + timedelta(
                days=item.loan_period_days()
            )

            self.loans[item_id] = {
                "member_id": member_id,
                "issue_date": str(issue_date),
                "due_date": str(due_date)
            }

            print("Borrow successful:", item_id)
            print("Due date:", due_date)

        except ValueError as error:
            print("Borrow failed:", error)

    @staticmethod
    def calculate_fine(due_date):
        today = date.today()
        due = date.fromisoformat(due_date)

        late_days = (today - due).days

        if late_days > 0:
            return late_days * 10

        return 0

    def return_item(self, item_id):
        if item_id not in self.loans:
            print("This item is not currently borrowed.")
            return

        loan = self.loans[item_id]
        member = self.members[loan["member_id"]]
        item = self.items[item_id]

        fine = self.calculate_fine(loan["due_date"])

        item.return_item()
        member.remove_loan(item_id)
        del self.loans[item_id]

        print("Item returned successfully.")
        print("Fine: Rs.", fine)

    def show_report(self):
        print("\n========== LIBRARY REPORT ==========")

        print("\nItems:")
        for item in self.items.values():
            status = "Available" if item.available else "Borrowed"
            print(item.item_id, "|", item.title, "|", status)

        print("\nMembers:")
        for member in self.members.values():
            print(
                member.member_id,
                "|",
                member.name,
                "| Borrowed:",
                member.borrowed_count
            )

        print("\nActive Loans:")
        if not self.loans:
            print("No active loans.")
        else:
            for item_id, loan in self.loans.items():
                print(
                    item_id,
                    "|",
                    loan["member_id"],
                    "| Due:",
                    loan["due_date"]
                )

    def save_data(self):
        data = {
            "items": [],
            "members": [],
            "loans": self.loans
        }

        for item in self.items.values():
            data["items"].append({
                "type": item.__class__.__name__,
                "id": item.item_id,
                "title": item.title
            })

        for member in self.members.values():
            data["members"].append({
                "type": member.__class__.__name__,
                "id": member.member_id,
                "name": member.name
            })

        with open("library_data.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Data saved.")

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)

            item_classes = {
                "Book": Book,
                "Magazine": Magazine,
                "ReferenceBook": ReferenceBook
            }

            member_classes = {
                "StudentMember": StudentMember,
                "ResearchStudent": ResearchStudent,
                "FacultyMember": FacultyMember
            }

            for item in data["items"]:
                item_class = item_classes[item["type"]]
                self.items[item["id"]] = item_class(
                    item["id"], item["title"]
                )

            for member in data["members"]:
                member_class = member_classes[member["type"]]
                self.members[member["id"]] = member_class(
                    member["id"], member["name"]
                )

            self.loans = data["loans"]

            print("Data loaded.")

        except FileNotFoundError:
            print("No previous data found.")


# MAIN PROGRAM 

library = LibraryManager()

while True:

    print("\n===LIBRARY SYSTEM ===")
    print("1. Add Book")
    print("2. Add Magazine")
    print("3. Add Reference Book")
    print("4. Add Student")
    print("5. Add Research Student")
    print("6. Add Faculty")
    print("7. Borrow Item")
    print("8. Return Item")
    print("9. View Report")
    print("10. Save Data")
    print("11. Load Data")
    print("0. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        item_id = input("Book ID: ")
        title = input("Book title: ")
        library.add_item(Book(item_id, title))

    elif choice == "2":
        item_id = input("Magazine ID: ")
        title = input("Magazine title: ")
        library.add_item(Magazine(item_id, title))

    elif choice == "3":
        item_id = input("Reference Book ID: ")
        title = input("Book title: ")
        library.add_item(ReferenceBook(item_id, title))

    elif choice == "4":
        member_id = input("Student ID: ")
        name = input("Student name: ")
        library.add_member(StudentMember(member_id, name))

    elif choice == "5":
        member_id = input("Research Student ID: ")
        name = input("Student name: ")
        library.add_member(ResearchStudent(member_id, name))

    elif choice == "6":
        member_id = input("Faculty ID: ")
        name = input("Faculty name: ")
        library.add_member(FacultyMember(member_id, name))

    elif choice == "7":
        member_id = input("Member ID: ")
        item_id = input("Item ID: ")
        library.borrow(member_id, item_id)

    elif choice == "8":
        item_id = input("Item ID: ")
        library.return_item(item_id)

    elif choice == "9":
        library.show_report()

    elif choice == "10":
        library.save_data()

    elif choice == "11":
        library.load_data()

    elif choice == "0":
        print("Thank you. Program ended.")
        break

    else:
        print("Invalid choice.")