from file_work import *

def read_in():
    """
    Function to read input data which will be used to create indices
    """
    in_file = open("input.txt", "r")
    reviews = open("reviews.txt", "w")
    pterms = open("pterms.txt", "w")
    rterms = open("rterms.txt", "w")
    scores = open("scores.txt", "w")

    # various counters
    counter = 1
    for line in in_file:
        if line != '\n':
            # split string based on position of ':'
            header = line.split(':', 1)[0]
            line = line.split(':', 1)[-1].rstrip('\n') + ","
            # replace quotation marks and slashes
            line = line.replace('"', ' &quot; ')
            line = line.replace("\\", "\\\\")
            review_work(header, line, reviews, counter)
            pterm_work(header, line, pterms, counter)
            rterm_work(header, line, rterms, counter)
            score_work(header, line, scores, counter)
        else:
            counter = counter + 1

    in_file.close()
    reviews.close()
    pterms.close()
    rterms.close()
    scores.close()

if __name__ == "__main__":
    read_in()
