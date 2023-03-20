import itertools
import random
import time


class Chessmaster:
    def __init__(self, name):
        self.name = name
        self.state = True
        self.opponents = []

    def add_opponent(self, opponent):
        self.opponents.append(opponent)

    def change_state(self):
        self.state = not self.state


class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def change_state(self):
        self.first.state = not self.first.state
        self.second.state = self.second.state


class Tour:
    def __init__(self, number):
        self.number = number
        self.__pairs = []

    def __call__(self, pair: Pair):
        if self.check_pair(pair):
            self.add_pair(pair)
            pair.change_state()

    def get_players(self):
        tour_players = []
        for pr in self.__pairs:
            tour_players.extend((pr.first, pr.second))
        return tour_players

    def add_opponents(self):
        for pr in self.__pairs:
            pr.first.add_opponent(pr.second)
            pr.second.add_opponent(pr.first)

    def add_pair(self, pair):
        self.__pairs.append(pair)

    def check_pair(self, pair):
        if pair.first.state and pair.second.state:
            return pair.first not in self.get_players() and pair.second not in self.get_players()
        return False

    def get_pairs(self):
        return self.__pairs

    def clear(self):
        for pr in self.__pairs:
            pr.change_state()
            pairs.remove(pr)
        self.__pairs.clear()

    def pick_up_pair(self):
        try:
            while True:
                last_pair = self.__pairs.pop()
                last_pair.change_state()
                n = len(players)//2 - len(self.__pairs)
                suitable_pairs = []
                for pr in pairs:
                    if self.check_pair(pr):
                        suitable_pairs.append(pr)
                for combination in itertools.combinations(suitable_pairs, n):
                    chessplayers = set(players) - set(self.get_players())
                    comb_players = []
                    for pr in combination:
                        comb_players.extend((pr.first, pr.second))
                    if set(comb_players) == set(chessplayers):
                        for pr in combination:
                            self.add_pair(pr)
                            pr.change_state()
                        return True
        except IndexError:
            return False


class Container:
    def __init__(self):
        self.text = ''

    def add_text(self, tour):
        self.text += f'Тур {tour.number}\n'
        for pr in tour.get_pairs():
            colours = self.gen_colours()
            self.text += f'{pr.first.name}({colours[0]}) - {pr.second.name}({colours[1]})\n'
        self.text += '-'*20 + '\n'

    def print_all(self):
        print(self.text)

    @staticmethod
    def gen_colours():
        state = random.choice((True, False))
        colours = {False: 'чёрные',
                   True: 'белые'
                   }
        return colours[state], colours[not state]


lst_players = [player.strip() for player in input().split(',')]
n = len(lst_players)
cr = Container()
start = time.time()
players = [Chessmaster(player) for player in lst_players]
pairs = [Pair(pair[0], pair[1]) for pair in itertools.combinations(players, 2)]
random.shuffle(pairs)
tour_number = 0
while tour_number < len(players) - 1:
    tour_number += 1
    tour = Tour(tour_number)
    for pair in pairs:
        tour(pair)
    if len(tour.get_players()) == len(players):
        tour.add_opponents()
        cr.add_text(tour)
        tour.clear()
    else:
        if tour.pick_up_pair():
            tour.add_opponents()
            cr.add_text(tour)
            tour.clear()
        else:
            pairs = [Pair(pair[0], pair[1]) for pair in itertools.combinations(players, 2)]
            random.shuffle(pairs)
            tour_number = 0
cr.print_all()
print(f'Ушедшее время на жеребьёвку {n} игроков: {time.time() - start:.2f} секунд')