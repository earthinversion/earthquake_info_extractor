import os
import glob
import eventCatalogDownloader as ecd
from datetime import datetime
import re


class eventinfo:
    now = datetime.now()
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def __init__(self, yrr, mon, day, hrr, mnn):
        inp = [int(yrr), int(mon), int(day), int(hrr), int(mnn)]
        catdirpath = "./catalogs"  # catalog directory
        if 2005 <= inp[0] <= self.now.year:
            catfile = self.months[int(mon) - 1] + str(yrr)[-2:] + ".ndk"
            ftype = "ndk"
        elif 1994 < inp[0] <= 2004:
            catfile = self.months[int(mon) - 1] + str(yrr)[-2:] + ".dek"
            ftype = "dek"
        elif inp[0] <= 1994:
            catfile = "oldEQs.dek"
            ftype = "dek"
        catfilefull = catdirpath + "/" + catfile
        if not os.path.exists(catfilefull):
            try:
                ecd.catalogueDownload(inp[0], inp[1], catdirpath)
            except:
                print("The catalogue file is not available!")

        for i in range(len(inp)):
            if inp[i] < 10:
                inp[i] = "%02d" % inp[i]
            if not type(inp[i]) is str:
                inp[i] = str(inp[i])

        if ftype == "ndk":
            dd = inp[0] + "/" + inp[1] + "/" + inp[2]  # yyyy/mm/dd
            tmm = inp[3] + ":" + inp[4]  # hh:mm
            eventRecogChar = ["PDE", "ISC", "SWE"]  # PDE for USGS location, ISC for ISC catalog, SWE for surface-wave location
            with open(catfilefull) as catalog:
                for line in catalog:
                    if any(s in line for s in eventRecogChar):
                        data = line.split()
                        evtime1 = data[2].split(":")
                        evtime2 = ":".join(evtime1[0:2])
                        if dd == data[1] and tmm == evtime2:
                            self.year, self.month, self.day = data[1].split("/")
                            self.hour, self.min, self.sec = data[2].split(":")
                            self.lat = data[3]
                            self.long = data[4]
                            self.depth = data[5]
                            self.mag = data[6]
                            self.name = " ".join(data[8:])
        elif ftype == "dek":
            dd = inp[1] + "/" + inp[2] + "/" + inp[0][-2:]  # mm/dd/yy
            tmm = inp[3] + ":" + inp[4]
            rex = re.compile("^[A-Z][0-9]*[A-Z]\s")
            with open(catfilefull, 'r') as file:
                for line in file:
                    if rex.match(line):
                        data = line.split()
                        evtime1 = data[2].split(":")
                        evtime2 = ":".join(evtime1[0:2])
                        if dd == data[1] and tmm == evtime2:
                            self.month, self.day, self.year = data[1].split("/")
                            self.hour, self.min, self.sec = data[2].split(":")
                            self.lat = data[3]
                            self.long = data[4]
                            self.depth = data[5][0:4]
                            self.mag = data[5][4:7]
                            self.name = data[5][10:] + " " + " ".join(data[6:])

    @classmethod
    def from_id(cls, idd):
        yr = idd[0:4]
        mn = idd[4:6]
        day = idd[6:8]
        hr = idd[8:10]
        mint = idd[10:12]
        return cls(yr, mn, day, hr, mint)


if __name__ == "__main__":
    userinput = "1976,3,8,4,39"
    yrr, mon, day, hrr, minn = list(map(int, userinput.split(",")))
    eqinfo = eventinfo(yrr, mon, day, hrr, minn)
    print("Event name: ", eqinfo.name)
    print("Event origin time: %s:%s:%s" % (eqinfo.hour, eqinfo.min, eqinfo.sec))
    print("Event latitude: ", eqinfo.lat)
    print("Event longitude: ", eqinfo.long)
    print("Event depth: ", eqinfo.depth)
    print("Event magnitude: ", eqinfo.mag)
