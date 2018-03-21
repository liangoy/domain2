if __name__=='__main__':
    import sys
    print(sys.path.append('../'))

from database.mongodb import DB
import time
from utils.agent import register_domain2

if __name__ == '__main__':
    while True:
        try:
            domains = [i['domain'] for i in DB.digit6.find({'status': 0, 'is_ours': 0}).sort('error').limit(10)]
            output = register_domain2(domains)
            print(output)
            for i in output:
                if i['status'] == 0:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'status': 1}})
                if i['status'] == 1:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'status': 1, 'is_ours': 1}})
                if i['status'] < 0:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'error': int(time.time())}})

            a1 = len([i for i in output if i['status'] == 1])
            a0 = len([i for i in output if i['status'] == 0])
            a_1 = len([i for i in output if i['status'] == -1])
            print(a0, a1, a_1)
            if len([i for i in output if i['status'] == -2]) > 0:
                print('出现链接断开错误，休眠7分钟')
                time.sleep(60 * 7)
            if len([i for i in output if i['status'] < 0]) == len(output):
                print('全部出错，休眠5分钟')
                time.sleep(60 * 5)
        except Exception as e:
            print(e)
