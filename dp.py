#!/usr/bin/env python3

import numpy
import math

file_a = 'city_mcepdata/city022/city022_'
file_b = 'city_mcepdata/city012/city012_'
#cross ptht penalty (NANAME) 
DP_PARAM =1
# define
GOAL   = 0
UE     = 1
NANAME = 2
HIDARI = 3

def get_frame(data_path):
    
    with open(data_path, 'r') as data_file:
        data_temp = data_file.read()
        splited_data = data_temp.split('\n')
        #print(splited_data[2])
        return splited_data

def calc_distance(a, b):

        nums_A = a.split(' ')
        nums_B = b.split(' ')
        distance_AB = 0
        for i in range(15):
            position_A = float(nums_A[i])
            position_B = float(nums_B[i])
            distance_AB += (position_A - position_B)**2
        return math.sqrt(distance_AB)


anser_result = 0
anser_score = 1024
anser_insdex = 0
for city_n in range(1,101):
    file_name_a = file_a
    str_city = '{0:03d}'.format(city_n)
    str_city = str(str_city)
    file_name_a += str_city
    file_name_a += '.txt'
    data_a = get_frame(file_name_a)
    max_a = int(data_a[2])

    anser_score = 10000
    anser_insdex = 0

    for n in range(1,101):
        file_name_b =file_b
        str_n = '{0:03d}'.format(n)
        str_n = str(str_n)
        file_name_b += str_n
        file_name_b += '.txt'

        data_b = get_frame(file_name_b)
        max_b = int(data_b[2])

        split_a = [0]*max_a
        split_b = [0]*max_b
# data cut
        for i in range(max_a):
            split_a[i] = data_a[i+3]
# data cut
        for i in range(max_b):
            split_b[i] = data_b[i+3]

        dp_map1 = numpy.zeros((max_a,max_b))
        dp_map2 = numpy.zeros((max_a,max_b))
        dp_map3 = numpy.zeros((max_a,max_b))
        dp_map4 = numpy.ones((max_a,max_b))
#dp_map1 create
        for i_a in range(max_a):
            for i_b in range(max_b):
                dp_map1[i_a][i_b] = (calc_distance(split_a[i_a],split_b[i_b]))

        dp_map2[0][0] = dp_map1[0][0]
        for i in range(1,max_a):
            dp_map2[i][0] = dp_map2[i-1][0]+dp_map1[i][0]
            dp_map3[i][0] = UE

        for i in range(1,max_b):
            dp_map2[0][i] = dp_map2[0][i-1]+dp_map1[0][i]
            dp_map3[0][i] = HIDARI

        for i_a in range(1, max_a):
            for i_b in range(1, max_b):

                minimum_dis = dp_map2[i_a - 1][i_b - 1] + dp_map1[i_a][i_b]* 2
                dp_map3[i_a][i_b] = NANAME

                if (dp_map2[i_a - 1][i_b] + dp_map1[i_a][i_b]) < minimum_dis:
                    minimum_dis = (dp_map2[i_a - 1][i_b])
                    dp_map3[i_a][i_b] = UE

                if dp_map2[i_a][i_b - 1] < minimum_dis:
                    minimum_dis = dp_map2[i_a][i_b - 1]
                    dp_map3[i_a][i_b] = HIDARI

                dp_map2[i_a][i_b] = (dp_map1[i_a][i_b])*DP_PARAM + minimum_dis

        dex_a = max_a-1
        dex_b = max_b-1

        dp_map3[0][0] = GOAL
        while (dp_map3[dex_a][dex_b]!=GOAL):
            dp_map4[dex_a][dex_b]=0

            if dp_map3[dex_a][dex_b] == UE:
#        dp_map3[dex_a][dex_b] =8
                dex_a = dex_a - 1

            elif dp_map3[dex_a][dex_b] == NANAME:
#        dp_map3[dex_a][dex_b] =8
                dex_a = dex_a - 1
                dex_b = dex_b - 1

            elif dp_map3[dex_a][dex_b] == HIDARI:
#       dp_map3[dex_a][dex_b] =8
                dex_b = dex_b - 1

            else :
                print('Direction ERR!')

        dp_map4[0][0] = 0
        numpy.set_printoptions(threshold=100000)
        numpy.set_printoptions(linewidth=300)
#print (dp_map3)
        #print (dp_map4)
        #print('{0:03d}'.format(n), ' distance = ',  ('{0:5.03f}'.format(dp_map2[max_a-1][max_b-1]/(max_a + max_b ))))
        
        anser_score_temp = (dp_map2[max_a-1][max_b-1]/(max_a + max_b))
        print('[',anser_result,'/', city_n,']', anser_insdex,'/',n,'BEST',anser_score, ' scoreTEMP=',anser_score_temp)

        if anser_score_temp < anser_score:
            anser_score = anser_score_temp
            anser_insdex = n


    if anser_insdex==city_n:
        anser_result += 1
    print('step=', city_n,'result=', anser_result)

print(anser_result)
print (file_name_a)
print (file_name_b)
