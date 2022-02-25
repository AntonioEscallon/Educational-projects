import buoypy as bp
import matplotlib.pyplot as plt

buoy = 41108 #wilmington harbor
B = bp.realtime(buoy) #wilmington harbor

df = B.txt()

# plotting
fig,ax = plt.subplots(2,sharex=True)
df.WVHT.plot(ax=ax[0])
ax[0].set_ylabel('Wave Height (m)',fontsize=14)

df.DPD.plot(ax=ax[1])
ax[1].set_ylabel('Dominant Period (sec)',fontsize=14)
ax[1].set_xlabel('')
#sns.despine()