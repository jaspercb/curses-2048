import curses
from game import Game2048

def main():
    def gamedriver(stdscr):
        curses.noecho()

        highscore = 0
        def redraw(state):
            stdscr.clear()
            stdscr.addstr(0, 0, 'High score: {0}'.format(highscore))
            stdscr.addstr(1, 0, 'Current score: {0}'.format(g.score))
            for y in range(4):
                for x in range(4):
                    stdscr.addstr(2 + y, x*5, str(state[y][x]))
        keys = {
            curses.KEY_DOWN  : 'down',
            curses.KEY_UP    : 'up',
            curses.KEY_LEFT  : 'left',
            curses.KEY_RIGHT : 'right',
        }
        overrides = {
            ord('u') : lambda: g.undo(),
        }
        while True:
            g = Game2048()
            redraw(g.state)
            try:
                while True:
                    key = stdscr.getch()
                    if key in overrides:
                        overrides[key]()
                        redraw(g.state)
                    elif key in keys:
                        g.move(keys[key])
                        highscore = max(highscore, g.score)
                        redraw(g.state)
                        # rerender
            except Game2048.GameOver:
                stdscr.addstr(5, 0, 'Game over. Press ENTER to start a new game.')
                while stdscr.getch() not in [curses.KEY_ENTER, ord('\n'), ord('\r')]:
                    pass

    curses.wrapper(gamedriver)


if __name__ == '__main__':
    main()
