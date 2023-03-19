from contextlib import redirect_stdout
import itertools as it
import os


class Ulam:
    @staticmethod
    def direction_gen():
        direction_generator = it.cycle(['right', 'up', 'left', 'down'])
        directs = direction_generator
        count = 1
        while True:
            for _ in range(2):
                direction = next(directs)
                for _ in range(count):
                    yield direction
            count += 1

    @staticmethod
    def is_prime(x :int):
        if x == 2:
            return True
        if x % 2 == 0 and x != 2:
            return False
        if x < 2:
            return False
        for i in range(3, int(x**0.5)+1, 2):
            if x % i == 0:
                return False
        return True

    def __init__(self, size :int):
        if size < 3:
            self.size = 3
        elif size % 2 == 0:
            self.size = size+1
        else:
            self.size = size
        self.matrix = self.create_matrix()

    def create_matrix(self):
        result = [[0 for i in range(self.size)] for j in range(self.size)]
        direction_gen = Ulam.direction_gen()
        height = self.size//2
        width = self.size//2
        total = 1
        number = 1
        while total <= self.size**2:
            direct = next(direction_gen)
            result[height][width] = total
            total += 1
            if direct == 'right':
                width += 1
            elif direct == 'up':
                height -= 1
            elif direct == 'left':
                width -= 1
            elif direct == 'down':
                height += 1
        return result

    def show(self, primes=False, show_lines=True, save_file=False, file_name='Ulam.txt'):
        if primes is True:
            matrix = [[element if isinstance(element, int) and Ulam.is_prime(element) else ''
                       for element in line] for line in self.matrix]
        else:
            matrix = self.matrix
        reserve = len(str(self.size**2))
        result = []
        temp = []
        for line in matrix:
            for element in line:
                temp.append(str(element).center(reserve))
                temp.append(''.center(reserve))
            result.append(temp[:-1])
            result.append([''.center(reserve) for i in range(len(temp))])
            temp = []
        result = result[:-1]
        direction_gen = Ulam.direction_gen()
        height = len(result) // 2
        width = len(result[0]) // 2
        counter = 0
        while counter != (self.size ** 2) - 1:
            direct = next(direction_gen)
            char = ''
            if show_lines is False:
                char = ''.center(reserve)
            elif direct == 'left' or direct == 'right':
                char = '—'.center(reserve)
            else:
                char = '|'.center(reserve)

            if direct == 'right':
                width += 2
                result[height][width-1] = char
            elif direct == 'up':
                height -= 2
                result[height+1][width] = char
            elif direct == 'left':
                width -= 2
                result[height][width+1] = char
            elif direct == 'down':
                height += 2
                result[height-1][width] = char
            counter += 1
        
        for line in result:
            print(*line, sep='')
        if save_file:
            file_name += '.txt'
            with open(file_name, 'w') as f:
                with redirect_stdout(f):
                    for line in result:
                        print(*line, sep='')
            print(f'\nFile path: {os.path.join(os.getcwd(), file_name)}.')


def get_int(text: str):
    result = 'x'
    while not result.isdigit():
        result = input(text)
    return int(result)


def get_y_or_n(text: str):
    """
    Ask question and expect y(es) or n(o).
    If yes return True, else False

    Args:
        text (str): Your questions
    """
    result = ''
    while result.lower() not in ('y', 'n', 'yes', 'no'):
        result = input(text)
    if result.lower() in ('y', 'yes'):
        return True
    else:
        return False
    

def main():
    size = get_int('Specify an odd spiral edge size (13 recommended): ')
    spiral = Ulam(size)
    more_options = get_y_or_n('Y(es) to more options, n(o) to show by default: ')
    if more_options:
        primes = get_y_or_n('Show ONLY prime numbers? Y/N: ')
        show_lines = get_y_or_n('Show direction lines? Y/N : ')
        save_file = get_y_or_n('Save spiral to file? Y/N')
        file_name = ''
        if save_file:
            file_name = input('Enter a file name: ')
        spiral.show(primes=primes, show_lines=show_lines, save_file=save_file, file_name=file_name)
    else:
        spiral.show()    
    input('\n\nEnter to exit...')


if __name__ == '__main__':
    main()
