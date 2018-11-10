import random

class Game2048:
    class GameOver(Exception):
        pass
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = [[0]*4 for i in range(4)]
        self.score = 0
        self.place_random_2()

    def place_random_2(self):
        empties = []
        for i in range(4):
            for j in range(4):
                if 0 == self.state[i][j]:
                    empties.append((i, j))
        if not len(empties):
            raise Game2048.GameOver
        i, j = random.choice(empties)
        self.state[i][j] = 2

    def move(self, direction):
        def fixline(l):
            # slide
            l = [n for n in l if n]
            l += [0] * (4 - len(l))
            # compress - hardcoded since dimensions are 4x4
            def combine(i, j):
                if l[i] == l[j]:
                    l[i] = 2 * l[i]
                    l[j] = 0
                    self.score += l[i]
            if l[0] == l[1]:
                combine(0, 1)
                combine(2, 3)
            elif l[1] == l[2]:
                combine(1, 2)
            else:
                combine(2, 3)
            # slide
            l = [n for n in l if n]
            l += [0] * (4 - len(l))
            return l

        # collapse in direction
        assert(direction in ['up', 'down', 'left', 'right'])
        if direction == 'left':
            for i in range(4):
                self.state[i] = fixline(self.state[i])
        elif direction == 'right':
            for i in range(4):
                self.state[i] = fixline(self.state[i][::-1])[::-1]
        elif direction == 'up':
            for c in range(4):
                col = fixline(list(self.state[r][c] for r in range(4)))
                for r in range(4):
                    self.state[r][c] = col[r]
        elif direction == 'down':
            for c in range(4):
                col = list(reversed(fixline(list(reversed([self.state[r][c] for r in range(4)])))))
                for r in range(4):
                    self.state[r][c] = col[r]
        
        # then randomly put something somewhere
        self.place_random_2()
        if not self.hasValidMove():
            raise Game2048.GameOver

    def hasValidMove(self):
        def lineHasMove(l):
            l = list(l)
            return any(i == 0 for i in l) or any(l[i] == l[i+1] for i in range(3))
        return any(lineHasMove(self.state[i]) for i in range(4)) or \
                any(lineHasMove(self.state[r][c] for r in range(4)) for c in range(4))

