# This sample uses pandas to manipulate data for a given age group 
# Complete these steps before testing this function
# 1. Select library management and add pandas library

import pandas as pd 
@app.function("manipulate_data")
def manipulate_data(data: dict)-> str:
    # Convert the data dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Perform basic data manipulation
    # Example: Add a new column 'AgeGroup' based on the 'Age' column
    df['AgeGroup'] = df['Age'].apply(lambda x: 'Adult' if x >= 18 else 'Minor')

    # Example: Filter rows where 'Age' is greater than 30
    df_filtered = df[df['Age'] > 30]

    # Example: Group by 'AgeGroup' and calculate the mean age
    df_grouped = df.groupby('AgeGroup')['Age'].mean().reset_index()
    resultsJSON = json.dumps({"values": df_grouped})          
    return resultsJSON