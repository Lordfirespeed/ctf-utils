from time import sleep

from utils.reprint import Printer


with Printer(line_count=3) as printer:
    for x in range(12):
        pos = (x % 3) - 3
        printer(f"hello {x}", line_pos=pos)
        sleep(0.2)
