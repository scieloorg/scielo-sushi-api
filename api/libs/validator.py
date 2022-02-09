import re

from api import errors, values
from api.libs import cleaner


def is_valid_date_range(begin_date, end_date):
    if end_date >= begin_date:
        return True
    return False


def is_valid_issn(issn):
    if re.match(pattern=values.REGEX_ISSN, string=issn):
        return True
    return False


def is_valid_date_format(date):
    if re.match(pattern=values.REGEX_DATE_FORMAT, string=date):
        return True
    return False


def is_valid_pid(pid):
    if pid.startswith('S'):
        if len(pid) == 23:
            return True
        else:
            return False
    return True


def is_valid_yop(yop):
    if yop and yop.isdigit() and int(yop) > 0:
        return True

    return False


def validate_date_format(param_date, name):
    if not param_date:
        return errors.error_required_filter_missing(name)

    if not is_valid_date_format(param_date):
        return errors.error_invalid_date_arguments()

    try:
        if name == 'end_date':
            return cleaner.handle_str_date(param_date, is_end_date=True)
        else:
            return cleaner.handle_str_date(param_date)

    except ValueError or TypeError or AttributeError as e:
        if 'unconverted data' or 'argument of type' or 'parameter date' in e:
            return errors.error_invalid_date_arguments()


def validate_parameters(params, expected_params_list=[]):
    validation_results = {'errors': []}

    for p in expected_params_list:
        if p not in params and p != 'customer':
            validation_results['errors'].append((p, errors.error_required_filter_missing(p)))

    for p_name, p_value in params.items():
        if 'date' in p_name:
            validation_value = validate_date_format(p_value, p_name)

            if isinstance(validation_value, dict):
                validation_results['errors'].append((p_name, validation_value))

            else:
                validation_results[p_name] = validation_value

        elif p_name != 'issn':
          validation_results[p_name] = p_value

    if 'begin_date' in validation_results and 'end_date' in validation_results:
        if not is_valid_date_range(validation_results['begin_date'], validation_results['end_date']):
            validation_value = errors.error_invalid_date_arguments()

            if isinstance(validation_value, dict):
                validation_results['errors'].append(('period', validation_value))

    if 'issn' in params:
        if not is_valid_issn(params['issn']):
            validation_value = errors.error_invalid_report_filter_value(params['issn'], severity='error')
            if isinstance(validation_value, dict):
                validation_results['errors'].append(('issn', validation_value))
        else:
            validation_results['issn'] = params['issn']

    if 'pid' in params:
        if not is_valid_pid(params['pid']):
            validation_value = errors.error_invalid_report_filter_value(params['pid'], severity='error')
            if isinstance(validation_value, dict):
                validation_results['errors'].append(('pid', validation_value))

    if 'yop' in params:
        if not is_valid_yop(params['yop']):
            validation_value = errors.error_invalid_report_filter_value(params['yop'], severity='error')
            if isinstance(validation_value, dict):
                validation_results['errors'].append(('yop', validation_value))

    return validation_results
