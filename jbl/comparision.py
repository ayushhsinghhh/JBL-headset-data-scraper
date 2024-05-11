import pandas as pd
import os


def compare_csv_files(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    if "IN" in file1:
        df1country = "IN"
    else:
        df1country = "UK"
    if "UK" in file2:
        df2country = "UK"
    else:
        df2country = "IN"
    df1.set_index('Name', inplace=True)
    df2.set_index('Name', inplace=True)

    for index, row in df1.iterrows():
        if index in df2.index:
            row2 = df2.loc[index]

            for column in df1.columns:
                if row[column] != row2[column]:
                    print(
                        f"Difference in '{index}': Spec '{column}' - {df1country}: '{row[column]}', {df2country}: '{row2[column]}'")


def compare_category_files(folder1, folder2):
    for file1, file2 in zip(os.listdir(folder1), os.listdir(folder2)):
        if file1.endswith('.csv') and file2.endswith('.csv'):
            category1 = os.path.splitext(file1)[0][:-3]
            category2 = os.path.splitext(file2)[0][:-3]
            print(category1, category2)
            if category1 == category2:
                compare_csv_files("D:\\Coding\\Webscrapping\\jbl\\IN_headsets\\"+file1, "D:\\Coding\\Webscrapping\\jbl\\UK_headsets\\"+file2)


compare_category_files('IN_headsets', 'UK_headsets')
