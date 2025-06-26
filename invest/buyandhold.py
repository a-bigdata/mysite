import pandas as pd
from datetime import datetime
import numpy as np

def bnh(
    _df,
    _start = '2010-01-01',
    _end = datetime.now(),
    _col = 'Adj Close'
):
    # 데이터프레임 복사본 생성
    df = _df.copy()
        #try: 
        #    _start = datetime.strptime(_start, '%Y-%m-%d')
        #   if type(_end) == 'str':
        #       _end = datetime.strptime(_end, '%Y-%m-%d')
        #except:
        #   print('시간의 포맷이 맞지 않습니다. (YYYY-mm-dd)')
        #   return ""
        # Date가 컬럼에 존재하면 Date를 인덱스로 변경
    if 'Date' in df.columns:
        df.set_index('Date', inplace = True)
    df.index = pd.to_datetime(df.index)
    flag = df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df=df.loc[~flag, ]
    try : 
        df = df.loc[_start : _end, [_col]]
    except Exception as e:
        print(e)
        print('입력된 인자값이 잘못됐습니다.')
        return ""
    # 일별 수익율 계산헤 rtn 컬럼에 대입
    df['rtn'] = (df[_col].pct_change() + 1).fillna(1)
    # 누적 수익율 계산해 acc_rtn 컬럼에 대입
    df['acc_rtn'] = df['rtn'].cumprod()
    acc_rtn = df.iloc[-1, -1]
    return df, acc_rtn