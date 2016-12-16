import fileinput
import re
import spreadsheet_functions

# '^' is the field separator for the MSR100 .
FIRST_AND_LAST_NAME = re.compile(r'(?<=\^)[A-Z ,\.\'-]+')

names = [string.lower() for string in spreadsheet_functions.get_names()]

class ParseException(Exception):
    pass

def index_of(list, item):
    try:
        return list.index(item)
    except ValueError:
        return -1

def parse(line):
    matches = FIRST_AND_LAST_NAME.findall(line)
    if not matches:
        raise ParseException
    # Grab the last group. There may be useless matches before the end.
    name = matches[-1]
    # drop final initial, which is for middle name
    first_and_last = name.split()[0] + " " + name.split()[1]
    # Convert to lower case.
    formatted_name = first_and_last.lower()
    return formatted_name

def process(line):
    try:
        name = parse(line)
    except ParseException:
        print 'CARD READ ERROR'
    else:
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
