import csv
import geohash

filename = "Parking_Tags_Data_2015_1_Geocoded.csv"    ## The original csv file
out_filename = "out_Parking_Tags_Data_2015_1.csv"   ## the file you want to save with zipcode

if __name__ == "__main__":
    with open(filename, 'r') as csvFile:
        with open(out_filename, 'w') as outFile:
            r = csv.reader(csvFile)
            w = csv.writer(outFile, lineterminator='\n')

            all = []
            row = next(r)
            row.append("Geohash")
            row.append("row_key")
            all.append(row)

            for row in r:
                lon = row[12]
                lat = row[13]
                ghash = geohash.encode(float(lat),float(lon),precision=9)
                row.append(ghash)

                row_key = ghash[3:] # omit commix prefix "dpz"
                while len(row[5]) < 4:
                    row[5] = '0' + row[5]
                row_key += row[5]
                row_key += row[0][-2:]  #row_key: geohash后六位+时间4位+tag_number后两位

                row.append(row_key)
                all.append(row)

            w.writerows(all)