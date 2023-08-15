import os
import yaml
import pandas as pd
import argparse


  
# general parameters for the script
# --dir XXXXXXXX - where the parent folder of the data is kept
# --subproject YYYYYY - the subset of data ie CPET
# --config - json file to define table headers of interest and cells required for output

# configs
# directory = "./"
# subproject = "CPET"
validate_sheets = ["Data", "Results"]
# os.chdir('D:/Cloud/Onedrive/Work/UCL/Projects/LHA/Code')


## functions
def parse_args():
  """Parses the arguments passed to the script."""
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--dir',
      help='The data directory.',
      type=str,
      required=True)
  parser.add_argument(
      '--subproject',
      help='The subproiject name, i.e. "CPET"',
      type=str,
      required=True)
  parser.add_argument(
      '--config',
      help='The configuration file .',
      type=str,
      required=True)
  parser.add_argument(
      '--output',
      help='The output file inc path.',
      type=str,
      required=True)
  return parser.parse_args()


def find_xlsx_files(directory):
  """Finds all .xlsx files under the specified directory recursively.

  Args:
    directory: The directory to search.

  Returns:
    A list of the full paths of all .xlsx files found.
  """
  xlsx_files = []
  for root, directories, files in os.walk(directory):
    for file in files:
      if file.endswith(".xlsx"):
        xlsx_files.append(os.path.join(root, file))
  return xlsx_files

def subset_on_project(list, subproject):
  """Subsets a list to return only those strings that contain the string "CPET".

  Args:
    list: The list to subset.

  Returns:
    A new list containing only the strings from the original list that contain
    the string 'subproject'.
  """
  new_list = []
  for string in list:
    if subproject in string:
      new_list.append(string)
  return new_list

def import_data(xlsx_file, validate_sheets):
  """Imports an Excel file into a Pandas DataFrame.

  Args:
    excel_file: The path to the Excel file to import.

  Returns:
    A Pandas DataFrame containing the data from the Excel file.
  """
  worksheet_names = pd.ExcelFile(xlsx_file).sheet_names
  if all(sheet in worksheet_names for sheet in validate_sheets):
    dataframe = pd.read_excel(xlsx_file, sheet_name=validate_sheets[1], header=None)
  else:
    print(f"The Excel file {xlsx_file} does not contain all of the sheets specified in the validate_sheets list.")
  return dataframe #dataframe




def find_rows_with_strings_at_location_0(dataframe):
  """Finds all the indexes in the DataFrame where the value at location 0 is a string and the rest of the row is NaN.

  Args:
    dataframe: The DataFrame to search.

  Returns:
    A list of the indexes where the value at location 0 is a string and the rest of the row is NaN.
  """

  rows = []
  for i in range(len(dataframe)):
    row = dataframe.iloc[i]
    if isinstance(row[0], str) and all(pd.isnull(value) for value in row[1:]):
      rows.append(i)

  return rows


def split_dataframe_by_rows(dataframe, rows):
  """Splits a Pandas DataFrame into smaller DataFrames based upon the rows variable.

  Args:
    dataframe: The DataFrame to split.
    rows: A list of the indexes to split the DataFrame at.

  Returns:
    A list of DataFrames, where each DataFrame contains the data from the rows variable to the next entry in rows-1.
  """

  split_dataframes = []
  current_dataframe = pd.DataFrame()
  for i in range(len(rows)-1):
    #print("The row number is", i)
    if i == 0:
      current_dataframe = dataframe.iloc[rows[i]:(rows[i + 1]-1)]
    else:
      current_dataframe = pd.concat([current_dataframe, dataframe.iloc[rows[i]:(rows[i + 1]-1)]])
    if i < len(rows) - 1:
      split_dataframes.extend([current_dataframe])
      current_dataframe = pd.DataFrame()
    else:
      current_dataframe = dataframe.iloc[rows[i]:]
      split_dataframes.extend([current_dataframe])
  # Drop the rows with all NaN entries from the dataframe.
  for df in split_dataframes:
    df = df.dropna(axis=0, how='all') 
  return split_dataframes

def add_name_column(list_of_df):
  """Adds a column called NAME to a pandas dataframe, containing the string present at location 0 of the first row.

  Args:
    df: The pandas dataframe to be modified.

  Returns:
    The modified pandas dataframe.
  """
  # Get the string present at location 0 of the first row.
  final_list = []
  for dfentry in list_of_df:
      name = dfentry.iloc[0, 0]
      # Remove the first row.
      dfentry = dfentry.iloc[1:,:]
      # Add a column called NAME to the dataframe, containing the string we just got.
      dfentry=dfentry.assign(Name=name)
      final_list.extend([dfentry])
  # Concatenate the dataframes along the axis=0.
  final_list = pd.concat(final_list, axis=0)
  return final_list


def find_values(df, config, config_to_check):
  """Takes a value for the configuration of results, and find all the entries, returning in a list.

  Args:
    df: the dataframe to process results from.
    config: The dictionary of the settings from the config yaml file.
    config_to_check: The main value set to keep.
    
  Returns:
    a dictionary of the specific results.
  """
  results_dict={}
  for entry in config[config_to_check]:
      df_subset = df.loc[df["Name"]==entry["table_name"]]
      df_subset.columns=df_subset.iloc[0]
      df_subset=df_subset.iloc[1:,:]
      # set row names
      df_subset = df_subset.set_index('MEASURES')
      res=[df_subset.loc[entry["row_number"], entry["column_name"]]]
      res_name=entry["table_name"]+"_"+entry["column_name"]+"_"+entry["row_number"]
      results_dict.update({res_name:res})
  return(results_dict)


def main():
  print("Loading configuration...")
  args = parse_args()
  print("Arguments passed to script:")
  print(args)
  
  print("Current working directory:", os.getcwd())
  directory = args.dir
  subproject = args.subproject
  output= args.output
  validate_sheets = ["Data", "Results"]
  os.chdir(directory)

  final_results=pd.DataFrame()
  # Import the YAML file.
  with open("./results_to_summarize.yaml", "r") as f:
    config = yaml.safe_load(f)
  # grab all XLSX files in parent directory, recursively
  xlsx_files = find_xlsx_files(directory)
  # subset on the project of interest
  new_list = subset_on_project(xlsx_files, subproject)
  print(subproject, " containing files only",new_list)
  
  for i in range(len(new_list)):
      delimiters="\\"
      file=new_list[i]
      patient_id=file.split(delimiters)[0]
      patient_id=patient_id[2:]
      dataframe = import_data(file, validate_sheets)
      indexes = find_rows_with_strings_at_location_0(dataframe)
      split_dataframes = split_dataframe_by_rows(dataframe, indexes)
      # Add a NAME column to the dataframe and rejoin into a single df
      df = add_name_column(split_dataframes)
      # Access the entries of interest.
      res=find_values(df, config, "results_to_summarise")
      res=pd.DataFrame(res)
      res=res.assign(patient_id=patient_id)
      res.set_index("patient_id", inplace=True)
      if i == 0:
          final_results=res
      else:
          final_results = pd.concat([final_results, res])
  print("Writing results to:", output)
  final_results.to_csv(output, quotechar="\"")
  

if __name__ == "__main__":
  main()


 
 
