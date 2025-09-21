# 負責TWSE上市公司ESG資料爬蟲與整合
# ===============================
# Modules
import pandas as pd
import requests
import os
from datetime import datetime
import json

# Confid
save_folder = r"D:\DataPool_D"
today = datetime.today().strftime("%Y%m%d")
filename = f"{today}_TWSE_Listed_Companies_ESG_data.csv"
filepath = os.path.join(save_folder, filename)
url = "https://openapi.twse.com.tw/v1/opendata/t187ap46_L_"

# Utils
def dev_tools (url, encoding: str = "utf-8"):
    """
        爬蟲測試工具
    """
    def subprocess (url):
        resp = requests.get(urlSet[i])
        resp.encoding = encoding
        data_list = json.loads(resp.text)
        df = pd.DataFrame(data_list)
        return df
    urlSet = [url + str(i) for i in range(1, 20 + 1)]
    for i in range(0, len(urlSet)):
        print(f"爬取網址: {urlSet[i]}")
        try:
            if i == 0:
                df = subprocess(urlSet[i])
            else:
                df_temp = subprocess(urlSet[i])
                df_temp_dropped = df_temp.iloc[:, 4:]  # 從第 4 欄開始取 (index 0 起算)
                df = pd.concat([df, df_temp_dropped], axis=1)
        except Exception as e: print(f"{urlSet[i]}抓取失敗：{e}\n")
    return df

if __name__ == "__main__":
    
    df = dev_tools(url)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    
    print("The end!")
