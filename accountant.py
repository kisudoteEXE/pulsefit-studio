
def read_all_payments():
    payments = []
    try:
        with open("payments.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line != "":
                    payments.append(line.split(","))
    except FileNotFoundError:
        payments = []
    return payments

def generate_next_payment_id():
    payments = read_all_payments()
    if len(payments) == 0:
        return "P001"

    highest_id = 0
    for payment in payments:
        if len(payment) > 0 and payment[0].startswith("P"):
            payment_id_number = int(payment[0][1:])
            if payment_id_number > highest_id:
                highest_id = payment_id_number

    next_id = highest_id + 1

    if next_id < 10:
        return "P00" + str(next_id)
    elif next_id < 100:
        return "P0" + str(next_id)
    else:
        return "P" + str(next_id)

def record_payment():
    print("\n--- Record New Payment ---")
    payment_id = generate_next_payment_id()
    print("Generated Payment ID:", payment_id)

    member_id = input("Enter Member ID (e.g., M001): ").strip()
    booking_id = input("Enter Booking ID (e.g., B001): ").strip()

    while True:
        amount_input = input("Enter payment amount: ").strip()
        try:
            amount = float(amount_input)
            if amount > 0:
                break
            else:
                print("Payment amount must be greater than 0. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numerical amount.")

    date = input("Enter payment date (YYYY-MM-DD): ").strip()


    while True:
        status = input("Enter payment status (Paid/Outstanding): ").strip()
        if status == "Paid" or status == "Outstanding":
            break
        else:
            print("Invalid status. Please enter either 'Paid' or 'Outstanding'.")

    with open("payments.txt", "a") as file:
        file.write(payment_id + "," + member_id + "," + booking_id + "," + str(round(amount, 2)) + "," + date + "," + status + "\n")

    print("Success: Payment recorded successfully with ID:", payment_id)

def update_payment_status():
    print("\n--- Update Payment Status ---")
    payments = read_all_payments()
    if len(payments) == 0:
        print("No payment records found in payments.txt.")
        return

    target_id = input("Enter Payment ID to update (e.g., P001): ").strip()
    found = False

    for record in payments:
        if record[0] == target_id:
            found = True
            print("Current Record Found:")
            print("Member ID:", record[1], "| Booking ID:", record[2], "| Amount: $" + str(record[3]), "| Current Status:", record[5])

            while True:
                new_status = input("Enter new status (Paid/Outstanding): ").strip()
                if new_status == "Paid" or new_status == "Outstanding":
                    record[5] = new_status
                    break
                else:
                    print("Invalid status. Please enter either 'Paid' or 'Outstanding'.")
            break

    if found:
        with open("payments.txt", "w") as file:
            for record in payments:
                file.write(record[0] + "," + record[1] + "," + record[2] + "," + record[3] + "," + record[4] + "," + record[5] + "\n")
        print("Success: Payment record", target_id, "has been updated.")
    else:
        print("Error: Payment ID", target_id, "was not found.")

def income_summary():
    payments = read_all_payments()
    total = 0.0
    for record in payments:
        if len(record) >= 6 and record[5] == "Paid":
            total = total + float(record[3])
    return round(total, 2)

def outstanding_list():
    payments = read_all_payments()
    outstanding = []
    for record in payments:
        if len(record) >= 6 and record[5] == "Outstanding":
            outstanding.append(record)
    return outstanding

def monthly_summary():
    records = read_all_payments()
    monthly_totals = {}
    for record in records:
        if len(record) >= 6 and record[5] == "Paid":
            date_str = record[4]
            if len(date_str) >= 7:
                month = date_str[5:7]
                amount = float(record[3])
                if month in monthly_totals:
                    monthly_totals[month] = monthly_totals[month] + amount
                else:
                    monthly_totals[month] = amount
    return monthly_totals

def accountant_menu():
    choice = ""
    while choice != "6":
        print("1. Record a payment")
        print("2. Update payment status")
        print("3. View total income summary")
        print("4. View outstanding payments")
        print("5. View monthly income summary")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            record_payment()

        elif choice == "2":
            update_payment_status()

        elif choice == "3":
            total = income_summary()
            print("\n--- Income Summary ---")
            print("Total Collected Income (Paid): $" + str(total))

        elif choice == "4":
            pending = outstanding_list()
            print("\n--- Outstanding Payments List ---")
            if len(pending) == 0:
                print("No outstanding payments found.")
            else:
                for p in pending:
                    print("Payment ID: " + p[0] + " | Member ID: " + p[1] + " | Booking ID: " + p[2] + " | Amount: $" + str(p[3]) + " | Date: " + p[4])

        elif choice == "5":
            summary = monthly_summary()
            print("\n--- Monthly Income Summary ---")
            if len(summary) == 0:
                print("No completed payments found.")
            else:
                for month in summary:
                    month_amount = round(summary[month], 2)
                    print("Month " + month + ": $" + str(month_amount))

        elif choice == "6":
            print("Exiting Accountant System. Goodbye!")

        else:
            print("Invalid selection. Please choose a valid option (1-6).")

if __name__ == "__main__":
    accountant_menu()
