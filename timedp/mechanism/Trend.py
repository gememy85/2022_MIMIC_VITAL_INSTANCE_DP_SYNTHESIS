
class Trend:
    '''
    This class is a class that defines trend type
    '''
    def __init__(self,value_before, value, value_after, time_window):
        self.value_before = value_before
        self.value = value
        self.value_after = value_after
        self.time_window = time_window

        if time_window <= 0 :
            raise ValueError('time window should be a positive integer!')

        self.trend = self._define_trend()
    
    def _define_trend_type(self, value):

        if value == 0 :
            return Zero(value)
        elif value > 0 :
            return Positive(value)
        else :
            return Negative(value)

    
    def _define_trend(self):
        between_value_before_and_value =  (self.value-self.value_before)/self.time_window
        between_value_after_and_value = (self.value_after-self.value)/self.time_window
    
        trend = tuple(list(map(self._define_trend_type,[between_value_before_and_value, between_value_after_and_value])))
        return trend
    

