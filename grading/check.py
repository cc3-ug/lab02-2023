import utils
import resource
import subprocess


# 195 MiB of memory
BYTES = 195 * 1024 * 1024

def check_cgdb():
    output = utils.parse_form('ex1.txt')
    expected = {'1': 'b', '2': 'c', '3': 'd', '4': 'b', '5': 'c', '6': 'c', '7': 'a', '8': 'a', '9': 'b'}
    grade = 0
    wrong = []
    for key in expected.keys():
        out = output.get(key)
        exp = expected.get(key)
        if exp == out:
            grade += 20/9
        else:
            wrong.append('q'+key)
    return (round(grade), utils.passed() if len(wrong) == 0 else utils.incomplete(','.join(wrong)))


def check_equal():
    try:
        task = utils.make(target='test_ll_equal')
        if task.returncode != 0:
            return (0, utils.failed('compilation error'), task.stderr.decode().strip())
        task = utils.execute(cmd=['./test_ll_equal'], timeout=10)
        if task.returncode != 0:
            return (0, utils.failed('runtime error'), task.stderr.decode().strip())
        output = task.stdout.decode().strip()
        expected = 'OK\nOK\n'
        expected = expected.strip()
        grade = 0
        if expected == output:
            grade += 40
        return (grade, utils.passed() if grade == 40 else utils.failed('failed some tests...'), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed('TIMEOUT'), '')
    except Exception:
        return (0, utils.failed('memory limit exceeded'), '')


def check_ll_cycle():
    try:
        task = utils.make(target='test_ll_cycle')
        if task.returncode != 0:
            return (0, utils.failed('compilation error'), task.stderr.decode().strip())
        task = utils.execute(cmd=['./test_ll_cycle'], timeout=10)
        if task.returncode != 0:
            return (0, utils.failed('Runtime error'), task.stderr.decode().strip())
        output = task.stdout.decode().strip()
        expected = 'OK\nOK\nOK\nOK\nOK\nOK\n'
        expected = expected.strip()
        grade = 0
        if expected == output:
            grade += 40
        return (grade, utils.passed() if grade == 40 else utils.failed('Failed some tests...'), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed('TIMEOUT'), '')
    except Exception:
        return (0, utils.failed('memory limit exceeded'), '')


def lab2_c_gdb():
    not_found = utils.expected_files(['./ex1.txt', './ll_equal.c', './ll_cycle.c'])
    if len(not_found) == 0:
        table = []
        
        cgdb = check_cgdb()
        table.append(['1. CGDB', cgdb[0], cgdb[1]])
        ll_equal = check_equal()
        table.append(['2. ll_equal', ll_equal[0], ll_equal[1]])
        ll_cycle = check_ll_cycle()
        table.append(['3. ll_cycle', ll_cycle[0], ll_cycle[1]])
        grade = 0
        grade += cgdb[0]
        grade += ll_equal[0]
        grade += ll_cycle[0]
        errors = ''
        errors += '\n' + utils.create_error('ll_equal.c', ll_equal[2])
        errors += '\n' + utils.create_error('ll_cycle.c', ll_cycle[2])
        errors = errors.strip()
        grade = min(grade, 100)
        report = utils.report(table)
        print(report)
        if errors != '':
            report += '\n\nMore Info:\n\n' + errors
        return utils.write_result(grade, report)
    else:
        utils.write_result(0, 'missing files: %s' % (','.join(not_found)))
    
    task = utils.make(target='autograder-clean')

if __name__ == '__main__':
    resource.setrlimit(resource.RLIMIT_AS, (BYTES, BYTES))
    lab2_c_gdb()
    utils.fix_ownership()
