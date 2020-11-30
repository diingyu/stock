from flask import Flask, redirect, url_for, request
from Stock import Stock
import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/kdj', methods=['POST', 'GET'])
def kdj():
    if request.method == 'POST':
        code = request.form['code']
    else:
        code = request.args.get('code')
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    stock = Stock(code, start_date=start_date, end_date=end_date)
    e, m = stock.get_data()
    if e == 1:  # error
        return m

    k, d, j = stock.kdj_sig()
    if j > 100:
        return "j=" + str(int(j)) + ", 可卖出！"
    elif j < 0:
        return "j=" + str(int(j)) + ", 可买入！"
    else:
        return "j=" + str(int(j)) + ", 不动！"


if __name__ == '__main__':
    app.run()
