import random

def get_move_time(random_value):
        if random_value == '10 min':
            return random.uniform(0.5, 7.5)
        elif random_value == '15 | 10':
            return random.uniform(6.5, 20.5)
        elif random_value == '20 min':
            return random.uniform(5.3, 18.4)
        elif random_value == '30 min':
            return random.uniform(8.2, 22.8)
        elif random_value == '60 min':
            return random.uniform(15.6, 27.4)
        elif random_value == '10 | 5':
            return random.uniform(3.8, 10.4)

        elif random_value == '3 min':
            return random.uniform(0.3, 3.5)
        elif random_value == '5 min':
            return random.uniform(0.5, 4.3)
        elif random_value == '5 | 5':
            return random.uniform(0.7, 3.9)
        elif random_value == '5 | 2':
            return random.uniform(0.6, 3.3)
        elif random_value == '3 | 2':
            return random.uniform(0.2, 2.9)

        elif random_value == '30 sec':
            return random.uniform(0.1, 0.3)
        elif random_value == '20 sec | 1':
            return random.uniform(0.1, 0.9)
        elif random_value == '1 min':
            return random.uniform(0.1, 0.9)
        elif random_value == '1 | 1':
            return random.uniform(0.1, 1.3)
        elif random_value == '2 | 1':
            return random.uniform(0.1, 1.3)
        else:
            return random.uniform(0.1, 1)
        

rn = get_move_time('1 min')
print(rn)