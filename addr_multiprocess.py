from multiprocessing import Pool
import multiprocessing
from geopy.geocoders import Nominatim
import csv
import time
from itertools import islice


filename = "data/Parking_Tags_Data_2015_1.csv"    ## The original csv file
out_filename = "data/out_Parking_Tags_Data_2015_4.csv"   ## the file you want to save with zipcode


start_time = time.time()

geolocator = Nominatim()


counter = 1
def process_row(row):
    addr = row[7] + ' Toronto'   # index for address is 7 in a row
    expire = 0

    while True:
        try:
            location = geolocator.geocode(addr)
        except:
            print "retry"
            expire += 1
            if expire < 3:
                continue
            else:
                location = None
                break
        break

    if location is not None:
        full_addr = location.raw['display_name']
        addr_split = full_addr.split(",")
        zipcode = addr_split[-2]
        longitude = location.raw['lon']
        latitude = location.raw['lat']

        row.append(zipcode)
        row.append(longitude)
        row.append(latitude)
    else:
        row.append("NA")
        row.append("NA")
        row.append("NA")
    global counter
    print "finished row " + str(counter)
    counter += 1
    return row

NUM_PROCS = multiprocessing.cpu_count()

if __name__ == "__main__":
    pool = Pool(8)

    with open(filename, 'rb') as csvFile:
        with open(out_filename, 'a') as outFile:   # 'a' is append, 'wb' is overwrite
            #head = [next(csvFile) for x in range(50,100)]
            r = csv.reader(csvFile, delimiter=',', quotechar='"')

            slice = islice(r, 400000, 400100)  # the row range you want to operate on in origin file
            w = csv.writer(outFile, delimiter=',', quotechar='"')

            resultset = pool.map(process_row, slice, 8)
            for listitem in resultset:
                try:
                    w.writerow(listitem)

                except:
                    print "line has problem"
    print("--- %s seconds ---" % (time.time() - start_time))

