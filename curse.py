import curses
import sys

import TreeMaker as TM

from curses import wrapper
from curses.textpad import rectangle

tm = TM.TreeMaker()

# directory levels we care about
above = []
curr = [tm.tree.root]
below = []

changes = 0

loc_stack = [0]
loc = loc_stack[-1]

indent = 8

finalized = 0

def main(stdscr):
    global above, curr, below
    global loc_stack

    height, width = stdscr.getmaxyx()
    # make stdscr.getch non-blocking
    stdscr.nodelay(True)
    # clear screen
    stdscr.clear()

    tree_scr = stdscr.subwin(height-2, 24, 1, 1)
    tree_scr.box()

    while True:
        # store keypress
        c = stdscr.getch()
        # clear terminal
        stdscr.clear()

        draw_tree(tree_scr)
        handle_keys(stdscr, c)

def draw_windows(stdscr):
    height, width = stdscr.getmaxyx()
    stdscr.addstr('Tree')
    rectangle(stdscr, 1, 0, height-2, 26)

def draw_tree(stdscr):
    global above, curr, below
    global loc, loc_stack


    if hasattr(curr[loc], 'children'):
        below = get_children(curr[loc])
    else:
        below = []

    if above:
        for i, node in enumerate(above):
            stdscr.addstr(i, 0, node.addr)

    for i in range(len(curr)):
        if i == loc:
            stdscr.addstr(i, indent, curr[i].addr+'*')
        else:
            stdscr.addstr(i, indent, curr[i].addr)

    for i in range(len(below)):
        stdscr.addstr(i, 2*indent, below[i].addr)

def handle_keys(stdscr, c):
    global above, curr, below

    height, width = stdscr.getmaxyx()

    if c == curses.KEY_UP or c == ord('k'):
        move(-1)

    elif c == curses.KEY_DOWN or c == ord('j'):
        move(1)

    elif c == curses.KEY_LEFT or c == ord('h'):
        ascend()

    elif c == curses.KEY_RIGHT or c == ord('l'):
        descend(stdscr)

    elif c == ord(':'):
        user_command(stdscr)

    elif c == ord('q'):
        sys.exit(0)

    elif c == ord('h'):
        stdscr.addstr(height-1, 0, 'Open input prompt with ":" key')

def user_command(stdscr):
    height, width = stdscr.getmaxyx()
    chars = []
    stdscr.addch(height-1, 0, ':')

    while True:
        try:
            c = stdscr.getch()

            if c == 10: # enter key
                break

            elif c == 127: # backspace key
                try:
                    chars.pop(-1)

                except IndexError:
                    pass

            else:
                chars.append(chr(c))

            stdscr.addstr(height-1, 1, ' '*(width-2))
            stdscr.addstr(height-1, 1, ''.join(chars))

        except ValueError:
            pass

    s = ''.join(chars)

    try:
        tm.parse(s)
    except:
        stdscr.addstr(height-1, 0, 'invalid command')

def move(dy):
    global loc

    loc = (loc + dy) % len(curr)

    if hasattr(curr[loc], 'children'):
        below = get_children(curr[loc])

    else:
        below = []

def descend(stdscr):
    global above, curr, below
    global loc, loc_stack

    stdscr.clear()

    if below:
        above = curr
        curr = below
        below = get_children(curr[loc])

        loc_stack.append(0)
        loc = loc_stack[-1]

def ascend():
    global above, curr, below
    global loc, loc_stack

    if above:
        below = curr
        curr = above

        if len(loc_stack) > 1:
            loc_stack.pop(-1)
            loc = loc_stack[-1]

        if curr[loc].parent:
                above = [curr[loc].parent]

        else:
            above = []

def get_children(node):
    children = []

    if hasattr(node, 'children'):
        for child in node.children.values():
            children.append(child)

    return children

wrapper(main)

