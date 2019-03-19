import pandas as pd
import pickle
from numpy import array, log1p, arange, abs as np_abs
from numpy.fft import rfft, rfftfreq, irfft
from numpy.random import uniform

def create_table():
    df = pd.DataFrame(columns=['range', 'a', 'b','is_image', 'name'])
    return df


def get_feature(data, len_window = 100, step = 50):
    data_res = data

    df = create_table()
    df = createDF(data_res, True,  "to_pred", df=df, len_window=len_window, step=step)
    df.drop(columns=["name", "is_image"], inplace=True)
    #print(df.shape)
    return df

def feature(data):
    np_df_first = []
    np_df_second = []

    np_df_first.append(get_feature(data[0]))
    np_df_second.append(get_feature(data[1]))

    np_df_first_conc = pd.concat(np_df_first)
    np_df_second_conc = pd.concat(np_df_second)

    df = pd.concat((np_df_first_conc, np_df_second_conc), axis=1)

    print(df[['a', 'b']])
    return df[['a', 'b']].values

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

def createDF(data, is_image, name, len_window = 100, step = 50, df = None):

    for i in range(0, len(data) - len_window, step):
        alpha_mean, betta_mean = getFeatures(data[i:min(len(data), i + len_window)])
        new_str = [str(i) + "-" + str(i + len_window)]
        new_str.append(alpha_mean)
        new_str.append(betta_mean)
        new_str.append(is_image)
        new_str.append(name)
        #print(len(new_str), df.shape)
        df.loc[len(df)] = new_str

    df = df.fillna(0)
    return df

