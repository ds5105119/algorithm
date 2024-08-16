from sys import stdin
import re
code = [chr(97 + i) + " = 0\n" for i in range(26)]
tab = 0


def _re_multiple(m):
    m = m.group()
    return m[0] + ' * ' + m[1]


def re_multiple(s):
    while s != re.sub('[0-9][a-z]', _re_multiple, s):
        s = re.sub('[0-9][a-z]', _re_multiple, s)
    return s


command = stdin.readline()
if "BEGIN" in command:
    tab += 1

while tab:
    command = stdin.readline().strip()
    cc = 0

    if "STOP" in command:
        command = 'pass' if "REPEAT" in code[-1] else ''
        cc -= 1
    elif "REPEAT" in command:
        command = "for a" + chr(96 + tab) + " in range(" + command[7:] + "):"
        cc += 1
    elif "PRINT" in command:
        command = 'print("' + command[6:] + ' = " + ' + 'str(int(' + command[6:] + ') % 10000))'
    else:
        command = re_multiple(command)
        command = command.split(' = ')
        command = command[0] + ' = int(' + command[1] + ') % 10000'

    code.append('    ' * (tab - 1) + command + '\n')
    tab += cc

print(''.join(code))
exec(''.join(code))