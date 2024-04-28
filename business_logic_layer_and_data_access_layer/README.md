# 使用Docker-Compose部屬 FastAPI, MongoDB

## 目標
透過實作登入系統，了解DAL和BLL分離設計。
Data Access Layer(DAL)和Business Logic Layer(BLL)分離
    - DAL將與資料庫的溝通分離出來
    - BLL透過使用DAL資料的方式進行邏輯處理
1. FastAPI 
    - get api
    - post api
2. MongoDB
    - Read
    - Write
    
功能說明：
    * 帳號申請
    * 登入驗證
    * 密碼更改
    * 帳號刪除

## 架設環境
Docker Desktop
WSL ubuntu 22.04
## 目錄結構
```
project
├── Dockerfile
├── README.md
├── app
│   ├── common
│   │   └── __init__.py
│   ├── dal.py
│   ├── main.py
│   ├── model.py
│   ├── myfile.log
│   └── services.py
├── docker-compose.yml
└── requirements.txt
```
### 操作指令
在docker-compose.yml所在目錄
#### 啟動

```bash
docker-compose up -d
```
#### 停止
```bash
socker-compose down
```
如果更新了程式碼必須重新啟動服務才會生效。
#### 查看服務
查看啟動的容器狀態
```
docker-compose ps
```

#### 看log
```
docker-compose logs name
```
> 或直接使用Docker Desktop操作
