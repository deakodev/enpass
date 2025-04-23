# 🔐 Enpass CLI

Enpass CLI is a lightweight, secure, and offline-first password manager built for the terminal. It lets you store, retrieve, and manage passwords, secure notes, and other sensitive data using strong encryption — all through a simple command-line interface.

![Enpass CLI Demo](./public/images/enpass_demo.gif)

---

## 🚀 Features

- 🔑 Store and retrieve encrypted passwords
- 📝 Secure notes and custom entries
- 📁 Categorized vault items (logins, notes, cards, projects, etc.)
- 🔒 AES-256 encryption using a master password
- 🧠 Login/logout session support
- 💾 Encrypted local vault file
- 📜 Clean CLI output
- 🧪 Simple unit testing support

---

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Encryption**: `cryptography` (Fernet/AES)
- **Interface**: Pure CLI (no GUI)
- **Scripts**: Bash-based helpers for testing and running

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/deakodev/enpass.git
cd enpass
```

(Optional) Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🧪 Running & Testing

Run the CLI app:

```bash
./scripts/run.sh
```

Run tests:

```bash
./scripts/test.sh
```

---

## 🔧 Basic Commands

| Command               | Description                     |
|----------------------|---------------------------------|
| `enpass init`        | Initialize the encrypted vault  |
| `enpass login`       | Unlock vault with master key    |
| `enpass logout`      | Lock the vault                  |
| `enpass add`         | Add a new item (login, note…)   |
| `enpass list`        | List all saved items            |
| `enpass view <name>` | View details of an item         |
| `enpass remove <name>` | Delete an item from the vault |

---

## 🧱 Project Structure

```
enpass/
├── cli/                # CLI entry points
├── core/               # Vault, encryption, storage logic
├── scripts/            # Run and test scripts
├── tests/              # Unit tests
├── vault.json.enc      # Your encrypted vault (created on init)
└── README.md
```

---

## 🔐 Security

- AES-256 encryption (via Fernet)
- Master password never stored
- Random salt and IV for each encryption cycle
- Vault file is unreadable without your master password

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Thanks to the Python open-source community and developers of cryptographic tools. Inspired by the simplicity of tools like `pass`, `bitwarden`, and `gopass`.

---
