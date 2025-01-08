
"""
Purpose:
    harvests fights departing and arriving from airports
"""

from bs4 import BeautifulSoup
import pandas as pd
from os.path import exists
import requests
import re
import random
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import date, datetime, timedelta, time
from time import sleep



#from selenium_stealth import stealth


def price_link_scrape(origin, destination, startdate):

    df = pd.DataFrame()

    url = "https://www.kayak.com/flights/" + origin + "-" + destination + "/" + startdate + "?sort=depart_a&fs=stops=0"#airlines=AC;
    print("\n" + url)

    chrome_options = webdriver.ChromeOptions()
    # enable headless mode
    chrome_options.add_argument("--headless")
    # disable sandbox to get around dockers security policies
    chrome_options.add_argument("--no-sandbox")
    ### SET ARGUMENTS FOR THE CHROME WEB DRIVER TO LOOK MORE LIKE A NORMAL USERS BROWSER
    # disabling infobars
    chrome_options.add_argument("--disable-infobars"); 
    # disable dev shm usage
    chrome_options.add_argument("--disable-dev-shm-usage")
    # set the language to base english and us english
    chrome_options.add_argument("--lang=['en-US', 'en']")
    # set the vendor
    chrome_options.add_argument("--vendor='GoogleInc.'")
    # set the current platform
    chrome_options.add_argument("--platform='Win32'")
    # set the webgl vendor
    chrome_options.add_argument("--webgl_vendor='Intel Inc.'")
    # set teh renderer
    chrome_options.add_argument("--rederer='Intel Iris OpenGL Engine'")
    # enable fix hairline
    chrome_options.add_argument("--fix_hairline=True")
    #start the browser maximized
    chrome_options.add_argument("--start-maximized")
    #disable extensions
    chrome_options.add_argument("--disable-extensions")
    # set no first run
    chrome_options.add_argument('--no-first-run')
    # set no service autorun
    chrome_options.add_argument('--no-service-autorun')
    # set no default browser check
    chrome_options.add_argument('--no-default-browser-check')
    # set password store to basic
    chrome_options.add_argument('--password-store=basic')
    # set no proxy server
    chrome_options.add_argument('--no-proxy-server')
    #chrome_options.add_argument('--remote-debugging-port=20')

    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    agents = ["Firefox/"+str(random.randint(60,70))+".0.3","Chrome/"+str(random.randint(70,80))+".0.3683.68","Edge/"+str(random.randint(10,20))+".16299"]
    print("User agent: " + agents[(0%len(agents))])
    chrome_options.add_argument('--user-agent=' + agents[(0%len(agents))] + '"')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    
    driver.implicitly_wait(random.randint(15,20))
    driver.get(url)

    #Check if Kayak thinks that we're a bot
    sleep(5) 
    soup=BeautifulSoup(driver.page_source, 'lxml')

    if soup.find_all('p')[0].getText() == "Please confirm that you are a real KAYAK user.":
        print("Kayak thinks I'm a bot, which I am ... so let's wait a bit and try again")
        driver.close()
        sleep(20)
        return "failure"
    
    #wait 20sec for the page to load
    sleep(10)

    # use soup to get the div data of the flights (arrival, departure, price, ect)
    soup=BeautifulSoup(driver.page_source, 'lxml')
    data = soup.find_all('div', attrs={'class': 'inner-grid keel-grid'})
    
        
    # convert div data to txt and append to list
    data_seperated = []
    for div in data:
        data_seperated.append(str(div.getText().replace("\n",'')))
    departure_time = []
    
    
    arrival_time = []
    airlines = []
    prices = []
    for i in range(len(data_seperated)):
        # original data
        while "Undisclosed Carrier" in data_seperated[i]:
            data_seperated.pop(i)
            if i not in range(len(data_seperated)):
                break
        if i not in range(len(data_seperated)):
            break
        print("\ndata seperated: ",data_seperated[i])

        booking_info = data_seperated[i].split('$')[0]
        booking_info = booking_info.replace("No change fees","")
        booking_info = booking_info.replace("Bus ticket","")
        booking_info = booking_info.replace("Train ticket","")
        # get departure time
        time_departure = booking_info.split('–')[0]
        time_departure = time_departure.replace(' ','')
        in_time = datetime.strptime(time_departure, "%I:%M%p")
        out_time = datetime.strftime(in_time, "%H:%M")
        departure_time.append(str(date.today())+" "+out_time)
        # get arrival time
        time_arrival = booking_info.split(' ')[1]
        time_arrival_remaining = booking_info.split(' ')[2]
        timething = time_arrival[3:]+time_arrival_remaining[:2]
        in_time = datetime.strptime(timething, "%I:%M%p")
        out_time = datetime.strftime(in_time, "%H:%M")
        arrival_time.append(str(date.today())+" "+out_time)
        # get flight price
        price = data_seperated[i].split('$')[1]
        price = price.split(' ')[0]
        prices.append('$'+price)
        # get airline name
        airline = booking_info.split('nonstop')[0]
        airline_remaining = airline.split(":", 2)[2]
        airline_remaining = airline_remaining[5:]
        if "+1" in airline_remaining:
            airline_remaining = airline_remaining.replace("+1","")
        airlines.append(airline_remaining)

    # get kayak.com url links to tickets
    urls = soup.select(".above-button")
    urls_clean = urls[::2]
    urls_clean_no_duplicates = []
    final_urls = []
    
    urls_clean_no_duplicates = []
    for i in range(len(urls_clean)):
        for link in urls_clean[i].findAll('a'):
            urls_clean_no_duplicates.append("https://www.kayak.com"+link.get('href'))
    # open the links and get the true ticket urls from the airline websites
    for i in range(len(urls_clean_no_duplicates)):
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            while "javascript:void(0)" in urls_clean_no_duplicates[i]:
                urls_clean_no_duplicates.pop(i)
                if i not in range(len(urls_clean_no_duplicates)):
                    break
            if i not in range(len(urls_clean_no_duplicates)):
                break
        except:
            break
        driver.get(urls_clean_no_duplicates[i])
        driver.implicitly_wait(10)
        sleep(3)
        # sleep(random.randint(4,10))
        final_urls.append(driver.current_url)

    # put all data into dataframe and return it
    df['Departure'] = departure_time
    df['Arrival'] = arrival_time
    df['Carrier'] = airlines
    df['Cost'] = prices
    df['Link'] = final_urls
    print(df)
    # df.to_csv(f"./__data/{origin}_flight_prices_urls.csv", index=False)
    return df

# format times
def clean_data(df):
    """
    Purpose:
        cleans the csv files so it's easier for the algo to read it
    Params:
        dataframe: dataframe of flights
    Returns:
        lists of cleaned data
    """
    cleanedflights_flightnumber = []
    cleanedflights_time = []
    flights = []
    #clean flight number
    for index,item in df['Flight'].items():
        item = str(item).replace(" ", "")
        if len(item) > 1:
            flights.append(str(item)[:6])
        else:
            df.drop(index,inplace=True)
    for i in range(len(flights)):
        if flights[i] == '':
            continue
        elif str(flights[i][len(flights[i])-1:]).isalpha():
            flights[i] = str(flights[i])[:-1]
            cleanedflights_flightnumber.append(flights[i])
        else:
            cleanedflights_flightnumber.append(flights[i])
    
    departure_or_arrival = ""
    if ('Departure' in df):
        departure_or_arrival = 'Departure'
    else:
        departure_or_arrival = 'Arrival'
    destination_or_origin = ""
    if ('Destination' in df):
        destination_or_origin = 'Destination'
    else:
        destination_or_origin = 'Origin'
        
    #clean time
    time_list = list(df[departure_or_arrival])
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i])
        if (len(time_list[i])>5):
            time_list[i] = time_list[i][-5:]

            cleanedflights_time.append(str(date.today())+" "+time_list[i])
        else:
            cleanedflights_time.append(str(date.today())+" "+time_list[i])
    df_cleaned = pd.DataFrame (cleanedflights_flightnumber, columns = ['Flight'])
    df_cleaned[departure_or_arrival] = cleanedflights_time
    df[departure_or_arrival] = df_cleaned[departure_or_arrival].values
    df['Flight'] = df_cleaned['Flight'].values
    # seperating airport code and city name
    new = df[destination_or_origin].str.split("(", n = 1, expand = True)
    df["City Name"]= new[0]
    df["Airport Code"] = new[1]
    df["Airport Code"] = df["Airport Code"].str.replace(r')', '')
    df.drop(columns =[destination_or_origin], axis=1,inplace = True)
    return (df)



def harvest_data_arrivals(arrival_location):
    """
    Purpose:
        scrapes flights arriving to the given airport
    Params:
        arrival_location: airport we are scraping
    Returns:
        dataframe with arriving flights to airport

    """
    url = "https://www.airports-worldwide.info/airport/"+arrival_location+"/arrivals"
    print(url)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    list_of_dataframes = []
    interval = soup.find_all("nav", {"id": "intervals"})
    if (len(interval)<=0):
        url = url.encode('ascii', errors='ignore')
        url = url.decode('ascii', errors='ignore')
        dataframes = pd.read_html(url.replace(" ","%20"))
        for i in range(len(dataframes)):
            list_of_dataframes.append(dataframes[i])
    else:
        data = re.findall(r'(https?://[^\s]+)', str(interval[0]))
        for i in range(len(data)):
            urls.append(data[i].split(">", 1)[0])

        for i in range(len(urls)):
            
            urls[i] = urls[i].encode('ascii', errors='ignore')
            urls[i] = urls[i].decode('ascii', errors='ignore')
            dataframes = pd.read_html(urls[i].replace(" ","%20"))
            for i in range(len(dataframes)):
                list_of_dataframes.append(dataframes[i])
    
    # combines dataframes
    df = pd.concat(list_of_dataframes)
    
    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]
    
    #remove unammed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])

    # remove flight loop
    discard = [arrival_location]
    df = df[df["Origin"].str.contains('|'.join(discard))==False]
    
    data = clean_data(df)
    
    return data


def harvest_data_departures(departure_location,initial_search):
    """
    Purpose:
        scrapes flights departing from given airport
    Params:
        departure_location: airport we are scraping
    Returns:
        dataframe with departing flights from airport
    
    """

    url = "https://www.airports-worldwide.info/airport/"+departure_location+"/departures"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    list_of_dataframes = []
    interval = soup.find_all("nav", {"id": "intervals"})
    if (len(interval)<=0):
        url = url.encode('ascii', errors='ignore')
        url = url.decode('ascii', errors='ignore')
        dataframes = pd.read_html(url.replace(" ","%20"))
        for i in range(len(dataframes)):
            list_of_dataframes.append(dataframes[i])
    else:
        data = re.findall(r'(https?://[^\s]+)', str(interval[0]))
        for i in range(len(data)):
            urls.append(data[i].split(">", 1)[0])

        for i in range(len(urls)):
            
            urls[i] = urls[i].encode('ascii', errors='ignore')
            urls[i] = urls[i].decode('ascii', errors='ignore')
            dataframes = pd.read_html(urls[i].replace(" ","%20"))
            for i in range(len(dataframes)):
                list_of_dataframes.append(dataframes[i])
    
    # combines dataframes
    df = pd.concat(list_of_dataframes)

    # removes all flights that do not contain "scheduled" in "Status" column
    df = df[df["Status"].str.contains('scheduled', regex=False)]

    #remove flights with no flight number
    df = df.dropna(axis=0, subset=['Flight'])
    
    #remove unammed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    #remove flight loop
    discard = [departure_location]
    df = df[df["Destination"].str.contains('|'.join(discard))==False]
    data = clean_data(df)

    return data


if __name__ == "__main__":
    browser = 0
    flights=[["YVR", "LAX"],["LAX","YVR"],["LAX","YYC"],["YYC","YVR"]]
    for f in flights:
        sleep(random.randint(4,9))
        # scrape departures from airport
        # airport flights depart from
        departure_airport = "YVR"
        initial_search = True
        # file out
        departures_file_out = f"./__data/{departure_airport}_airport_departures.csv"

        # scrape airport departures
        airport_dept_df = harvest_data_departures(departure_airport, initial_search)
        initial_search = False
        # save airport departures to csv
        airport_dept_df.to_csv(departures_file_out, index=False)


        separator = '('
        departure_airports = airport_dept_df['Airport Code'].unique().tolist()
        departure_connections = f"./__data/{departure_airport}_connections.csv"
        for i in range(len(departure_airport)):
            departure_airports[i] = departure_airports[i].split(separator, 1)[0]
            departure_airports[i] = departure_airports[i].rstrip()
            departure_airport = departure_airports[i]

            try:
                ap_dep_df = harvest_data_departures(departure)
        
                if not exists(file_output_origin_departures):
                    ap_dep_df.to_csv(file_output_origin_departures, index=False)
                else:
                    ap_dep_df.to_csv(file_output_origin_departures, mode='a', header=False, index=False)
            except Exception as e:
                print(f"skipping url for {departure} do to an exception:",e)
            
        # scrape arrivals to airport
        # airport flights arrive to
        arrival_airport = "YYC"
        # file out
        arrival_file_out = f"./__data/{arrival_airport}_airport_arrivals.csv"
        arrival_connections = f"./__data/{arrival_airport}_connections.csv"
        # scrape airport arrivals
        airport_arvl_df = harvest_data_arrivals(arrival_airport)

            # save airport arrivals to csv
        airport_arvl_df.to_csv(arrival_file_out, index=False)

        #scrape for prices from the departing airport
        prices_file_out = f"./__data/{departure_airport}_flight_prices_urls.csv"
        prices_df = price_link_scrape(departure_airport, arrival_airport, str(date.today()))
        prices_df.to_csv(prices_file_out, index=False)
        i=0
        while i<5:
            print("waiting")
            time.sleep(5)
            i+=1
        separator = '('
        departures = user_airport_timetable_data['Origin'].unique().tolist()

        for i in range(len(arrival_airport)):
            departures[i] = departures[i].split(separator, 1)[0]
            departures[i] = departures[i].rstrip()
            departure = departures[i]

            try:
                ap_dep_df = harvest_data_departures(departure, initial_search)

                if not exists(arrival_connections):
                    ap_dep_df.to_csv(arrival_connections, index=False)
                else:
                    ap_dep_df.to_csv(arrival_connections, mode='a', header=False, index=False)
            except Exception as e:
                print(f"skipping url for {departure} do to an exception:",e)
        

        #scrape for prices from the departing airport
        price_link_scrape("YKA", "YVR", str(date.today()))