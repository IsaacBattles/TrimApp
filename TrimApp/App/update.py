import pandas as pd

# Function to check for duplicates and update the row
def update_tote(data, file_path, tote_number, updates):
    try:
        # Locate the row for the tote number
        tote_index = data[data['Tote #'] == tote_number].index[0]
        
        # Check if any data exists in the row (excluding the date column)
        is_duplicate = not data.iloc[tote_index, 3:].isnull().all()  # Assumes "Date" is column 1
        
        if is_duplicate:
            return "duplicate"
        
        # Update the row with new values
        for key, value in updates.items():
            data.at[tote_index, key] = value

        # Save the updated data
        data.to_csv(file_path, index=False)
        return "success"

    except IndexError:
        return "not_found"