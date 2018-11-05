import xlrd, csv
import itertools
import re
from operator import itemgetter
import os, json, getpass, imp
import pandas as pd


def get_cell_range(sh, start_col, start_row, end_col, end_row):
    sh_list = [sh.row_slice(row, start_colx=start_col, 
                            end_colx=end_col+1) for row in range(start_row, end_row+1)]
    sh_val_list = []
    for i, row in enumerate(sh_list):
        sh_val_list.append([])
        for cell in row:
            sh_val_list[i].append(cell.value)
    return sh_val_list


def check_col_dict(fname, col_dict):
    """
    Arg:
        - fname: file name
        - col_dict: {year: {ftype: {tab_num:#, start_row:#, end_row:#, cols:[]}}}
    Return:
        - ftype
        - tab_num
        - start_row
        - end_row
        - cols: list of column indexes
    """
    year = fname[:7]
    year = year[:5] + '20' + year[-2:]
    if "ChildCareData" in fname:
           ftype = "ChildCareData"
    elif "KindergartenData" in fname:
        ftype = "KindergartenData"
    elif "7thGradeData" in fname:
        ftype = "7thGradeData"
    else:
        raise ValueError("not-supported file type")
    tab_num = col_dict[year][ftype]['tab_num']
    start_row = col_dict[year][ftype]['start_row']
    end_row = col_dict[year][ftype]['end_row']
    cols = col_dict[year][ftype]['cols']
    return ftype, tab_num, start_row, end_row, cols


def str_int_check(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    

x = '''
def cols2take(fname, sh, col_dict):
    """
    Args:
        - fname: input file name
        - sh: excel sheet in nested list format
        - col_dict: dict of the col indexes to subset and corresponding col names
    """
    new_sh = [] 
    if "ChildCareData" in fname:
        col_index = list(col_dict["ChildCareData"].keys())[:-1]
        col_def = list(col_dict["ChildCareData"].values())
        for i, row in enumerate(sh):
            ct = list(itemgetter(*col_index)(row))
            if str_int_check(ct[0]):
                new_sh.append(ct)
                new_sh[i].append("childcare")
    elif "KindergartenData" in fname:
        col_index = list(col_dict["KindergartenData"].keys())[:-1]
        col_def = list(col_dict["KindergartenData"].values())
        for i, row in enumerate(sh):
            ct = list(itemgetter(*col_index)(row))
            if str_int_check(ct[0]):
                new_sh.append(ct)
                new_sh[i].append("kindergarten")
    elif "7thGradeData" in fname:
        col_index = list(col_dict["7thGradeData"].keys())[:-1]
        col_def = list(col_dict["7thGradeData"].values())
        for i, row in enumerate(sh):
            ct = list(itemgetter(*col_index)(row))
            if str_int_check(ct[0]):
                new_sh.append(ct)
                new_sh[i].append("7th_grade")
    else:
        raise ValueError("not-supported file type")
    return new_sh, col_def
'''


def take_cols(sh, col_index, ftype):
    subset_sh = []
    missing_index = [i for i, num in enumerate(col_index) if num == -1]
    col_index = [num for i, num in enumerate(col_index) if num != -1]
    for i, row in enumerate(sh):
        line = list(itemgetter(*col_index)(row)) 
        for j in missing_index:
            line = line[:j] + [""] + line[j:]
        line = line + [ftype]
        #if str_int_check(line[0]):
        subset_sh.append(line)
    return subset_sh


def xlsx2csv(input_file_path, output_file_path, col_dict):
    wb = xlrd.open_workbook(input_file_path)
    shs = wb.sheet_names()
    fname = input_file_path.split("/")[-1]
    ftype, tab_num, start_row, end_row, col_index = check_col_dict(fname = fname, col_dict = col_dict)
    print("processing input file: ", fname, "\ntab: ", shs[tab_num])
    sh = wb.sheet_by_name(shs[tab_num])
    m = sh.ncols
    print(m, " columns and ", end_row, "rows")
    ## get all the value cells in defined range
    sh_list = get_cell_range(sh, 0, start_row, m-1, end_row)
    ## subset only the wanted columns
    subset_sh = take_cols(sh = sh_list, col_index = col_index, ftype = ftype)
    ## write to csv file
    with open(output_file_path, "w") as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for row in subset_sh:
            wr.writerow(row)
    return subset_sh


def merge_csv(input_files, output_file_path, cols):
    """
    Arg:
        - input_files : [input_file_path]
        - output_file_path : string path
        - cols : [column definition]
    """
    final_df = pd.DataFrame([])
    for i, input_file in enumerate(input_files):
        #print("processing file: ", input_file)
        df = pd.read_csv(input_file, skipinitialspace = True, sep = ",", names = cols)
        final_df = final_df.append(df)
    final_df.to_csv(output_file_path, sep=',')
    return final_df
        
            