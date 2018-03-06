from database.mongodb import DB
from utils.agent import is_registered

if __name__=='__main__':
    while True:
        try:
            domains=DB.digit6.find({'status':''})#!!!!!
            output=is_registered(domains)
            DB.update()#!!!!!!!
        except Exception as e:
            print(e)
