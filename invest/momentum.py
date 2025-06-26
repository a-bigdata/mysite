from datetime import datetime
import pandas as pd
import numpy as np

def create_YM(
    _df,
    _col = 'Adj Close'
):
    df = _df.copy()
    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    flag = df.isin( [np.nan, np.inf, -np.inf] ).any(axis=1)
    df = df.loc[~flag, ]
    df = df[[_col]]
    df['STD-YM'] = df.index.strftime('%Y-%m')
    return df

def create_last_month(
        _df,
        _start = '2010-01-01',
        _end = datetime.now(),
        _momentum = 12
):

        col = _df.columns[0]
        flag = _df['STD-YM'] != _df.shift(-1)['STD-YM']
        df = _df.loc[flag, ]
        df['BF1'] = df.shift(1)[col].fillna(0)
        # _momentum의 개월 전의 데이터를 생성
        df['BF2'] = df.shift(_momentum)[col].fillna(0)
        df= df.loc[_start : _end, ]
        return df

def create_rtn(
    _df1, _df2,
    _score = 1
):
    df = _df1.copy()
    df['trade'] = ""
    df['rtn'] = 1

    for idx in _df2.index:
        signal = ""

        momentum_index = _df2.loc[idx, 'BF1'] / _df2.loc[idx, 'BF2'] - _score

        flag = (momentum_index > 0) & (momentum_index != np.inf)

        if flag :
            signal = 'buy'
        df.loc[idx: , 'trade'] = signal
    col = df.columns[0]
    for idx in df.index:
        if (df.shift().loc[idx, 'trade'] == "") & (df.loc[idx, 'trade'] == "buy"):
            buy = df.loc[idx, col]
            print(f"매수일 : {idx}, 매수가: {buy}")
        elif (df.shift().loc[idx, 'trade'] == 'buy') & (df.loc[idx, 'trade'] == ""):
            sell = df.loc[idx, col]
            rtn = sell / buy
            df.loc[idx, 'rtn'] = rtn
            print(f"매도일: {idx}, 매도가: {sell}, 수익률: {rtn}")
    df['arr_rtn'] = df['rtn'].cumprod()
    acc_rtn = df.iloc[-1, -1]
    return df, acc_rtn