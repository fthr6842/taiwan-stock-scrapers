# Modules
import pandas as pd
import requests
from io import StringIO
import os
from datetime import datetime
import sys

# Config
save_folder = r"D:\DataPool_D"
Date = "20250919"
today = datetime.today().strftime("%Y%m%d")
NameDict = {"上市個股日成交資訊":"/exchangeReport/STOCK_DAY_ALL"}

# Utils
def fetch_twse_api(api: str, encoding: str = "big5") -> pd.DataFrame:
    """
    通用型 TWSE/TPEX API 讀取函數
    :param url: API 網址 (需加上 response=csv 或 json)
    :param encoding: 預設 big5 (台灣證交所 CSV 編碼)
    :return: pandas DataFrame
    """
    url = f"https://www.twse.com.tw{api}?response=csv"
    resp = requests.get(url)
    resp.encoding = encoding

    # 移除空行
    lines = [line for line in resp.text.splitlines() if line.strip() != ""]

    # 找到 header 行
    header_index = None
    for i, line in enumerate(lines):
        if "," in line:  # 找到可能的表頭
            header_index = i
            break

    if header_index is None:
        raise ValueError("找不到表頭，請檢查 API 輸出格式")

    # 轉成 DataFrame
    csv_text = "\n".join(lines[header_index:])
    df = pd.read_csv(StringIO(csv_text), header=0)
    # 檢查最後一個col是否全為nan
    if df.shape[1] > 0:  
        last_col = df.columns[-1]
        if df[last_col].isna().all():
            df = df.drop(columns=[last_col])
    # 檢查證券代號        
    if "證券代號" in df.columns:
        df["證券代號"] = df["證券代號"].astype(str).str.replace(r'^="(.+)"$', r'\1', regex=True)
    # 強制轉型為str
    df = df.astype(str)
    return df

def dev_tools (api:str, encoding: str = "utf-8"):
    """
        爬蟲測試工具
    """
    #url = f"https://www.twse.com.tw{api}?response=csv"
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    resp = requests.get(url)
    resp.encoding = encoding
    print(resp.status_code)
    #df = pd.read_csv(StringIO(resp.text))
    # 移除空行
    #lines = [line for line in resp.text.splitlines() if line.strip() != ""]
    return resp.text

# 測試區域
#df = fetch_twse_api("/exchangeReport/MI_INDEX")
df = dev_tools ("/exchangeReport/TWTB4U")


# 執行區域
if __name__ != "__main__":
    print("基本參數:")
    print("資料儲存資料夾: ", save_folder)
    x = input("是否使用系統時間(Y/N)")
    if x == "Y":
        Date = today
    elif x == "N":
        Date = Date 
    else:
        print("輸入錯誤...")
        sys.exit()
    
    for name, path in NameDict.items():
        print(f"抓取資料：{name} ...")
        try:
            df = fetch_twse_api(path)
            filename = f"{Date}_{name}.csv"
            filepath = os.path.join(save_folder, filename)
            #df.to_csv(filepath, index=False, encoding="utf-8-sig")
            print(df.head())
            print(f"完成，已存檔到 {filepath}\n")
        except Exception as e: print(f"{name} 抓取失敗：{e}\n")
    
    end = input("程式執行完畢, 按下任意鍵結束!")

