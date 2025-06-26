# 프레임워크 로드 
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from invest import Quant
from database import MyDB

# MyDB class 생성
mydb = MyDB(
    _host = 'Jay00.mysql.pythonanywhere-services.com',
    _port = 3306,
    _user = 'Jay00',
    _pw = '1234567!'
    _db_name = 'Jay00$default'
)

# Flask class 생성 
# 생성자 함수 필요한 인자 : 파일의 이름 
app = Flask(__name__)

# 네비게이터 -> 특정한 주소로 요청이 들어왔을때 함수와 연결
# route()함수에 인자가 의미하는것은? 
# root url + 주소(route함수에 인자) 
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main', methods=['post'])
def main():
    # 유저가 보낸 데이터를 변수에 저장
    # get 방식으로 보낸 데이터 : request.args
    # post 방식으로 보낸 데이터 : request.form
    user_id = request.form['input_id']
    user_pass = request.form['input_pass']
    print(f"id : {user_id}, pass: {user_pass}")
    # 유저가 입력한 아이디와 비밀번호에 대해 DB server 해당 데이터가 존재하는가?
    login_query = """
        select * from `user`
        where `id` = %s and `password` = %s
    """
    result_sql = mydb.sql_query(
        login_query, user_id, user_pass
    )
    # result_sql이 존재한다면? -> 로그인이 성공
    if result_sql:
        return render_template('index.html')
    # 존재하지 않으면 -> 로그인이 실패
    else:
        # 로그인 페이지를 보여주는 주소로 이동
        return redirect('/')

    return render_template('index.html')
    # csv 파일 로드 
    #df = pd.read_csv("csv/AAPL.csv").tail(20)
    # 컬럼의 이름들을 리스트로 변경하여 변수에 저장
    #cols = list(df.columns)
    # values를 리스트 안에 딕셔너리 형태로 변show환 
    #value = df.to_dict('records')
    # 그래프에서 보여질 데이터를 생성 
    #x = list(df['Date'])
    #y = list(df['Adj Close'])
    #return render_template('index.html', 
    #                       columns = cols, 
    #                       values = value, 
    #                       axis_x= x, 
    #                       axis_y = y)
    return render_template('test.html')


@app.route('/invest')
def invest():
    input_code = request.args['code']
    input_start_time = f"{request.args['s_year']}-{request.args['s_month']}-{request.args['s_day']}"
    input_end_time = input_end_time = (
    f"{request.args['e_year']}-"
    f"{request.args['e_month']}-"
    f"{request.args['e_day']}"
)
    input_kind = request.args['kind']
    print(
        f"""
            {input_code}
            {input_start_time}
            {input_end_time}
            {input_kind}
        """
    )
    # input_code를 이용해서 csv 파일을 로드
    # local에서는 상대 경로
    # df = pd.read_csv(f"csv/{input_code}.csv")
    # pythonanywhere에서는 절대 경로 사용
    df = pd.read_csv(f"/home/jay00/mysite/csv/{input_code}.csv")
    df.rename(
        columns = {
            '날짜' : 'Date'
        }, inplace=True
    )
    quant = Quant(df, _start = input_start_time, _end = input_end_time, _col='Close')
    if input_kind == 'bnh':
        result, rtn = quant.buyandhold()
    elif input_kind == 'boll':
        result, rtn = quant.bollinger()
    elif input_kind == 'hall':
        result, rtn = quant.halloween()
    elif input_kind == 'mmt':
        result, rtn = quant.momentum()
    result.reset_index(inplace=True)
    result = result.loc [ result['rtn'] != 1, ]
    cols = list(result.columns)
    value = result.to_dict('records')
    x = list(result['Date'])
    y = list(result['acc_rtn'])
    res_data = {
        'columns' : cols,
        'values' : value,
        'axis_x' : x,
        'axis_y' : y
    }
    return res_data