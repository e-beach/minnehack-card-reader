import fileinput
import re
import spreadsheet_functions

FIRST_AND_LAST_NAME = re.compile(r'[A-Z ,\.\'-]+')

names = [string.lower() for string in spreadsheet_functions.get_names()]

def index_of(list, item):
    try:
        return list.index(item)
    except ValueError:
        return -1

def parse(line):
    matches = FIRST_AND_LAST_NAME.findall(line)
    # Grab the last group. There may be useless matches before the end.
    name = matches[-1]
    # drop final initial, which is for middle name
    first_and_last = name.split()[0] + " " + name.split()[1]
    # Convert to lower case.
    formatted_name = first_and_last.lower()
    return formatted_name

def process(line):
    name = parse(line)
    index = index_of(names, name)
    if index == -1:
        print 'Name %s is not registered.' % name
    else:
        spreadsheet_functions.check_attendance(index)
        print 'Name %s is registered.' % name
    return name

def test():
        data = r'%123478912347^892^^^2357892351^BEACH, ELLIOTT T?'
        assert process(data) == 'beach, elliott'
        data = r'%123478912347^892^^^2357892351^AI, HA L'
        assert process(data) == 'ai, ha'

def main():
        while True:
            print ">>>"
            process( raw_input() )

test()
main()
