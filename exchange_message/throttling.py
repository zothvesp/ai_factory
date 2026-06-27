import time
errors_time = {}
errors_count = {}

def free_error(error_message):
    print(errors_count)
    errors_time.pop(error_message, None)
    errors_count.pop(error_message, None)


def get_error_count(error_message, reset_count_of_error=True):
    result = errors_count[error_message] if error_message in errors_count else 0
    if reset_count_of_error:
        errors_count[error_message] = 0
    return result


def check_error_throttling(error_message, throttling_sec=300):
    now_time = time.time()
    prev_time = 0
    if error_message in errors_time:
        prev_time = errors_time[error_message]
    elif error_message in errors_count:
        errors_count[error_message] += 1
    else:
        errors_count[error_message] = 1
    if now_time - prev_time < throttling_sec:
        return False
    errors_time[error_message] = now_time
    return True

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/exchange_message/throttling.pyc
