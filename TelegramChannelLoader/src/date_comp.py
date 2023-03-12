import datetime


# compares two dates only by day, month and year
def compare_dates(a: datetime, b: datetime):
    if a.day == b.day and a.month == b.month and a.year == b.year:
        return True
    return False


# returns True if a < b, compared by day, month and year
def date_is_less(a: datetime, b: datetime):
    if a.year < b.year:
        return True
    if a.month < b.month:
        return True
    if a.day < b.day:
        return True
    return False
