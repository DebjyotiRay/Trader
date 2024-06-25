import datetime
curr=str(datetime.datetime.now())
date=curr[:10]
print("aaj ka date",date)
TRAIN_START_DATE = '2024-01-01'
TRAIN_END_DATE = date
TEST_START_DATE = '2024-03-01'
TEST_END_DATE =  date
DOW_30TICKER=['EURUSD=X']
from finrl.meta.preprocessor.yahoodownloader import YahooDownloader
df = YahooDownloader(start_date = TRAIN_START_DATE,
                     end_date = TEST_END_DATE,
                     ticker_list = DOW_30TICKER).fetch_data()


print(df.head())