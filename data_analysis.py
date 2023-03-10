#!/usr/bin/env python
# coding: utf-8

# ### Step1: Import necessary python packages

# In[1]:


from astropy.io import fits
import matplotlib.pyplot as plt
import math
from argparse import ArgumentParser

# ### Step2: Choose and open data file

# In[14]:



#filename = '/data/serendip6_data/serendip6_panoseti_sxp_1_1_20230221_145626.working'
filename = '/data/serendip6_data/serendip6_panoseti_sxp_1_1_20230221_141850.working'
#filename = '/data/serendip6_data/serendip6_panoseti_sxp_1_1_20230221_150005.working'





# ### Step5: read data out and plot the data

# specify the data is from which BinTableHDU





def plot_data(detpow, meanpow, coarchan, finechan, fft_points, fs):
    # calculate the freq range
    freq = finechan/fft_points*fs
    # convert the power to log scale
    meanpow_log = []
    detpow_log = []
    for i in range(len(detpow)):
        meanpow_log.append(math.log(meanpow[i] + 0.000001,10))
        detpow_log.append(math.log(detpow[i],10))

    # plot the data
    # fig1
    plt.subplot(2,2,1)
    plt.plot(freq, detpow, color='r')
    plt.plot(freq, meanpow, color='g')
    plt.title('Spec')
    plt.xlabel('MHz')
    plt.ylabel('detpow and meanpow')
    #fig2
    plt.subplot(2,2,2)
    plt.scatter(freq, detpow_log, color='r')
    plt.scatter(freq, meanpow_log, color='g')
    plt.title('Spec (log10(power))')
    plt.xlabel('MHz')
    plt.ylabel('detpow and meanpow')
    #fig3
    plt.subplot(2,2,3)
    d = detpow/meanpow
    print(d)
    plt.scatter(freq,d)
    plt.title('detpow divided by meanpow')
    plt.xlabel('MHz')
    plt.ylabel('detpow/meanpow')
    #fig4
    plt.subplot(2,2,4)
    plt.plot(freq,meanpow)
    plt.title('meanpow')
    plt.xlabel('MHz')
    plt.ylabel('meanpow')
    # show the figures
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    
    parser = ArgumentParser(description="Usage for checking data generated by SERENDIP6")
    parser.add_argument("--file",type=str, dest="file",help="the fits file name ")
    parser.add_argument("--hdu",type=int, dest="hdu",default=18,help="read the data from which hdu")
    parser.add_argument("--fft",type=int, dest="fft",default=1024,help="specify the fft number.Eg. 1024 means 1024M points fft.")
    parser.add_argument("--fs",type=int, dest="fs",default=1000,help="adc sampling frequency")
    args = parser.parse_args()
    try:
        hdu=fits.open(args.file)
    except:
        print('Please check the file name.')
        exit()
    
    # Show PrimaryHDU header
    print('************************')
    print('PrimaryHDU header:')
    print('************************')
    hdr = hdu[0].header
    for key in hdr.keys():
        print("%8s: %s"%(key, hdr[key]))
    # Show BinTableHDU header
    print('************************')
    print('BinTableHDU header:')
    print('************************')
    hdr = hdu[1].header
    for key in hdr.keys():
        print("%8s: %s"%(key, hdr[key]))
    print('************************')
    
    fft_points = args.fft*1024*1024
    fs = args.fs
    n = 18
    # get data
    detpow = hdu[n].data.field('DETPOW')
    meanpow = hdu[n].data.field('MEANPOW')
    coarchan =hdu[n].data.field('COARCHAN')
    finechan = hdu[n].data.field('FINECHAN')
    plot_data(detpow, meanpow, coarchan, finechan, fft_points, fs)
