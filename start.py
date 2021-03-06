import argparse
from app import client, server


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Start {client} or {server}")

    args = parser.parse_args()

    if args.mode == "client":
        client.start()
        pass
    elif args.mode == "server":
        server.serve()
    else:
        parser.error("Arguments must be either {client} or {server}")


if __name__ == "__main__":
    main()
