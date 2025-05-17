import requests
import json
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from settings import *


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
    Date : {datetime.datetime.today().date()}<br><br>

    <h2> Equity Portfolio </h2> <br>
    <b>overall equity portfolio summary:</b> <br>
    Investment Value:
        ₹({round(float(summary_portfolio["CostValue"]), 2)})<br>
    Current Market Value:
        ₹({round(float(summary_portfolio["Mkt_Value"]), 2)})<br>
    Net Profit/loss:
        ₹({round(float(summary_portfolio["UnRealised"]), 2)})<br>
    Net Profit/loss:
        %({round(float(summary_portfolio["AbsPer"]), 2)}%)<br><br>

    details of each Equity<br><br>
    """
    
    return summary_portfolio

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
    {i}. {d["scripname"]}<br>
    Quantity: {int(d["QTY"])}<br>
    Original Buy Price : ₹({round(d["AVGCOST"], 2)})<br>
    Total Investment: ₹({round(d["InvestmentValue"], 2)})<br>
    Current market value: per share ₹({round(float(d["LTP"]), 2)}) total ₹({round(d["MarketValue"], 2)})<br>
    Net gain/loss: ₹({round(d["difference"], 2)}) %({round(d["difference%"], 2)}%)<br><br>
    """
        i += 1

        if i % 15 == 1 or d == portfolio[-1]:
            str_list.append(str)
            str = ""

    return str_list

def get_equity_summary_table(userid, token, accid):
    url = "https://connect.reliancesmartmoney.com/Portfolio.svc/GetEquityDetails"
    payload = {
        "userid": userid,
        "token": token,
        "accid": accid
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

    table_html = f"""date - {datetime.datetime.today().date()} <br> <h2>Equity Portfolio</h2><table border="1" style="border-collapse: collapse; width: 100%; text-align: left; font-family: Arial, sans-serif;">
<tr style="background-color: #f2f2f2; padding: 10px;">
    <th style="padding: 10px; text-align: center;">#</th>
    <th style="padding: 10px;">Scrip Name</th>
    <th style="padding: 10px;">Quantity</th>
    <th style="padding: 10px;">Original Buy Price (₹)</th>
    <th style="padding: 10px;">Current Market Value per Share (₹)</th>
    <th style="padding: 10px;">Total Investment (₹)</th>
    <th style="padding: 10px;">Total Current Market Value (₹)</th>
    <th style="padding: 10px;">Net Gain/Loss (₹)</th>
    <th style="padding: 10px;">Percentage Gain/Loss (%)</th>
</tr>
"""

    for i, d in enumerate(portfolio, start=1):
        gain_loss_color = "#008000" if d["difference"] >= 0 else "#ff0000"
        table_html += f"""
    <tr style="margin: 5px; padding: 10px;">
        <td style="padding: 10px; text-align: center;">{i}</td>
        <td style="padding: 10px;">{d["scripname"]}</td>
        <td style="padding: 10px;">{int(d["QTY"])}</td>
        <td style="padding: 10px;">{round(d["AVGCOST"], 2)}</td>
        <td style="padding: 10px;">{round(float(d["LTP"]), 2)}</td>
        <td style="padding: 10px;">{round(d["InvestmentValue"], 2)}</td>
        <td style="padding: 10px;">{round(d["MarketValue"], 2)}</td>
        <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{round(d["difference"], 2)}</td>
        <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{round(d["difference%"], 2)}%</td>
    </tr>
    """
    summary_portfolio = get_portfolio_summary(reliance_userid, reliance_token, reliance_accid)
    table_html += f"""
<tr style="background-color: #e0e0e0; font-weight: bold;">
    <td colspan="5" style="text-align: right; padding: 10px;">Overall Portfolio Summary</td>
    <td style="padding: 10px;">{round(float(summary_portfolio["CostValue"]), 2)}</td>
    <td style="padding: 10px;">{round(float(summary_portfolio["Mkt_Value"]), 2)}</td>
    <td style="padding: 10px; color:{"#008000" if float(summary_portfolio["UnRealised"]) >= 0 else "#ff0000"}; font-weight: bold;">{round(float(summary_portfolio["UnRealised"]), 2)}</td>
    <td style="padding: 10px; color:{"#008000" if float(summary_portfolio["AbsPer"]) >= 0 else "#ff0000"}; font-weight: bold;">{round(float(summary_portfolio["AbsPer"]), 2)}%</td>
</tr>
"""


    table_html += "</table><br>"


    return table_html

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

def send_mail(str, to, cc):
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL
    sender_email = "authoritytendermanagement@gmail.com"
    password = "jnue bwjv vseu ntyk"  # Use the generated app password
    receiver_email = to
    cc_email = cc
    subject = f"Portfolio Summary for Ketan [date - {datetime.datetime.today().date()}]"
    body = f"""\
    {str}"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to)
    message["Cc"] = ", ".join(cc)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Exception:", e)

def get_sip_mutual_fund_data():
    session = requests.session()

    session_url = "https://shahinv.wealthmagic.in/"

    payload='__VIEWSTATE=%2FwEPDwUKLTgyMzEwMzk3Ng9kFgJmD2QWDgIFDxYCHgNzcmMFKH4vSW1hZ2VIYW5kbGVyLmFzaHg%2FaW1hZ2VJRD1JTlZFU1RPUkxPR09kAgcPFgIeB1Zpc2libGVoZAIJDxYCHglpbm5lcmh0bWwFCjk4OTg5OTk4MTFkAgsPFgIfAgUeTWFpbCBJRDogbmFpdGlrbXNoYWhAZ21haWwuY29tZAIXDxYCHwIFG1NIQUggSU5WRVNUTUVOVCBDT05TVUxUQU5UU2QCGQ8WAh8CBRYyMy8yNCwgS2F2ZXJpIENvbXBsZXgsZAIbDxYCHwIFE05hdmFwYXJhLCBCaGF2bmFnYXJkZH9Xyf2tm0Ihj4CpWKM%2FOvCPOsVIFSpDZX%2BYW2WScLoZ&__EVENTVALIDATION=%2FwEdAA3IknD155gK044g3IHcykqvzMfdf1SCzaerLkyvZSvSMr3AemLN%2BEUjX9s2qlvhkSZ2NvjHOkq5wKoqN6Aim8WGop4oRunf14dz2Zt2%2BQKDEMiXDnca0jLUXCrxNEVt8Wk15XIrO4rDl1XK%2FwHi%2FZtcCR1A8gUSyycTKQV%2BcfJPt7YxRTOwrRPvxWS2JKbW1qvZSBEyYVEUHTBPdIEnjDeEsHSRJtf6jc3RzuXHUc6l33haDblFtgwdBawW5RMPkuDq%2B8KAFXmT90AD%2FaBcOEqIpTAC%2BENjPnOTNH4WeIOTovoHlcMW3zJM%2F8t3ljlxCGk%3D&txtLoginID=ketanmakwana2906%40gmail.com&txtPassword=290603&btnLogin=Login&txtPANNo=&txtMOB=&txtEMAILADD=&txtOTPNo='
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = session.post(session_url, headers=headers, data=payload, verify=False)

    url = "https://shahinv.wealthmagic.in/MutualFund/DPPortFolioValuationGridReport.aspx?paraID=da4EP9blwvOxpKEozRg%2b7SrvpiCX7VaJfGqkJiRyQrcC2h%2btEkgEbhU0J8S8FquJoQCSodi6zE2eQfwCoVExGrs3OouQZAGMG6miuzZRZk9X%2fVDV9EW3UA%3d%3d"

    payload={}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Connection': 'keep-alive'
    }

    response = session.get(url, headers=headers, data=payload, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="spacing-tbl-innerpg")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        columns = row.find_all("td")
        row_data = [col.text.strip() for col in columns]  
        data.append(row_data)

    data_rows = []
    grand_total_rows = []

    for index, row in enumerate(data):
        if index > 1:
            if "Grand Total" not in row[0]:  
                data_rows.append(row)  
            else:
                grand_total_rows.append(row)  


    final_dict = {"data_rows":data_rows,"grand_total":grand_total_rows}

    print(final_dict)

    str = ""

    for index, row in enumerate(grand_total_rows, start=1):
        str += f"""<br>
    <h2> Mutual Fund(SIP) Portfolio </h2> <br>
    <b> overall mutual fund (SIP) portfolio summary </b> <br>
    total investment value : {row[5]}<br>
    total current market value : {row[7]}<br>
    Net Profit/loss : ₹({(float(row[7]) - float(row[5]))})<br>
    net Profit/loss : %({row[9]})<br><br>
    details of each Mutual Funds<br><br>
    """
    for index, row in enumerate(data_rows, start=1):
        print(row)
        str += f"""
    {index}. {row[0]}<br>
    start date : {row[2]}<br>
    current investment value : {row[5]}<br>
    current market value : {row[7]}<br>
    Net Profit/loss : ₹({(float(row[7]) - float(row[5]))})<br>
    Net Profit/loss : %({row[9]})<br><br>
    """

    table_html = """<h2>Mutual fund (SIP) Portfolio</h2><table border="1" style="border-collapse: collapse; width: 100%; text-align: left; font-family: Arial, sans-serif;">
<tr style="background-color: #f2f2f2; padding: 10px;">
    <th style="padding: 10px; text-align: center;">#</th>
    <th style="padding: 10px;">Mutual Fund Name</th>
    <th style="padding: 10px;">Start Date</th>
    <th style="padding: 10px;">Total Investment (₹)</th>
    <th style="padding: 10px;">Total Current Market Value (₹)</th>
    <th style="padding: 10px;">Net Gain/Loss (₹)</th>
    <th style="padding: 10px;">Percentage Gain/Loss (%)</th>
</tr>
"""

    for i, row in enumerate(data_rows, start=1):
        gain_loss_color = "#008000" if float(row[9]) >= 0 else "#ff0000"
        table_html += f"""
    <tr style="margin: 5px; padding: 10px;">
        <td style="padding: 10px; text-align: center;">{i}</td>
        <td style="padding: 10px;">{row[0]}</td>
        <td style="padding: 10px;">{row[2]}</td>
        <td style="padding: 10px;">{row[5]}</td>
        <td style="padding: 10px;">{row[7]}</td>
        <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{(float(row[7]) - float(row[5]))}</td>
        <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{row[9]}%</td>
    </tr>
    """
    for index, row in enumerate(grand_total_rows, start=1):
        table_html += f"""
<tr style="background-color: #e0e0e0; font-weight: bold;">
    <td colspan="3" style="text-align: right; padding: 10px;">Overall Portfolio Summary</td>
    <td style="padding: 10px;">{row[5]}</td>
    <td style="padding: 10px;">{row[7]}</td>
    <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{(float(row[7]) - float(row[5]))}</td>
    <td style="padding: 10px; color:{gain_loss_color}; font-weight: bold;">{row[9]}%</td>
</tr>
"""


    table_html += "</table>"

    return table_html
  
def get_str_for_wa_msg():
    str = get_portfolio_summary(reliance_userid, reliance_token, reliance_accid)
    str_list = get_equity_summary(reliance_userid, reliance_token, reliance_accid)
    str_list.append(get_sip_mutual_fund_data())
    str += str_list[0]
    str_remain = str_list[1:]
    return str, str_remain

def get_html_for_mail():
    str = get_equity_summary_table(reliance_userid, reliance_token, reliance_accid)
    str += get_sip_mutual_fund_data()
    return str
