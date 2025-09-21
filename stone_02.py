# 負責上市公司基本資料爬蟲
# =======================
# Modules
import pandas as pd
import requests
import os
from datetime import datetime
import json

#Config
url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
save_folder = r"D:\DataPool_D"
today = datetime.today().strftime("%Y%m%d")
filename = f"{today}_TWSE_Listed_Companies.csv"
filepath = os.path.join(save_folder, filename)

#utils
def dev_tools (url, encoding: str = "utf-8"):
    """
        爬蟲測試工具
    """
    resp = requests.get(url)
    resp.encoding = encoding
    print(resp.status_code)
    data_list = json.loads(resp.text)
    df = pd.DataFrame(data_list)
    return df

# 執行區域
if __name__ == "__main__":
    
    df = dev_tools(url)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    
    print("The end!")