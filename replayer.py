import argparse
from helper import DynamicUpdate, load_obj
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Plots the data from pressure measurement and laser scan.')
    parser.add_argument('-f', '--file', help='Description of file argument', )

    parser.add_argument('-x', '--xlim', nargs=2, type=float, help='Description of xlim argument', )

    parser.add_argument('-y', '--ylim', nargs=2, type=float, help='Description of ylim argument', )

    parser.add_argument('-a', '--animation', action='store_true', help='Description of animation argument', )

    parser.add_argument('-o', '--output', help='Description of output argument', )
    
    return parser.parse_args()

def main(args):
    data = load_obj(args.file)
    
    if args.animation:
        plt.ion()
        
        if args.xlim and args.ylim:
            d = DynamicUpdate(args.xlim[0], args.xlim[1], args.ylim[0], args.ylim[1])
        elif args.xlim:
            d = DynamicUpdate(args.xlim[0], args.xlim[1])
        elif args.ylim:
            d = DynamicUpdate(min_y=args.ylim[0], max_y=args.ylim[1])
        else:
            d = DynamicUpdate()
        
    list_of_timestamps = []
    list_of_pressures = []
    diff_list = []
    t0 = None
    
    for idx, timestamp in enumerate(data[0]):
        if not t0: t0 = timestamp
        list_of_timestamps.append(timestamp - t0)
        list_of_pressures.append(data[1][idx])
        X = data[2][idx][0]
        Z = data[2][idx][1]
        # filtering_condition = (X>-3) & (X<-2) & (Z>11) & (Z<12) # for powder_double2
        # filtering_condition = (X>-3) & (X<-2) & (Z>11) & (Z<11.5) # for powder_double_vacuum2
        if args.xlim and args.ylim:
            filtering_condition = (X>args.xlim[0]) & (X<args.xlim[1]) & (Z>args.ylim[0]) & (Z<args.ylim[1])
            # filtering_condition = (X>-4) & (X<-2) & (Z>6.5) & (Z<7.5)
            new_X = X[filtering_condition]
            new_Z = Z[filtering_condition]
        else:
            new_X = X
            new_Z = Z
            
        diff = 0
        if new_X.shape[0] and new_Z.shape[0]:
            diff = new_X.max() - new_X.min() + .023 # correction of points
            
        diff_list.append(diff)
        
        if args.animation:
            # if not d(list_of_timestamps, diff_list , list_of_timestamps, list_of_pressures, ): break
            if not d(X, Z , list_of_timestamps, list_of_pressures,): break
        
    if args.output:
        df = pd.DataFrame(
            {'timestamp': list_of_timestamps,
            'pressure': list_of_pressures,
             'opening': diff_list, })
        df.to_csv(args.output, index=False)
        
        
    # apply moving average filter
    diff_list = np.convolve(diff_list, np.ones((12,))/12, mode='same')

    plt.figure(figsize=(10, 10))
    plt.subplot(311)
    plt.plot(list_of_pressures, diff_list, 'r-', markersize=1)
    plt.xlabel('Pressure kPa')
    # invert x axis
    # plt.gca().invert_xaxis()
    plt.ylabel('Opening mm')
    
    plt.subplot(312)
    # plot opening vs time
    plt.plot(list_of_timestamps, diff_list, 'r-', markersize=1)
    plt.xlabel('Time s')
    plt.ylabel('Opening mm')
    # plot pressure vs time
    plt.subplot(313)
    plt.plot(list_of_timestamps, list_of_pressures, 'b-', markersize=1)
    plt.xlabel('Time s')
    plt.ylabel('Pressure kPa')
    
    plt.show()
    
    
            
        
        
        
        
    

if __name__ == "__main__":
    args = parse_args()
    main(args)


