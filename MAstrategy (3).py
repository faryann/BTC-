#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf


# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[4]:


# We download Bitcoin price data since 2018:
df= yf.download('BTC-USD', start='2018-01-01')


# In[6]:


import datetime
df_opt=df
df.head(1)


# 
# # =============================================================
# 
# # A widely-used strategy in trading involves comparing Moving Averages (MAs). 
# 
# # In financial markets, MA represents the average price of an asset over a specific period, typically measured in a certain number of data-points (e.g., days, 4 hours, or 1 hour).
# 
# # The fundamental concept behind this strategy is that every system tends to revert to its mean.
# 
# # A trader assesses the MA over an extended timeframe and compares it to the MA over a shorter one.
# 
# # When the short MA crosses above the long MA, it is commonly regarded as a buying signal.
# 
# # In this study, we examine the performance of this strategy on Bitcoin (BTC) price data dating back to 2018.
# # =============================================================

# # Let us look at the graph of the price with a short and a long MA's

# In[22]:


fig, ax= plt.subplots(figsize=(15, 6))
refdf.plot(x='Date', y=['Close', 'MA_SH', 'MA_L'], figsize=(15, 6), ax=ax, color= ['k','b', 'r'] )


# # It appears that when the short MA (the bule line) crosses the long MA (red line) from below we see an increase in the price. Also when the short MA (the bule line) crosses the long MA (red line) from above we see a decrease in the price.  
# 
# # But is this a good strategy? 
# 
# # We will look more closely to data. 
# 
# # We compare buying/selling based on MA strategy with someone who bought BTC at its lowest price and sold it at the highest since 2018.

# In[7]:


df= df.reset_index()


# In[8]:


# function to round price just up to two decimal digits
def dec2(x):
    x= x*100
    x= int(x)
    return x/100

dec2(3275.37793)


# In[9]:


#finding the lowest price BTC had since 2018. 
f=df[df['Close']== df['Close'].min()]['High']
dateee=df[df['Close']== df['Close'].min()]['Date']
print('The lowest price $', dec2(f),'\nReched at following', str(dateee).split(' ')[3][:-7])


# # We write a function that takes your entry date to the market as veiable 'd'; 
# # assuming after entering at date 'd' you bought the BTC at the lowest and 
# # sold it at the highest price (deep/top strategy), we write another function
# #  that shows your return 
# 

# In[10]:


def Entry_date():
    s= input('Insert the date you entered the market, YYYY, M, D: ', )
    s=s.split(',')
    date= datetime.date(int(s[0]), int(s[1]), int(s[2]))
    return date
def deeptop(df, d):
#   Lets get the date fram from the entry date  
    dff= df[df['Date'] > str(d)]
    minn= dff[dff['Close']== dff['Close'].min()]['High']
    minnD= str(dff[dff['Close']== dff['Close'].min()]['Date']).split(' ')[3][:-7]
    minn= int(minn)
    maxx= dff[dff['Close']== dff['Close'].max()]['High']
    maxx= int(maxx)
    maxxD= str(dff[dff['Close']== dff['Close'].max()]['Date']).split(' ')[3][:-7]
    print('If you had employed the deep/top stratedgy, you could make your mony', dec2(maxx/minn),'X \nAssuming you purchased the asset at its lowest point, which occurred at', minnD, 'at price= $',minn,           '\nand sold it at', maxxD, 'at price= $',maxx,  '\nwhich is the highest price BTC ever had!' )
    return dec2(maxx/minn)

# This function asks for number of days for short MA and long MA for the strategy
def ma_request():
    sh_ma= input('insert number of days for your short moving average strategy:\n', )
    sh_ma= int(sh_ma)
    L_ma= input('insert number of days for your long moving average strategy:\n', )
    L_ma= int(L_ma)
    return (sh_ma, L_ma)         
                


# In[ ]:





# # This function takes a DF and returns an
# # enhanced DF applying the MA strategy
# 

# In[11]:


def strategy(df):
    (ma_sh, ma_L)= ma_request()
    dff= df.copy()
#   Note that dff.Close.pct_change()+1 = tomorow's price/todays price   
    dff['ret']= np.log(dff.Close.pct_change()+1)
    dff['MA_SH']= dff.Close.rolling(ma_sh).mean()
    dff['MA_L']= dff.Close.rolling(ma_L).mean()
    dff= dff.dropna()
    dff['position']= np.where(dff['MA_SH']>dff['MA_L'], 1, 0)
    dff['pos.ret']=dff['position'].shift(1)*dff['ret']
    dff= dff.dropna()
    return dff


# # The performance function assesses your gains when applying the Moving Average (MA) strategy and compares it with a straightforward 'buy low, sell high' approach.
# 
# 

# In[12]:



def performence(df):
    dd= str(Entry_date())
    dfff= df[df['Date'] > dd]
    wma=np.exp(strategy(dfff)['pos.ret'].sum())
    return (dec2(wma), dd)
def comp(df):
    (woma, date)= performence(df)
    print('Employing MA strategy you made your money', woma ,'X')
    print('============================================')
    print(deeptop(df, date))
    


# In[17]:


comp(df)


# In[14]:


import seaborn as sns


# In[15]:


refdf= strategy(df)
refdf.head(1)


# In[16]:


# Let us visualize MA strategy. The black line shows buy or sell position
# If it is at 1 we by and hold, when it hit zero we sell. 
fig, ax= plt.subplots(figsize=(15, 6))
refdf.plot(x='Date', y=['Close', 'MA_SH', 'MA_L'], figsize=(15, 6), ax=ax)
ax1=ax.twinx()
refdf.plot(x='Date', y=['position'], figsize=(15, 6), ax=ax1, color='k')


# In[21]:


# Lets try it for different MA's
refdf1= strategy(df)
fig, ax= plt.subplots(figsize=(15, 6))
refdf1.plot(x='Date', y=['Close', 'MA_SH', 'MA_L'], figsize=(15, 6), ax=ax)
ax1=ax.twinx()
refdf1.plot(x='Date', y=['position'], figsize=(15, 6), ax=ax1, color='k')


# In[ ]:


# Now Let us find the best combination of days for our short\long MA's strategy


# In[29]:


# Lets refine our strategy function
def ref_strategy(df, L):
    L_R=[]
    for (ma_sh, ma_L) in L:
        dff= df.copy()
    #   Note that dff.Close.pct_change()+1 = tomorow's price/todays price   
        dff['ret']= np.log(dff.Close.pct_change()+1)
        dff['MA_SH']= dff.Close.rolling(ma_sh).mean()
        dff['MA_L']= dff.Close.rolling(ma_L).mean()
        dff= dff.dropna()
        dff['position']= np.where(dff['MA_SH']>dff['MA_L'], 1, 0)
        dff['pos.ret']=dff['position'].shift(1)*dff['ret']
        dff= dff.dropna()
        wma=np.exp(dff['pos.ret'].sum())
        L_R.append(dec2(wma))
        
    return L_R


# In[41]:


# Let us make a list of short, long days
L1= np.arange(5, 50, 5)
L2=  np.arange(25, 150, 5)
L=[]
for l1 in L1:
    for l2 in L2:
        if l2>l1:
            L.append((l1, l2))


# In[43]:


L_R= ref_strategy(df_opt, L)


# In[48]:


#  our maximum return using MA is
mL= max(L_R)
mL


# In[50]:


# We achieve this with 
(sh, lo)= L[L_R.index(11.36)]
print('By taking short MA=', sh, ' and long MA=', lo, 'we would have made our money', mL, 'times the original investment.')


# # ======================Summary =======================
# # We examined a well-known trading strategy known as moving averages (MA) using data from 2018. Our analysis revealed that the maximum return achieved through this strategy is approximately 11 times the original investment.
# 
# # Additionally, we compared this return to that of an individual who bought Bitcoin (BTC) at its lowest price since 2018 and sold it at the highest price BTC has ever reached. In this case, the return amounted to around 20 times the original investment.
# 
# # Our conclusion is clear: when employed in isolation, the MA strategy falls short in comparison to a straightforward 'buy low, sell high' approach.
# 
# # Furthermore, our findings suggest that the optimal parameters for the MA strategy are a short MA period of 5 days and a long MA period of 125 days

# In[ ]:





# In[ ]:




