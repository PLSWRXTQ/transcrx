from sys import path
path.append(r'E:\CODE\WS_SAF\Python')
from Module import SocketTemplate, HttpAnalyzer
from Module.Transaltion import trans
import logging, json

logger = logging.Logger('TransServerLogger')

handler = logging.FileHandler('trans.log')
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s'))
logger.addHandler(handler)
server = SocketTemplate.Server('127.0.0.1', 1024)
with open(r'E:\CODE\WS_TPM\AzureToolbox\info.json') as f:
    info = json.load(f)
while True:
    try:
        conn = server.connect()
        requ = conn.send(None).decode('gbk')
        logging.info("Connection is successful")
        if requ:
            httpmsg = HttpAnalyzer.loads(requ)
            if 't' in httpmsg['Kernel'][1]:
                text = httpmsg['Content']
                res = trans(text)
                if conn.send(HttpAnalyzer.dumps({'Kernel': ['HTTP/1.1', '200', 'OK'], 'Access-Control-Allow-Origin': '*', 'Content': res}).encode(errors='ignore')):
                    logger.info("Connection closed")
                    info['transaltion_history'][text] = res
                    with open(r'E:\CODE\WS_TPM\AzureToolbox\info.json', 'w', encoding='utf-8') as f:
                        f.write(str(json.dumps(info)))
                else:
                    logger.error('ConnectionAbortedError passed')
    except Exception as err:
        logger.error(err.args[0])
