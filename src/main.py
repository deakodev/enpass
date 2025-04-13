from en_cli import cli_args, cli_init, cli_login

def main():
    result = None
    args = cli_args()
    match args.command:
        case "init": result = cli_init()
        case "login": result = cli_login(args.master)
    print(result)

if __name__ == "__main__":
    main()