# Log Execution Decorator

This is a decorator function that logs changes made to specified input arguments and output values of a function. When using the decorator, it is important to note that the order of the input arguments in the decorator should match the order of the input arguments in the function being logged, as well as the order of the output values.

### Example Usage

```
@log_execution("df", "df_2")
def drop_na(df, df_2):
    # do something
    return df
```

In the above example, the arguments of the decorator ("df", "df_2") are in the same order as the arguments of the function (df, df_2). Note that the function returns only 1 element which is df. So, df will be the only dataframe for which the function will log changes.

If the decorator is applied with @log_execution("df", "df_2"), then the function being logged should have input arguments in the order of (df, df_2) and should return output values in the order of (df, df_2).

```
@log_execution("df", "df_2")
def drop_na(df, df_2):
    # do something
    return df, df_2
```

Note that in the above example that df, df_2 are both an argument and an output of the function. Thus, there will be a record log of those changes.

### Parameters
`log_execution(*input_names)`

* `*input_names`: A list of names of the input dataframes to be logged.

### Returns

The decorator returns the wrapper function, which logs changes made to specified input arguments and output values of a function. The wrapper function also returns the output of the decorated function.

### Logging Information
The decorator logs the following information:

* The name of the function being logged
* The name of the dataframe being logged
* The initial size of the dataframe before the function was executed
* The current size of the dataframe after the function was executed
* The number of observations removed
* The percentage of observations removed

The decorator logs this information in a dataframe and saves it to an Excel file named `log.xlsx`. The logging information is sorted by the name of the dataframe and the initial size of the dataframe in descending order.