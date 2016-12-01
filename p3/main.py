from bsddb3 import db
from handle_query import *

def main():
    db_objs = load()  # load db objs
    print("Welcome to Mini Project 2 By Tony and Joey\n")
    prompt(db_objs)
    unload(db_objs)

def prompt(db_objs):
    cont = True
    while(cont):
        query = input("Enter your query to the terminal and then hit enter.\n")
        query = fix_spaces(query)
        handle_query(query.lower(), db_objs)
        cont = input("New query? [y/N]: ")
        if cont == 'y':
            cont = True
        else:
            cont = False

def load():
    # database obj for each idx file
    reviews = db.DB()
    pterms = db.DB()
    rterms = db.DB()
    scores = db.DB()

    # load idx files into database objs
    rterms.set_flags(db.DB_DUP)
    reviews.open('../p2/rw.idx', None, db.DB_HASH, db.DB_CREATE)
    pterms.open('../p2/pt.idx', None, db.DB_BTREE, db.DB_CREATE)
    rterms.open('../p2/rt.idx', None, db.DB_BTREE, db.DB_CREATE)
    scores.open('../p2/sc.idx', None, db.DB_BTREE, db.DB_CREATE)
    return reviews, pterms, rterms, scores


def unload(db_objs):
    for database in db_objs:
        database.close()


def fix_spaces(query):
    # add spaces around > or <
    q_list = list(query)  # split into chars
    index = 0  # will need index to see characters before and after 
    while index < len(q_list):
        if q_list[index] == '>':
            if q_list[index-1] != ' ' and q_list[index+1] != ' ':
                q_list[index] = ' > '
            elif q_list[index-1] != ' ':
                q_list[index] = ' >'
            elif q_list[index+1] != ' ':
                q_list[index] = '> '
        elif q_list[index] == '<':
            if q_list[index-1] != ' ' and q_list[index+1] != ' ':
                q_list[index] = ' < '
            elif q_list[index-1] != ' ':
                q_list[index] = ' <'
            elif q_list[index+1] != ' ':
                q_list[index] = '< '
        index = index + 1
    return ''.join(q_list)

if __name__ == "__main__":
    main()
