import fileinput
import re
import spreadsheet_functions

"""
We need to
1. read first & last name from scanned card.
2. Locate row in google sheet that contains this name, ignoring case in format `<first-name>, <last-name>`.
3. Update column L of the spreadsheet to record that the user is signed in.
"""

FIRST_AND_LAST_NAME = re.compile(r'[A-Z ,\.\'-]+')

print spreadsheet_functions.get_names()
names = [string.lower() for string in spreadsheet_functions.get_names()]

def index_of(list, item):
    try:
        return list.index(item)
    except ValueError:
        return -1

def process(line):
        matches = FIRST_AND_LAST_NAME.findall(line)
        # Grab the last group. There may be useless matches before the end.
        name = matches[-1]
        # drop final initial, which is for middle name
        first_and_last = name.split()[0] + " " + name.split()[1]
        # Convert to lower case.
        formatted_name = first_and_last.lower()
        index = index_of(names, formatted_name)
        if index == -1:
            print 'Name %s is not registered.' % name
        else:
            spreadsheet_functions.check_attendance(index)
            print 'Name %s is registered.' % name
        return name

def test():
        data = r'%123478912347^892^^^2357892351^BEACH, ELLIOTT T?'
        assert process(data) == 'BEACH, ELLIOTT T'
        data = r'%123478912347^892^^^2357892351^AI, HA L'
        assert process(data) == 'AI, HA L'

def main():
        for line in fileinput.input():
                print process(line)

test()
main()
