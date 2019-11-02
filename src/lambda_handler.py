import os
import json
import requests
import locale
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
today = datetime.now()

def lambda_handler(event, context):
  # デバッグ用
  print("=" * 40)
  print(event)
  print("=" * 40)
  print(context)
  print("=" * 40)
  
  # 調整さんURLを環境変数から取得する
  url = os.getenv("URL")
  if url is None:
    return {
      'text': "環境変数URLを指定してください。"
    }
    
  # 調整さんに接続してHTMLを取得する
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")
  
  # スケジュール表の取得
  schedules = []
  for tr in soup.find(id="nittei").find_all("tr"):
    schedule = [td.text.strip() for td in tr.find_all("td")]
    schedules.append(schedule)
  
  # データ加工
  # ◯は担当者の名前に、それ以外は削除
  schedules = np.array(schedules)
  schedules = np.where(schedules == '○', schedules[0], schedules)
  schedules = np.where(schedules == '△', None, schedules)
  schedules = np.where(schedules == '×', None, schedules)
  schedules = schedules[1:-1]
  
  # マスタースケジュール
  masterSchedules = np.array([convertDate(t) for t in schedules.T[0]])
  
  # 今日日付より後のスケジュール
  pickupSchedules = masterSchedules[masterSchedules > today]

  # 検索用の辞書を用意
  searchBox = {}
  for key, value in zip(masterSchedules, schedules[:, 1:]):
    searchBox[key] = value[value != None]

  # 表示
  texts = []
  for pSchedule in pickupSchedules:
    texts.append(pSchedule.strftime("%Y/%m/%d %H:%M"))
    texts.append(", ".join(searchBox[pSchedule]))
    texts.append("=" * 30)
    
  texts = "\n".join(texts)
  print(texts)
    
  return {
    'text': texts
  }


# 調整さん日付を標準日付に変更する
def convertDate(dateFormat):
  return datetime.strptime(dateFormat, "%m/%d(%a) %H:%M〜").replace(year=today.year)

# Local debug.
if __name__ == "__main__":
  print(lambda_handler(None, None))