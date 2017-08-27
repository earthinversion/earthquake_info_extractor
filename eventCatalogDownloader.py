import requests
import os
import sys
import numpy as np
import re
from datetime import datetime, date

headerstr = '''This program gathers the event information from the Global CMT website
http://www.globalcmt.org/CMTsearch.html
Monthly catalogue is available for EQs from 1994-present.
-Utpal Kumar
##############################################################'''


now = datetime.now()

# Function for downloading the catalogue


def catalogueDownload(year, month, loc):
    try:
        if year < 1976:
            print("Catalog file is not available")
            sys.exit()
        yrsuffix = str(year)[-2:]
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        filename = months[int(month) - 1] + yrsuffix

        if 2005 <= year <= now.year:
            url = 'http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/NEW_MONTHLY/%s/%s.ndk' % (str(year), filename)
            ftype = ".ndk"
            filename = filename + ftype
        elif 1994 < year <= 2004:
            url = "http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/MONTHLY/%s.dek" % (filename)
            ftype = ".dek"
            filename = filename + ftype
        elif year <= 1994:
            url = 'http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog/jan76_dec04.dek'
            ftype = ".dek"
            filename = "oldEQs" + ftype
        fullfilename = loc + "/" + filename
        if not os.path.isdir(loc):
            os.makedirs(loc)
        if not os.path.exists(fullfilename):
            print("Downloading the catalog file...")
            r = requests.get(url)
            with open(fullfilename, "wb") as file:
                file.write(r.content)
    except:
        print("ERROR downloading the data")


if __name__ == "__main__":
    print(headerstr, "\n")
    yearrange = input("Enter the year/month range(1994-present)\nFormat:'yyyy/mm-yyyy/mm'\ne.g. '2003/01-2004/12': ")
    # Checking for the input format
    rex = re.compile("^[0-9]{4}/[0-9]{2}-[0-9]{4}/[0-9]{2}$")
    if not rex.match(yearrange):
        print("Please enter the correct format")
        sys.exit()

    years1 = yearrange.split("-")
    yearS, monS = list(map(int, years1[0].split("/")))
    yearE, monE = list(map(int, years1[1].split("/")))

    if yearS > yearE or now.year < yearE:  # exit if the year entry is incorrect
        print("Please enter proper format!")
        sys.exit()
    outdir = input("Enter the path to the download directory (else Enter for current directory): ")
    if outdir == "":
        outdir = "."

    startTime = date(yearS, monS, 1)
    endTime = date(yearE, monE, 1)

    ym_start = 12 * startTime.year + startTime.month - 1
    ym_end = 12 * endTime.year + endTime.month
    for ym in np.arange(ym_start, ym_end):
        y, m = divmod(ym, 12)
        catalogueDownload(y, m, outdir)
