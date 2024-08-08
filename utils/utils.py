from typing import Tuple, List


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args
