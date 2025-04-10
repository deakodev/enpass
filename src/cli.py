

def password_confirmed_from_user(message):
    while True:
        master = input(message)
        master2 = input("Confirm password: ")
        if master == master2:
            return master
        else:
            print("Passwords do not match. Please try again.")