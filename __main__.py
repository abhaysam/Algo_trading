#%% Testing the Simple Moving Average trading strategy (We use two different SMAs and take position when one SMA overlaps other SMA)

from SMABacktester import SMABacktester
tester = SMABacktester("EURUSD=X", 50,200,"2004-01-01","2020-06-30",0.0000)    
tester.test_strategy()
tester.optimize_parameters((10,50,1),(100,252,1))
tester.plot_results()
tester.results_overview

#%% Testing the Contrarian or Momentum trading strategy (We take positions exactly opposite to the trends)

from ConBacktester import ConBacktester
tester = ConBacktester("intraday.csv", 3,"2018-01-01","2019-12-30",0.0000)    
tester.test_strategy()
tester.plot_results()
tester.optimize_parameters((1,10,1))
all_results = tester.results_overview

#%% Mean reversion strategy

from MeanRevBacktester import MeanRevBacktester
tester = MeanRevBacktester("intraday_pairs.csv", 30,2,"2018-01-01","2018-12-31",0.00007, "EURUSD")    
tester.test_strategy()
tester.plot_results()

# Optimizing on the training set
optimized_results = tester.optimize_parameters((25,100,1), (1,5,1))
all_results = tester.results_overview

# Trying optimized parameters on the test set
SMA = optimized_results[0][0]
dev = optimized_results[0][1]
tester_opt = MeanRevBacktester("intraday_pairs.csv", SMA,dev,"2019-01-01","2019-12-31",0.00007, "EURUSD")  
tester_opt.test_strategy()