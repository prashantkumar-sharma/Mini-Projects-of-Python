print("========== SMART CANTEEN ==========")
print("1. Veg Sandwich - Rs.60")
print("2. Masala Dosa  - Rs.80")
print("3. Chole Rice   - Rs.90")
print("4. Paneer Roll  - Rs.100")
print("5. Tea          - Rs.20")

subtotal = 0
receipt = ""
again = "y"

while again == "y":
    choice = int(input("\nChoose item number: "))

    if choice == 1:
        item = "Veg Sandwich"
        price = 60
    elif choice == 2:
        item = "Masala Dosa"
        price = 80
    elif choice == 3:
        item = "Chole Rice"
        price = 90
    elif choice == 4:
        item = "Paneer Roll"
        price = 100
    elif choice == 5:
        item = "Tea"
        price = 20
    else:
        print("Invalid item number!")
        continue

    quantity = int(input("Enter quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero!")
        continue

    amount = price * quantity
    subtotal += amount

    print(f"Added: {item} x {quantity} = Rs.{amount:.2f}")
    line = f"{item} x {quantity}: Rs.{amount}"
    receipt = receipt + line + "\n"

    again = input("Add another item? (y/n): ").lower()

discount = 0
final_total = subtotal - discount

print("\n========== RECEIPT ==========")
print(receipt, end="")
print(f"Subtotal: Rs.{subtotal:.2f}")
print(f"Discount: Rs.{discount:.2f}")
print(f"Final total: Rs.{final_total:.2f}")
print("Thank you!")