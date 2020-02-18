import csv
import os

inputFileName = "abi.developmental_matrix.CE.csv"
outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

with open(inputFileName, 'rb') as inFile, open("headers",'rb') as headerF,open(outputFileName, 'wb') as outfile:
    r = csv.reader(inFile)
    h = csv.reader(headerF)
    w = csv.writer(outfile)
    
    head=[]
    for d in h:
        head.append(d[0])

    next(r, None)  # skip the first row from the reader, the old header
    # write new header
    w.writerow(head)

    # copy the rest
    for row in r:
        w.writerow(row)
