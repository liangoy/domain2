from database.mongodb import DB
from utils.agent import is_registered

if __name__ == '__main__':
    while True:
        try:
            domains = [i['domain'] for i in DB.digit6.find({'status': ''}).limit(200)]
            output = is_registered(domains)
            for i in output:
                DB.digit6.update({'domain': i['domain']}, {'$set': {'status': i['status']}})
            print(len(domains))
        except Exception as e:
            print(e)
