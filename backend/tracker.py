from nicegui import ui
from time import time, sleep
from typing import Optional, Iterable

class IterableTracker(Iterable):
    def __init__(self, tracker_name: str, data_source: Optional[Iterable], visual: str='', min_iters: int = 0):
        self.tracker_name = tracker_name
        # if type(data_source) != Iterable:
        #     raise TypeError(f'Parameter "data_source" must be iterable object, but got {type(data_source)}')
        self.iter_obj = data_source
        self.iter_round = len(data_source)
        self.current_round = 0
        self.min_iters = min_iters
        # Init the time counter and time breakpoint
        self._time = time
        self.last_iter_t = self._time()
        self.start_iter_t = self.last_iter_t 
        # Init average iter_time
        self.sum_iter_t = 0       
        
    def __iter__(self):
        iter_obj = self.iter_obj
        iter_round = self.iter_round
        current_round = self.current_round
        min_iters = self.min_iters
        last_iter_t = self.last_iter_t
        sum_iter_t = self.sum_iter_t
        time = self._time
        
        try:
            for obj in iter_obj:
                yield obj
                current_round += 1
                cur_t = time()
                d_t = cur_t - last_iter_t
                sum_iter_t += d_t
                avg_iter_t = sum_iter_t / current_round
                last_iter_t = cur_t
                print("DEBUG: AVG Times usage => ", avg_iter_t, "!!!", sum_iter_t)
                
        finally:
            self.current_round = current_round
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    
    def update(self, data):
        pass

    
if __name__ == "__main__":
    with IterableTracker('test', range(10)) as tt:
        for t in tt:
            print("curent iter:", t)
            sleep(2)