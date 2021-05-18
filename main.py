
# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    import pandas as pd
    import datetime 
    import numpy as np


    args = config()
    df_g = pd.read_csv(args.generation)
    df_c = pd.read_csv(args.consumption)


    one_day_g = df_g[-24:-1]
    one_day_c = df_c[-24:-1]
    # print(one_day_g.values[0][1])
    # print(one_day_c.values)

    result = []
    for i in range(len(one_day_g.values)):
        result.append([one_day_g.values[i][0], round(one_day_g.values[i][1] - one_day_c.values[i][1], 2)])


    print(result)
    # consume = one_day_c['consumption'].sum()
    # generation = one_day_g['generation'].sum()

    # buy_sell = round(generation - consume, 2)
    data = []
    for i in range(len(result)):
        date = datetime.datetime.strptime(result[i][0] , "%Y-%m-%d %H:%M:%S")
        date += datetime.timedelta(days=1)
        tomorrow_date = date.strftime("%Y-%m-%d %H:%M:%S")
        if result[i][1] > 0:
            data.append([tomorrow_date, "sell", 2.4, result[i][1]])
        elif result[i][1] < 0:
            data.append([tomorrow_date, "buy", 2.8, abs(result[i][1])])
    # date = datetime.datetime.strptime(one_day_g.values[0][0] , "%Y-%m-%d %H:%M:%S")
    # date += datetime.timedelta(days=1)
    # tomorrow_date = date.strftime("%Y-%m-%d %H:%M:%S")

    # if buy_sell > 0:
    #     data = [[tomorrow_date, "sell", 2.4, buy_sell]]
    # elif buy_sell < 0:
    #     data = [[tomorrow_date, "buy", 2.8, abs(buy_sell)]]
    # else:    
    #     data = [[]]

    output(args.output, data)
