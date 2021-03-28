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


if __name__ == '__main__':
  pytrend = TrendReq()

  searches_museum = ['zoo', 'kids'] # search terms you want to download data for

  s=Spread('Google Trend') #name of sheet you are connected to
  
  groupkeywords_museum = list(zip(*[iter(searches_museum)]*1))
  groupkeywords_museum = [list(x) for x in groupkeywords_museum]
  
  dicti = {}
  i = 1
  for trending in groupkeywords_museum:
    try:
      pytrend.build_payload(trending, timeframe='today 5-y', geo='US-NY-501')
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
      pytrend.build_payload(trending, timeframe='today 3-m', geo= 'US-NY-501')
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

                        
  related_searches = ['zoo', 'kids',]

  related_groupkeywords = list(zip(*[iter(related_searches)]*1))
  related_groupkeywords = [list(x) for x in related_groupkeywords]

  dicti = {}
  i = 1
  dfs = []
  for related_trending in related_groupkeywords:
        pytrend.build_payload(related_trending, timeframe='today 3-m', geo= 'US-NY-501')
        dicti[related_trending[0]] = pytrend.related_queries()
        related_query = dicti[related_trending[0]]
        df = related_dict(related_query, related_trending)
        df = pd.concat(dfs)
        df = df.reset_index()
        df = df.drop(columns=('index'))
        s.df_to_sheet(df, sheet='Related Search Terms',
                      start='A1', replace=True, index=False)
                      
