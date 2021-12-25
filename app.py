from FundamentalAnalysis.details import profile
from flask import Flask, render_template, request,redirect,url_for
import pprint
from flask.helpers import send_from_directory
import requests 
from textblob import TextBlob
import json
import numpy as np
import pickle
import pandas as pd
import FundamentalAnalysis as fa
from datetime import date
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sqlite3
from flask import jsonify

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
companyname=""
query=""
api_key_fmp="639ad0383d5548a11c1f1864ab499672"

def income_statement():
    ticker = companyname
    api_key = api_key_fmp
    income_statement=fa.income_statement(ticker, api_key, period="annual")
    income_list=income_statement.values.tolist()
    reportedCurrency=income_list[0]
    fillingDate=income_list[1]
    acceptedDate=income_list[2]
    revenue=income_list[4]
    costofRevenue=income_list[5] 
    grossProfit=income_list[6]
    grossProfitRatio=income_list[7]
    researchAndDevelopmentExpenses=income_list[8]
    generalAndAdministrativeExpenses=income_list[9]
    sellingAndMarketingExpenses=income_list[10]
    sellingGeneralAndAdministrativeExpenses=income_list[11]
    otherExpenses=income_list[12]
    operatingExpense=income_list[13]
    costAndExpenses=income_list[14]
    interestExpense=income_list[15]
    link=income_list[32]
    income=[]
    income.append(reportedCurrency)
    income.append(fillingDate)
    income.append(acceptedDate)
    income.append(revenue)
    income.append(costofRevenue)
    income.append(grossProfit)
    income.append(grossProfitRatio)
    income.append(researchAndDevelopmentExpenses)
    income.append(generalAndAdministrativeExpenses)
    income.append(sellingAndMarketingExpenses)
    income.append(sellingGeneralAndAdministrativeExpenses)
    income.append(otherExpenses)
    income.append(operatingExpense)
    income.append(costAndExpenses)
    income.append(interestExpense)
    income.append(link)
    return income
    


def finance_profile():
    ticker = companyname
    api_key = api_key_fmp
    profile = fa.profile(ticker, '639ad0383d5548a11c1f1864ab499672')
    profile_values=profile.values.tolist()
    range=profile_values[6]
    marketCap=profile_values[4]
    ceo=profile_values[18]
    sector=profile_values[19]
    country=profile_values[20]
    industry=profile_values[15]
    name=profile_values[8]
    description=profile_values[17]
    website=profile_values[16]
    state=profile_values[25]
    profileList=[]
    profileList.append(range)
    profileList.append(marketCap)
    profileList.append(ceo)
    profileList.append(sector)
    profileList.append(country)
    profileList.append(industry)
    profileList.append(name)
    profileList.append(description)
    profileList.append(website)
    profileList.append(state)
    return profileList
def finance_records():
    ticker = companyname
    api_key = api_key_fmp
    # Quote 
    quotes = fa.quote(ticker, '639ad0383d5548a11c1f1864ab499672')
    quotes_values=quotes.values.tolist()
    symbol=quotes_values[0]
    name=quotes_values[1]
    price=quotes_values[2]
    changesPercentage=quotes_values[3]
    dayLow=quotes_values[5]
    dayHigh=quotes_values[6]
    yearHigh=quotes_values[6]
    yearLow=quotes_values[7]
    volume=quotes_values[12]
    marketCap=quotes_values[9]
    exchange=quotes_values[14]
    open_price=quotes_values[14]
    previous_close=quotes_values[15]

    growth_annually = fa.financial_statement_growth(ticker, api_key, period="annual")
    # Revenue Growth 2020
    fy_growth_annually= growth_annually.get("2020")
    fy_growth_annually_list_2020=fy_growth_annually.values.tolist()
    revenuegrowth2020=fy_growth_annually_list_2020[1]
    #print(revenuegrowth2020)
    # Revenue Growth 2019
    fy_growth_annually= growth_annually.get("2019")
    fy_growth_annually_list_2019=fy_growth_annually.values.tolist()
    revenuegrowth2019=fy_growth_annually_list_2019[1]
    #print(revenuegrowth2019)
    # Revenue Growth 2018
    fy_growth_annually= growth_annually.get("2018")
    fy_growth_annually_list_2018=fy_growth_annually.values.tolist()
    revenuegrowth2018=fy_growth_annually_list_2018[1]

    stock_data = fa.stock_data(ticker, period="ytd", interval="1d")
    stock_data.to_csv(r'datasets/stock_data.csv')
    #
    # print(revenuegrowth2018)
    financialdatalist=[]
    financialdatalist.append(quotes_values)
    financialdatalist.append(symbol)
    financialdatalist.append(name)
    financialdatalist.append(price)
    financialdatalist.append(changesPercentage)
    financialdatalist.append(dayLow)
    financialdatalist.append(dayHigh)
    financialdatalist.append(yearHigh)
    financialdatalist.append(yearLow)
    financialdatalist.append(marketCap)
    financialdatalist.append(volume)
    financialdatalist.append(exchange)
    financialdatalist.append(open_price)
    financialdatalist.append(previous_close)
    financialdatalist.append(revenuegrowth2020)
    financialdatalist.append(revenuegrowth2019)
    financialdatalist.append(revenuegrowth2018)
    return(financialdatalist)

# News Sentiment Analysis
def news_sentiment_analysis():
    news_headlines_list = []
    headlines_sentiment_text = []
    positive_news_sentiment=0
    negative_news_sentiment=0
    neutral_news_sentiment=0
    f = open('datasets/CompanyRecords.json',)
    global query
    data = json.load(f)
    for i in data['comprecords']:
        if(i['symbol']==companyname):
            print(i['name'])
            query=i['name']
    
    query=query
    news_api_key='5db27ca0ffa74759b164a1143e94ebe1'
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
    'q': query, # query phrase
    'pageSize': 30,  # maxiAMZNm is 100
   'sources':'bloomberg',
    'apiKey': news_api_key,
     'language':'en'
    
    }
   
    response = requests.get(url, params=parameters)
    response_json = response.json()
    news_urls=[]
    news_author=[]
    news_publishedat=[]
    for i in response_json['articles']:
        news_headlines_list.append(i['title'])
        news_urls.append(i['url'])
        news_author.append(i['author'])
        news_publishedat.append(i['publishedAt'])
        #print(news_headlines_list)
    for i in range(len(news_headlines_list)):
        analysis = TextBlob(news_headlines_list[i])
        if analysis.sentiment.polarity > 0:
            positive_news_sentiment+=1
        elif analysis.sentiment.polarity == 0:
            neutral_news_sentiment+=1
        else:
            negative_news_sentiment+=1
    #print(positive_news_sentiment)
    #print(negative_news_sentiment)
    #print(neutral_news_sentiment)
    positive_news_sentiment=round(int(positive_news_sentiment)/30*100)
    
    negative_news_sentiment=round(int(negative_news_sentiment)/30*100)
    
    neutral_news_sentiment=round(int(neutral_news_sentiment)/30*100)
    sentiment_list=[]
    sentiment_list.append(positive_news_sentiment)
    sentiment_list.append(negative_news_sentiment)
    sentiment_list.append(neutral_news_sentiment)
    sentiment_list.append(news_headlines_list)
    sentiment_list.append(news_author)
    sentiment_list.append(news_urls)
    sentiment_list.append(news_publishedat)
    return sentiment_list




########## Stock Prediction System ###########
def Average(lst):
    return sum(lst) / len(lst)

def prepare_data(df,forecast_col,forecast_out,test_size):
    label = df[forecast_col].shift(-forecast_out) #creating new column called label with the last 5 rows are nan
    X = np.array(df[[forecast_col]]) #creating the feature array
    X = preprocessing.scale(X) #processing the feature array
    X_lately = X[-forecast_out:] #creating the column i want to use later in the predicting method
    X = X[:-forecast_out] # X that will contain the training and testing
    label.dropna(inplace=True) #dropping na values
    y = np.array(label)  # assigning Y
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size, random_state=0) #cross validation

    response = [X_train,X_test , Y_train, Y_test , X_lately]
    return response



def predStockPrice():
	df = pd.read_csv(r'datasets/stock_data.csv')
	df.head()
	forecast_col='close'
	forecast_out=5
	test_size=0.2
	X_train, X_test, Y_train, Y_test , X_lately =prepare_data(df,forecast_col,forecast_out,test_size); #calling the method were the cross validation and data preperation is in
	learner = LinearRegression() #initializing linear regression model
	learner.fit(X_train,Y_train) #training the linear regression model
	score=learner.score(X_test,Y_test)#testing the linear regression model
	forecast= learner.predict(X_lately) #set that will contain the forecasted data
	response={}#creting json object
	response['test_score']=score
	response['forecast_set']=forecast
	return(round(forecast[4],2))






###############################################




# Flask App Section
app = Flask(__name__)
@app.route("/",methods =["GET", "POST"])
def homepage():
     global companyname
     if request.method == "POST":
        companyname = request.form.get("companyname")
        print("Company Name"+companyname)
     return render_template('homepage.html')

@app.route("/dashboard",methods =["GET", "POST"])
def dashboard():
    #SENTIMENT SECTION
    global companyname
   
    if request.method == "POST":
        companyname = request.form.get("companyname")
        companyname=companyname.upper()
        print("Company Name"+companyname)
        
    local_sentiment_list=news_sentiment_analysis()
    positive_news_sentiment=local_sentiment_list[0]
    negative_news_sentiment=local_sentiment_list[1]
    neutral_news_sentiment=local_sentiment_list[2]
    news_titles_lists=local_sentiment_list[3]
    news_authors=local_sentiment_list[4]
    news_urls=local_sentiment_list[5]
    news_publishedat=local_sentiment_list[6]
    
    print("Company Name1"+companyname)
 
    #FINANCIAL SECTION
    financiallist=finance_records()
    revenuegrowthyearly=[]
    revenuegrowthyearly.append(float(round(financiallist[16],4)))
    
    revenuegrowthyearly.append(float(round(financiallist[15],4)))
    
    revenuegrowthyearly.append(float(round(financiallist[14],4)))
    today = date.today()
    dt_string = today.strftime("%d/%m/%Y")

    predicted_stock_price=predStockPrice()
    compayname=companyname
    profile_list=finance_profile()
    symbol=query
    return render_template('dashboard.html',positive_news_sentiment=positive_news_sentiment,
    neutral_news_sentiment=neutral_news_sentiment,negative_news_sentiment=negative_news_sentiment,
    quotes_values=financiallist[0],symbol=symbol,name=financiallist[2],price=financiallist[3],
    changesPercentage=financiallist[4],dayLow=financiallist[5],dayHigh=financiallist[6],yearHigh=str(financiallist[7]),
    yearLow=financiallist[8],marketCap=financiallist[9],volume=financiallist[10],exchange=financiallist[11],
    open_price=financiallist[12],previous_price=financiallist[13],revenuegrowthyearly=revenuegrowthyearly,date_time=dt_string,
    news_titles_lists=news_titles_lists,news_authors=news_authors,news_urls=news_urls,news_publishedat=news_publishedat,
    predicted_stock_price=predicted_stock_price,rangeprice=profile_list[0],ceo=profile_list[2],sector=profile_list[3],
    country=profile_list[4],industry=profile_list[5],description=profile_list[7],website=profile_list[8],state=profile_list[9],
   companyname=compayname )



@app.route("/incomestatement")
def incomestatement():
    income_list=income_statement()
    return render_template('incomestatement.html',
    reportedCurrency=income_list[0],fillingDate=income_list[1],acceptedDate=income_list[2],revenue=income_list[3],costofRevenue=income_list[4],
    grossProfit=income_list[5],grossProfitRatio=income_list[6],researchAndDevelopmentExpenses=income_list[7],generalAndAdministrativeExpenses=income_list[8],
    sellingAndMarketingExpenses=income_list[9],sellingGeneralAndAdministrativeExpenses=income_list[10],otherExpenses=income_list[11],operatingExpenses=income_list[12],
    costAndExpenses=income_list[13],interestExpense=income_list[14],link=income_list[15])
from datetime import date
@app.route("/portfoliomanager",methods =["GET", "POST"])
def portfoliomanager():
    if request.method == "POST":  
        try:  
            symbol = companyname
            date = "25-12-2021"
            quotes = fa.quote(symbol, '639ad0383d5548a11c1f1864ab499672')
            quotes_values=quotes.values.tolist()
            pricedata=quotes_values[2]
            price=float(pricedata[0])
            quantity = request.form["quantity"]  
            total = round(price*float(quantity) ,2)
            with sqlite3.connect("portfoliodata.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT INTO PORTFOLIO(SYMBOL, BUY_DATE, QUANTITY, PRICE, TOTAL) VALUES (?,?,?,?,?)",(symbol,date,quantity,price,total))
                con.commit()  
        except Exception as e:
            print(e)
    con = sqlite3.connect('portfoliodata.db')
    cursor = con.cursor()  
    items=[]
    cursor.execute('SELECT SYMBOL, BUY_DATE, QUANTITY, PRICE, TOTAL FROM PORTFOLIO')
    items = cursor.fetchall()

    
    return render_template('portfoliomanager.html',item=items)

@app.route('/delete', methods = ['POST'])
def delete():
     if request.method == 'POST':
         my_data =request.form['symbol1']
         con = sqlite3.connect('portfoliodata.db')
         cursor = con.cursor()  
         items=[]
         cursor.execute("DELETE FROM PORTFOLIO WHERE SYMBOL = ?",(my_data,))
         #rcursor.execute("DELETE FROM PORTFOLIO")
         cursor.execute('SELECT SYMBOL, BUY_DATE, QUANTITY, PRICE, TOTAL FROM PORTFOLIO')
         con.commit()
         items = cursor.fetchall()
     return render_template('portfoliomanager.html',item=items)



@app.errorhandler(404)
  
# inbuilt function which takes error as parameter
def not_found(e):
  
# defining function
  return render_template("404.html")



if __name__ == '__main__':
    app.run(debug=True)
  


