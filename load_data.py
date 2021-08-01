import server
from load_data.load_data import load_all, clear_db

if __name__ == '__main__':
    clear_db()
    load_all()