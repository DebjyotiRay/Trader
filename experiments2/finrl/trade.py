from __future__ import annotations

# from finrl.meta.env_stock_trading.env_stock_papertrading import AlpacaPaperTrading
from finrl.meta.env_stock_trading.script import AlpacaPaperTrading
from finrl.test import test
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
APCA_API_KEY_ID = 'PK6OLMQA3TSKGUT30NG7'
APCA_API_SECRET_KEY = 'Jb2dE9ir20DlosSvfkP9YI8Tywtec9KJPP446cy6'
import alpaca_trade_api as tradeapi
# Set up Alpaca API
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL, api_version='v2')

def trade(
    start_date,
    end_date,
    ticker_list,
    data_source,
    time_interval,
    technical_indicator_list,
    drl_lib,
    env,
    model_name,
    API_KEY,
    API_SECRET,
    API_BASE_URL,
    trade_mode,
    if_vix=True,
    **kwargs,
):
    if trade_mode == "backtesting":
        # use test function for backtesting mode
        test(
            start_date,
            end_date,
            ticker_list,
            data_source,
            time_interval,
            technical_indicator_list,
            drl_lib,
            env,
            model_name,
            if_vix=True,
            **kwargs,
        )

    elif trade_mode == "paper_trading":
        # read parameters
        try:
            net_dim = kwargs.get("net_dimension", 2**7)  # dimension of NNs
            cwd = kwargs.get("cwd", "./" + str(model_name))  # current working directory
            state_dim = kwargs.get("state_dim")  # dimension of state/observations space
            action_dim = kwargs.get("action_dim")  # dimension of action space
        except:
            raise ValueError(
                "Fail to read parameters. Please check inputs for net_dim, cwd, state_dim, action_dim."
            )

        # initialize paper trading env
        paper_trading = AlpacaPaperTrading(
            ticker_list, #kaunse kaunse stock mein trade karega
            time_interval,
            drl_lib, #library: stablebaselines3
            model_name,
            cwd,
            net_dim,
            state_dim,
            action_dim,
            API_KEY,
            API_SECRET,
            API_BASE_URL,
            technical_indicator_list,
            turbulence_thresh=30,
            max_stock=1e2,
            latency=None,
        )

        # AlpacaPaperTrading.run()  # run paper trading
        paper_trading.run()
        # bug fix run is a instance function not static

    else:
        raise ValueError(
            "Invalid mode input! Please input either 'backtesting' or 'paper_trading'."
        )
import datetime
curr=str(datetime.datetime.now())
date=curr[:10]
print("aaj ka date",date)
TRAIN_START_DATE = '2010-01-01'
TRAIN_END_DATE = '2021-10-01'
TEST_START_DATE = '2021-10-01'
TEST_END_DATE =  date
DOW_30_TICKER=['AXP','AAPL', 'AMGN','MSFT', 'JPM']
print("ye trade wala file hai")
from finrl.meta.preprocessor.yahoodownloader import YahooDownloader
df = YahooDownloader(start_date = TRAIN_START_DATE,
                     end_date = TEST_END_DATE,
                     ticker_list = DOW_30_TICKER).fetch_data()
from finrl.config import INDICATORS
from finrl.meta.preprocessor.preprocessors import FeatureEngineer
import numpy as np
fe = FeatureEngineer(use_technical_indicator=True,
                     tech_indicator_list = INDICATORS,
                     use_turbulence=True,
                     user_defined_feature = False)

processed = fe.preprocess_data(df)
processed = processed.copy()
processed = processed.fillna(0)
processed = processed.replace(np.inf,0)

# print(processed.sample(5))
stock_dimension = len(processed.tic.unique())
state_space = 1 + 2*stock_dimension + len(INDICATORS)*stock_dimension
print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

env_kwargs = {
    "hmax": 100,
    "initial_amount": 1000000,
    "buy_cost_pct": 0.001,
    "sell_cost_pct": 0.001,
    "state_space": state_space,
    "stock_dim": stock_dimension,
    "tech_indicator_list": INDICATORS,
    "action_space": stock_dimension,
    "reward_scaling": 1e-4,
    "print_verbosity":5

}
from finrl.meta.env_stock_trading.env_stocktrading import StockTradingEnv as st_env
from finrl.agents.stablebaselines3.models import DRLEnsembleAgent
# time_interval,
# technical_indicator_list,
# drl_lib,
# env,
# model_name,
# API_KEY,
# API_SECRET,
# API_BASE_URL,
# trade_mode = "backtesting",
# if_vix = True,
# ** kwargs,
trade(TEST_START_DATE, TEST_END_DATE, DOW_30_TICKER , data_source=processed, time_interval="60Min", technical_indicator_list=INDICATORS, drl_lib="stable_baselines3", env=st_env, model_name= DRLEnsembleAgent )