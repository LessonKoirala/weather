import requests
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns

# API key (consider using environment variables for security)
apikey = os.getenv('Your own Apikey code from the https://openweathermap.org/')

# Read city names from the CSV file
city_file = 'city_names .csv'  # Ensure there's no space in the filename
cities = []

with open(city_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cities.append(row['City'])

# Initialize an empty list to store structured weather data
weather_data_list = []

# Loop through each city and fetch weather data
for city in cities:
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={apikey}'
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses
        weather_data_json = response.json()

        if 'main' in weather_data_json and 'weather' in weather_data_json and 'wind' in weather_data_json and 'clouds' in weather_data_json:
            city_weather = {
                'City': city,
                'Temperature': weather_data_json['main']['temp'],
                'Humidity': weather_data_json['main']['humidity'],
                'Pressure': weather_data_json['main']['pressure'],
                'Weather': weather_data_json['weather'][0]['description'],
                'Wind Speed': weather_data_json['wind']['speed'],
                'Cloudiness': weather_data_json['clouds']['all']
            }

            weather_data_list.append(city_weather)
            print(f"Weather data for {city} retrieved successfully.")
        else:
            print(f"Invalid response structure for city: {city}")

    except requests.RequestException as e:
        print(f"Request error for {city}: {e}")
    except KeyError as e:
        print(f"Missing key in response data for {city}: {e}")

# Convert the list of structured data to a DataFrame
df = pd.DataFrame(weather_data_list)

# Ensure the new file doesn't overwrite the old one
output_file = 'weather_data.csv'
if not os.path.exists(output_file):
    df.to_csv(output_file, index=False)
    print(f"All weather data saved to {output_file}.")
else:
    print(
        f"File {output_file} already exists. Please specify a different file name."
    )

# Read the CSV file into a DataFrame
df = pd.read_csv(output_file)

# Calculate statistics
statistics = {
    'Temperature': {
        'Mean': df['Temperature'].mean(),
        'Median': df['Temperature'].median(),
        'Standard Deviation': df['Temperature'].std()
    },
    'Humidity': {
        'Mean': df['Humidity'].mean(),
        'Median': df['Humidity'].median(),
        'Standard Deviation': df['Humidity'].std()
    },
    'Pressure': {
        'Mean': df['Pressure'].mean(),
        'Median': df['Pressure'].median(),
        'Standard Deviation': df['Pressure'].std()
    },
    'Wind Speed': {
        'Mean': df['Wind Speed'].mean(),
        'Median': df['Wind Speed'].median(),
        'Standard Deviation': df['Wind Speed'].std()
    },
    'Cloudiness': {
        'Mean': df['Cloudiness'].mean(),
        'Median': df['Cloudiness'].median(),
        'Standard Deviation': df['Cloudiness'].std()
    }
}

# Print statistical data
for key, value in statistics.items():
    print(f"\nStatistics for {key}:")
    for stat, val in value.items():
        print(f"  {stat}: {val:.2f}")

# Create a text file with the statistical analysis report
report_file = 'weather_statistics_report.txt'

with open(report_file, 'w') as file:
    file.write("Weather Data Analysis Report\n")
    file.write("============================\n\n")

    # Temperature
    file.write("1. Temperature\n")
    file.write("---------------\n")
    file.write(
        f"- Mean: The average temperature across all cities is {statistics['Temperature']['Mean']:.2f}°C.\n"
    )
    file.write(
        f"- Median: The median temperature is {statistics['Temperature']['Median']:.2f}°C.\n"
    )
    file.write(
        f"- Standard Deviation: The standard deviation is {statistics['Temperature']['Standard Deviation']:.2f}°C.\n\n"
    )

    # Humidity
    file.write("2. Humidity\n")
    file.write("-----------\n")
    file.write(
        f"- Mean: The average humidity level across all cities is {statistics['Humidity']['Mean']:.2f}%.\n"
    )
    file.write(
        f"- Median: The median humidity is {statistics['Humidity']['Median']:.2f}%.\n"
    )
    file.write(
        f"- Standard Deviation: The standard deviation of humidity is {statistics['Humidity']['Standard Deviation']:.2f}%.\n\n"
    )

    # Pressure
    file.write("3. Pressure\n")
    file.write("-----------\n")
    file.write(
        f"- Mean: The average atmospheric pressure recorded is {statistics['Pressure']['Mean']:.2f} hPa.\n"
    )
    file.write(
        f"- Median: The median pressure is {statistics['Pressure']['Median']:.2f} hPa.\n"
    )
    file.write(
        f"- Standard Deviation: The standard deviation for pressure is {statistics['Pressure']['Standard Deviation']:.2f} hPa.\n\n"
    )

    # Wind Speed
    file.write("4. Wind Speed\n")
    file.write("--------------\n")
    file.write(
        f"- Mean: The average wind speed observed is {statistics['Wind Speed']['Mean']:.2f} m/s.\n"
    )
    file.write(
        f"- Median: The median wind speed is {statistics['Wind Speed']['Median']:.2f} m/s.\n"
    )
    file.write(
        f"- Standard Deviation: The standard deviation of wind speed is {statistics['Wind Speed']['Standard Deviation']:.2f} m/s.\n\n"
    )

    # Cloudiness
    file.write("5. Cloudiness\n")
    file.write("--------------\n")
    file.write(
        f"- Mean: The average cloudiness across the cities is {statistics['Cloudiness']['Mean']:.2f}%.\n"
    )
    file.write(
        f"- Median: The median cloudiness is {statistics['Cloudiness']['Median']:.2f}%.\n"
    )
    file.write(
        f"- Standard Deviation: The standard deviation of cloudiness is {statistics['Cloudiness']['Standard Deviation']:.2f}%.\n\n"
    )

    file.write("Conclusion\n")
    file.write("----------\n")
    file.write(
        "The statistical analysis provides valuable insights into the weather patterns observed across different cities. By understanding the mean, median, and standard deviation of each weather attribute, we can better grasp the typical conditions as well as the variability present in the dataset.\n"
    )
    file.write(
        "For visual representation, histograms and pairplots of the data are available, illustrating the distribution and relationships among the weather attributes.\n\n"
    )

    file.write("End of Report\n")

print(f"Statistical report saved to {report_file}.")

# Create graphical representations

# Set up the plotting style
sns.set(style="whitegrid")

# Plot Temperature
plt.figure(figsize=(12, 6))
sns.histplot(df['Temperature'], kde=True, color='blue')
plt.title('Temperature Distribution')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.savefig('temperature_distribution.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping

# Plot Humidity
plt.figure(figsize=(12, 6))
sns.histplot(df['Humidity'], kde=True, color='green')
plt.title('Humidity Distribution')
plt.xlabel('Humidity (%)')
plt.ylabel('Frequency')
plt.savefig('humidity_distribution.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping

# Plot Pressure
plt.figure(figsize=(12, 6))
sns.histplot(df['Pressure'], kde=True, color='red')
plt.title('Pressure Distribution')
plt.xlabel('Pressure (hPa)')
plt.ylabel('Frequency')
plt.savefig('pressure_distribution.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping

# Plot Wind Speed
plt.figure(figsize=(12, 6))
sns.histplot(df['Wind Speed'], kde=True, color='purple')
plt.title('Wind Speed Distribution')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Frequency')
plt.savefig('wind_speed_distribution.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping

# Plot Cloudiness
plt.figure(figsize=(12, 6))
sns.histplot(df['Cloudiness'], kde=True, color='orange')
plt.title('Cloudiness Distribution')
plt.xlabel('Cloudiness (%)')
plt.ylabel('Frequency')
plt.savefig('cloudiness_distribution.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping

# Plot pairplot for all numerical features
plt.figure(figsize=(12, 10))
sns.pairplot(
    df[['Temperature', 'Humidity', 'Pressure', 'Wind Speed', 'Cloudiness']])
plt.suptitle('Pairplot of Weather Data', y=1.02)
plt.savefig('pairplot_weather_data.png')  # Save plot to file
plt.close()  # Close the plot to avoid overlapping
