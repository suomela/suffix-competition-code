# Code for the article "New methods for analysing diachronic suffix competition across registers"

This repository contains source code connected to the following article:

- Rodríguez-Puente, Paula, Tanja Säily and Jukka Suomela. "New methods for analysing diachronic suffix competition across registers: How *-ity* gained ground on *-ness* in Early Modern English". *International Journal of Corpus Linguistics.* https://doi.org/10.1075/ijcl.22014.rod


## Quick start

To reproduce the figures and other results in the paper, clone this repository and run:

    ./run-all.sh 


## More details

The script will:

- fetch input data from https://github.com/suomela/suffix-competition
- fetch and build the TypeRatio tool from https://github.com/suomela/type-ratio
- run Python scripts that read the input data and use the TypeRatio tool to produce the results.

You will find the final results in these directories:

- `type-ratio-result-100`
- `type-ratio-result-50`
- `type-ratio-result-legal`

More specifically, you will find the figures in the article in the following places:

- Figure 1: `type-ratio-result-100/timeseries.pdf`
- Figure 2: `type-ratio-result-100/period-1600-1699.pdf`
- Figure 3: `type-ratio-result-100/timeseries-S-1600-1699.pdf`
- Figure 4: `type-ratio-result-100/timeseries-W-1600-1699.pdf`
- Figure 5: `type-ratio-result-100/trend-S-W.pdf`
- Figure 6: `type-ratio-result-50/trend-S-W.pdf`
- Figure 7: `type-ratio-result-legal/timeseries-L.pdf`


## Requirements

Please see https://github.com/suomela/type-ratio for more information on the software that you need to install, and on suitable Docker images that you can use.


## Author

Jukka Suomela, https://jukkasuomela.fi/
