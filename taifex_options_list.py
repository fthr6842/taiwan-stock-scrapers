# Modules
from datetime import datetime
import requests
from io import StringIO
import pandas as pd
# configs
comm_list = ["TXO", "TEO", "TFO", "TGO"]

# Utils
def taifex_options_list(date_str: str, Type, commodity_id = "TXO"):
    """
    取得台指選擇權某日某交易時段之所有可交易的合約
    input:
        date_str: str, 格式為 'YYYY-MM-DD'
        Type: int, 0 (一般交易時段); 1 (盤後交易時段)
        commodity_id: str, 商品種類 (TXO: 台指期選; TEO: 電子期選; TFO: 金融期選; TGO: 黃金期選)
    output:
        df: Dataframe, 包含該日該時段所有可供交易之台指選擇權標的
        contract_list: list, 包含該日該時段所有可供交易之台指選擇權標的(僅月份)
    """
    date = datetime.strptime(date_str, "%Y-%m-%d") # 西元紀年日期
    url = "https://www.taifex.com.tw/cht/3/optDailyMarketReport" # 行情網址
    payload = {'queryType': '2',
               'marketCode': str(Type),
               'dateaddcnt': '',
               'commodity_id': commodity_id,
               'queryDate': date.strftime('%Y/%m/%d')} # 資訊封包
    res = requests.post(url, data=payload)
    if '查無資料' in res.text:
        print("查無資料")
        return None
    try:
        tables = pd.read_html(StringIO(res.text))
        df = pd.concat(tables, axis=0, ignore_index=True)
        df = df.iloc[:, 0:3]
        df = df.iloc[:-1]
        contract_list = df["到期月份 (週別)"].unique()
        return df, contract_list
    except Exception as e:
        print("爬蟲失敗:", e)
        return None

# Exe. Zone
if __name__ == "__main__":
    for i in comm_list:
        df, contract_list = taifex_options_list("2022-01-07", 0, commodity_id=i)
        print(df.head())
        print(contract_list)
    pass
