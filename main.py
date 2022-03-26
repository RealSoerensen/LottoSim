from random import randint
from curses import wrapper
import curses

def gen_lines():
    num_list = []
    while len(num_list) != 7:
        new_int = randint(1, 36)
        if new_int not in num_list:
            num_list.append(new_int)
    return sorted(num_list)

def check_nums(ticket, lotto_nums):
    correct_list = []
    for line in ticket:
        correct_nums = 0
        for num in line:
            for lotto_num in lotto_nums:
                if num == lotto_num:
                    correct_nums += 1
        correct_list.append(correct_nums)
    return correct_list

def game(stdscr, lines, mode):
    ticket = [gen_lines() for _ in range(lines)]
    lotto_nums = gen_lines()
    weeks = 0
    four_right = 0
    five_right = 0
    six_right = 0
    seven_right = 0
    profit = 0
    while seven_right == 0:
        profit -= lines*6
        weeks+=1
        for correct_num in check_nums(ticket, lotto_nums):
            if correct_num == 4:
                four_right += 1
                profit+=60
            elif correct_num == 5:
                five_right += 1
                profit+=152
            elif correct_num == 6:
                six_right += 1
                profit+=1924
            elif correct_num == 7:
                seven_right += 1
                profit+=19000000

        try:
            stdscr.addstr(0, 0, "My lines:\n")
            for i, x in enumerate(ticket):
                stdscr.addstr(f"{i+1}. {str(x)}\n")
            stdscr.addstr(len(ticket)+1, 0, "Lotto lines: {}".format(lotto_nums))
            stdscr.addstr(len(ticket)+2, 0, "Week: {}".format(weeks))
            stdscr.addstr(len(ticket)+3, 0, "Years: {}".format(round(weeks/52)))
            stdscr.addstr(len(ticket)+4, 0, "Profit: {}kr".format(profit))
            stdscr.addstr(len(ticket)+5, 0, "4 correct: {}".format(four_right))
            stdscr.addstr(len(ticket)+6, 0, "5 correct: {}".format(five_right))
            stdscr.addstr(len(ticket)+7, 0, "6 correct: {}".format(six_right))
            stdscr.addstr(len(ticket)+8, 0, "7 correct: {}".format(seven_right))
            
        except curses.error:
            stdscr.clear()
            stdscr.addstr(0, 0, "Error, terminal too small")
            stdscr.addstr(1, 0, "Please make the terminal bigger and reset the application")
            stdscr.getkey()
            break

        stdscr.refresh()
        if mode == 2:
            ticket = [gen_lines() for _ in range(lines)]
        lotto_nums = gen_lines()

    stdscr.clear()
    if seven_right == 1:
        stdscr.addstr(0, 0, "You won!")
        stdscr.addstr(1, 0, "It took {} weeks or {} years to win the lotto".format(weeks, round(weeks/52)))
        stdscr.addstr(2, 0, "You made {}kr".format(profit))  

def main(stdscr):
    stdscr.clear()
    while True:
        stdscr.addstr(0, 0, "Welcome to the lotto game!")
        stdscr.addstr(1, 0, "How many lines do you want per ticket? 6kr per line.\n")
        stdscr.addstr(2, 0, "Enter a number between 1 and 25: ")
        curses.echo()
        lines = stdscr.getstr()
        try:
            lines = int(lines)
        except ValueError:
            stdscr.clear()
            stdscr.addstr(0, 0, "Invalid input.\n")
            continue
        if lines < 1 or lines > 25:    
            stdscr.clear()
            stdscr.addstr(0, 0, "Invalid input.\n")
            continue
        break

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Welcome to the lotto game!")
        stdscr.addstr(1, 0, "Same numbers [1] or different numbers? [2]\n")
        curses.echo()
        mode = stdscr.getstr()
        try:
            mode = int(mode)
        except ValueError:
            stdscr.clear()
            stdscr.addstr(0, 0, "Invalid input.\n")
            continue
        if mode == 1 or mode == 2:    
            break
    game(stdscr, lines, mode)
    stdscr.refresh()

wrapper(main)