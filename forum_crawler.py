from LinkParser import LinkParser
import sys
import re
import csv


def spider(url):  

    pAnswers = re.compile('\d+ Answers')
    pQuestions = re.compile('\d+ Questions')
    pComments = re.compile('\d+ Comments')

    results = []

    try:
        parser = LinkParser()
        data, links = parser.getLinks(url)

        rs = pQuestions.search(data)
        if rs is not None:
            results.append(rs.group())
        else:
            results.append("N/A")

        rs = pAnswers.search(data)
        if rs is not None:
            results.append(rs.group())
        else:
            results.append("N/A")

        rs = pComments.search(data)
        if rs is not None:
            results.append(rs.group())
        else:
            results.append("N/A")

        return results

    except:
        print(" **Failed!**", sys.exc_info())


def read_csv(filename):
    accounts = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            accounts.append(row)
    return accounts

def write_csv(accounts):
    outfile = open('accounts_details.csv', 'w', newline='')
    csvwriter = csv.writer(outfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Account", "Url", "Questions", "Answers", "Comments"])
    for acc in accounts:
        csvwriter.writerow(acc)
    outfile.flush()
    outfile.close()


def crawl():
    accounts = read_csv("accounts.csv")
    pNumber = re.compile('\d+')
    for acc in accounts:
        rs = spider(acc[1])
        print(acc, rs)
        for item in rs:
            if item != 'N/A':
                acc.append(pNumber.match(item).group())
            else:
                acc.append(item)
        
    return accounts

accounts = crawl()
write_csv(accounts)
