
import sys
import csv
import re


def main():
    table_counter = 0
    index = 0
    string = ''
    first_traversal = True
    output = []
    printer = csv.writer(sys.stdout)

    for line in sys.stdin:
        line = line.replace('\n', '')
        string += line

    table_match = re.findall('<\s*table.*?>.*?<\s*/\s*table\s*>', string, re.IGNORECASE)
    for tables in table_match:
        first_traversal = True
        table_counter += 1
        cell_number = 0
        print(f'TABLE {table_counter}:')
        row_match = re.findall('<\s*tr.*?>.*?<\s*/tr\s*>', tables)
        for rows in row_match:
            header_match = re.findall('<\s*th.*?>.*?<\s*/th\s*>', rows)
            if header_match:
                for headers in header_match:

                    if first_traversal:
                        cell_number += 1

                    front = re.search('<\s*th.*?>\s*.', headers)
                    back = re.search('\s*<\s*/\s*th\s*>?', headers)
                    result = headers[len(front.group())-1:-len(back.group())]
                    cell_result = re.sub('\s\s+', ' ', result)

                    output.append(cell_result)

                printer.writerow(output)
                output = []
                first_traversal = False

            cell_match = re.findall('<\s*td.*?>.*?<\s*/td\s*>', rows)
            if cell_match:
                for cells in cell_match:

                    if first_traversal:
                        cell_number += 1

                    front = re.search('<\s*td.*?>\s*.', cells)

                    back = re.search('\s*<\s*/\s*td\s*>?', cells)

                    result = cells[len(front.group())-1:-len(back.group())]
                    cell_result = re.sub('\s\s+', ' ', result)

                    output.append(cell_result.strip(' '))

                if first_traversal:
                    first_traversal = False

                if len(output) <= cell_number:
                    cell_index = len(output)
                    while(cell_index <= cell_number):
                        cell_index += 1
                        output.append('')

                printer.writerow(output)
                output = []

        print('\n')

    if table_counter == 0:
        sys.stderr = open('6.err', 'w')
        sys.stderr.write(f"Error: File does not contain any tables\n")
        sys.exit(6)

if __name__ == '__main__':
    main()
