import csv
from datetime import datetime


def p_term_search(query, pt_obj):
    if query[-1] == '%':
        results = _term_search(query, pt_obj.cursor())
        print(str(len(results)) + " reviews were found with " + query +
          " in their product name")
        return results      
    else:
        return _p_term_search(query, pt_obj)


def r_term_search(query, rt_obj):
    if query[-1] == '%':
        results = _term_search(query, rt_obj.cursor())
        print(str(len(results)) + " reviews were found with " + query +
              " in their review text/summary")
        return results
    else:
        return _r_term_search(query, rt_obj)


def _p_term_search(query, pt_obj):
    found = set()  # MUCH faster for duplicate checking than list
    results = list()
    cur = pt_obj.cursor()
    temp = cur.set(query.encode("utf-8"))

    # let's go crazy.
    while True:
        if temp is not None:
            if temp[1] not in found:
                found.add(temp[1])
                results.append(temp[1].decode('utf-8'))
        else:
            break  # once all duplicates are found exit loop
        temp = cur.next_dup()

    print(str(len(results)) + " reviews were found with " + query +
          " in their product name")
    cur.close()
    return results


def _r_term_search(query, rt_obj):
    found = set()  # MUCH faster for duplicate checking than list
    results = list()
    cur = rt_obj.cursor()
    temp = cur.set(query.encode("utf-8"))

    # let's go crazy.
    while True:
        if temp is not None:
            if temp[1] not in found:
                found.add(temp[1])
                results.append(temp[1].decode('utf-8'))
        else:
            break  # once all duplicates are found exit loop
        temp = cur.next_dup()

    print(str(len(results)) + " reviews were found with " + query +
          " in their review text/summary")
    cur.close()
    return results


def search_all(query, pt_db, rt_db):
    # concatenate results
    results = p_term_search(query, pt_db) + r_term_search(query, rt_db)
    print(str(len(results)) + " reviews were found with " + query +
          " in their review text/summary or product name")
    return results


def r_p_term_search(query, pt_obj):
    cur = pt_obj.cursor()
    cur.set_range(query[0:-1].encode("utf-8"))
    return _term_search(query, cur)


def r_r_term_search(query, rt_obj):
    cur = rt_obj.cursor()
    cur.set_range(query[0:-1].encode("utf-8"))
    return _term_search(query, cur)


def _term_search(query, cur):
    found = set()  # MUCH faster for duplicate checking than list
    found.add(None)
    results = list()
    temp = cur.set_range(query[0:-1].encode('utf-8'))
    keys = set()
    key = temp[0]
    while True:
        if temp not in found:
            found.add(temp)
            results.append(temp[1].decode('utf-8'))
            temp = cur.next_dup()
        if temp is None:
            temp = cur.next_nodup()
        if temp[0].decode("utf-8")[0:len(query)-1] != query[0:-1]:
                break
    # remove duplicates
    results = list(set(results))
    results.sort()
    cur.close()
    return results


def score_search(query, sc_obj):
    found = set()
    results = list()
    cur = sc_obj.cursor()
    in_arg = str(float(query[1])).encode('utf-8')  # format value so bdb reads
    # algorithm essentially searches from first set marker fulfilling
    # condition until condition is no longer true
    if query[0] == '>':
        # go forward
        temp = cur.set_range(in_arg)
        temp = cur.next_nodup()
        while temp is not None:
            if temp not in found:
                found.add(temp)
                results.append(temp[1].decode('utf-8'))
                temp = cur.next_dup()
            else:
                temp = cur.next_nodup()
                if temp is None:
                    break
                if float(temp[0].decode('utf-8')) <= float(query[1:len(query)]):
                    break
    else:
        temp = cur.first()
        # go backwards
        while temp is not None:
            if temp not in found:
                found.add(temp)
                if float(temp[0].decode("utf-8")) < float(query[1:len(query)]):
                    results.append(temp[1].decode('utf-8'))
                    temp = cur.next_dup()
            else:
                temp = cur.next_nodup()
                if temp is None:
                    break
                if float(temp[0].decode("utf-8")) >= float(query[1:len(query)]):
                    break

    cur.close()
    print(str(len(results)) + " results.")
    return results


def price_search(operator, price, reviews, database):
    final_results = list()
    price = float(price)
    if operator == '>':
        for reviewno in reviews:
            # find all with price greater than
            text = database.get(reviewno.encode('utf-8')).decode('utf-8')
            reader = next(csv.reader([text]))
            if reader[2] != 'unknown':
                if float(reader[2]) > price:
                    final_results.append(reviewno)
    else:
        for reviewno in reviews:
            # find all with price less than
            text = database.get(reviewno.encode('utf-8')).decode('utf-8')
            reader = next(csv.reader([text]))
            if reader[2] != 'unknown':
                if float(reader[2]) < price:
                    final_results.append(reviewno)

    return final_results


def date_search(operator, date, reviews, database):
    # some initial variable declarations
    final_results = list()
    date = datetime.strptime(date, "%Y/%m/%d")
    if operator == '<':
        # find all with date after (greater than means later)
        for reviewno in reviews:
            # find date
            text = database.get(reviewno.encode('utf-8')).decode('utf-8')
            reader = next(csv.reader([text]))
            temp_date = datetime.fromtimestamp(int(reader[7]))
            if date > temp_date:
                final_results.append(reviewno)
    else:
        # find all with date before (less than means earlier)
        for reviewno in reviews:
            # find date
            text = database.get(reviewno.encode('utf-8')).decode('utf-8')
            reader = next(csv.reader([text]))
            temp_date = datetime.fromtimestamp(int(reader[7]))
            if date < temp_date:
                final_results.append(reviewno)

    return final_results



