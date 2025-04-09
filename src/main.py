

import argparse


def main():
    parser = argparse.ArgumentParser(description="Enpass CLI")
    parser.add_argument("command", choices=["login", "set", "get", "init"], help="Command to execute")
    parser.add_argument("--account", help="The name of the service / account")
    parser.add_argument("--pass", help="The password to store")
    parser.add_argument("--master", help="Master password for login")

    args = parser.parse_args()
    print(args)

    if (args.command == "init"):
        print("init")


if __name__ == "__main__":
    main()