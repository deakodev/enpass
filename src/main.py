from en_cli import cli_args, command_map

def main():
    args = cli_args()
    cli_func = command_map[args.command]
    result = cli_func(args)
    print(result)

if __name__ == "__main__":
    main()