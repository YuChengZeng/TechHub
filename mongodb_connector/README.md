# MongoDB重新連線問題(AutoReconnect)

## 如何正確建立連線
1. 安裝pymongo
```bash
pip install pymongo
```
2. 連接到mongoDB 
```python!
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['your_database_name']
```
3. 如有需要，可將連線行為單獨存到db_config,py以便日後維護和做特殊處理
## 如何正確的自動重連
目標：重新連接的邏輯：檢查頻率、檢查條件、重新連接次數、重新連接時間(延遲)、特定log
pympngo本身有連線池的機制，會自動處理重新連線。
### 錯誤處理
* 如果DB超過時間無回應就會出現AutoReconnect錯誤，表示pymongo自動重連後失敗，會拋出錯誤並繼續嘗試重新連線。
* 如果重啟container，pymongo會自動重新連上db -> 正常使用
* 對於特殊的DB指令，如某項insert需要確保一定會執行，可以把該指令單獨放在一個while內特殊處理。

## 需不需要關閉連線？

pymongo如果close MongoDBClient，從連線池刪掉這個client開啟的連線，如果要重新連線必須重新初始化MongoDBClient。根據mongoDB的文件，並不需要主動做close，頂多在應用程式結束時，比如說fastapi結束時再close。

---


## 總結

* pymongo內建有自動重連的機制，若是自動重連失敗的話會噴出AutoReconnect的error，原本的pymongo指令就會被跳過(比如insert_one被跳過)，針對有需要保證成功的db指令，我們可以再去用try except 處理AutoReconnect
* client 和db 如果手動重新連線可能會出現原本的資料被覆蓋掉，而導致出現衝突或錯誤

## Resource
https://devpress.csdn.net/mongodb/62f1ff1ac6770329307f5c3b.html
https://blog.csdn.net/az9996/article/details/110181518

## 範例

### 目錄結構
```bash!
mongodb_connector/
├── Dockerfile
├── README.md
├── app
│   ├── common
│   │   └── __init__.py
│   ├── dal.py
│   ├── db_config.py
│   ├── main.py
│   ├── model.py
│   └── services.py
├── docker-compose.yml
├── requirements.txt
└── static
    └── index.html
```