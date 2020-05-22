def tryint(value):
    try:
        return int(value)
    except:
        return value

def compare_ranks(old_rank, now_rank):
    diff = old_rank - now_rank
    result = '='
    if diff > 0:
        result = f'+{diff}'
    elif diff < 0:
        result = str(diff)
    return result