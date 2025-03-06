"""
See: https://docs.python.org/3/library/secrets.html
"""
from secrets import token_bytes as random_bytes


def main():
    print(random_bytes())


if __name__ == "__main__":
    main()
