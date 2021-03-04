import pandas as pd
import numpy as np


# Data Preprocess
def unit_conversion(df):
    """
    :param df: the original data with units as feet and ms
    :return: data with units as meters and s
    """
    ft_to_m = 0.3048
    df['Global_Time'] = df['Global_Time'] / 1000  # ms to s
    for elements in ["Global_X", "Global_Y", "Local_X", "Local_Y", "v_Length", "v_Width"]:  # feet to meter
        df[elements] = df[elements] * ft_to_m
    df["v_Vel"] = df["v_Vel"] * ft_to_m * 3.6  # velocity
    return df


if __name__ == '__main__':
    US101_part1 = pd.read_csv('./trajectories-0750am-0805am.csv')
    df1 = unit_conversion(US101_part1)
    # print(df1.head(4))
    # print(df1.columns)
    # print(df1.index)
    # print(len(df1))
    vehicle_id = df1['Vehicle_ID']
    vehicle_id_list = [] # all vehicles during this period
    for i in range(len(df1)):
        if vehicle_id[i] not in vehicle_id_list:
            vehicle_id_list.append(vehicle_id[i])
    # print(vehicle_id_list)
    print(f'There are {len(vehicle_id_list)} vehicles in this time period.')
    # filter the changing-lane vehicles
    f1 = df1[['Vehicle_ID', 'Lane_ID']]
    # print(f1.head(4))
    change_id = []
    change_row = []
    change_right_id = []
    change_right_row = []
    change_left_id = []
    change_left_row = []
    for i in range(len(f1)):
        if i == 0:
            continue
        else:
            # select the vehicles in lane 2, lane 3 and lane 4 first
            # if f1['Lane_ID'][i] == 2 or f1['Lane_ID'][i] == 3 or f1['Lane_ID'][i] == 4:
            if f1['Vehicle_ID'][i] == f1['Vehicle_ID'][i - 1] and f1['Lane_ID'][i] != f1['Lane_ID'][i - 1]:
                if f1['Lane_ID'][i] not in change_id:
                    change_id.append(f1['Lane_ID'][i])
                change_row.append(i-1)
                change_row.append(i)
            # changing right
            if f1['Vehicle_ID'][i] == f1['Vehicle_ID'][i - 1] and f1['Lane_ID'][i] == f1['Lane_ID'][i - 1] + 1:
                if f1['Lane_ID'][i] not in change_right_id:
                    change_right_id.append(f1['Vehicle_ID'][i])
                change_right_row.append(i-1)
                change_right_row.append(i)
            # changing left
            if f1['Vehicle_ID'][i] == f1['Vehicle_ID'][i - 1] and f1['Lane_ID'][i] == f1['Lane_ID'][i - 1] - 1:
                if f1['Lane_ID'][i] not in change_left_id:
                    change_left_id.append(f1['Vehicle_ID'][i])
                change_left_row.append(i-1)
                change_left_row.append(i)
            # else:
            #     continue

    # filter the keeping-straight vehicles
    lane_keep_id1 = vehicle_id_list
    lane_keep_id2 = []
    for i in range(len(change_left_id)):
        if change_left_id[i] in lane_keep_id1:
            lane_keep_id1.remove(change_left_id[i])
    for i in range(len(change_right_id)):
        if change_right_id[i] in lane_keep_id1:
            lane_keep_id1.remove(change_right_id[i])
    print(f'The number of keeping straight vehicles is {len(lane_keep_id1)} (with method 1)')

    for i in vehicle_id_list:
        if i not in change_id:
            lane_keep_id2.append(i)
    print(f'The number of keeping straight vehicles is {len(lane_keep_id2)} (with method 2)')
    print(f'The number of turning right vehicles is {len(change_right_id)}')
    print(f'The number of turning light vehicles is {len(change_left_id)}')
