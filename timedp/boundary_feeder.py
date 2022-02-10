
class BoundaryFeeder:
    '''
    This object is a boundary feeder used when the Timeseries DP algorithm is onging.
    This class give the boundary information to the BLM
    '''

    def __init__(self, timeseries : np.array, window_size: int):
        self.timeseries = timeseries
        self.window_size = window_size
        self.boundary_information = self._make_boundary_information() 
    
    def _get_boundary(self, idx):
        value = self.timeseries[idx]
        v_before, v_after = self.timeseries[idx - self.window_size], self.timeseries[idx + self.window_size]
        return v_before, v_after

    def _make_boundary_information(self):
        theLength = len(self.timeseries)
        idx_list = [idx for idx in range(self.window_size, theLength-self.window_size)]
        boundary_list = map(self._get_boundary, idx_list)

        return {idx : (v_before, v_after) for idx, (v_before, v_after) in zip(idx_list, boundary_list)}

    def _check_trend(self, value, boundary:tuple):
        '''
        checks the trend of t-window_size, t, t+window_size
        classifies the the trend
        '''
        # case increasing or decreasing
        

    # def _feed(self):
        
