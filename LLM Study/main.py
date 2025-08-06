import random
from processing import *


# generates an output file based on data connections
def generate(destFilename, model, numChars, initial):

    with open(destFilename, 'w') as file:
        nGram = initial
        print("inital: ", initial)
        file.write(initial)
        chars = len(initial)
        nextChar = None
        # checks that there is a proper character as nextChar
        while nextChar != '' and chars < numChars:
            total = sum(model[nGram].values())
            print("total: ", total)
            keysList = [k for k in model[nGram].keys()]
            weight = [value / total for value in model[nGram].values()]

            # chooses a nextChar based on random probability
            nextChar = ''.join(random.choices(keysList, weight))

            file.write(nextChar)
            chars += 1
            nGram = nGram[1:] + nextChar



#        print(nGram)
        return chars

if __name__ == '__main__':

    from string import ascii_uppercase

    n = 0
    while n <= 0:
        try:
            n = int(input("What value of n for n-grams? "))
            if n <= 0:
                print("Must choose positive n")
        except ValueError:
            print("Invalid integer")

    src = None
    while not src:
        filename = input("Input filename? ")
        try:
            fp = open(filename)
            initial = fp.read(n)
            fp.close()
            src = filename
        except IOError:
            print("Unable to read file \'", filename, "\', use format: root/fileName.txt")

    default = filename.split('/')[-1].split('.')[0] + '_' + str(n) + '.txt'
    output = None
    while not output:
        filename = input("Output filename? [default: %s] " % default)
        if not filename:
            filename = default
        try:
            fp = open(filename, 'w')
            fp.close()
            output = filename
        except IOError:
            print("Unable to write to file", filename)

    total = 0
    while not 0 < total:
        try:
            total = int(input("How many characters of output are desired? "))
            if total <= 0:
                print("Must choose positive value")
        except ValueError:
            print("Invalid integer")

    seed = None
    seed = input("Randomization Seed [press enter for random seed]: ").strip()
    if not seed:
        seed = ''.join(random.choice(ascii_uppercase) for _ in range(6))
        print('Using seed:', seed)
    random.seed(seed)

    model = preprocess(src, n)
    print("this: ", model['Aes'])
    c = generate(output, model, total, initial)
    print(f'Generated {c} characters of output')
