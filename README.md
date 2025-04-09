# enpass

cml password encryptor and manager

Great! Let's start with building a **simple password manager and encryptor**. We'll focus on a basic **command-line tool** that allows you to:

1. **Add passwords**.
2. **Retrieve passwords**.
3. **Encrypt and decrypt passwords**.
4. **Store passwords securely** using encryption.

We’ll use **Python** and **AES encryption** to store passwords safely. I'll guide you through the steps, and you can add or modify features as needed.

### **Step-by-Step Plan**:

#### 1. **Set Up Dependencies**:

We'll need some libraries:

- **`cryptography`**: For AES encryption and decryption.
- **`argparse`**: For command-line argument parsing.
- **`json`**: For storing passwords in a simple JSON format.

To install the `cryptography` library, run:

```bash
pip install cryptography
```

#### 2. **Basic Structure**:

- We'll store passwords in a **JSON file**.
- We'll encrypt the passwords using **AES** encryption.
- The password manager will provide CLI commands to **add**, **retrieve**, and **list** stored passwords.

#### 3. **Encryption Setup**:

We’ll use **AES** (Advanced Encryption Standard) to encrypt and decrypt the passwords. To simplify, we'll use **`Fernet`**, which is a symmetric encryption method provided by the `cryptography` library.

### **Step 1: Implement Basic Password Manager and Encryptor**

Here’s a simple implementation in Python:

```python
import json
import argparse
from cryptography.fernet import Fernet

# Function to generate a key and instantiate a Fernet object
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the secret key from a file
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the password
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Save the passwords to a JSON file
def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

# Load the passwords from the JSON file
def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            passwords = json.load(f)
    except FileNotFoundError:
        passwords = {}
    return passwords

# Add a new password
def add_password(name, password, key):
    passwords = load_passwords()
    encrypted_password = encrypt_password(password, key)
    passwords[name] = encrypted_password.decode()  # Store encrypted password
    save_passwords(passwords)
    print(f"Password for {name} added successfully.")

# Retrieve a password
def get_password(name, key):
    passwords = load_passwords()
    if name in passwords:
        encrypted_password = passwords[name].encode()
        decrypted_password = decrypt_password(encrypted_password, key)
        print(f"Password for {name}: {decrypted_password}")
    else:
        print(f"No password found for {name}")

# Command-line interface (CLI)
def main():
    parser = argparse.ArgumentParser(description="Password Manager with Encryption")
    parser.add_argument("command", choices=["add", "get", "generate_key"], help="Command to execute")
    parser.add_argument("--name", help="The name of the service or account")
    parser.add_argument("--password", help="The password to store")

    args = parser.parse_args()

    if args.command == "generate_key":
        generate_key()
        print("Key generated and saved as 'secret.key'.")

    else:
        key = load_key()

        if args.command == "add":
            if args.name and args.password:
                add_password(args.name, args.password, key)
            else:
                print("Please provide both name and password.")

        elif args.command == "get":
            if args.name:
                get_password(args.name, key)
            else:
                print("Please provide the name of the account.")

if __name__ == "__main__":
    main()
```

### **How the Program Works**:

1. **Generate Key**:

   - The `generate_key` function creates a new encryption key and saves it to a file (`secret.key`). This key is used to encrypt and decrypt passwords.

2. **Add Password**:

   - The `add_password` function takes a service name (e.g., "Google") and a password, encrypts the password using the loaded encryption key, and stores it in a JSON file (`passwords.json`).

3. **Get Password**:

   - The `get_password` function allows you to retrieve a password by specifying the service name. It decrypts the stored password using the encryption key.

4. **Encryption/Decryption**:

   - **AES (Fernet)** is used for encryption and decryption. The password is encrypted when saved and decrypted when retrieved.

5. **Command-Line Interface**:
   - `add`: Adds a password for a specific service.
   - `get`: Retrieves the password for a specific service.
   - `generate_key`: Generates a new encryption key.

### **Example Usage**:

1. **Generate Key**:
   This will create the `secret.key` file that’s used for encryption/decryption.

   ```bash
   python password_manager.py generate_key
   ```

2. **Add a Password**:
   This will add a password for a specific service (e.g., Google).

   ```bash
   python password_manager.py add --name "google" --password "mysecretpassword"
   ```

3. **Get a Password**:
   This will retrieve the password for a given service (e.g., Google).
   ```bash
   python password_manager.py get --name "google"
   ```

### **Security Notes**:

- **Encryption Key**: The security of this system heavily depends on the **`secret.key`**. You must keep this key secure; if someone has access to this file, they can decrypt your passwords.
- **Password Storage**: Passwords are stored in a **JSON file** in plaintext, but the passwords themselves are encrypted before storage. Always keep backups of your encrypted password data in a secure location.

### **Enhancements and Next Steps**:

- **Error Handling**: Improve error handling for cases where files are missing or corrupted.
- **Password Validation**: Add password validation (e.g., checking for length or complexity).
- **Password Deletion**: Add functionality to delete stored passwords.
- **Password Generation**: Implement a password generator to create secure random passwords.
- **Database Integration**: For a more robust solution, integrate an encrypted database to store passwords securely.

---

This should give you a solid foundation for building your password manager and encryptor! You can extend it further with more features as needed. Let me know if you'd like help with any specific part of the project!
