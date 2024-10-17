import sqlite3

# Function to create the database table if it doesn't exist


def create_table():
    open = sqlite3.connect("contacts.db")
    cursor = open.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       address TEXT,
                       phone TEXT,
                       email TEXT)''')
    open.commit()
    open.close()


# Function to add a new contact
def add_contact(name, address, phone, email):
    open = sqlite3.connect("contacts.db")
    cursor = open.cursor()
    cursor.execute("INSERT INTO contacts (name, address, phone, email) VALUES (?, ?, ?, ?)",
                   (name, address, phone, email))
    open.commit()
    open.close()


# Function to edit an existing contact

def edit_contact(contact_id, name=None, address=None, phone=None, email=None):
    with sqlite3.connect("contacts.db") as conn:
        # Retrieve the existing values for the specified contact
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, address, phone, email FROM contacts WHERE id=?", (contact_id,))
        existing_values = cursor.fetchone()

        # Update the contact information
        conn.execute(
            "UPDATE contacts SET name=?, address=?, phone=?, email=? WHERE id=?",
            (name or existing_values[0], address or existing_values[1],
             phone or existing_values[2], email or existing_values[3], contact_id)
        )
        conn.commit()


# Function to delete a contact


def delete_contact(contact_id):
    open = sqlite3.connect("contacts.db")
    cursor = open.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    open.commit()
    open.close()


# Function to list all contacts
def list_contacts():
    open = sqlite3.connect("contacts.db")
    cursor = open.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    open.close()

    if not contacts:
        print("No contacts found.")
    else:
        for contact in contacts:
            print(f"ID: {contact[0]}, Name: {contact[1]}, Address: {
                  contact[2]}, Phone: {contact[3]}, Email: {contact[4]}")

# Function to search for a contact in a contact list


def search_contact(search_term):
    open = sqlite3.connect("contacts.db")
    cursor = open.cursor()
    #This line executes an SQL query with placeholders (?) to prevent SQL injection. The query searches for rows in the contacts table where the name or email column contains the specified search_term. The % symbols are used as wildcards for partial matches.
    cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR email LIKE ?",
                   ('%' + search_term + '%', '%' + search_term + '%'))
    result = cursor.fetchall()
    open.close()
    return result


# Define a global variable
loop = True

# Function to set a global variable and break the loop


def breaking_loop():
    global loop
    loop = False


def Exit():
    option = input(
        "\nEnter 1 to go back to Main Menu. 2 to Exit: ")
    if option == "1":
        main()
    elif option == "2":
        print("Exiting Contact Book. Goodbye!")
        breaking_loop()

    else:
        print("Invalid choice. Back to Main Menu <<<")
        main()


# Main function to interact with the user
def main():
    #The create_table() ensures there is an existing table before any further action of input
    create_table()
    print("\nContact Book Menu:")
    print("1. Add Contact")
    print("2. Edit Contact")
    print("3. Delete Contact")
    print("4. Search Contact")
    print("5. View All Contacts")
    print("6. Exit\n")


# Initial execution of the main function
main()
while loop:
    choice = input("Enter your choice (1-6): ")
    print("\n")

    if choice == "1":
        # Code for adding a new contact
        name = input("Enter name: ")
        address = input("Enter address: ")
        phone = input("Enter phone number: ")
        email = input("Enter email address: ")
        add_contact(name, address, phone, email)
        print("Contact added successfully.")
        # Code to exit the Adding Contact Menu
        Exit()
    elif choice == "2":
        # Code for editing an existing contact
        list_contacts()
        contact_id = input("\nEnter the ID of the contact you want to edit: ")
        name = input("Enter new name: ")
        address = input("Enter new address: ")
        phone = input("Enter new phone number: ")
        email = input("Enter new email address: ")
        edit_contact(contact_id, name, address,
                     phone, email)
        print("Contact edited successfully.")
        # Code to exit the Editing contact Menu
        Exit()
    elif choice == "3":
        # Code for deleting a contact
        list_contacts()
        contact_id = input(
            "\nEnter the ID of the contact you want to delete: ")
        delete_contact(contact_id)
        print("Contact deleted successfully.")
        # Code to exit the Delete contact Menu
        Exit()

    elif choice == "4":
        # Code for searching for a contact
        while True:
            # Asking user to input the search term.
            search_term = input(
                "Enter the name or email of the contact to search: ")
            # We are taking a blank list.Here we will store all the contacts that are matching with our search term.
            found_contacts = search_contact(search_term)
            if found_contacts:  # Checking if any contact is the in the found_contacts list.
                print("Matching contacts found:")
                # Looping through the found_contacts list to print each contact details that is matching our search term.
                for contact in found_contacts:
                    print(f"ID: {contact[0]}, Name: {contact[1]}, Address: {
                          contact[2]}, Phone: {contact[3]}, Email: {contact[4]}")
                    main()
                break
            else:
                print("No matching contacts found.")
                main()
                break
    elif choice == "5":
        # Code for displaying all contacts
        list_contacts()
        Exit()

    elif choice == "6":
        # Code to Exit the Main Menu
        print("Exiting Contact Book. Goodbye!")
        breaking_loop()
    else:

        print("\nInvalid choice. \nPlease Enter a number between 1 and 6.")
        