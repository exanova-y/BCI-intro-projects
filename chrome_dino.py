import time
import pyautogui

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions


def main ():
    # initialize variables
    
    board_id = 1 # ganglion board id #
    params = BrainFlowInputParams ()
    params.board_id = 1   
    params.serial_port = 'COM3'                    
    
    time_thres =  200    # ignore blinks detected in the last 500 ms
    sampling_rate  = BoardShim.get_sampling_rate (board_id)
    window = sampling_rate*5 
    blink_thres =  0.75                                                           
                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                             
    # preparing session
                                                                            
    BoardShim.enable_dev_board_logger ()
    board = BoardShim (board_id, params)                                            
    board.prepare_session ()

    board.start_stream (45000) # size of ring buffer to keep data
    time.sleep(10)       # wait for data to stabilize


    # start session

    print("start blinking")
    prev_time = int(round(time.time() * 1000)) 
    while True:

        data = board.get_current_board_data(window) # get data 
        ch4 = data[4]

        DataFilter.perform_rolling_filter (ch4, 2, AggOperations.MEAN.value) # denoise data
        maximum = max(ch4)
        minimum = min(ch4)
        norm_data = (data[4,(window-(int)(sampling_rate/2)):(window-1)] - minimum) / (maximum - minimum) 

        if((int(round(time.time() * 1000)) - time_thres) > prev_time): # if enough time has gone by since the last blink
            prev_time = int(round(time.time() * 1000)) # update time
            for element in norm_data:
                if(element >= blink_thres):
                    pyautogui.press('space') 
                    break
                                            
    board.stop_stream ()
    board.release_session ()


if __name__ == "__main__":
    main ()
