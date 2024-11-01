# Duration
# Peyton Wall
# 10/29/2024 created constructor and string converter logic
# 10/30/2024 created other functions and mathmatic/comparison operators; also did doctests with coverage

class Duration:
    def __init__(self, *args):
        """
        >>> Duration(3661).total_seconds
        3661
        >>> Duration("01:30:30").total_seconds
        5430
        >>> Duration(1, 30, 30).total_seconds
        5430
        >>> Duration("2h15m45s").total_seconds
        8145
        """
        self.total_seconds = 0

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, int):
                self.total_seconds = arg
            elif isinstance(arg, str):
                self.total_seconds = self.convert_from_string(arg)
        elif len(args) == 3:
            hours, minutes, seconds = args
            self.total_seconds = hours * 3600 + minutes * 60 + seconds

    def convert_from_string(self, duration_str):
        """
        converts a string duration format to total secs
        
        >>> Duration().convert_from_string("1:30:15")
        5415
        >>> Duration().convert_from_string("-2:15:30")
        -8130
        >>> Duration().convert_from_string("10h5m30s")
        36330
        >>> Duration().convert_from_string("5m")
        300
        """
        hours = 0
        minutes = 0
        seconds = 0
        sign = -1 if duration_str.startswith('-') else 1
        duration_str = duration_str.lstrip('-')
        self.total_seconds = 0

        if ':' in duration_str:
            parts = list(map(int, duration_str.split(':')))
            parts = [0] * (3 - len(parts)) + parts  # pad list to make sure there's 3 parts
            hours = parts[0]
            minutes = parts[1]
            seconds = parts[2]
            return sign * (hours * 3600 + minutes * 60 + seconds)
        else:
            # handle formats like "10h5m30s"
            time_units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
            current_value = ''
            for char in duration_str:
                if char.isdigit():
                    current_value += char
                elif char in time_units:
                    if current_value:
                        self.total_seconds += int(current_value) * time_units[char]
                        current_value = ''
            return sign * self.total_seconds

    def __repr__(self):
        """    
        >>> repr(Duration("01:30:30"))
        "Duration('1:30:30')"
        >>> repr(Duration("5m"))
        "Duration('0:05:00')"
        >>> repr(Duration("1h3m34s"))
        "Duration('1:03:34')"
        """
        return f"Duration('{self}')"

    def __str__(self):
        """ 
        >>> str(Duration("01:30:30"))
        '1:30:30'
        >>> str(Duration("5m"))
        '0:05:00'
        >>> str(Duration("1h3m34s"))
        '1:03:34'
        >>> str(Duration("0:00:00"))
        '0:00:00'
        >>> str(Duration("-1h2m3s"))
        '-1:02:03'
        >>> str(Duration(3661))
        '1:01:01'
        >>> str(Duration(-3661))
        '-1:01:01'
        >>> str(Duration(0))
        '0:00:00'
        """
        abs_seconds = abs(self.total_seconds)
        hours, remainder = divmod(abs_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        sign = '-' if self.total_seconds < 0 else ''
        return f"{sign}{hours}:{minutes:02}:{seconds:02}"

    def __add__(self, other):
        """
        >>> (Duration(3600) + Duration(7200)).total_seconds
        10800
        >>> (Duration(3600) + Duration("0:30:00")).total_seconds
        5400
        """
        return Duration(self.total_seconds + other.total_seconds)

    def __sub__(self, other):
        """
        >>> (Duration(7200) - Duration(3600)).total_seconds
        3600
        >>> (Duration(3600) - Duration("0:30:00")).total_seconds
        1800
        """
        return Duration(self.total_seconds - other.total_seconds)

    def __mul__(self, multiplier):
        """
        >>> (Duration(3600) * 2).total_seconds
        7200
        >>> (Duration(3600) * 0).total_seconds
        0
        """
        return Duration(self.total_seconds * multiplier)

    # comparison operators
    def __eq__(self, other):
        """
        >>> Duration(3600) == Duration(3600)
        True
        >>> Duration(3600) == Duration(7200)
        False
        """
        return self.total_seconds == other.total_seconds

    def __lt__(self, other):
        """  
        >>> Duration(3600) < Duration(7200)
        True
        >>> Duration(3600) < Duration(1800)
        False
        """
        return self.total_seconds < other.total_seconds

    def __le__(self, other):
        """
        >>> Duration(3600) <= Duration(3600)
        True
        >>> Duration(3600) <= Duration(1800)
        False
        """
        return self.total_seconds <= other.total_seconds

    def __gt__(self, other):
        """     
        >>> Duration(7200) > Duration(3600)
        True
        >>> Duration(7200) > Duration(1800)
        True
        """
        return self.total_seconds > other.total_seconds

    def __ge__(self, other):
        """
        >>> Duration(3600) >= Duration(3600)
        True
        >>> Duration(3600) >= Duration(7200)
        False
        """
        return self.total_seconds >= other.total_seconds
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()