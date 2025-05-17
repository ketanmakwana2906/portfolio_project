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
# cf_confluence = json.loads(os.environ.get("PORTFOLIO_PARAM"))
# d360_api_key = cf_confluence["D360_API_KEY"]
# to_number_d360 = cf_confluence["TO_NUMBER_D360"]
# reliance_userid = cf_confluence["Reliance_UserID"]
# reliance_token = cf_confluence["Reliance_Token"]
# reliance_accid = cf_confluence["Reliance_AccId"]

# Create Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    try:
        data = request.json
        to_mails = data.get("to_mails", [])
        cc_mails = data.get("cc_mails", [])
        if not to_mails:
            return "E-mail id required for API", 401
        if is_email_sent_today():
            return "Email already sent today!", 200
        print("hello")
        str_mail = get_html_for_mail()
        print("hello 1")
        send_mail(str_mail, to_mails, cc_mails)
        update_email_log()
        # str_wa = get_str_for_wa_msg()
        # send_whatsapp_msg(str, str_remain, d360_api_key, to_number_d360)
        return "Portfolio sent!!", 200
    except Exception as e:
        print(e)
        return f"An error occurred: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
