from GetTA import GetAnalysisTA
# from flask import Flask

# app = Flask(__name__)

# @app.route("/getdata/<symbolname>")
# def get_notify(symbolname):
#     GetAnalysisTA(symbolname=symbolname)
#     return "<p>Please see detail on line notify</p>"

# if __name__ == "__main__":
#     app.run()
import time
for i in ["BTCUSDT","ETHUSDT","LTCUSDT","DOGEUSDT"]:
    GetAnalysisTA(i)
    