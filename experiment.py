from functools import reduce

from datetime import datetime

from dateutil import relativedelta
from functional import seq


def read_data():
    with open('fakereal.txt') as f:
        return f.read().splitlines()


def get_individual_heartrate(all_data):
    return (int(l) for l in all_data)


def accumulate_immutable(acc, current):
    return [acc[0] + 1,  *acc[1:]] if current > 0 else [0,  *acc[0:]]


def accumulate_mutable(acc, current):
    if current > 0:
        acc[-1] = acc[-1] + 1
        return acc
    else:
        acc.append(0)
        return acc


def is_mvpa_minute(mvpa_threshold):
    return lambda heart_rate: 1 if heart_rate > mvpa_threshold else 0


def get_result_with_py_functional():
    return seq(get_individual_heartrate(read_data())) \
        .map(lambda heart_rate: is_mvpa_minute(mvpa_threshold=119)(heart_rate)) \
        .reduce(accumulate_mutable, [0, 0]) \
        .reduce(lambda acc, current: acc + current if current > 10 else acc, 0)


def get_result_with_functools():
    return reduce(
        lambda acc, current: acc + current if current > 10 else acc,
        reduce(
            lambda acc, current: [acc[0] + 1,  *acc[1:]] if current > 0 else [0,  *acc[0:]],
            map(is_mvpa_minute(mvpa_threshold=5),  get_individual_heartrate(read_data())),
            [0, 0]),
        0
    )


if __name__ == '__main__':
    start = datetime.now()
    result = get_result_with_py_functional()
    end = datetime.now()
    time_taken = relativedelta.relativedelta(end, start)
    print('Result is ', result, ' with processing time ', time_taken)

