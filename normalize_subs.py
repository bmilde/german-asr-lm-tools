#import normalisierung
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True)
parser.add_argument('-o', '--output', required=True)
args = parser.parse_args()
input_file = args.file
output_file = args.output

sent_write = True

i = 0

with open(input_file) as in_file, open(output_file, 'w') as out_file:
    sent = []
    line_length = 0
    for line in in_file:
        if line[-1] == '\n':
            line = line[:-1]

        line = line.strip()

        if len(line) == 0:
            print('Warning, empty line!')
            continue
        if line.lower() == 'keine ut':
            continue
        if line[-1] == '*':
            continue
        if line[0] == '#' or line[0]=='-' or line[0] == '♪':
            continue
        if (line[0]=='(' and line[-1] == ')') or (line[0]=='"' and line[-1] == '"') or (line[0]=="'" and line[-1] == "'"):
            line = line[1:-1]
       
        line = line.replace('<FONT COLOR="Yellow">', ' ').replace('<FONT COLOR="White">',' ').replace('<FONT COLOR="Red">',' ')
     
        if len(line) == 0:
            print('Warning, empty line!')
            continue

        line = line.strip()

        if sent_write:
            if not (line[-1] == '.' or line[-1] == '!' or line[-1] == '?'):
                line_length += 1
                
                sent += [line]
            else:
                sent += [line]

                out_str = ' '.join(sent)
                if i % 1000000 == 0:
                    print(i,sent)
                out_file.write(out_str + '\n')
                line_length = 0
                sent = []
        else:
            #print(line)
            out_file.write(line + '\n')

        if sent_write and line_length > 10:
            print('Warning, line length overflow:', sent)
            sent = []
            line_length = 0

        i += 1
