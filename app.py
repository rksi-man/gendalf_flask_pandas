from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

xls = pd.ExcelFile('content/_100 вопросов мастеру.xlsx')
data_frame_dict = {}

for sheet_name in xls.sheet_names:
    data_frame_dict[sheet_name] = pd.read_excel(xls, sheet_name, index_col=0)

def get_sample_and_delete(sheet_name):
  df = data_frame_dict[sheet_name]
  try:
    sample_obj = df.sample()
    data_frame_dict[sheet_name].drop(sample_obj.index, inplace=True)
    left_rows = len(df.index)
    return sample_obj, left_rows
  except:
    return 'No Data'

@app.route("/")
def index():
    name_book = xls.io.split('/')[-1].strip('_')
    return render_template("index.html", data_frame_dict=list(data_frame_dict.keys()), name_book=name_book)

@app.route('/sheet/<name>')
def sheet(name):
    sheet_list = get_sample_and_delete(name)
    try:
        return render_template('sheet.html', sheet_list=sheet_list[0].to_dict('records')[0], left = sheet_list[1])
    except: 
       return render_template('error.html', msg='Error')
