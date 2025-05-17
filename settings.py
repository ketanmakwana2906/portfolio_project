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
