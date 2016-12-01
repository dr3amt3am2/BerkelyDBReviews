import re
from specified_searches import *
from bsddb3 import db
from datetime import datetime


def handle_query(query, db_objs):
    query = query.replace("'", "")
    query = query.split(" ")
    if len(query) == 1:
        final_results = _handle_query(query[0], db_objs)

    if len(query) == 2:
        # case 5
        # need to handle the equality join
        # make a new database
        print("Join mode enabled")
        results1 = _handle_query(query[0], db_objs)
        results2 = _handle_query(query[1], db_objs)
        final_results = list(set(results1) & set(results2))
        final_results.sort()
        print(str(len(final_results)) + " reviews satisfy both conditions.")

    if len(query) == 3:
        final_results = _handle_query(query[0]+query[1]+query[2], db_objs)

    if len(query) >= 4:
        print("Join mode enabled")

        query = swap_if_necessary(query)
        # limiting indices
        length = len(query)
        list_index = 0 # always points to most recent results
        i = 1
        results = list()

        results.append(_handle_query(query[0], db_objs))
        while i < length:
            if query[i] == 'rscore':
                results.append(_handle_query(query[i]+query[i+1]+query[i+2], db_objs))
                list_index = list_index + 1
                results.append(list(set(results[list_index]) & set(results[list_index-1])))
                list_index = list_index + 1
                i = i + 3
                results[list_index].sort()
            elif query[i] == 'pprice':
                print("Searching by price")
                results.append(price_search(query[i+1], query[i+2], results[list_index], db_objs[0]))
                list_index = list_index + 1
                i = i + 3
            elif query[i] == 'rdate':
                print("Searching by date")
                results.append(date_search(query[i+1], query[i+2], results[list_index], db_objs[0]))
                list_index = list_index + 1
                i = i + 3
            else:
                # query is likely a second/third/etc search keyword
                results.append(_handle_query(query[i], db_objs))
                list_index = list_index + 1
                results.append(list(set(results[list_index]) & set(results[list_index-1])))
                list_index = list_index + 1
                i = i + 1
        final_results = results[list_index]
        print(str(len(final_results)) + " results satisfy all conditions")


    # print results
    for i in final_results:
        print('Displaying Review #%s' % i)
        print_review(db_objs[0], i)
        if len(final_results) <= 1:
            break
        next_rev = input("display next? [y/N]: ")
        if next_rev == 'y':
            continue
        else:
            break


def _handle_query(query, db_objs):
    # unpack db objs
    reviews = db_objs[0]
    pterms = db_objs[1]
    rterms = db_objs[2]
    scores = db_objs[3]

    # check if there is colon specifier
    specifier = None  # None for now
    query = query.split(":")
    if len(query) == 2:
        # there is a specifier
        specifier = query[0]
        query = query[1]
    else:
        query = query[0]

    # various syntaxical decisions...
    if specifier == "p":
        print("Product Name Term Search Specified.")
        return p_term_search(query, pterms)
    if specifier == "r":
        print("Review Text Term Search Specified")
        return r_term_search(query, rterms)
    if specifier is None:
        if query[0:6] == 'rscore':
            print("Searching based on review rating...")
            return score_search(query[6:len(query)], scores)
        else:
            print("Searching Product Name and Review Text")
            return search_all(query, pterms, rterms)


def print_review(reviews,idno):
    result = reviews.get(idno.encode('utf-8')).decode('utf-8') # string dump
    re_quote = re.compile(',"(.+?)"') # regex for split by quotes
    # split fields by quotes
    quote = re.split(re_quote, result) 
    # save fields inside quotes
    info = {'tit':quote.pop(1).replace('&quot;', '\"'), 
    'nam':quote.pop(2).replace('&quot;', '\"'),
    'summ':quote.pop(3).replace('&quot;', '\"'), 
    'txt':quote.pop(4).replace('&quot;', '\"')}
    # rebuild with fields out of quotes and split by commas
    comma = ''.join(quote).split(',')
    # save fields between commas
    info.update({'pid':comma[0],'pri':comma[1],'uid':comma[2],
    'hel':comma[3],'sco':comma[4],'tim':datetime.fromtimestamp(int(comma[5]))})
    # print fields
    print("ID: %s\nTitle: %s\nPrice: %s\nUserId: %s\nprofName: %s\n"\
    "Helpfulness: %s\nScore: %s\nDate: %s\nSummary: %s\nText: %s" 
    % (info['pid'], info['tit'], info['pri'], info['uid'], info['nam'], 
    info['hel'], info['sco'], info['tim'], info['summ'], info['txt']))


def swap_if_necessary(query):
    nQuery = [' ']
    i = 0
    while query[i] == 'rscore' or query[i] == 'pprice' or query[i] == 'rdate':
       nQuery.append(query[i].strip())
       nQuery.append(query[i+1].strip())
       nQuery.append(query[i+2].strip())
       i = i + 3
    nQuery[0] = query[i].strip()
    nQuery = nQuery + query[i+1:len(query)]
    return nQuery
