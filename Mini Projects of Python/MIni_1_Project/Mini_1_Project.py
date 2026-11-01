
# Student Monthly Budget Analyzer

Name = input("Enter your name: ")


Monthly_Income = float(input("Enter your monthly income: "))

Food_Expenses = float(input("Enter your food expenses: "))
Travel_Expenses = float(input("Enter your travel expenses: "))
Study_Materials = float(input("Enter your study material expenses: "))
Mobile_Internet = float(input("Enter your mobile/internet expenses: "))
Other_Expenses = float(input("Enter your other expenses: "))


Total_Expenses = (Food_Expenses + Travel_Expenses + Study_Materials + Mobile_Internet + Other_Expenses)


Remaining_Balance = Monthly_Income - Total_Expenses



Food_Percentage = (Food_Expenses / Total_Expenses) * 100
Travel_Percentage = (Travel_Expenses / Total_Expenses) * 100
Study_Percentage = (Study_Materials / Total_Expenses) * 100
Mobile_Percentage = (Mobile_Internet / Total_Expenses) * 100
Other_Percentage = (Other_Expenses / Total_Expenses) * 100

# 
if Monthly_Income > 0:
    Savings_Percentage = (Remaining_Balance / Monthly_Income) * 100
else:
    Savings_Percentage = 0

# Display 
print("\n===== STUDENT MONTHLY BUDGET REPORT =====")
print(f"Student Name: {Name}")
print(f"Monthly Income: Rs. {Monthly_Income:.2f}")

print(f"1. Food Expenses: Rs. {Food_Expenses:.2f} ({Food_Percentage:.2f}%)")
print(f"2. Travel Expenses: Rs. {Travel_Expenses:.2f} ({Travel_Percentage:.2f}%)")
print(f"3. Study Materials: Rs. {Study_Materials:.2f} ({Study_Percentage:.2f}%)")
print(f"4. Mobile/Internet: Rs. {Mobile_Internet:.2f} ({Mobile_Percentage:.2f}%)")
print(f"5. Other Expenses: Rs. {Other_Expenses:.2f} ({Other_Percentage:.2f}%)")

print(f"\nTotal Expenses: Rs. {Total_Expenses:.2f}")
print(f"Remaining Balance: Rs. {Remaining_Balance:.2f}")
print(f"Savings Rate: {Savings_Percentage:.2f}%")
