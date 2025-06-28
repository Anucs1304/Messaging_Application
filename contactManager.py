contact_list = set()

def add_contact(name):
    if name not in contact_list:
        contact_list.add(name)
        print(f"[+] Contact '{name}' added.")
    else:
        print(f"[!] '{name}' already in contacts.")

def remove_contact(name):
    if name in contact_list:
        contact_list.remove(name)
        print(f"[-] Contact '{name}' removed.")
    else:
        print(f"[!] '{name}' not found in contacts.")

def view_contacts():
    if not contact_list:
        print("[*] No contacts yet.")
    else:
        print("[📇] Your Contacts:")
        for user in sorted(contact_list):
            print(f" - {user}")
