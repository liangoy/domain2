from database.mongodb import DB
from utils.agent import register_domain

if __name__ == '__main__':
    while True:
        try:
            domains = [i['domain'] for i in DB.digit6.find({'status': 0, 'is_ours': ''}).limit(1)]
            output = register_domain(domains)
            for i in output:
                if i['status'] == 0:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'status': 0}})
                if i['status'] == 1:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'status': 1, 'is_ours': 1}})
                if i['status'] == -1:
                    DB.digit6.update_one({'domain': i['domain']}, {'$set': {'is_ours': -1}})

            a1=len([i for i in output if i['status']==1])
            a0=len([i for i in output if i['status']==0])
            a_1=len([i for i in output if i['status']==-1])
            print(a0,a1,a_1)
        except Exception as e:
            print(e)