import matplotlib.pyplot as plt
from numpy import array
from pandas import to_datetime
from matplotlib.dates import DateFormatter
from collections import Counter


def data_visualizer(df):
    print("Tell me fields you want me to display:")
    while True:
        for i in range(1, len(df.columns)):
            print('(' + str(i) + ')' + ' -> ' + str(df.columns[i]))
        print('(' + str(11) + ')' + ' -> ' + 'Exit Program')
        menu_input = array(list(map(int, input().split())))

        if 11 in menu_input:
            if len(menu_input) > 1:
                raise ValueError("Please, input any menu from 1 to 10 or just 11 to end program.")
            else:
                print("Thanks for using our product!")
                break

        for menu in menu_input:
            if type(df.iloc[0, menu]) is not str:
                chart = plt.figure().add_subplot()
                x = to_datetime(df.index.astype(str) + ' ' + df['Time'].astype(str))
                y = array(df.iloc[:, menu])
                chart.plot(x, y, label=df.columns[menu])
                chart.grid(which='major', color='black', linestyle='dashdot')
                chart.grid(which='minor', color='black', linestyle='dotted')
                chart.minorticks_on()
                chart.xaxis.set_major_formatter(DateFormatter('%m.%d'))
                plt.xlabel('Date')
                plt.ylabel(df.columns[menu])
                plt.legend()
            else:
                data = Counter(df.iloc[:, menu])
                legend_params = array(list(data.keys()))
                data_values = array(list(data.values()))
                fig, chart = plt.subplots()
                chart.pie(data_values, radius=1.3, explode=[0.07] * len(data_values), shadow=True, startangle=90)
                plt.legend(labels=legend_params, bbox_to_anchor=(1.7, 1.1))
            plt.show()
