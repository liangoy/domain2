from database.mongodb import DB
import time

if __name__ == '__main__':
    while True:
        domains_to_register = DB.digit6.find()  # !!!!
        register()  # !!!!!!
        fn()  # !!!!!!!
        time.sleep(60)
