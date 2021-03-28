#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:49:17 2020

@author: prianka.ball
"""
from pytrends.request import TrendReq
import pandas as pd
from gspread_pandas import Spread #details https://github.com/aiguofer/
import numpy as np
#from fbprophet import Prophet
import sys
import os
from gspread_pandas import conf
import requests.exceptions
import time


def clean_interest(file, column):
  df = file
  df['date'] = pd.to_datetime(df['date'])
  df = df[df['date'] <= '2020-03-01']
  df = df[['date', column]]
  df.columns = ['ds', 'y']
  return df

def interest(file, column):
  df = file
  df['date'] = pd.to_datetime(df['date'])
  df = df[['date', column]]
  df.columns = ['ds', 'y']
  return df

# def make_comparison_dataframe(historical, forecast):
#   return forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(historical.set_index('ds'))


# def calculate_forecast_errors(df, prediction_size):
#   df = df.copy()
#   df['e'] = df['y'] - df['yhat']
#   df['p'] = 100 * df['e'] / df['y']

#   predict_part = df[-prediction_size:]
#   error_mean = lambda error_name: np.mean(np.abs(predict_part[error_name]))

#   return {'MAPE': error_mean('p'), 'MAE': error_mean('e')}


# def prediction(file, search_term):
#   df = clean_interest(file, search_term)
#   prediction_size = 30
#   train_df = df[:-prediction_size]
#   m = Prophet()
#   m.fit(train_df)
#   future = m.make_future_dataframe(periods=50, freq='W')
#   forecast = m.predict(future)
#   df = interest(file, search_term)
#   cmp_df = make_comparison_dataframe(df, forecast)  
#   return cmp_df


def related_dict(related_query,related_trending):
  df = related_query[related_trending[0]]['top']
  df['search term'] = related_trending[0]
  df['Type'] = 'top'
  dfs.append(df)
  df = related_query[related_trending[0]]['rising']
  df['search term'] = related_trending[0]
  df['Type'] = 'rising'
  dfs.append(df)
  return df

#for err_name, err_value in calculate_forecast_errors(cmp_df, prediction_size).items():
#    print (err_name, err_value)
#############################################################################

#will run first. You can jusy hit this and it would run

if __name__ == '__main__':
  pytrend = TrendReq()

#  searches_museum = ['science and industry', 'science museum', 'field museum', 'shedd aquarium', 'art institute',
#                       'navy pier','lincoln park zoo', 'chicago children museum','museum of contemporary art',
#                       'zoo brookfield', 'peggy notebaert', 'museum','art museum', 'zoo', 'home with kids', 
#                       'Science for kids', 'things to do','diy', 'near me', 'virtual', 'virtual field trips', 
#                       'virtual tour','virtual museum tours']


  searches_museum = ['science and industry', 'field museum', 'shedd aquarium', 'art institute',
                      'lincoln park zoo','zoo brookfield', 'museum','art museum', 'zoo', 'marvel']

  s=Spread('MSI_Google Trend') 
  
    #s=Spread('MSI_Google Trend', config=dict)
    #s = Spread('Test', config=dict)

    #d = {'col1': [889, 669], 'col2': [890, 409]}
    #df = pd.DataFrame(data=d)
    #s.df_to_sheet(df, sheet='testsheet', start='A1', index=False, replace=True)

  groupkeywords_museum = list(zip(*[iter(searches_museum)]*1))
  groupkeywords_museum = [list(x) for x in groupkeywords_museum]

  #Last 5 Years
  # dicti = {}
  # i = 1
  # for trending in groupkeywords_museum:
  #       pytrend.build_payload(trending, timeframe='today 5-y', geo='US-IN-602')
  #       dicti[i] = pytrend.interest_over_time()
  #       i += 1
  #       result_museum = pd.concat(dicti, axis=1)
  #       result_museum.columns = result_museum.columns.droplevel(0)
  #       result_museum = result_museum.drop('isPartial', axis=1)
  #       result_museum = result_museum.reset_index()
  #       result_museum = result_museum.rename(columns={'index': 'date'})
  #       s.df_to_sheet(result_museum, sheet='Result_Museum_5years',
  #                     start='A1', index=False, replace=True)
  
  dicti = {}
  i = 1
  for trending in groupkeywords_museum:
    try:
      pytrend.build_payload(trending, timeframe='today 5-y', geo='US-IN-602')
      dicti[i] = pytrend.interest_over_time()
      i += 1
      time.sleep(6)
    except requests.exceptions.Timeout:
      print("Timeout occured")
  result_museum = pd.concat(dicti, axis=1)
  result_museum = result_museum.droplevel(0, axis=1)
  result_museum = result_museum.drop('isPartial', axis=1)
  result_museum = result_museum.reset_index()
  result_museum = result_museum.rename(columns={'index': 'date'})
  s.df_to_sheet(result_museum, sheet='Result_Museum_5years',
                      start='A1', index=False, replace=True)
  
  
  #Last 90 days
  dicti = {}
  i = 1
  for trending in groupkeywords_museum:
    try:
      pytrend.build_payload(trending, timeframe='today 3-m', geo= 'US-IN-602')
      dicti[i] = pytrend.interest_over_time()
      i += 1
      time.sleep(6)
    except requests.exceptions.Timeout:
      print("Timeout occured")
  result_museum90 = pd.concat(dicti, axis=1)
  result_museum90 = result_museum90.droplevel(0, axis=1)
        #result_museum90.columns = result_museum90.columns.droplevel(0)
  result_museum90 = result_museum90.drop('isPartial', axis=1)
  result_museum90 = result_museum90.reset_index()
  result_museum90 = result_museum90.rename(columns={'index': 'date'})
  s.df_to_sheet(result_museum90, sheet='Result_Museum_90days',
                      start='A1', index=False, replace=True)

  #Prediction
  # search_term = ['science and industry', 'museum', 'zoo']

  # for term in search_term:
  #       file = result_museum
  #       df = prediction(file, term)
  #       s.df_to_sheet(df, sheet=term, start='A1', replace=True)

  #TOP and RISING related words
  #related_searches = ['virtual', 'science', 'kids',
  #                      'museum', 'zoo', 'things to do', 'online', 'summer']
                        
  related_searches = ['science', 'kids','museum', 'marvel']

  related_groupkeywords = list(zip(*[iter(related_searches)]*1))
  related_groupkeywords = [list(x) for x in related_groupkeywords]

  dicti = {}
  i = 1
  dfs = []
  for related_trending in related_groupkeywords:
        pytrend.build_payload(related_trending, timeframe='today 3-m', geo= 'US-IN-602')
        dicti[related_trending[0]] = pytrend.related_queries()
        related_query = dicti[related_trending[0]]
        df = related_dict(related_query, related_trending)
        df = pd.concat(dfs)
        df = df.reset_index()
        df = df.drop(columns=('index'))
        s.df_to_sheet(df, sheet='Related Search Terms',
                      start='A1', replace=True, index=False)
                      

"""
 #Last 5 Years
    dicti = {}
    i = 1
    for trending in groupkeywords_museum:
        pytrend.build_payload(trending, timeframe='today 5-y', geo='US-IN-602')
        dicti[i] = pytrend.interest_over_time()
        i += 1
        result_museum = pd.concat(dicti, axis=1)
        result_museum.columns = result_museum.columns.droplevel(0)
        result_museum = result_museum.drop('isPartial', axis=1)
        result_museum = result_museum.reset_index()
        result_museum = result_museum.rename(columns={'index': 'date'})
        s.df_to_sheet(result_museum, sheet='Result_Museum_5years',
                      start='A1', index=False, replace=True)

#Last 90 days
    dicti = {}
    i = 1
    for trending in groupkeywords_museum:
        pytrend.build_payload(trending, timeframe='today 3-m', geo= 'US-IN-602')
        dicti[i] = pytrend.interest_over_time()
        i += 1
        result_museum90 = pd.concat(dicti, axis=1)
        result_museum90.columns = result_museum90.columns.droplevel(0)
        result_museum90 = result_museum90.drop('isPartial', axis=1)
        result_museum90 = result_museum90.reset_index()
        result_museum90 = result_museum90.rename(columns={'index': 'date'})
        s.df_to_sheet(result_museum90, sheet='Result_Museum_90days',
                      start='A1', index=False, replace=True) """
