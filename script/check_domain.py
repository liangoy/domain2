from database.mongodb import DB
from utils.agent import is_registered

if __name__ == '__main__':
    while True:
        try:
            domains = [i['domain'] for i in DB.digit6.find({'status': {'$in': ['', -1]}}).limit(64)]
            output = is_registered(domains)
            for i in output:
                DB.digit6.update_one({'domain': i['domain']}, {'$set': {'status': i['status']}})

            a1 = len([i for i in output if i['status'] == 1])
            a_1 = len([i for i in output if i['status'] == -1])
            a0 = len([i for i in output if i['status'] == 0])
            print(a0, a1, a_1)
        except Exception as e:
            print(e)
