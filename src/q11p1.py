from extras.math_extras.discrete_log.lib import Group
from extras.math_extras.discrete_log.shanks import shanks_discrete_log


def main():
    group = Group(2579, 2, 2578)
    result = shanks_discrete_log(group, 949)
    print(f"{result = }")


if __name__ == "__main__":
    main()
