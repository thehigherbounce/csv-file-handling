import csv
import os
import sys
from datetime import datetime


csv_main_fields = ['Timestamp', 'Direction', 'Symbol', 'Share Count', 'Price', 'Commissions'] # fields

def makeNewCsvData(oldCsv):
    f = open(oldCsv)
    csv_f = csv.reader(f)

    csv_data = []
    for idx, row in enumerate(csv_f): # read csv rows one by one
        if idx > 0: # ignore first row
            new_row = { # make new row with dictionary, it can be changable by old.csv file.
                "Symbol": "",
                "Direction": "",
                "Price": "",
                "Timestamp": '',
                "Share Count": "",
                "Commissions": "",
            } # format new row
            keyAry = list(new_row.keys()) # convert keys to array
            cnt = 0
            for index, cell in enumerate(row):
                if index == 3 or index > 4 and index < 8: # ignore unneccsary fields
                    pass
                else:
                    if index == 1: # handle description
                        cell = cell[0].lower()
                    if index == 2: # handle price
                        cell = cell.splitlines()
                        cell = cell[1].strip("$")
                    if index == 4: # handle timefield
                        dateAry = cell.splitlines()
                        time = datetime.strptime(dateAry[0], "%I:%M:%S %p") # convert pm am to 24 hours
                        dateAry[0] = time.strftime("%X")
                        cell =  " ".join(dateAry)
                    if index == 8:
                        cell = cell.replace(",", "")
                    new_row[keyAry[cnt]] = cell # set cell
                    cnt += 1
            # start change order by main fields
            tmp = {}
            for field in csv_main_fields:
                tmp[field] = new_row[field]
            new_row = tmp
            # end
            csv_data.append(new_row)
    return csv_data

def makeNewCsvFile(newfile, context):
    with open(newfile, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(csv_main_fields) # write first row with field names
        for row in context:
            writer.writerow(list(row.values()))
    print("#############> " + newfile + " is created successfully!")
                
            
def main(argv):
    oldCsv = argv[0]
    newfile = os.path.splitext(oldCsv)[0]
    newfile += '-clean.csv'

    context = makeNewCsvData(oldCsv)
    makeNewCsvFile(newfile, context)


if __name__ == "__main__":
    main(sys.argv[1:])