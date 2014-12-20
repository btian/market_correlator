market_correlator
=================

Find highly correlated stocks.

Requirements
  * Python 2.7+
  * numpy
  * ystockquote

Example usage

```
$ python market_correlator.py symbols.txt SPY 2014-01-01 2014-12-18 10

Ticker	R-value
IVV	0.999986
VOO	0.999948
VV	0.999749
SCHX	0.999664
MGC	0.999655
SSO	0.999172
ITOT	0.999163
IWB	0.999161
VONE	0.999129
IWL	0.998720
```
```
$ python market_correlator.py symbols.txt GLD 2014-01-01 2014-12-18 10 --skip_dataload

Ticker	R-value
SGOL	0.999953
IAU	0.999869
DGL	0.999010
DGP	0.998088
UGL	0.998006
PHYS	0.997431
UGLD	0.995061
UBG	0.987453
DBP	0.986974
GTU	0.974220
```
