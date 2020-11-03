import pandas as pd
import time
import pandas_datareader.data as web
from pandas_datareader import wb
from pandas.plotting import table
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.2f}'.format

def webscrape(url):
    innosoup = BeautifulSoup(urlopen(url), 'html.parser')
    ullist = list(innosoup.find_all('ul', attrs={'class':'list-inline'}))
    textlist = []
    for ul in ullist:
        for li in ul.find_all('li'):
            if li.find('a'):
                break
            textlist.append(li.get_text())
    economy = textlist[1::6]
    for i in range(len(economy)-1):
        economy[i+1] = economy[i+1].partition("\r")[0]
    country = {'country':economy[1:]}

    score = textlist[5::6]
    for i in range(len(score)-1):
        score[i+1] = score[i+1][-5:]
    innoscore = {score[0]:score[1:]}

    inno = pd.DataFrame.from_dict(MergeDict(country, innoscore)).rename(columns = {'Score':'Inno'})
    inno['Inno'] = inno['Inno'].apply(pd.to_numeric)

    return inno

def downloaddata(dic):
    for key, url in dic.items():
        if key == "imfdata":
            print('Downloading',key, '...')
            data = requests.get(url)
            output = open(key+'.txt', 'wb')
            output.write(data.content)
            output.close()
        elif key == "innoindex" or key == "eduind":
            break
        else:
            print('Downloading',key, '...')
            data = requests.get(url)
            output = open(key+'.xlsx', 'wb')
            output.write(data.content)
            output.close()

def readdata(dic,list):
    for key in dic.keys():
        if key == 'imfdata':
            print('Reading',key, '...')
            list[0] = pd.read_csv(os.getcwd()+'/'+key+'.txt', sep='\t', encoding = "ISO-8859-1")
        elif key == "Sustainability Index":
            print('Reading',key, '...')
            list[1] = pd.read_excel(os.getcwd()+'/'+key+'.xlsx', header = 1)
        elif key == "ezbus":
            print('Reading',key, '...')
            list[2] = pd.read_excel(os.getcwd()+'/'+key+'.xlsx', sheet_name = 'All Data',header = 1)
        elif key == "innoindex":
            print('Reading',key, '...')
            list[3] = webscrape(dic[key])
        elif key == "eduind":
            print('Reading',key, '...')
            list[4] = wb.download(indicator = 'SE.TER.ENRR', country = 'all', start = 2000, end = 2017).reset_index().dropna()
        else:
            print('Reading',key, '...')
            list[5] = pd.read_excel(os.getcwd()+'/'+key+'.xlsx')

def MergeDict(dict1, dict2):
    DIC = {**dict1, **dict2}
    return DIC

def mergemany(list):
    for i in range(len(list)-1):
        list[i+1] = list[i].merge(list[i+1], on='country', how='inner')
    return list[-1]



## Setup
sustain = 'https://www.sdgindex.org/assets/files/2018/Global_Index_Data.xlsx'
imfindicator = 'https://www.imf.org/external/pubs/ft/weo/2019/01/weodata/weoreptc.aspx?sy=2017&ey=2018&ssd=1&sort=country&ds=.&br=1&pr1.x=70&pr1.y=17&c=512%2C668%2C914%2C672%2C612%2C946%2C614%2C137%2C311%2C546%2C213%2C674%2C911%2C676%2C314%2C548%2C193%2C556%2C122%2C678%2C912%2C181%2C313%2C867%2C419%2C682%2C513%2C684%2C316%2C273%2C913%2C868%2C124%2C921%2C339%2C948%2C638%2C943%2C514%2C686%2C218%2C688%2C963%2C518%2C616%2C728%2C223%2C836%2C516%2C558%2C918%2C138%2C748%2C196%2C618%2C278%2C624%2C692%2C522%2C694%2C622%2C962%2C156%2C142%2C626%2C449%2C628%2C564%2C228%2C565%2C924%2C283%2C233%2C853%2C632%2C288%2C636%2C293%2C634%2C566%2C238%2C964%2C662%2C182%2C960%2C359%2C423%2C453%2C935%2C968%2C128%2C922%2C611%2C714%2C321%2C862%2C243%2C135%2C248%2C716%2C469%2C456%2C253%2C722%2C642%2C942%2C643%2C718%2C939%2C724%2C734%2C576%2C644%2C936%2C819%2C961%2C172%2C813%2C132%2C726%2C646%2C199%2C648%2C733%2C915%2C184%2C134%2C524%2C652%2C361%2C174%2C362%2C328%2C364%2C258%2C732%2C656%2C366%2C654%2C144%2C336%2C146%2C263%2C463%2C268%2C528%2C532%2C923%2C944%2C738%2C176%2C578%2C534%2C537%2C536%2C742%2C429%2C866%2C433%2C369%2C178%2C744%2C436%2C186%2C136%2C925%2C343%2C869%2C158%2C746%2C439%2C926%2C916%2C466%2C664%2C112%2C826%2C111%2C542%2C298%2C967%2C927%2C443%2C846%2C917%2C299%2C544%2C582%2C941%2C474%2C446%2C754%2C666%2C698&s=NGDP_RPCH%2CTMG_RPCH%2CTXG_RPCH%2CLP&grp=0&a='
econfreedom = 'https://www.heritage.org/index/excel/2018/index2018_data.xls'
easebus = 'http://www.doingbusiness.org/content/dam/doingBusiness/excel/Historical-data---complete-data-with-scores.xlsx'
innoindex = 'https://www.globalinnovationindex.org/analysis-indicator'
eduind = 'SE.TER.ENRR'

downloadlink = {"Sustainability Index":sustain,
                "imfdata":imfindicator,
                "econfdm":econfreedom,
                "ezbus":easebus,
                "innoindex":innoindex,
                "eduind": eduind}

imf = pd.DataFrame()
sustain = pd.DataFrame()
econfdm = pd.DataFrame()
inno = pd.DataFrame()
highedu = pd.DataFrame()
ezbus = pd.DataFrame()
dflist = [imf, sustain, ezbus, inno, highedu, econfdm]

## Download and Read Data

downloaddata(downloadlink)
readdata(downloadlink,dflist)
imf = dflist[0]
sustain = dflist[1]
ezbus = dflist[2]
inno = dflist[3]
highedu = dflist[4]
econfdm = dflist[5]

## Clean Individual Dataset
# sustainability index
suskeep = ['country','Global Index Score (0-100): 2018 version']
susrename = {'Global Index Score (0-100): 2018 version':'Sustainability Index'}
sustain = sustain[suskeep].rename(columns = susrename).dropna()

# Population Change
pop = imf.loc[imf['Units'] !='Percent change'][['Country', '2017', '2018']].reset_index().dropna()
pop['2018'] = pd.to_numeric(pop['2018'].apply(lambda r: r.replace(",","")))
pop['2017'] = pd.to_numeric(pop['2017'].apply(lambda r: r.replace(",","")))
pop['PopChange'] = (pop['2018']-pop['2017'])/pop['2017']*100
pop = pop[['Country','PopChange']].rename(columns = {'Country':'country'})

# gdp, import and export
imfcolumns =['Country','Subject Descriptor','2018']
imfrest = imf.loc[imf['Units'] =='Percent change'][imfcolumns].pivot(index='Country', columns='Subject Descriptor', values='2018').reset_index().dropna()
IMFrename = {'Country':'country',
             'Gross domestic product, constant prices':'gdp',
             'Volume of Imports of goods':'import',
             'Volume of exports of goods':'export'}
IMF = imfrest.rename(columns=IMFrename).merge(pop, on = 'country')
IMF[IMF.columns[1:]] = IMF[IMF.columns[1:]].apply(pd.to_numeric)

# economic freedom
efdkeep = ['Country Name', '2018 Score']
efdrename = {'Country Name':'country', '2018 Score':'econfdm'}
econfdm = econfdm[efdkeep].rename(columns = efdrename)

# ease of doing business
ezbuslist = ['Country code','Economy','DB Year','Ease of doing business score (DB17-19 methodology)']
ezbusrename = {'Economy':'country', 'Ease of doing business score (DB17-19 methodology)':'easebus'}
ezbus = ezbus[ezbuslist].loc[ezbus['DB Year'] == 2018].rename(columns =ezbusrename)[['country','easebus']]

# HighEdu Enrollment
highedu[['year']] = highedu[['year']].applymap(lambda r: int(r))
herename = {'SE.TER.ENRR':'highedu'}
hekeep = ['country','highedu']
highedu = highedu.drop_duplicates('country', keep='first').rename(columns = herename)[hekeep]

# merge data
mergelist = [sustain, IMF, ezbus, inno, highedu, econfdm]
mergeddata = mergemany(mergelist)
mergeddata.to_csv(os.getcwd()+'/mergeddata.csv', index = False)

## OLS Regression

mergeddata['const'] = 1
y = mergeddata['Sustainability Index']
reg0 = sm.OLS(y,mergeddata[['const','gdp','import','export','PopChange','easebus','Inno', 'highedu','econfdm']]).fit()
print(reg0.summary())
reg1 = sm.OLS(y,mergeddata[['const','gdp','import','export','PopChange','easebus','Inno', 'highedu']]).fit()
print(reg1.summary())
reg2 = sm.OLS(y,mergeddata[['const','gdp','export','PopChange','easebus','Inno', 'highedu']]).fit()
print(reg2.summary())
reg3 = sm.OLS(y,mergeddata[['const','gdp','PopChange','easebus','Inno', 'highedu']]).fit()
print(reg3.summary())
reg4 = sm.OLS(y,mergeddata[['const','gdp','PopChange','Inno', 'highedu']]).fit()
print(reg4.summary())
reg5 = sm.OLS(y,mergeddata[['const','PopChange','Inno', 'highedu']]).fit()
print(reg5.summary())

allreg = [reg0, reg1, reg2, reg3, reg4, reg5]
output = summary_col(allreg,stars=True,float_format='%0.2f',
                     info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                                'R2':lambda x: "{:.2f}".format(x.rsquared)})

print(output)
output_as_html = output.as_html()
outputdf = pd.read_html(output_as_html, header=0,index_col=0)[0]

outputdf.to_csv(os.getcwd()+'/multiregression table.csv')

## Visualizations

#Inno & HighEdu
fig, ax = plt.subplots()
ax.scatter(mergeddata['Inno'], mergeddata['Sustainability Index'], label = 'Innovation Index',
               alpha=0.8, edgecolors='none')
ax.scatter(mergeddata['highedu'], mergeddata['Sustainability Index'], label = 'HighEdu Enrollment',
               alpha=0.8, edgecolors='none')
ax.grid(True)
ax.legend()
plt.savefig('InnoHighEdu_Scatter.png')
plt.show(block=False)
plt.pause(3)
plt.close()


#GDP & POP
fig, ax = plt.subplots()
ax.scatter(mergeddata['gdp'], mergeddata['Sustainability Index'], label = 'GDP',
               alpha=0.8, edgecolors='none')
ax.scatter(mergeddata['PopChange'], mergeddata['Sustainability Index'], label = 'Population Growth',
               alpha=0.8, edgecolors='none')
ax.grid(True)
ax.legend()
plt.savefig('GdpPop_Scatter.png')
plt.show(block=False)
plt.pause(3)
plt.close()



#Other Variables
fig, ax = plt.subplots()
ax.scatter(mergeddata['import'], mergeddata['Sustainability Index'], label = 'Import change',
               alpha=0.8, edgecolors='none')
ax.scatter(mergeddata['export'], mergeddata['Sustainability Index'], label = 'Export change',
               alpha=0.8, edgecolors='none')
ax.scatter(mergeddata['easebus'], mergeddata['Sustainability Index'], label = 'Ease of doing bus',
               alpha=0.8, edgecolors='none')
ax.scatter(mergeddata['econfdm'], mergeddata['Sustainability Index'], label = 'Economic Freedom',
               alpha=0.8, edgecolors='none')
ax.grid(True)
ax.legend()
plt.savefig('InsigVars_Scatter.png')
plt.show(block=False)
plt.pause(3)
plt.close()
