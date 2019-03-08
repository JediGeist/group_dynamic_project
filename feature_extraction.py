import pandas as pd
import pickle
from numpy import array, log1p, arange, abs as np_abs
from numpy.fft import rfft, rfftfreq, irfft
from numpy.random import uniform

def create_table( len_window = 100, len_min = 100):
    df = pd.DataFrame()

    for i in range(len_min):
        cur_str = "a" + str(i)
        tmp = pd.DataFrame(columns=[cur_str])
        df = df.join(tmp)

    for i in range(len_min):
        cur_str = "b" + str(i)
        tmp = pd.DataFrame(columns=[cur_str])
        df = df.join(tmp)
    df = df.join(pd.DataFrame(columns=['is_image', 'name']))

    return df


def get_feature(data, len_window = 50, len_min = 50):
    data_res = data

    df = create_table(len_window=len_window, len_min=len_min)
    df = createDF(data_res, True,  "to_pred", df=df, len_window=len_window, len_min=len_min)

    df.drop(columns=["name", "is_image"], inplace=True)
    print(df.shape)
    return df.values

def getFeatures(data):
    res = rfft(data)
    FD = 256
    N = data.shape[0]
    #plt.plot(rfftfreq(N, 1./FD), np_abs(res)/N)
    amp = np_abs(res)/N
    chastota = rfftfreq(N, 1./FD)
    alpha = amp[(chastota >= 8) & (chastota < 12)]
    #plt.plot(alpha)
    
    betta = amp[(chastota >= 12) & (chastota < 30)]
    #plt.plot(betta)
    
    #alpha_HZ = irfft(alpha)
    #plt.plot(alpha_HZ)
    #betta_HZ = irfft(betta)
    #plt.plot(betta_HZ)
    #print(alpha)
    return alpha.mean() if len(alpha) > 0 else 0, betta.mean() if len(betta) > 0 else 0

# def createDF(data, is_image, name, len_window = 100, len_min = 100, df = None):

#     for i in range(0, len(data), len_window):
#         alpha_arr = []
#         betta_arr = []
#         for j in range(i, i + len_window):
#             cur_alpha_mean, cur_betta_mean = getFeatures(data[j:min(len(data), j + len_min)])
#             #alpha_arr = np.append(alpha_arr, str(cur_alpha_mean))
#             #alpha_arr = np.append(alpha_arr, str(cur_alpha_mean))
#             alpha_arr.append(cur_alpha_mean)
#             betta_arr.append(cur_betta_mean)
#         new_str = alpha_arr + betta_arr
#         new_str.append(is_image)
#         new_str.append(name)
#         df.loc[len(df)] = new_str

#     df = df.fillna(0)
#     return df

def createDF(data, is_image, name, len_window = 100, len_min = 100, df = None):
   
    for i in range(0, len(data) - len_min, len_min):
        alpha_arr = []
        betta_arr = []
        for j in range(i, i + len_window):
            cur_alpha_mean, cur_betta_mean = getFeatures(data[j:min(len(data), j + len_min)])
            #alpha_arr = np.append(alpha_arr, str(cur_alpha_mean))
            #alpha_arr = np.append(alpha_arr, str(cur_alpha_mean))
            alpha_arr.append(cur_alpha_mean)
            betta_arr.append(cur_betta_mean)
        new_str = alpha_arr + betta_arr
        new_str.append(is_image)
        new_str.append(name)
        print(len(new_str), df.shape)
        df.loc[len(df)] = new_str

    df = df.fillna(0)
    return df
