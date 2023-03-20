import logging
import functools
import pandas as pd

logging.basicConfig(level=logging.INFO)


def log_execution(*input_names):
    """The function log_execution(*input_names) is a decorator that logs changes made to specified input arguments and output values of a function.
    When using the decorator, it is important to note that the order of the input arguments in the decorator should match the order of the input arguments 
    in the function being logged, as well as the order of the output values.
    
    For example:
    ______________________________
    @log_execution("df", "df_2")
    def drop_na(df, df_2):
        # do something
        return df
    ______________________________
            
    In the example above the arguments of the decorator ´("df", "df_2")´ are in the same order as the arguments of the function ´(df, df_2)´. 
    Note that the function returns only 1 element which is ´df´. So, ´df´ will be the only dataframe for which the function will log changes.
    
    If the decorator is applied with @log_execution("df", "df_2"), then the function being logged should have input arguments in the order of (df, df_2) 
    and should return output values in the order of (df, df_2).
    
    For example:
    ______________________________
    @log_execution("df", "df_2")
    def drop_na(df, df_2):
        # do something
        return df, df_2
    ______________________________
        
    Note that in the above example that ´df´, ´df_2´ are both an argument and a output of the function. Thus, there will be a record log of those changes.
    
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            
            file_naming = {'df_1': 'First file', 
                           'df_2': 'Second file',
                           'df_3' : 'Third file'}
            
            logging.info(f"Executing {func.__name__}")

            df_sizes_before = {}
            for i, arg in enumerate(args):
                if isinstance(arg, pd.DataFrame):
                    if len(input_names) == 1:
                        i = 0
                    df_sizes_before[input_names[i]] = arg.shape[0]
            try:
                result = func(*args, **kwargs)
                
            except Exception as e:
                logging.error(f"Error executing {func.__name__}: {e}")
                raise

            df_sizes_after = {}
            if isinstance(result, pd.DataFrame):
                df_sizes_after[input_names[0]] = result.shape[0] # the order input_names in the decorator should be aligned as how the function return the elements 
                
            elif isinstance(result, tuple) or isinstance(result, list):
                for i, arg in enumerate(result):
                    if isinstance(arg, pd.DataFrame):
                        df_sizes_after[input_names[i]] = arg.shape[0]
            
            logging.info(f"Finished executing {func.__name__}")

            # Create a dataframe with the logging information
            df_logs = pd.DataFrame(columns=['function_name', 'file_name', 'initial_size', 'current_size', 'obs_removed', 'pct_removed'])
            for input_name in input_names:
                try:
                    initial_size = df_sizes_before[input_name]
                    current_size = df_sizes_after[input_name]
                except KeyError:
                    continue
                
                new_row = pd.Series({
                    'function_name': func.__name__,
                    'file_name': file_naming.get(input_name, input_name),
                    'initial_size': initial_size,
                    'current_size': current_size,
                    'obs_removed': abs(current_size - initial_size),
                })
                df_logs = pd.concat([df_logs, new_row.to_frame().T], ignore_index=True)

            df_logs['pct_removed'] = df_logs['obs_removed'] / df_logs['initial_size'] * 100
            df_logs['pct_removed'] = df_logs['pct_removed'].apply(lambda x: f'{x:.2f}%')
            try:
                existing_data = pd.read_excel('log.xlsx')
            except FileNotFoundError:
                existing_data = pd.DataFrame(columns=['function_name', 'file_name', 'initial_size', 'current_size', 'obs_removed', 'pct_removed'])

            # Check for duplicates and only append non-duplicated rows to file
            new_data = pd.concat([existing_data, df_logs], ignore_index=True)
            new_data = new_data[new_data['file_name'].isin(file_naming.values())]  # keep only dataframe logs
            new_data = new_data.drop_duplicates(subset=['function_name', 'file_name'])
            new_data = new_data.sort_values(by=['file_name', 'initial_size'], ascending=[True, False])
            new_data.to_excel('log.xlsx', index=False)
            logging.info(f"__________"*10)

            return result
        return wrapper
    return decorator