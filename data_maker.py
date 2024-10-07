import pandas as pd


def extract_homicide_rates(input_file, output_file):
    # Load the dataset
    data = pd.read_excel(input_file)

    # Set the correct headers (assuming headers start from the second row, index 1)
    columns = data.iloc[1]
    df = data[2:]  # Exclude the header rows
    df.columns = columns  # Set the correct column headers

    # Filter rows where the 'Unit of measurement' is 'Rate per 100,000'
    filtered_df = df[df["Unit of measurement"] == "Rate per 100,000 population"]

    # Select only the relevant columns: 'Country', 'Region', 'Year', 'VALUE'
    filtered_df = filtered_df[["Country", "Region", "Year", "VALUE"]]

    # Save the filtered dataset to a new Excel file
    filtered_df.to_excel(output_file, index=False)


def find_max_homicide_rate(file_path):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Find the maximum value in the 'VALUE' column (assuming this column contains the homicide rates)
    max_value = data["VALUE"].max()

    # Find the row(s) with the maximum value
    max_row = data[data["VALUE"] == max_value]

    # Return the maximum value and the corresponding row(s)
    return max_value, max_row


def extract_homicide_rates_per_year(input_file):
    # Load the dataset
    homicide_data = pd.read_csv(input_file, skiprows=4)

    # Filter the columns to include data from 1990 to 2021
    homicide_years = [
        str(year) for year in range(1990, 2022)
    ]  # Years from 1990 to 2021 inclusive

    # Ensure only relevant columns (country and years 1990-2021) are used
    homicide_data_filtered = homicide_data[["Country Name"] + homicide_years]

    # Melt the dataset to have one row per country and year
    extracted_data = homicide_data_filtered.melt(
        id_vars=["Country Name"], var_name="Year", value_name="Homicide Rate"
    )

    # Remove rows where the Homicide Rate is NaN
    extracted_data = extracted_data.dropna(subset=["Homicide Rate"])

    # Return the cleaned data
    return extracted_data


def reshape_gpi_data(input_file):
    # Load the dataset
    gpi_data = pd.read_excel(input_file)

    # Reshape the data to have one row per country and year
    gpi_melted = gpi_data.melt(
        id_vars=["Country", "iso3c"], var_name="Year", value_name="GPI"
    )

    # Drop rows where GPI is missing
    gpi_melted = gpi_melted.dropna(subset=["GPI"])

    # Return the cleaned data
    return gpi_melted


# Example usage
if __name__ == "__main__":
    # Example usage
    input_file = "data\GPI_Data_clean.xlsx"  # Replace with the path to your Excel file
    gpi_cleaned_data = reshape_gpi_data(input_file)

    # Save the cleaned data to a new CSV file
    output_file = "reshaped_gpi_data.csv"
    gpi_cleaned_data.to_csv(output_file, index=False)

    print(f"Data has been reshaped and saved to {output_file}")
