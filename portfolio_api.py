import requests
import json
import datetime


def get_portfolio_summary(userid, token, accid):
    url = "https://connect.reliancesmartmoney.com/Portfolio.svc/getPortfolioSummary"
    payload = {
        "UserID" : userid,
        "UserToken" : token,
        "UserAccId" : accid
    }
    data = json.dumps(payload)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    data = json.loads(response.text)
    summary_portfolio = json.loads(data["d"][0])[0]
    str = f"""
    Date : {datetime.datetime.today().date()}
    Portfolio of Mr. Ketan
    *overall portfolio summary*
    Investment Value:
        ₹({round(float(summary_portfolio["CostValue"]), 2)})
    Current Market Value: 
        ₹({round(float(summary_portfolio["Mkt_Value"]), 2)})
    Net Profit/loss: 
        ₹({round(float(summary_portfolio["UnRealised"]), 2)})
    Net Profit/loss: 
        %({round(float(summary_portfolio["AbsPer"]), 2)}%)

    details of each Equity
    """
    
    return str


def get_equity_summary(userid, token, accid):
    url = "https://connect.reliancesmartmoney.com/Portfolio.svc/GetEquityDetails"
    payload = {
        "userid" : userid,
        "token" : token,
        "accid" : accid
    }
    data = json.dumps(payload)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=data)
    data = json.loads(response.text)
    portfolio = json.loads(data["d"][0])
    i = 1
    str = ""
    str_list = []
    for d in portfolio:
        str += f"""
    *{i}. {d["scripname"]}*
    Net gain/loss: ₹({round(d["difference"], 2)}) ({round(d["difference%"], 2)}%)
    Quantity: {d["QTY"]} share at buy price ₹({round(d["AVGCOST"], 2)}) = ₹({round(d["QTY"]*d["AVGCOST"], 2)})
    Current market value: per share ₹({round(d["LTP"], 2)}) total ₹({round(d["MarketValue"], 2)})
    """
        i += 1

        if i % 15 == 1 or d == portfolio[-1]:
            str_list.append(str)
            str = ""

    return str_list

def get_str_for_wa_msg():
    str = get_portfolio_summary()
    str_list = get_equity_summary()
    str += str_list[0]
    str_remain = str_list[1:]
    return str, str_remain

def send_whatsapp_msg(str, str_remain, d360_api_key, to):
    str_list = [str] + str_remain
    url = "https://waba-sandbox.360dialog.io/v1/messages"

    for str in str_list:
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "body": str
            }
        })
        headers = {
            'D360-API-KEY': d360_api_key,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=False)

    return response.text
