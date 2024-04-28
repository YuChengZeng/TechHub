import logging

def create_logger():

    # 創建一個 logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # 設置日誌級別

    # 創建兩個 handlers：一個用於文件，一個用於控制台
    file_handler = logging.FileHandler('myfile.log')
    console_handler = logging.StreamHandler()

    # 設置日誌格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加 handlers 到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 記錄一條消息
    logger.info('這是一條僅供測試的日誌信息')

def get_logger():

    logger = logging.getLogger('my_logger')

    return logger

create_logger()