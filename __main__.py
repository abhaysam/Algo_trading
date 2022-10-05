#%% Testing the Simple Moving Average trading strategy (We use two different SMAs and take position when one SMA overlaps other SMA)

from SMABacktester import SMABacktester
tester = SMABacktester("EURUSD=X", 50,200,"2004-01-01","2020-06-30")    
tester.test_strategy()
tester.optimize_parameters((10,50,1),(100,252,1))
tester.plot_results()
tester.results_overview

#%% Testing the Contrarian or Momentum trading strategy (We take positions exactly opposite to the trends)

from ConBacktester import ConBacktester
tester = ConBacktester("EURUSD=X", 50,200,"2004-01-01","2020-06-30")    
tester.test_strategy()
tester.optimize_parameters((10,50,1),(100,252,1))
tester.plot_results()
tester.results_overview