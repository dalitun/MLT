"""
Dealing with missing data:
1. Fill forward (to avoid peeking into the future)
2. Fill backward
"""

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method='ffill', inplace=True)
    df_data.fillna(method='bfill', inplace=True)
    return df_data