import csv

filename = "out_Parking_Tags_Data_2015_1.csv"    ## The original csv file
out_filename = "avg_out_Parking_Tags_Data_2015_1.csv"   ## the file you want to save with zipcode


def getavg(dict):
    size = len(dict)
    count = 0
    for key, value in dict.items():
        count += value
    print(size)
    print(count)
    return float(count) / float(size)

if __name__ == "__main__":
    with open(filename, 'r') as csvFile:

        r = csv.reader(csvFile)

        all = []
        row = next(r)
        row.append("Geohash")
        row.append("row_key")
        all.append(row)
        geohash_dict6 = dict()
        geohash_dict7 = dict()
        geohash_dict8 = dict()
        geohash_dict9 = dict()

        for row in r:
            rowkey = row[0]
            precision6 = rowkey[:3]
            precision7 = rowkey[:4]
            precision8 = rowkey[:5]
            precision9 = rowkey[:6]
            if precision6 in geohash_dict6:
                geohash_dict6[precision6] += 1
            else:
                geohash_dict6[precision6] = 1

            if precision7 in geohash_dict7:
                geohash_dict7[precision7] += 1
            else:
                geohash_dict7[precision7] = 1

            if precision8 in geohash_dict8:
                geohash_dict8[precision8] += 1
            else:
                geohash_dict8[precision8] = 1

            if precision9 in geohash_dict9:
                geohash_dict9[precision9] += 1
            else:
                geohash_dict9[precision9] = 1

        avg6 = getavg(geohash_dict6)
        avg7 = getavg(geohash_dict7)
        avg8 = getavg(geohash_dict8)
        avg9 = getavg(geohash_dict9)


        print(avg6)
        print(avg7)
        print(avg8)
        print(avg9)

