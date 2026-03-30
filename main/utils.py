def safe_divide(a, b):
    if b == 0:
        return 0
    return round(a / b, 2)