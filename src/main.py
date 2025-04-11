
from cli import cli_args, cli_init, cli_login

def main():
    status = None
    args = cli_args()
    match args.command:
        case "init":
            status = cli_init()
        case "login":
            status = cli_login(args.master)
            
    if status:  
        print(status) 

if __name__ == "__main__":
    main()