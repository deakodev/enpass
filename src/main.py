from en_cli import cli_args, COMMAND_MAP

def main():
    args = cli_args()
    cli_func = COMMAND_MAP[args.command]
    result = cli_func(args)
    print(result)

if __name__ == "__main__":
    main()