import json
from pprint import pprint

alphabet_json_file = "alphabet.json"


def main():
    print alphabet_json_file
    parse_letters(alphabet_json_file)

def parse_letters(filename):
    json_data = open(filename)

    data = json.load(json_data)
    rowLength = len(data['A'][0])
    columnHeight = 5
    # for row in data['A']:
    for i in range(0, rowLength):
        for j in range(0, columnHeight):
            print data['A'][j][i]

        print ""
    json_data.close()


if __name__ == '__main__':
    main()