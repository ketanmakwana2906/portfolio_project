import json, os

# with open("portfolio_env.json") as f:
#     creds_json = f.read()
#     os.environ["PORTFOLIO_PARAM"] = creds_json
cf_confluence = json.loads(os.environ.get("PORTFOLIO_PARAM"))
d360_api_key = cf_confluence["D360_API_KEY"]
to_number_d360 = cf_confluence["TO_NUMBER_D360"]
reliance_userid = cf_confluence["Reliance_UserID"]
reliance_token = cf_confluence["Reliance_Token"]
reliance_accid = cf_confluence["Reliance_AccId"]

LOG_FILE = "sent_mail_log.txt"

def is_email_sent_today():
    """Checks if an email was already sent today"""
    today = str(datetime.datetime.today().date())
    
    if not os.path.exists(LOG_FILE):
        return False

    with open(LOG_FILE, "r") as file:
        last_sent_date = file.read().strip()
    
    return last_sent_date == today

def update_email_log():
    """Updates log file after sending an email"""
    with open(LOG_FILE, "w") as file:
        file.write(str(datetime.datetime.today().date()))
