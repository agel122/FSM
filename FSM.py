"""let's realize FSM for 3 positions:
initial: A
from A: if value>=10: B
        else: A
from B: if value<=3: C
        else B"""


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class FSM:
    def __init__(self):
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()

        self.current_state = self.q1
        self.stopped = False

    def send(self, value):
        try:
            self.current_state.send(value)
        except StopIteration:
            self.stopped = True

    def does_match(self):
        if self.stopped:
            print('iteration stopped')
        elif self.current_state == self.q1:
            print('A')
        elif self.current_state == self.q2:
            print('B')
        elif self.current_state == self.q3:
            print('C')

    @prime
    def _create_q1(self):
        while True:
            value = yield
            if value >= 10:
                self.current_state = self.q2
            else:
                self.current_state = self.q1

    @prime
    def _create_q2(self):
        while True:
            value = yield
            if value <= 3:
                self.current_state = self.q3
            else:
                self.current_state = self.q2

    @prime
    def _create_q3(self):
        while True:
            value = yield
            break


def myfsm(values):
    evaluator = FSM()
    for value in values:
        evaluator.send(value)
    return evaluator.does_match()


list1 = [10, 3]
myfsm(list1)
list2 = [2, 3]
myfsm(list2)
list3 = [12, 5, 5]
myfsm(list3)
list4 = [10, 3, 3, 3]
myfsm(list4)

