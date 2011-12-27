## Copyright (c) 2011 Pablo Ariel Duboue <pablo.duboue@gmail.com>

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the
## "Software"), to deal in the Software without restriction, including
## without limitation the rights to use, copy, modify, merge, publish,
## distribute, sublicense, and/or sell copies of the Software, and to
## permit persons to whom the Software is furnished to do so, subject to
## the following conditions:

## The above copyright notice and this permission notice shall be
## included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
## EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
## MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
## NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
## OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
## WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description='Transform a hash into a name.')
    parser.add_argument('--datafolder', nargs='?', default='.',
                       help='data folder (default: current folder)')
    parser.add_argument('hash', metavar='HASH', help='hash to verbalize or name to parse')
    parser.add_argument('--parse', nargs='?', default=False, const=True, help='whether to parse the name')

    args = parser.parse_args()

    colors = open(args.datafolder + "/colors.list").readlines()
    animals = open(args.datafolder + "/animals.list").readlines()
    locations = open(args.datafolder + "/locations.list").readlines()

    if args.parse:
        colors_idx = dict()
        animals_idx = dict()
        locations_idx = dict()
        for idx, lists in [(colors_idx, colors), (animals_idx, animals), (locations_idx, locations)]:
            for i in xrange(len(lists)):
                lists[i] = str.lower(str.rstrip(lists[i]))
                idx[lists[i]] = i
            
        name = re.sub('-', ' ', args.hash)
        from_pos = str.find(name, ' from ')
        value = 0
        if from_pos == -1:
            # no location, no number
            animal_color = re.split(' ', name)
            if len(animal_color) == 1:
                value = animals_idx[str.lower(animal_color[0])]
            else:
                value = animals_idx[str.lower(animal_color[1])] + colors_idx[str.lower(animal_color[0])] * len(animals)
        else:
            parts = re.split(' from ', name)
            animal_color = re.split(' ', parts[0])
            value = animals_idx[str.lower(animal_color[1])] + colors_idx[str.lower(animal_color[0])] * len(animals)
            if len(animal_color) > 2:
                # leftover
                value += int(animal_color[2][1:]) * len(colors) * len(animals) * len(locations)
            # location
            value += locations_idx[str.lower(parts[1])] * len(colors) * len(animals)
        print hex(value)[2:]
                
    else:
        number = int(args.hash, 16)
        animal = number % len(animals)
        number = number / len(animals)
        if number == 0:
            print str.capitalize(str.rstrip(animals[animal]))
            sys.exit()

        color = number % len(colors)
        number = number / len(colors)
        if number == 0:
            print '-'.join((str.capitalize(str.rstrip(colors[color])),
                            str.capitalize(str.rstrip(animals[animal]))))
            sys.exit()

        location = number % len(locations)
        number = number / len(locations)

        if number == 0:
            print '-'.join((str.capitalize(str.rstrip(colors[color])),
                            str.capitalize(str.rstrip(animals[animal])),
                            "from",
                            re.sub(' ', '-', str.capitalize(locations[location]))))
            sys.exit()

        print '-'.join((str.capitalize(str.rstrip(colors[color])),
                        str.capitalize(str.rstrip(animals[animal])),
                        '#' + str(number),
                        "from",
                        str.capitalize(re.sub(' ', '-', locations[location]))))

if __name__ == '__main__':
    main()
