import json
from datetime import datetime
DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"
def format_temperature(temp):
 
    return f"{temp}{DEGREE_SYBMOL}"

def convert_date(iso_string):
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')

def convert_f_to_c(temp_in_farenheit):
    
    temp_in_celcius = (temp_in_farenheit - 32)*5/9
    temp_in_celcius = round(temp_in_celcius, 1)
    return temp_in_celcius
def calculate_mean(total, num_items):

    mean = total/num_items

    mean = round(mean, 1)
    return mean


def process_weather(forecast_file):
 
    with open(forecast_file) as json_file:
        data = json.load(json_file)

    days = []
    minimum_temps = []
    maximum_temps = []
    chance_of_rain_days = []
    long_days = []
    long_nights = []
    chance_of_rain_nights = []
    max_mean = []
    min_mean = []
    low_day = []
    high_day = []
    num_items = 0
    num_items = num_items + 1

    for item in data["DailyForecasts"]:
        days.append(convert_date(item["Date"]))
        minimum_temps.append(convert_f_to_c(
            item["Temperature"]["Minimum"]["Value"]))
        maximum_temps.append(convert_f_to_c(
            item["Temperature"]["Maximum"]["Value"]))
        long_days.append(item["Day"]["LongPhrase"])
        long_nights.append(item["Night"]["LongPhrase"])
        chance_of_rain_days.append(item["Day"]["RainProbability"])
        chance_of_rain_nights.append(item["Night"]["RainProbability"])
        
    min_mean = calculate_mean(sum(minimum_temps), len(minimum_temps))
    max_mean = calculate_mean(sum(maximum_temps), len(maximum_temps))
 
    index_min = minimum_temps.index(min(minimum_temps))
    low_day = days[index_min]
    index_max = maximum_temps.index(max(maximum_temps))
    high_day = days[index_max]
  
    output = []
    output.append("{} Day Overview".format(len(minimum_temps)))
    output.append( f"    The lowest temperature will be {min(minimum_temps)}{DEGREE_SYBMOL}, and will occur on {low_day}.")
    output.append(f"    The highest temperature will be {max(maximum_temps)}{DEGREE_SYBMOL}, and will occur on {high_day}.")
    output.append(f"    The average low this week is {min_mean}{DEGREE_SYBMOL}.")
    output.append( f"    The average high this week is {max_mean}{DEGREE_SYBMOL}.")
    output.append("")
    
    for i in range(len(days)):
        output.append("-------- " + days[i] + " --------")
        output.append(f"Minimum Temperature: {minimum_temps[i]}{DEGREE_SYBMOL}")
        output.append(f"Maximum Temperature: {maximum_temps[i]}{DEGREE_SYBMOL}")
        output.append(f"Daytime: {long_days[i]}\n    Chance of rain:  {chance_of_rain_days[i]}%")
        output.append(f"Nighttime: {long_nights[i]}\n    Chance of rain:  {chance_of_rain_nights[i]}%")
        output.append("")

    output.append("")
    final_output = "\n".join(output)
    return(final_output)

if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))
