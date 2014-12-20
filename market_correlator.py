#!/usr/bin/env python

# Copyright (c) 2014, Bo Tian <tianbo@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors may
# be used to endorse or promote products derived from this software without specific
# prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import numpy as np
import ystockquote

import logging
import operator
import os
import sys

logger = logging.getLogger(__name__)
handler = logging.FileHandler('market_correlator.INFO')
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def main():
  """
  Find highly correlated publicly traded securities.
  Usage:
    python market_correlator.py TICKERS_FILE TICKER START_DATE END_DATE NUM_TO_DISPLAY \
      [--skip_dataload]
  Example:
    python market_correlator.py symbols.txt IBM 2014-01-01 2014-12-15 10
  Args:
    TICKERS_FILE - text file containing all tickers to look for correlation in.
    TICKER - ticker of the security to find correlation in.
    START_DATE - start date to find correlation.
    END_DATE - end date to find correlation.
    NUM_TO_DISPLAY - number of highest correlated securities to show.
  Optional:
    --skip_dataload to use data loaded by previous runs.
  """
  
  args = sys.argv
  print args
  logger.info(str(args))
  assert len(args) == 6 or len(args) == 7
  tickers_file = args[1]
  ticker = args[2]
  start_date = args[3]
  end_date = args[4]
  num_to_display = int(args[5])
  if len(args) == 6:
    load_data(tickers_file, start_date, end_date)
  correlations = find_correlations(ticker)
  print_correlations(correlations, num_to_display)

def load_data(input_file, start_date, end_date):
  logger.info('Loading data...')
  if not os.path.exists('data'):
    os.makedirs('data')
  for ticker in open(input_file, 'r'):
    ticker = ticker.rstrip()
    logger.info('Processing %s' % ticker)
    historical_prices = {}
    try:
      historical_prices = ystockquote.get_historical_prices(ticker, start_date, end_date)
    except Exception as e:
      logger.exception('Failed to get price for %s' % ticker)
      continue
    # Sort historical prices by date.
    historical_prices = sorted(historical_prices.items(), key=operator.itemgetter(0))
    _, v = historical_prices[0]
    base_price = float(v['Adj Close'])
    out = open('data/%s' % ticker, 'w')
    for _, v in historical_prices:
      adj_close = float(v['Adj Close'])
      change = adj_close / base_price
      out.write(str(change) + ',')
    out.close()

def find_correlations(ticker):
  """Returns sorted list of correlated securities."""
  avail_tickers = [ f for f in os.listdir('data') if os.path.isfile(os.path.join('data', f)) ]
  prices = {}
  for t in avail_tickers:
    with open(os.path.join('data', t), 'r') as fin:
      historical_prices = fin.read().rstrip(',').split(',')
      historical_prices = [ float(p) for p in historical_prices ]
      prices[t] = historical_prices
  correlations = {}
  ticker_prices = prices[ticker]
  for k, v in prices.items():
    if k == ticker:
      continue
    if len(ticker_prices) != len(v):
      logger.warning('Cannot calculate corr coef of %s and %s '
                     'due to different number of data points' % (ticker, k))
      continue
    correlations[k] = np.corrcoef(ticker_prices, v)[0][1]
  #import pdb; pdb.set_trace()
  return sorted(correlations.items(), key=operator.itemgetter(1), reverse=True)

def print_correlations(correlation_list, num_to_print):
  print 'Ticker\tR-value'
  for i in range(num_to_print):
    ticker, r_val = correlation_list[i] 
    print '%s\t%f' % (ticker, r_val)
      

if __name__ == "__main__":
    main()
