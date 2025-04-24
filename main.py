from flask import Flask, request
from portfolio_api import *
import os
import urllib3
import json

# Disable warnings for insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables
# with open("portfolio_env.json") as f:
#     creds_json = f.read()
#     os.environ["PORTFOLIO_PARAM"] = creds_json
cf_confluence = json.loads(os.environ.get("PORTFOLIO_PARAM"))
d360_api_key = cf_confluence["D360_API_KEY"]
to_number_d360 = cf_confluence["TO_NUMBER_D360"]
reliance_userid = cf_confluence["Reliance_UserID"]
reliance_token = cf_confluence["Reliance_Token"]
reliance_accid = cf_confluence["Reliance_AccId"]

# Create Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    try:
        # Get portfolio data and send WhatsApp messages
        str = get_portfolio_summary(reliance_userid, reliance_token, reliance_accid)
        str_list = get_equity_summary(reliance_userid, reliance_token, reliance_accid)
        str += str_list[0]
        str_remain = str_list[1:]
        send_whatsapp_msg(str, str_remain, d360_api_key, to_number_d360)
        return "Portfolio sent!!", 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
