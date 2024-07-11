#Defining function to trim, bin and normalize the model spectra
#returns arrays for wavelength and flux
def modspec_tbn(spec): #spec is a Spectrum1D object model from phoenix
    wlen_m=spec.spectral_axis.value
    flux_m=spec.flux.value

    wlen_m1=wlen_m[np.logical_and(wlen_m>4000.,wlen_m<10000.)]
    flux_m1=flux_m[np.logical_and(wlen_m>4000.,wlen_m<10000.)]
    #eflux1=eflux[np.logical_and(wlen>4000.,wlen<7595.)]

    ###########################    Binning     ##################################################

    #nb=860 #number of bins
    dt=70 #bin size
    #bspec,bstep=binningx0dt(wlen_m1,flux_m1,nbins=nb, useBinCenter=True, yvalFunc=percentiles) 
    bspec,bstep=binningx0dt(wlen_m1,flux_m1,dt=dt, useBinCenter=True, yvalFunc=percentiles) 
    #bspec is an array of 4 columns,[new wlen,new binned flux,flux errors,nmber of input points to create the bin]
    #bstep is the with of the bins
    bwlen,bflux=bspec[::,0],bspec[::,1]
    
    ##########################   Polynomial fit    #############################################33
    
    n=40 #order of polinomial fit
    pfit0=np.polyfit(bwlen,bflux,n)
    #pfit1=np.polyfit(bwlen,yintp,n)
    poli0=np.poly1d(pfit0)
    #
    '''
    fig, ax=plt.subplots( figsize=(8,5))
    ax.plot(wlen_m,flux_m,alpha=0.3,lw=0.3,label='original model') #original spectra
    ax.plot(wlen_m1,flux_m1,alpha=0.3,lw=0.3,label='original model (wv>3700A')
    ax.plot(bwlen,bflux,'-.',lw=1,label='binned spectra')   # binned spectra
    plt.plot(bwlen,poli0(bwlen),'r-',lw=1,label='polifit order '+str(n))
    plt.legend()
    '''
    ###########################    Normalization    ############################################
    #the polinomial fit is done in the binned spectra but the original model is normalized with that fit
    
    wav=wlen_m1
    flu=flux_m1/poli0(wlen_m1)
    '''
    fig, ax=plt.subplots(figsize=(12,7))
    ax.plot(wav,flu,lw=0.3,alpha=0.9)
    '''
    
    return wav,flu
