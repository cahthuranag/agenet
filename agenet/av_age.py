def  av_age_func(v,T):

    import numpy as np
    import math 
    import matplotlib.pyplot as plt
    import itertools
    from scipy.integrate import simpson
    import sys
    #T=[1,2,3,4]
    #v=[2,3,4,5]
    if np.size(T) != np.size(v) or np.size(T) == 0 or np.size(v) == 0:
        print("Error: The number of elements in T and v should be same or non-zero")
        sys.exit()
    
    kt=[0]
    times =  np.append(T,(v[-1]))
    times=np.append(kt,times)
    #print(times.tolist())
    ii = 0
    offset = 0
    #print(times.tolist()) 
    age = times.copy()
    agep = np.zeros(np.size(T))

    #age[1]=times[1]
    lent=len(times)  
    for i in range(1,lent):
            if times[i] == v[ii]:
                offset = T[ii]
                ii +=1
                age[i] = age[i] - offset


    k=np.size(T)
    agep[0]=v[0]
    for i in range(1,k):
        #diff=T[iii]  
        agep[i]=v [i]-T[i-1]


    newtimes=np.repeat(times,2)  
    newpagep=np.append((age[1]),agep)     
    newpagep=np.append((kt),newpagep) 
    final=list(itertools.chain.from_iterable(zip(newpagep,age)))

    #print(times.tolist())  
    #plt.plot(times, age)
    #plt.plot(newtimes, final)
    #print(np.trapz(final,newtimes))
    av_age_fn = np.trapz(final,newtimes)/np.max(newtimes)
    return [av_age_fn,newtimes, final]
def printageex():
    from agewire import av_age
    av_age_fn,_,_=av_age.av_age_func([2,3,4,5], [1,2,3,4])
    print("Average age of information  when  time slots are [2,3,4,5], [1,2,3,4]:", av_age_fn)
def plotageex():
    from agewire import av_age
    import matplotlib.pyplot as plt
    av_age_print, newtimesex, final =av_age.av_age_func([2,3,4,5], [1,2,3,4])
    print("Average age of information  when  time slots are [2,3,4,5], [1,2,3,4]:", av_age_print)
    plt.plot(newtimesex, final)  
    plt.xlabel("Time")
    plt.ylabel("Age")
    plt.show()   

def validate(args):
    return args    
                     

