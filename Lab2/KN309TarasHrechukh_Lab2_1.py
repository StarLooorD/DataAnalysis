import KN309TarasHrechukh_Lab2_2
from numpy import array
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from collections import Counter


def get_sum_data(line, region_names):
    values = []
    for region in region_names:
        values.append(covid_data.loc[covid_data['registration_area'] == region][line].sum())
    return values


def regionsList(df):
    regions = array(list(Counter(df.loc[:, 'registration_area']).keys()))
    for i in range(len(regions)):
        print('(' + str(i + 1) + ') --> ' + regions[i])
    region_number = int(input('Input: ')) - 1
    return df[covid_data['registration_area'] == regions[region_number]], regions[region_number]


covid_data = pd.read_csv("covid19_by_settlement_dynamics.csv", delimiter=",")
# print(covid_data)

while True:
    print("----------------------------------------------------------------------------------------------------------")
    print("Please choose menu:")
    print("(1) --> COVID-19 spread for All Ukraine")
    print("(2) --> COVID-19 spread for Specific Region")
    print("(3) --> Compare spread in some Regions")
    print("(4) --> View COVID-19 spread on a MAP")
    print("(5) --> Export data to XLSX")
    print("(6) --> Exit Program")
    command = int(input('Input: '))

    if command == 1:
        country = covid_data.groupby('zvit_date').sum()
        # print(country)
        print("------------------------------------------------------------------------------------------------------")
        print("Please choose menu:")
        print("(1) --> Graph")
        print("(2) --> Pie Chart")
        plot_kind = int(input('Input: '))
        KN309TarasHrechukh_Lab2_2.plot_maker(plot_kind, country)
    elif command == 2:
        region, regionName = regionsList(covid_data)
        grouped_regions = region.groupby('zvit_date').sum()
        # print(grouped_regions)
        print("------------------------------------------------------------------------------------------------------")
        print("Please choose menu:")
        print("(1) --> Graph")
        print("(2) --> Pie Chart")
        plot_kind = int(input('Input: '))
        KN309TarasHrechukh_Lab2_2.plot_maker(plot_kind, grouped_regions, False, regionName)
    elif command == 3:
        regions = array(list(Counter(covid_data.loc[:, 'registration_area']).keys()))
        print("------------------------------------------------------------------------------------------------------")
        print("Please choose regions to compare (using SPACE for multiply choice):")
        for i in range(len(regions)):
            print('(' + str(i + 1) + ') --> ' + regions[i])
        regs = array(list(map(int, input().split()))) - 1
        new_regions = []
        for i in range(len(regions)):
            if i in regs:
                new_regions.append(regions[i])
        KN309TarasHrechukh_Lab2_2.compare_data_plot(covid_data, new_regions)
    elif command == 4:
        print("Chose field:")
        for i in range(4, len(covid_data.columns)):
            print('(' + str(covid_data.columns[i]) + ')')
        print('Input: ', end=' ')
        category = input()
        map_data = gpd.read_file('ukr_admbnda_adm1_q2_sspe_20171221.shp', encoding='utf-8')
        new_map_data = get_sum_data(category, map_data['ADM1_UA'])
        map_data['adm1Clas'] = new_map_data
        map_data.plot(column='adm1Clas', legend=True, cmap='coolwarm')
        plt.show()
    elif command == 5:
        writer = pd.ExcelWriter('my_output.xlsx', engine='xlsxwriter')

        region, regName = regionsList(covid_data)
        region = region.groupby('zvit_date').sum()

        comp1 = covid_data[covid_data['registration_area'] == 'Львівська']
        comp1 = comp1.groupby(['zvit_date']).agg({'active_confirm': "sum"}).rename(
            columns={'active_confirm': 'Львівська'})

        comp2 = covid_data[covid_data['registration_area'] == 'Київська']
        comp2 = comp2.groupby(['zvit_date']).agg({'active_confirm': "sum"}).rename(
            columns={'active_confirm': 'Київська'})

        comp3 = pd.concat([comp1, comp2], axis=1)

        region.to_excel(writer, sheet_name=regName)
        comp3.to_excel(writer, sheet_name='Compare')
        map_data.to_excel(writer, sheet_name='Map Data')

        writer.save()
    else:
        print("Thanks you for using our product!")
        break
