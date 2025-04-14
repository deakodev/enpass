from en_cli import cli_args, cli_init, cli_login, cli_logout

def main():
    result = None
    args = cli_args()
    match args.command:
        case "init": result = cli_init()
        case "login": result = cli_login(args.master)
        case "logout": result = cli_logout()
    print(result)

if __name__ == "__main__":
    main()