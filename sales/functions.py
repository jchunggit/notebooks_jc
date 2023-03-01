from scipy.stats import linregress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import datetime
import time
from datetime import datetime, timedelta
import concurrent.futures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from prophet import Prophet
import xgboost as xgb
from scipy.stats import mstats

class forecaster:
    def __init__(self, df, start_date, end_date, ext_store_fam, hp):
        self.df = df
        self.start_date = start_date
        self.end_date = end_date
        self.ext_store_fam = ext_store_fam
        self.hyperparameters = hp
        
    def f_prophet(self, store_nbr, family):
        df_subset = self.df[(self.df['store_nbr'] == store_nbr) & 
                            (self.df['family'] == family) & 
                            (pd.to_datetime(self.df['date']) >= pd.to_datetime('2013-01-01', format='%Y-%m-%d')) & 
                            (pd.to_datetime(self.df['date']) < self.start_date)].reset_index()
    
        if not all(col in df_subset.columns for col in ['ds', 'y']):
            df_subset = df_subset.rename(columns={'date': 'ds', 'sales': 'y'})
    
        results = pd.DataFrame()
    
        model = Prophet()
        model.add_regressor('onpromotion')
    
        model.fit(df_subset)
    
        future = model.make_future_dataframe(periods=(self.end_date - self.start_date + datetime.timedelta(days=1)).days, 
                                             freq='D')
        future['onpromotion'] = df_subset['onpromotion'].reindex(index=future.index, method='ffill')
    
        forecast = model.predict(future)
    
        for index, row in forecast.iterrows():
            results_new = pd.DataFrame([{'store_nbr': int(store_nbr), 
                                         'family': family, 
                                         'date': row['ds'], 
                                         'yhat': row['yhat']}])
            results = pd.concat([results, results_new], ignore_index=True)
        return results
    
    def f_xg(self, store_nbr, family):
        df_subset = self.df[(self.df['store_nbr'] == store_nbr) & 
                                    (self.df['family'] == family)].drop(['store_nbr', 
                                                                         'family'], axis = 1).reset_index(drop = True)

        for i in range(1, self.hyperparameters['in_length'] + 1):
            df_subset['sales_' + str(i)] = df_subset['sales'].shift(-i)
            df_subset['onpromotion_' + str(i)] = df_subset['onpromotion'].shift(-i)
            
        df_subset['date'] = df_subset['date'].shift(-1*(self.hyperparameters['in_length']+1))
        df_subset['date'] = pd.to_datetime(df_subset['date'])
        df_subset['is_weekend'] = df_subset['date'].dt.dayofweek.isin([5, 6]).astype(int)
        
        df_subset = df_subset.iloc[:-1*(self.hyperparameters['in_length']+1)].set_index('date')

        first_date = min(df_subset.index)
        end_date = '2017-08-15'

        test_start_date = datetime.strptime('2016-01-01', '%Y-%m-%d')
        test_end_date = test_start_date + timedelta(days = 90)
        test_end_date = test_end_date.strftime('%Y-%m-%d')

        results = []
        while test_start_date < datetime.strptime(end_date, '%Y-%m-%d'):
            train_data = df_subset[(df_subset.index < test_start_date.strftime('%Y-%m-%d'))&
                                   (df_subset.index >= first_date)]
            test_data = df_subset[(df_subset.index >= test_start_date.strftime('%Y-%m-%d'))&
                                  (df_subset.index < test_end_date)]

            X_train = train_data.drop('sales', axis = 1)
            y_train = train_data['sales']
            X_test = test_data.drop('sales', axis = 1)
            y_test = test_data['sales']
            if (store_nbr, family) in self.ext_store_fam:
                model = xgb.XGBRegressor(
                    n_estimators = self.hyperparameters["n_estimators"],
                    max_depth = self.hyperparameters["max_depth"],
                    learning_rate = self.hyperparameters["learning_rate"],
                    subsample = self.hyperparameters["subsample"],
                    min_child_weight = self.hyperparameters["min_child_weight"],
                    objective = self.hyperparameters["objective"],
                    tree_method = self.hyperparameters["tree_method"],
                    colsample_bytree = self.hyperparameters["colsample_bytree"],
                    gamma = self.hyperparameters["gamma"]
                )
            else:
                model = xgb.XGBRegressor()
                
                
            model.fit(X_train, y_train,
                    eval_set=[(X_train, y_train), (X_test, y_test)],
                    verbose=False)
            y_pred = model.predict(X_test)
            y_test = np.array(y_test)
            test_mae = mean_absolute_error(y_test, y_pred)

            result = pd.DataFrame()
            result['date'] = df_subset.loc[X_test.index].index
            result['family'] = family
            result['store_nbr'] = int(store_nbr)
            result['yhat'] = y_pred
            results.append(result)

            test_start_date = test_start_date + timedelta(days = 90)
            
            if isinstance(test_end_date, str):
                test_end_date = datetime.strptime(test_end_date, '%Y-%m-%d') + timedelta(days = 90)
            else:
                test_end_date = test_end_date + timedelta(days = 90)
            test_end_date = test_end_date.strftime('%Y-%m-%d')
            
            if isinstance(first_date, str):
                first_date = datetime.strptime(first_date, '%Y-%m-%d') + timedelta(days = 90)
            else:
                first_date = first_date + timedelta(days = 90)
            first_date = first_date.strftime('%Y-%m-%d')
        results = pd.concat(results)
        return results
    
    def run_parallel(self, method, num_workers=7):
        store_family_combinations = self.df[['store_nbr', 'family']].drop_duplicates()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            start = time.time()
            results = [executor.submit(method, 
                                       row['store_nbr'], row['family']) 
                       for index, row in store_family_combinations.iterrows()]
            completed = 0
            total = len(results)
            output = pd.DataFrame()
            for future in concurrent.futures.as_completed(results):
                completed += 1
                print("Progress: {}/{} ({:.2f}%)".format(completed, total, (completed / total) * 100))
                output = pd.concat([output, future.result()], ignore_index=True)
            end = time.time()
        print(end-start)
        return output

def rmsle1617(df, pred_col):
    df_subset = df[(pd.to_datetime(df['date']) >= pd.to_datetime('2016-01-01', format='%Y-%m-%d')) & 
                   (pd.to_datetime(df['date']) <= pd.to_datetime('2017-08-15', format='%Y-%m-%d'))].reset_index()
    return np.sqrt(np.mean(np.power(np.log1p(df_subset['sales']) - np.log1p(df_subset[pred_col]), 2)))

def winsorize_by_group(df, group_cols, target_col, lower_pct, upper_pct):
    df_winsorized = df.copy()
    
    groups = df_winsorized.groupby(group_cols)
    
    for name, group in groups:
        winsorized_vals = mstats.winsorize(groups['sales'].get_group((name[0], name[1])), 
                                           limits=(lower_pct, upper_pct))
        
        df_winsorized.loc[group.index, target_col] = winsorized_vals
    
    return df_winsorized

def hill_estimator(df, epsilon=1e-8):

    df.loc[df['sales'] == 0, 'sales'] = epsilon

    grouped = df.groupby(['store_nbr', 'family'])['sales']
    
    order_stats = grouped.apply(lambda x: np.sort(x)[::-1])
    
    hill = order_stats.apply(lambda x: linregress(np.log(np.arange(1, len(x)+1)),
                                                  np.log(x)).slope)
    
    result = pd.DataFrame({'hill_estimator': hill})
    result.index.names = ['store_nbr', 'family']
    
    return result.reset_index()

def plot_fam(df, family):
    fig, axs = plt.subplots(nrows=4, ncols=5, figsize=(16, 16))
    fig.suptitle(family, fontsize=20, y=1.02)
    df_sub = df[df['family'] == family]
    for i, store_nbr in enumerate(df_sub['store_nbr'].unique()):
        row = i // 5
        col = i % 5
        ax = axs[row, col]
        df_subset = df_sub[df_sub['store_nbr'] == store_nbr]
        df_subset.plot(x='date', y='sales', ax=ax, title=f"Store {store_nbr}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        ax.grid()
    plt.tight_layout()

def plot_store(df, store_nr):
    fig, axs = plt.subplots(nrows = 8, ncols= 5, figsize=(20, 30))
    fig.suptitle(store_nr, fontsize=20, y=1.02)
    df_sub = df[df['store_nbr'] == store_nr]
    for i, family in enumerate(df_sub['family'].unique()):
        row = i // 5
        col = i % 5
        ax = axs[row, col]
        df_subset = df_sub[df_sub['family'] == family]
        df_subset.plot(x='date', y='sales', ax=ax, title=f"Prod Family {family}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        ax.grid()
    plt.tight_layout()