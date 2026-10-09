classes_file = "classes.txt"
booking_file = "booking.txt"
payment_file = "payment.txt"

def read_classes():
    classes = [] 
    open(classes_file, "a").close()

    with open(classes_file, "r") as f:
        for line in f:
           line = line.strip()
           if line:
            classes.append(line.split(","))
    return classes

def write_classes(classes):
   with open(classes_file, "w") as f:
      for c in classes:
         f.write(",".join(c) + "\n")

def create_class_code(classes):
   if not classes:
      return "001"

   highest = 0
   for c in classes:
      if c[0].isdigit():
         number = int(c[0])
         if number > highest:
            highest = number
   return f"{highest + 1:03d}"

   
def add_class():
   classes = read_classes()
   name = input("Enter class name: ")
   trainer = input("Enter trainer name: ")
   time_slot = input("Enter time slot: ")

   while True:
      total_pax = input("Enter total pax: ")
      if total_pax.isdigit() and int(total_pax) > 0:
         break
      print("Please enter a valid number. Don't fool us like how you fool your gains.")

   new_code = create_class_code(classes)
   new_class = [new_code, name, trainer, time_slot, total_pax, "0"]
   classes.append(new_class)
   write_classes(classes)

   print(f"\nClass added successfully. Class code: {new_code}\n")


def view_classes():
   classes = read_classes()
   if not classes:
      print("\nNo classes found. \n")
      return 

   print(f"\n{'Code':<6}{'Name':<15}{'Trainer':<15}{'Time Slot':<12}{'Total Pax':<10}{'Booked':<8}")
   print("-" * 66)
   for c in classes: 
      class_code, name, trainer, time_slot, total_pax, booked = c 
      print(f"{class_code:<6}{name:<15}{trainer:<15}{time_slot:<12}{total_pax:<10}{booked:<8}")
   print()

def find_class_by_code (classes, class_code):
      for c in classes:
         if c[0] == class_code:
            return c
      return None

def update_class():
   classes = read_classes()
   view_classes()
   class_code = input("Enter the Class Code to update: ")

   target = find_class_by_code(classes, class_code)
   if target is None:
      print("\nClass ID not found. \n")
      return 

   print("Leave a field blank to keep current value. ")
   name = input(f"New name [{target[1]}]: ")
   trainer = input(f"New trainer [{target[2]}]: ")
   time_slot = input(f"New time slot [{target[3]}]: ")
   total_pax = input(f"New total pax [{target[4]}]: ")

   if name:
      target[1] = name
   if trainer:
         target[2] = trainer
   if time_slot:
         target[3] = time_slot
   if total_pax:
      booked = int(target[5])
      if total_pax.isdigit() and int(total_pax) >= booked:
         target[4] = total_pax
      else:
         print (f"That won't do. Must be a num >= current bookings {booked}. Old value saved.")

   write_classes(classes)
   print("\nClass updated successfully. \n")

def delete_class():
   classes = read_classes()
   view_classes()
   class_code = input ("Enter the Class ID to remove: ")

   target = find_class_by_code(classes, class_code)
   if target is None:
            print("\nClass ID not found. \n")
            return 

   if target[5] != "0":
      print(f"\n Cannot delete: this class has {target[5]} active booking(s). Cancel your active bookings before deleting. \n")
      return

   confirm = input(f"Do you want to remove '{target[1]}'? (y/n:): ")
   if confirm.lower() == "y":
      classes.remove(target)
      write_classes(classes)
      print("\nClass removed. \n")
   else:
      print("\nDeletion cancelled. \n")


def read_bookings():
   bookings = [] 
   open(booking_file, "a").close()

   with open(booking_file, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            bookings.append(line.split(","))
   return bookings

def read_payments():
   payments = [] 
   open(payment_file, "a").close()

   with open(payment_file, "r") as f:
      for line in f:
         line = line.strip()
         if line:
            payments.append(line.split(","))
   return payments

def generate_report():
   classes = read_classes()
   bookings = read_bookings()
   payments = read_payments()

   print("\n===== OVERALL STUDIO REPORT =====")
   print(f"Total classes offered: {len(classes)}")
   print(f"Total bookings made: {len(bookings)}")

   if classes:
      most_popular = max(classes, key=lambda c: int(c[5]))
      print(f"Most popular class: {most_popular[1]} ({most_popular[5]} bookings)")

      all_pax = sum(int(c[4]) for c in classes)
      total_booked = sum(int(c[5]) for c in classes)
      if all_pax > 0:
         utilization = (total_booked / all_pax) * 100
         print(f"Overall capacity utilization: {utilization:.2f}%")

   if payments:
      total_income = sum(float(p[2]) for p in payments if p[3].lower() == "paid")
      print(f"Total income collected: RM{total_income:.2f}")
   else:
      print("Total income collected: (payment.txt not available yet)")

   print("==================================\n")




def admin_menu():
   while True:
      print("===== ADMIN MENU =====")
      print("1. Add Class")
      print("2. View Classes")
      print("3. Update Classes")
      print("4. Remove Classes")
      print("5. Generate Overall Report")
      print("6. Main Menu")

      option = input("Enter option: ")

      if option == "1":
         add_class()
      elif option == "2":
         view_classes()
      elif option == "3":
         update_class()
      elif option == "4":
         delete_class()
      elif option == "5":
         generate_report()
      elif option == "6":
         break
      else:
         print("\nInvalid option, please try again.\n")



if __name__ == "__main__":
   admin_menu()


