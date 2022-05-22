import TextParser
import R_O
#version 0.4
def main():
    R_O.start_message()
    while True:
        temp = TextParser.parse()
        if temp[0] == '#':
            R_O.pront(temp[1:])
        else:
            if len(temp) == 1:
                R_O.verb_id_dict[temp[0]].execute()
            elif len(temp) == 2:
                R_O.verb_id_dict[temp[0]].execute(temp[1])
            elif len(temp) == 3:
                R_O.verb_id_dict[temp[0]].execute(temp[1], temp[2])

        print()

if __name__ == "__main__":
    main()
