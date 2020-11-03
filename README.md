# Country SDGs index vs. macro elements

This reproducible research looks into the relationships between multiple country-magnitude parameters with the country’s overall sustainability level, aiming to discover whether countries with specific characteristics are more advanced in achieving sustainable development. This study uses the Sustainable Development Goals (SDGs) index, as measured by the Sustainable Development Solutions Network (SDSN) and the Bertelsmann Stiftung to evaluate countries’ progress towards achieving the SDGs. The score provided by the SDGs index represents the percentage of achievement.

The independent variables used in this study includes each country’s: 

**gdp**: Gross domestic product, constant prices (Percent change)  
*Rationale*: The relationship might be in both directions. On one hand, the more GDP a country has, the more production power it may need to utilize. If a country is in pursuit of a high GDP, sustainability might be compromised. On the other hand, countries with high GDPs may put more focus on sustainability building. 

**import**: Volume of Imports of goods (Percent change). 
*Rationale*: if a country has a great volume of imports of goods, the country might mitigate its impact on sustainability as they do not need to harness too much production power to support domestic market.

**export**: Volume of Exports of goods (Percent change). 
*Rationale*: if a country heavily relies on exporting goods, it might require a huge amount of production power, which will have a negative impact on sustainability goal achievement.

**PopChange**: Population (Percent change). 
*Rationale*: a growing population cast heavier burden on the environment and thus impeding the country’s progress towards achieving SDGs.

**econfdm**: Economic Freedom Index  
*Rationale*: The relationship might be in both directions. Countries with higher economic freedom may provide a more efficient environment for business to operate, which will likely facilitate better SDGs achievement. However, on the other hand, a freer economic environment might induce irresponsible activities by both domestic and international business, which will hurt a country’s sustainability score.

**easebus**: Ease of Doing Business Score  
*Rationale*: The relationship might be in both directions with a similar logic as in econfdm. The easier it is for a business to operate in a country, the less waste might be generated from business activities. However, the opposite could happen. An easy business environment may encourage more waste and reckless behaviors as well, resulting in a lower progress towards SDGs. 

**Inno**: Global Innovation Index   
*Rationale*: the more technologically innovative a country is, the better the country is at implementing environmentally friendly and sustainable solutions.

**highedu**: Tertiary school enrollment  
*Rationale*: A well-educated population may come with a higher awareness of sustainability, thus facilitating the country’s progress towards SDGs.

The goal of this study is to find out how the variables above are correlated with a country’s progress towards SDGs. In other words, how could countries adjust on a macro level to better achieve SDGs.


### Data Attainment and Limitations

Based on the availability of the data online, this study uses data in 2018. This study retrieves *gdp*, *import*, *export* and population data from the IMF World Economic Outlook Database. *PopChange* was calculated based on the absolute population data of 2017 and 2018. 

*econfdm* is downloaded from The Heritage Foundation’s 2018 Index of Economic Freedom, which covers 12 different economic freedoms metrics for 186 countries. This study only uses the calculated index score.

*easebus* is obtained from the Rankings & Ease of Doing Business Score from The World Bank. Countries with higher scores have more conducive regulatory environment to start and operate a local firm.

*Inno* is web-scraped from the Global Innovation Index (GII), which is one of the two popular index that measure worldwide countries’ innovation performance. The GII covers 126 countries, with a special topic to focus on each year. In 2018, the index is dedicated to the theme of energy innovation, which should go hand in hand with the dependent variable, the SDG index, in this study. 

However, there is some limitations about this data retrieval. Since the website is written in JavaScript, by using BeautifulSoup to parse the page, I could only get the most recent data. Currently it is not an issue, since the 2018 index is GII’s most recent data, but when new data is issued in the future, the web scraping technique needs to be improved.

Finally, *highedu* is attained from The World Bank’s database, measuring the ratio of total enrollment, regardless of age, to the population of the age group that officially and successfully complete education at the secondary level. 

The data itself has some limitations. First of all, a high ratio doesn’t necessarily mean a higher educated population. It may be corresponded to a large number of overaged enrollments because of repetition. Moreover, different country may have different length and standard of secondary education, therefore it is hard to discern whether a high ratio is good or bad without detailed examination for each country’s education system. Finally, this data itself is highly incomplete in that it is not collected every year in every country. Therefore, this study takes the most recent data of each country as their corresponded highedu score. 

Additionally, a more ideal measurement for this variable is each country’s population attainment of a college degree or higher, because higher education is more closely related to technology innovation. However, the data for bachelor enrollment from the World Bank are scattered and incomplete for so many countries. If this study uses that measurement, the number of observations will be largely compromised.

After merging and cleaning, the final master dataset contains data for 106 countries.


### Findings and Policy Implications

This study uses the classical OLS model to explore the relationship between Sustainability Index and *gdp*, *import*, *export*, *PopChange*, *econfdm*, *easebus*, *Inno* and *highedu*. 

The first regression includes all the independent variables. The result has a 0.86 R-square and four statistically significant variables, including the constant. *easebus*, *econfdm*, *import* and *export* bare little statistical significance. Several additional regressions were conducted with gradually reduced independent variables. The results show that among the independent variables, *PopChange*, *Inno*, *gdp* and *highedu* keep the most statistical significance and their signs correspond with theoretical logic [Table 1]. 

In the first regression, *Inno* has a coefficient of 0.38 with a strong statistical significance. This implies that the higher a country’s innovation score is, the better progress the country is making towards SDGs.  

*PopChange* has a coefficient of -2.22 with a strong statistical significance. This is in accordance with the theoretical assumption at the beginning – a bigger population base cast a heavier burden on achieving sustainability. With 1 percent of population increase, there is an associated 2.43 decrease in a country’s progress towards SDGs.

*gdp* has a coefficient of -0.36, with a relatively weaker statistical significance. This shows that on average, a high gdp is corresponded with a slower progress towards SDGs. 

*highedu* has a coefficient of 0.06 with a strong statistical significance. In accordance with the assumption at the beginning, the higher educated a country’s population is, the better performance it has on SDGs achievement

Even though not statistically significant, *econfdm*, *import* and *export* all have a negative coefficient, while *easebus* has a positive coefficient. Whereas if not taking other variables into account, both *econfdm* and *easebus* have a positive correlation with Sustainability Index, as shown in the scatter plot. This might imply that even though an open economy might be beneficial in facilitating a country’s sustainability progress, it might also induce irresponsible activities of both domestic and international business if without good regulation. This results in a stagnating progress on sustainability.

![scatter plot] 
(https://github.com/xinlinzh/HarrisDataCourse/blob/main/GdpPop_Scatter.png)

After dropping several insignificant independent variables, the fifth regression contains only the constant (53.24), *gdp* (-0.46), *Inno* (-0.42), *PopChange* (-2.43) and *highedu* (0.07), with corresponding coefficient in the parenthesis.

In summary, the regression results imply that in order to achieve higher SDGs progress, countries should invest in education and innovative technology development. At the same time, countries should actively take sustainable development into consideration when regulating business, trade and the overall economic production activities. 


### Future Improvement of the study

Despite the limitations mentioned in the previous section, a more rigorous model could be implemented, instead of a simple OLS model. Based on the criteria each index (variables) is calculated, it is highly possible that there is auto-correlation among them. A 0.85 R square is a good proof of this. 

Additionally, since each country has unique characteristics, more data modification could be done to take that into consideration. For example, the highedu data could be modified based on the specific education system each country has. 

Finally, to make the study more accurate in capturing country-specific characteristics, it might be helpful to include multiple years data to form a cross-sectional time series data. This might allow researchers to observe the relationship between a country’s progress in each variable and the country’s SDGs achievement. In this case, a more complicated model needs to be used and there will be a tradeoff between country-specification and generalization.
