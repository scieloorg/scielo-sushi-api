import argparse
import json


def extract_data(file_data):
    v = [] 
    for i in file_data.get('Item_ID'):
        ivalue = i.get('Value') 
        v.append(ivalue) 
    vkey = '-'.join(sorted(v)) 
     
    p = [] 
    for x in file_data.get('Performance'):
        pi = x.get('Instance').get('Count') 
        p.append(pi) 
    return (vkey, p)


def create_dict(report):
    td = {}
    for i in report['Report_Items']:
        k, v = extract_data(i)
        if k in td:
            print(k)
        else:
            td[k] = v
    return td


def compare(report1, report2, print_mode=0):
    t1d = create_dict(report1)
    t2d = create_dict(report2)

    total_keys_t1d = len(t1d.keys())
    total_keys_t2d = len(t2d.keys())
    print('Chaves: %d vs %d' % (total_keys_t1d, total_keys_t2d))

    diff_values_countage = 0
    diff_values = []
    equal_values_countage = 0
    for k, v in t1d.items():
        if v == t2d[k]:
            equal_values_countage += 1
        if v != t2d[k]:
            diff_values_countage += 1
            diff_values.append((k, v, t2d[k]))

    try:
        print('Valores iguais: %d (%.2f %%)' %(equal_values_countage, equal_values_countage/total_keys_t1d * 100))
        print('Valores distintos: %d (%.2f %%)' % (diff_values_countage, diff_values_countage/total_keys_t1d * 100))
    except ZeroDivisionError:
        print('N/A')

    sum_v1_diffs = 0
    total_r1_v1 = 0
    total_r2_v1 = 0

    sum_v2_diffs = 0
    total_r1_v2 = 0
    total_r2_v2 = 0

    if print_mode > 0:
        if print_mode > 1:
            if diff_values:
                print('issn\tr1_v1\tr2_v1\tdiff\tdiff_percent')

        for i in diff_values:
            issn = i[0]
            r1_v1 = int(i[1][0])
            r1_v2 = int(i[1][1])

            r2_v1 = int(i[2][0])
            r2_v2 = int(i[2][1])

            v1_diff = r1_v1 - r2_v1
            v1_diff_percent = float(v1_diff/r1_v1) * 100

            v2_diff = r1_v2 - r2_v2
            v2_diff_percent = float(v2_diff/r1_v2) * 100

            if print_mode > 1:
                print('%s\t%d\t%d\t%d\t%.2f%%' % (issn, r1_v1, r2_v2, r1_v1 - r2_v1, v1_diff_percent))
                print('%s\t%d\t%d\t%d\t%.2f%%' % (issn, r1_v2, r2_v2, r1_v1 - r2_v2, v2_diff_percent))

            sum_v1_diffs += v1_diff
            total_r1_v1 += r1_v1
            total_r2_v1 += r2_v1

            sum_v2_diffs += v2_diff
            total_r1_v2 += r1_v2
            total_r2_v2 += r2_v2

        try:
            print('sum_diffs_v1\ttotal_r1_v1\ttotal_r2_v1\tdiff_percent_v1')
            print('%d\t%d\t%d\t%.2f%%' % (sum_v1_diffs, total_r1_v1, total_r2_v1, sum_v1_diffs/total_r1_v1 * 100))
            print('sum_diffs_v2\ttotal_r1_v2\ttotal_r2_v2\tdiff_percent_v2')
            print('%d\t%d\t%d\t%.2f%%' % (sum_v2_diffs, total_r1_v2, total_r2_v2, sum_v2_diffs/total_r1_v2 * 100))
        except ZeroDivisionError:
            print('N/A')


def main():
    usage = 'Compara dois relatórios COUNTER em formato JSON'
    parser = argparse.ArgumentParser(usage)

    parser.add_argument(
        '-1', '--file1',
        dest='file1',
        required=True,
        help='Caminho do relatório 1'
    )

    parser.add_argument(
        '-2', '--file2',
        dest='file2',
        required=True,
        help='Caminho do relatório 2'
    )

    parser.add_argument(
        '-d', '--detailed',
        dest='print_mode',
        choices=['0', '1', '2'],
        default=0,
        help='Nível de detalhamento da impressão: 0: baixo, 1: médio, 2: alto'
    )

    params = parser.parse_args()

    try:
        report_1 = json.load(open(params.file1))
    except:
        print('Arquivo 1 inválido: %s' % params.file1)
        exit(1)

    try:
        report_2 = json.load(open(params.file2))
    except:
        print('Arquivo 2 inválido: %s' % params.file2)
        exit(1)

    compare(report_1, report_2, print_mode=int(params.print_mode))


if __name__ == '__main__':
    main()
