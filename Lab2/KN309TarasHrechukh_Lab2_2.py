import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from numpy import array, arange
from matplotlib.dates import MonthLocator, DateFormatter, DayLocator

chart_types = {1: 'Linear', 2: 'Scatter', 3: 'Bar'}


# Function for selecting columns which data we need to show
def data_selector(dataframe):
    print("Choose columns (using SPACE for multiply choice):")
    for i in range(0, len(dataframe.columns)):
        print('(' + str(i + 1) + ') --> ' + str(dataframe.columns[i]))
    print('Input: ', end=' ')
    return array(list(map(int, input().split()))) - 1


# Ploting data
def plot_maker(plot_kind, dataframe, allArea=True, region=None):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(1, 1, 1)

    # For Graph plot
    if plot_kind == 1:
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')

        x = pd.to_datetime(dataframe.index)

        # Selecting chart type
        print("------------------------------------------------------------------------------------------------------")
        print("Please choose menu:")
        for key, value in chart_types.items():
            print(f"({key}) --> {value}")
        plot_type = int(input('Input: '))
        selected_columns = data_selector(dataframe)

        # Linear plot
        if plot_type == 1:
            for column in selected_columns:
                y = dataframe.iloc[:, column].cumsum()
                ax.plot(x, y, label=dataframe.columns[column])

        # Scatter plot
        elif plot_type == 2:
            for column in selected_columns:
                y = dataframe.iloc[:, column]
                ax.scatter(x, y, label=dataframe.columns[column])

        # Bar chart
        elif plot_type == 3:
            i = len(selected_columns)
            widths = arange(0, 14, 14 / i)
            for column in selected_columns:
                y = dataframe.iloc[:, column]
                ax.bar(x + timedelta(hours=int(widths[i - 1])), y, 0.25, label=dataframe.columns[column])
                i -= 1

        # Setting labels
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Count', fontsize=10)
        plt.legend(fontsize=10)

    # For PieChart
    elif plot_kind == 2:
        pieData = dataframe.sum()
        labels = list(dataframe.columns)
        ax.pie(pieData, autopct='%1.1f%%', rotatelabels=True, shadow=True, startangle=45)
        plt.legend(labels=labels, fontsize=10)

    # Setting title
    if allArea:
        title_label = 'COVID-19 Statistic for all Ukraine'
    else:
        title_label = f'COVID-19 Statistic for {region} region'
    plt.title(title_label, fontsize=10)
    plt.show()


# Comparison between selected regions
def compare_data_plot(dataframe, regions):
    temp = []
    for col in regions:
        temp.append(dataframe[dataframe.registration_area == col].groupby(dataframe['zvit_date']).sum().active_confirm)
    plt.xlabel('Timeline')
    i = 0
    for col in temp:
        plt.plot(col.tail(20).index, col.tail(20), label=regions[i])
        i += 1
    plt.xticks(rotation=90)
    plt.title("Active Confirm")
    plt.legend()
    plt.show()
