from functools import reduce


def read_data():
    with open('fake.txt') as f:
        return f.read().splitlines()


def get_individual_heartrate(all_data):
    return (int(l) for l in all_data)


if __name__ == '__main__':
    result = \
        reduce(
            lambda acc, current: acc + current if current > 10 else acc,
            reduce(
                lambda acc, current: [acc[0] + 1,  *acc[1:]] if current > 0 else [0,  *acc[0:]],
                map(lambda hr: 1 if hr > 5 else 0,  get_individual_heartrate(read_data())),
                [0, 0]),
            0
        )

    print(result)