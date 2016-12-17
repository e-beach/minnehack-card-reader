import fileinput
import re
import spreadsheet_functions

# '^' is the field separator for the MSR100 .
FIRST_AND_LAST_NAME = re.compile(r'(?<=\^)[A-Z ,\.\'-]+')

registered_names = [string.upper() for string in spreadsheet_functions.get_names()]

class ParseException(Exception):
    pass

def index_of(list, item):
    """Take a list and item and return -1 if item is not in collection , else the index of that item"""
    try:
        return list.index(item)
    except ValueError:
        return -1

def parse(line):
    """ Extract <FIRST-NAME, LAST-NAME> from card input """
    matches = FIRST_AND_LAST_NAME.findall(line)
    if not matches:
        raise ParseException
    # Grab the last group. There may be useless matches before the end.
    name = matches[-1]
    # Drop final initial, which is for middle name.
    if index_of(name, ',') != -1:
        # UMN ID
        first_and_last = name.split()[0] + " " + name.split()[1]
    else:
        # Driver's license
        first_and_last = name.split()[2] + ", " + name.split()[0]
    # Convert to upper case.
    formatted_name = first_and_last.upper()
    return formatted_name

def process(line):
    """Take a line of card input, display whether encoded name is registered. If name is registered, mark that they have attended event."""
    try:
        name = parse(line)
    except ParseException:
        print 'CARD READ ERROR'
    else:
        index = index_of(registered_names, name)
        if index == -1:
            print 'Name %s is not registered.' % name
        else:
            spreadsheet_functions.check_attendance(index)
            print 'Name %s is registered.' % name
        return name

def test():
    """Given some spoofed input data, check that we can detect who is registered """
    data = r'%123478912347^892^^^2357892351^BEACH, ELLIOTT T?'
    assert process(data) == 'BEACH, ELLIOTT'
    data = r'%123478912347^892^^^2357892351^AI, HA L'
    assert process(data) == 'AI, HA'

def main():
    """ Read lines of card data """
    while True:
        print ">>>"
        process( raw_input() )

test()
main()
