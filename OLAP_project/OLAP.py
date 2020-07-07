#!/usr/bin/env python3

import argparse
import os
import sys
import csv

##top k function, took a while to figure it out the first time
def top(in_file, k_value, field):
    with open(in_file, mode = 'r', encoding = 'utf-8-sig') as file:
        data = csv.DictReader(file)
        dictionary = {}
        duplicates = {}

        line_value = 0
        distinct = 0
        error_value = 0

        for line in data:
            line_value = line_value + 1

            if distinct > 20:
                sys.stderr = ('n.err', 'w')
                sys.stderr.write(f'ERROR: {in_file}: {field} has been capped at 20 distinct values\n')
                sys.stderr.write(f'{field}_capped\n')
                sys.exit('n')


            if distinct <= 20:
                if line[field] not in dictionary:
                    dictionary[line[field]] = 1
                    distinct = distinct + 1

                if line[field] in dictionary:
                    dictionary[line[field]] += 1

        keys = list(dictionary.keys())
        values = list(dictionary.values())

        for x in range(int(k_value)):
            if int(k_value) > 20:
                sys.stderr = open('6.err', 'w')
                sys.stderr.write(f"Error: program can only handle up to 20 distinct values\n")
                sys.exit(6)
            if values != []:
                max_value = keys[values.index(max(values))]
                duplicates[max_value] = max(values)
                values.remove(max(values))
                keys.remove(max_value)
            else:
                continue
    return duplicates

##Created a class that stores the values into an array based ont the order
## of calls
order = []

class order_dictionary(argparse.Action):
    def __call__(self, parser, args, value, option_string = None):

        if self.dest == 'max_result':
            if args.max_result == None:
                args.max_result = []

            args.max_result.append(value)

        if self.dest == 'min_result':
            if args.min_result == None:
                args.min_result = []

            args.min_result.append(value)

        if self.dest == 'mean_result':
            if args.mean_result == None:
                args.mean_result = []

            args.mean_result.append(value)

        if self.dest == 'sum_field':
            if args.sum_field == None:
                args.sum_field = []

            args.sum_field.append(value)

        if self.dest == 'count':
            if args.count != True:
                args.count = True

            order.append(value)
            return

        if self.dest != 'sum_field':
            path = self.dest.strip('result')
            order.append(f'{path}{value}')


        if self.dest == 'sum_field':
            path = self.dest.strip('field')
            order.append(f'{path}{value}')

##the use of argparse for each specific calls
def main():
    parser = argparse.ArgumentParser(description = 'Compute the values on certain methods')
    parser.add_argument('--input', dest = 'input', required = True, help = 'input file to parse')
    parser.add_argument('--top', nargs = 2, dest = 'top', help = 'gets the most common value')
    parser.add_argument('--max', action = order_dictionary, dest = 'max_result', help = 'gets the largest value' )
    parser.add_argument('--min', action = order_dictionary, dest = 'min_result', help = 'gets the smallest value')
    parser.add_argument('--mean', action = order_dictionary, dest = 'mean_result', help = 'gets the mean of all the values')
    parser.add_argument('--sum', action = order_dictionary, dest = 'sum_field', help = 'sum the integers')
    parser.add_argument('--count', action = order_dictionary, dest = 'count', help = 'counts the number of records')
    parser.add_argument('--group-by', dest = 'group', help = 'groups the column' )
    args = parser.parse_args()


    with open(args.input, 'r', encoding = 'utf-8-sig') as file:
        data = csv.DictReader(file)
        group_distinct_values = 0
        top_distinct_values = 0
        main_dictionary = {}
        max_error_value = 0
        min_error_value = 0
        sum_error_value = 0
        mean_error_value = 0
        group_error_value = 0
        top_error_value = 0
        value = 0
        overflow = {}
        temp = {}
        max_value = 0
        total = 0
        max_line_value = 0
        min_line_value = 0
        top_line_value = 0
        count_line_value = 0
        sum_line_value = 0
        mean_line_value = 0
        group_line_value = 0
        mean_total_value = 0
        mean_result = 0
        max_counter = 0
        argument_flag = False

        if args.group == None:
            main_dictionary['UNGROUPED'] = {}

##In one traversal, the program will check every functions that are called
##.......except for top k (without group-by)
##The way I handle errors is outputing an error file with stderr message
        for line in data:
            count_line_value += 1

            if args.group == None:
                main_dictionary['UNGROUPED'][f'count'] = count_line_value

            if args.group != None:
                argument_flag = True

                if group_distinct_values > 20:
                    sys.stderr = open('n.err', 'w')
                    main_dictionary["_OTHER"] = {}
                    main_dictionary["_OTHER"][f'count'] = 0
                    value = line[args.group]
                    sys.stderr.write(f'ERROR: {args.input}: {args.group} has been capped at 20 distinct values for {value}\n')
                    sys.stderr.write(f'ERROR: {args.input} group-by argument has high cardinality')
                    break

                if group_distinct_values <= 20:
                    try:
                        if line[args.group] not in main_dictionary:

                            main_dictionary[line[args.group]] = {}
                            main_dictionary[line[args.group]][f'count'] = 0
                            group_distinct_values = group_distinct_values + 1

                        if line[args.group] in main_dictionary:
                            main_dictionary[line[args.group]][f'count'] += 1

                    except KeyError:
                        sys.stderr = open('9.err', 'w')
                        sys.stderr.write(f"ERROR: {args.input}: no group-by argument with name '{args.group}' found\n")
                        sys.exit(9)

            if args.max_result:
                argument_flag = True
                if args.group == None:
                    max_line_value += 1
                    for group in args.max_result:
                        current_value = line[group]
                        try:
                            current_value = float(line[group])
                            if f'max_{group}' in main_dictionary['UNGROUPED']:
                                if current_value > main_dictionary['UNGROUPED'][f'max_{group}']:
                                    main_dictionary['UNGROUPED'][f'max_{group}'] = current_value

                            else:
                                main_dictionary['UNGROUPED'][f'max_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            if max_error_value <= 100:
                                max_error_value += 1
                                main_dictionary['UNGROUPED'][f'max_{group}'] = 'NaN'
                                sys.stderr.write(f"Error: {args.input}: {max_line_value} can't compute non-numeric value '{current_value}'\n")

                                if max_error_value > 100:
                                    sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {group}\n")
                                    sys.exit(7)

                if args.group != None:
                    for group in args.max_result:
                        group.lower()
                        current_value = line[group]
                        max_line_value += 1

                        try:
                            current_value = float(line[group])
                            if f'max_{group}' in main_dictionary[line[args.group]]:
                                if current_value > main_dictionary[line[args.group]][f'max_{group}']:
                                    main_dictionary[line[args.group]][f'max_{group}'] = current_value

                            elif line[args.group] in main_dictionary:
                                main_dictionary[line[args.group]][f'max_{group}'] = current_value

                            else:
                                main_dictionary[line[args.group]][f'max_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            if max_error_value <= 100:
                                max_error_value += 1
                                sys.stderr.write(f"Error: {args.input}: {max_line_value} can't compute non-numeric value '{current_value}'\n")
                                main_dictionary[line[args.group]][f'max_{group}'] = 'NaN'

                            if max_error_value > 100:
                                sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {group}\n")
                                sys.exit(7)


            if args.min_result:
                argument_flag = True
                if args.group == None:
                    min_line_value += 1
                    for group in args.min_result:
                        current_value = line[group]
                        try:
                            current_value = float(line[group])
                            if f'min_{group}' in main_dictionary['UNGROUPED']:
                                if current_value < main_dictionary['UNGROUPED'][f'min_{group}']:
                                    main_dictionary['UNGROUPED'][f'min_{group}'] = current_value

                            else:
                                main_dictionary['UNGROUPED'][f'min_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            if min_error_value <= 100:
                                min_error_value += 1
                                main_dictionary['UNGROUPED'][f'min_{group}'] = 'NaN'
                                sys.stderr.write(f"Error: {args.input}: {min_line_value} can't compute non-numeric value '{current_value}'\n")

                                if min_error_value > 100:
                                    sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {group}\n")
                                    sys.exit(7)

                if args.group != None:
                    for group in args.min_result:
                        group.lower()
                        current_value = line[group]
                        min_line_value += 1

                        try:
                            current_value = float(line[group])
                            if f'min_{group}' in main_dictionary[line[args.group]]:
                                if current_value < main_dictionary[line[args.group]][f'min_{group}']:
                                    main_dictionary[line[args.group]][f'min_{group}'] = current_value

                            elif line[args.group] in main_dictionary:
                                main_dictionary[line[args.group]][f'min_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            if min_error_value <= 100:
                                min_error_value += 1
                                sys.stderr.write(f"Error: {args.input}: {min_line_value} can't compute non-numeric value '{current_value}'\n")
                                main_dictionary[line[args.group]][f'min_{group}'] = 'NaN'

                            if min_error_value > 100:
                                sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {group}\n")
                                sys.exit(7)

            if args.mean_result:
                argument_flag = True
                for group in args.mean_result:
                    if args.sum_field != None:
                        if group not in args.sum_field:
                            args.sum_field.append(group)
                    else:
                        args.sum_field = []
                        args.sum_field.append(group)

            if args.sum_field:
                argument_flag = True
                if args.group == None:
                    for group in args.sum_field:
                        group.lower()
                        sum_line_value += 1
                        current_value = line[group]
                        try:
                            current_value = float(line[group])
                            if f'sum_{group}' in main_dictionary['UNGROUPED']:
                                main_dictionary['UNGROUPED'][f'sum_{group}'] += current_value

                            else:
                                main_dictionary['UNGROUPED'][f'sum_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            sum_error_value += 1
                            main_dictionary['UNGROUPED'][f'sum_{group}'] = 'NaN'
                            sys.stderr.write(f"Error: {args.input}: {sum_line_value} can't compute non-numeric value '{current_value}'\n")

                            if sum_error_value >= 100:
                                sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {args.sum_field[sum_call_count]}\n")
                                sys.exit(7)

                if args.group != None:
                    for group in args.sum_field:
                        sum_line_value += 1
                        group.lower()
                        current_value = line[group]
                        #print(current_value)
                        try:
                            current_value = float(line[group])
                            if f'sum_{group}' in main_dictionary[line[args.group]]:
                                main_dictionary[line[args.group]][f'sum_{group}'] += current_value

                            elif f'sum_{group}' in main_dictionary[line[args.group]]:
                                main_dictionary[line[args.group]][f'sum_{group}'] = current_value

                            else:
                                main_dictionary[line[args.group]][f'sum_{group}'] = current_value

                        except ValueError:
                            sys.stderr = open('7.err', 'w')
                            sum_error_value += 1
                            main_dictionary['UNGROUPED'][f'sum_{group}'] = 'NaN'
                            sys.stderr.write(f"Error: {args.input}: {sum_line_value} can't compute non-numeric value '{current_value}'\n")

                            if sum_error_value >= 100:
                                sys.stderr.write(f"Error: {args.input}: more than than 100 non-numeric values found in aggregate column {args.sum_field[sum_call_count]}\n")
                                sys.exit(7)


            if args.count:
                argument_flag = True
                if args.group == None:
                    main_dictionary['UNGROUPED'][f'count'] = count_line_value
                if args.group != None:
                    main_dictionary[line[args.group]][f'count'] == count_line_value

            if args.top:
                argument_flag = True
                if args.group != None:
                        current_value = line[args.top[1]]
                        if top_distinct_values <= 20:
                            if f'top_{args.top[1]}' not in main_dictionary[line[args.group]]:
                                main_dictionary[line[args.group]][f'top_{args.top[1]}'] = {}
                            if current_value not in main_dictionary[line[args.group]][f'top_{args.top[1]}']:
                                main_dictionary[line[args.group]][f'top_{args.top[1]}'][current_value] = 1
                                top_distinct_values += 1
                            else:
                                main_dictionary[line[args.group]][f'top_{args.top[1]}'][current_value] += 1

                        if top_distinct_values > 20:
                            sys.stderr.write(f'ERROR: {in_file}: {field} has been capped at 20 distinct values\n')
                            sys.stderr.write(f'{field}_capped\n')


        if args.top:
            argument_flag = True
            if args.group == None:
                top_value = top(args.input, args.top[0], args.top[1])


            if args.group != None:
                for each in main_dictionary:
                    keys = list(main_dictionary[each][f'top_{args.top[1]}'].keys())
                    values = list(main_dictionary[each][f'top_{args.top[1]}'].values())
                    main_dictionary[each][f'top_{args.top[1]}'] = {}
                    for x in range(int(args.top[0])):

                        if int(args.top[0]) > 20:
                            sys.stderr = open('6.err', 'w')
                            sys.stderr.write(f"Error: program can only handle up to 20 values\n")
                            sys.exit(6)
                        if values != []:
                            max_value = keys[values.index(max(values))]
                            main_dictionary[each][f'top_{args.top[1]}'][max_value] = max(values)
                            values.remove(max(values))
                            keys.remove(max_value)
                        else:
                            continue



        for group in main_dictionary:
            if args.mean_result != None:
                if args.group != None:
                    for mean_field in args.mean_result:
                        main_dictionary[group][f'mean_{mean_field}'] = main_dictionary[group][f'sum_{mean_field}'] / main_dictionary[group][f'count']

                else:
                    for mean_field in args.mean_result:
                        main_dictionary['UNGROUPED'][f'mean_{mean_field}'] = main_dictionary['UNGROUPED'][f'sum_{mean_field}'] / main_dictionary['UNGROUPED'][f'count']


##Outputing the dictionary into print statements
        printer = csv.writer(sys.stdout)
        headers = []

        if argument_flag == False:
            array_result= []
            headers.append('count')
            array_result.append(main_dictionary['UNGROUPED']['count'])
            printer.writerow(headers)
            printer.writerow(array_result)

        if argument_flag == True:
            if args.group:
               headers.append(args.group)
               if args.top == None:
                   headers.append('count')

            if args.top:
                headers.append(f'top_{args.top[1].lower()}')

            for each in order:
                headers.append(each.lower())
            printer.writerow(headers)

            for group in main_dictionary:
                array_result = []

                if args.group:
                    array_result.append(group)
                    if args.top == None:
                        array_result.append(main_dictionary[group]['count'])

                for each in order:
                    array_result.append(main_dictionary[group][each])

                if args.top:
                    value = ""
                    if args.group != None:
                        for item in main_dictionary[group][f'top_{args.top[1]}']:
                            value = f'{item}:{main_dictionary[group][f"top_{args.top[1]}"][item]}, '
                            value = value.strip(", ")
                            array_result.append(value)

                    if args.group == None:
                        value = ""
                        for item in top_value:
                            value = f'{item}: {top_value[item]}, '
                            value = value.strip(", ")
                            array_result.append(value)
                printer.writerow(array_result)


if __name__ == '__main__':
    main()
