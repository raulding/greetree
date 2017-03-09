#! /usr/bin/env python2.7
#coding=utf-8

import numpy as np
import pylab as pl
from datetime import *
import sys
#from pylab import *

reload(sys)
sys.setdefaultencoding("utf-8")

from pylab import *
zhfont1=matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/chinese/TrueType/ukai.ttf')

day = sys.argv[1]
dev = sys.argv[2]
file = sys.argv[3]

data_p2p = np.genfromtxt(file, delimiter="|", names="date, p25, p50, p75, p90, p95, suc_rate, fail_rate, record", usecols=(1,4,5,6,7,8,10,12,15), dtype="S8,f4,f4,f4,f4,f4,f4,f4,d8")

x = range(0, len(data_p2p["date"]))
date = []
for i in x:
    #print data_p2p["date"][i]
    date.append(int(data_p2p["date"][i][6:]))

fig = pl.figure(figsize=(12, 6))

ax1 = fig.add_subplot(3,1,1, xticks=range(0, len(date)), xticklabels=date[0:len(date):1], ylim=(0, 5000), yticks=np.linspace(0, 5000, 6, endpoint=True))
ax2 = fig.add_subplot(3,1,2, xticks=range(0, len(date)), xticklabels=date[0:len(date):1], ylim=(0, 30), yticks=np.linspace(0, 30, 7, endpoint=True))
ax3 = fig.add_subplot(3,1,3, ylim=(0, 100), yticks=np.linspace(0, 100, 11, endpoint=True), xticks=range(0, len(date)), xticklabels=date[0:len(date):1])

colors=["red", "yellow", "blue", "black", "cyan", "magenta", "green", "#2F0000", "#003E3E"]

ax1.set_title(u"Live fbuffer QoS - %s - %s"%(dev, day), fontproperties=zhfont1)
ax1.plot(x, data_p2p['record'], color=colors[0], linewidth=1.0, label="PV")

ax2.plot(x, data_p2p['p25'], color=colors[0], linewidth=1.0, label="P25")
ax2.plot(x, data_p2p['p50'], color=colors[3], linewidth=1.0, label="P50")
ax2.plot(x, data_p2p['p75'], color=colors[2], linewidth=1.0, label="P75")
ax2.plot(x, data_p2p['p90'], color=colors[5], linewidth=1.0, label="P90")
ax2.plot(x, data_p2p['p95'], color=colors[6], linewidth=1.0, label="P95")

ax3.plot(x, data_p2p['suc_rate'], color=colors[0], linewidth=1.0, label="sucrate")
ax3.plot(x, data_p2p['fail_rate'], color=colors[2], linewidth=1.0, label="failrate")

ax1.legend(loc=0, prop=zhfont1,)
ax2.legend(loc=0, prop=zhfont1)
ax3.legend(loc=0, prop=zhfont1)
ax1.grid()
ax2.grid()
ax3.grid()

pl.savefig("./live_fbuffer_qos_%s_%s.png"%(dev,day))

#pl.show()
