import PatternMatch
import random
from matplotlib import pyplot as plt
from time import sleep
def cold_start():

    score = [[random.randint(0,30)] for i in range(60)]

    jump = score[int(len(score)/2):]
    # jump = score[5:]

    obj = PatternMatch.MEDBuffer(score,plot=True)

    calls = [obj.add_note(i) for i in jump]
    print(calls)
    sleep(10)
    obj.close_live_view()


def missed_notes():
    score = [[random.randint(0,30)] for i in range(30)]

    jump = score.copy()

    [jump.pop(5) for i in range(5)]

    print(jump)
    print(score)

    obj = PatternMatch.MEDBuffer(score)

    calls = [obj.add_note(i) for i in jump]

    obj.view_table()
    print(calls)
    plt.figure()
    plt.plot(calls, ".k")
    plt.xlabel("Interpreted Note Sequence Number")
    plt.ylabel("Matched Score Note Sequence Number")
    plt.show()


def extra_notes():
    score = [[random.randint(0, 30)] for i in range(30)]

    jump = score.copy()

    [jump.insert(5,[random.randint(0,30)]) for i in range(5)]

    print(jump)
    print(score)

    obj = PatternMatch.MEDBuffer(score)

    calls = [obj.add_note(i) for i in jump]

    obj.view_table()
    print(calls)
    plt.figure()
    plt.plot(calls, ".k")
    plt.xlabel("Interpreted Note Sequence Number")
    plt.ylabel("Matched Score Note Sequence Number")
    plt.show()



if __name__ == "__main__":
    cold_start()
    missed_notes()
    extra_notes()
