import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# import talib
import pytz
import time


class MT5_Trader:
    def __init__(self, server_name, login, password):
        self.sever_name = server_name
        self.login = login
        self.password = password
        self.broker_data = {
            "server": server_name,
            "password": password,
            "login": login
        }
        if not mt5.initialize(**self.broker_data):
            print("initialize() failed")
            mt5.shutdown()
            exit()
        print(mt5.version())
        print(mt5.account_info())

    def submitOrder(self, symbol: str, qty: float, side: str, resp: list[bool]):
        if qty <= 0:
            print(f"Quantity is 0, order of | {qty} {
                  symbol} {side} | not completed.")
            resp.append(False)
            return
        try:
            if not mt5.terminal_info().trade_allowed:
                print(
                    "AutoTrading is disabled by client. Please enable AutoTrading in the terminal.")
                resp.append(False)
                return
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                print(f"Symbol info for {symbol} not found")
                resp.append(False)
                return

            tick_info = mt5.symbol_info_tick(symbol)
            if tick_info is None:
                print(f"Tick info for {symbol} not found")
                resp.append(False)
                return

            filling_mode = mt5.ORDER_FILLING_IOC
            ask_price = tick_info.ask
            bid_price = tick_info.bid
            point = symbol_info.point
            deviation = 20  # You can customize or fetch dynamically

            if side == 'buy':
                type_trade = mt5.ORDER_TYPE_BUY
                sl = ask_price * (1 - 0.01)
                tp = ask_price * (1 + 0.01)
                price = ask_price
            elif side == 'sell':
                type_trade = mt5.ORDER_TYPE_SELL
                sl = bid_price * (1 + 0.01)
                tp = bid_price * (1 - 0.01)
                price = bid_price
            else:
                print(f"Invalid side: {side}")
                resp.append(False)
                return

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": qty,
                "type": type_trade,
                "price": price,
                "deviation": deviation,
                "sl": sl,
                "tp": tp,
                "magic": 234000,  # Unique id for our monitoring
                "comment": f"{qty} {symbol} {side}",
                "type_time": mt5.ORDER_TIME_GTC,  # Still when the order will be in queue
                # Similar to above property but deals with volume
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Order failed: {result.comment}")
                resp.append(False)
            else:
                print(f"Order successful: {result.comment}")
                resp.append(True)

        except Exception as e:
            print(f"Order of | {qty} {symbol} {
                  side} | did not go through. Error: {str(e)}")
            resp.append(False)

    @staticmethod
    def check_symbol_info(symbol: str) -> None:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"{symbol} not found, cannot proceed")
            mt5.shutdown()
            exit()

    @staticmethod
    def awaitMarketOpen(symbol: str, check_interval: int = 60) -> None:
        while True:
            try:
                symbol_info = mt5.symbol_info(symbol)
                
                if symbol_info is None:
                    print(f"Error retrieving symbol information for {symbol}")
                    time.sleep(check_interval)
                    continue
                
                if symbol_info.session_deals > 0 or symbol_info.session_buy_orders > 0:
                    print(f"Market is open for {symbol}")
                    break
                
                print(f"Market is closed for {symbol}. Checking again in {check_interval} seconds.")
                time.sleep(check_interval)
            
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    @staticmethod
    def fetch_latest_data(ticker_list: list[str], time_interval: timedelta, tech_indicator_list: list[str]):
        end_time = datetime.now()
        start_time = end_time - time_interval

        all_data = {}
        # for ticker in ticker_list:
        #     rates = mt5.copy_rates_range(ticker, mt5.TIMEFRAME_M1, start_time, end_time)
        #     if rates is None:
        #         print(f"Failed to get rates for {ticker}")
        #         continue

        #     df = pd.DataFrame(rates)
        #     df['time'] = pd.to_datetime(df['time'], unit='s')
        #     df.set_index('time', inplace=True)
        #     for indicator in tech_indicator_list:
        #         df[indicator] = getattr(talib, indicator)(df['close'])

        #     all_data[ticker] = df

        return all_data

    @staticmethod
    def list_positions():
        positions = mt5.positions_get()
        if positions is None:
            print("No positions found, error code =", mt5.last_error())
            return []

        print("Total positions found:", len(positions))
        positions_df = pd.DataFrame(
            list(positions), columns=positions[0]._asdict().keys())
        print(positions_df)
        return positions_df

    @staticmethod
    def get_account():
        account_info = mt5.account_info()
        # how to format the data??

    @staticmethod
    def list_orders():
        orders = mt5.orders_get()
        if orders is None:
            print("No orders found, error code =", mt5.last_error())
            return

        print("Total orders found:", len(orders))
        orders_df = pd.DataFrame(
            list(orders), columns=orders[0]._asdict().keys())
        print(orders_df)

    @staticmethod
    def cancel_order(ticket):
        result = mt5.order_delete(ticket)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Failed to cancel order #{
                  ticket}, error code =", result.retcode)
        else:
            print(f"Order #{ticket} canceled successfully")

    def get_market_close_time(self, symbol):
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"{symbol} not found, cannot proceed")
            return None

        sessions = symbol_info.trade_hours

        now = datetime.now(pytz.timezone(symbol_info.exchange_timezone))
        for session in sessions:
            start_time = datetime.strptime(session['open'], '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)
            end_time = datetime.strptime(session['close'], '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)

            if start_time <= now <= end_time:
                return end_time

        return None

    def time_to_close(self, symbol):
        market_close_time = self.get_market_close_time(symbol)
        if market_close_time is None:
            print(f"Market close time not found for {symbol}")
            return None

        now = datetime.now(pytz.timezone(
            mt5.symbol_info(symbol).exchange_timezone))
        time_remaining = market_close_time - now
        return time_remaining


bot = MT5_Trader(login=175127194, server_name="Exness-MT5Trial7",
                 password="swaroop1946@A")
response_list = []

bot.awaitMarketOpen("AUDUSDm", 60)
bot.submitOrder(symbol="AUDUSDm", qty=0.01, side="buy", resp=response_list)
print("Response list:", response_list)

time.sleep(2)

bot.submitOrder(symbol="AUDUSDm", qty=0.01, side="sell", resp=response_list)
print("Response list:", response_list)



## Return value type matting with existing code