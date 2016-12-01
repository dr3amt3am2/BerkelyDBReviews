from mod_tools import ModTools
import re


def review_work(header, line, file_obj, counter):
    write_flag = False  # only write out if line belongs in reviews
    line = line[1: -1]  # remove leading whitespace
    # for productid (also needs index no.)
    if header == "product/productId":
        line = ModTools.add_comma(str(counter)) + ModTools.add_comma(line)
        write_flag = True

    # requires a comma and nothing else
    if header == "product/price" or header == "review/userId" or \
            header == "review/helpfulness" or header == "review/score" \
            or header == "review/time":
        line = ModTools.add_comma(line)
        write_flag = True

    # product title, profile name, review summary and review text all
    # require "" around them as well as a comma
    if header == "product/title" or header == "review/profileName" or \
            header == "review/summary":
        line = ModTools.add_quotes(line)
        line = ModTools.add_comma(line)
        write_flag = True

    # requires quotation marks but a newline instead of a comma
    if header == "review/text":
        line = ModTools.add_quotes(line)
        line = ModTools.add_new_line(line)
        write_flag = True

    # write out the string!
    if write_flag is True:
        file_obj.write(line)


def pterm_work(header, line, file_obj, counter):
    line = line[1: -1]  # remove leading whitespace
    line = line.lower()  # make case insensitive

    if header == "product/title":
        # return split words and check length, then write
        # remove commas
        line = line.replace("&#39", "'")
        line = line.replace("'", " ")
        line = re.sub('\W', " ", line)
        """
        line = line.replace(",", " ").replace("'", " ").replace("(", " ").replace(")", " ")
        line = line.replace("-", " ").replace("`", " ").replace("/", " ").replace(";", " ")
        line = line.replace("$", " ").replace("&", " ").replace("^", " ").replace("%", " ")
        line = line.replace("*", " ").replace("@", " ").replace("!", " ").replace("?", " ")
        line = line.replace("|", " ").replace("}", " ").replace("{", " ").replace("=", " ")
        line = line.replace("+", " ").replace("[", " ").replace("]", " ").replace(">", " ").replace("<", " ")
        """
        for word in line.split():
            if len(word) >= 3:
                file_obj.write(ModTools.add_comma(word) + str(counter) + "\n")


def rterm_work(header, line, file_obj, counter):
    line = line[1: -1]  # remove leading whitespace
    line = line.lower()  # make case insensitive
    line = line.replace("&#39", "'")
    line = line.replace("'", " ")

    line = re.sub('\W', " ", line)
    # remove special characters
    """
    line = line.replace(".", " ").replace(":", " ").replace(",", " ").replace(";", " ")
    line = line.replace("-", " ").replace("!", " ").replace("?", " ").replace("/", " ")
    line = line.replace(")", " ").replace("(", " ").replace("'", " ").replace("`", " ")
    line = line.replace("$", " ").replace("&", " ").replace("^", " ").replace("%", " ")
    line = line.replace("*", " ").replace("@", " ").replace("|", " ").replace("[", " ")
    line = line.replace("}", " ").replace("{", " ").replace("+", " ").replace("=", " ")
    line = line.replace("]", " ").replace(">", " ").replace("<", " ")
    """

    if header == "review/text" or header == "review/summary":
        # return split words and check length, then write
        for word in line.split():
            if len(word) >= 3:
                file_obj.write(ModTools.add_comma(word) + str(counter) + "\n")


def score_work(header, line, file_obj, counter):
    line = line[1: -1]  # remove leading whitespace

    if header == "review/score":
        # write score and review no.
        file_obj.write(ModTools.add_comma(line) + str(counter) + "\n")
