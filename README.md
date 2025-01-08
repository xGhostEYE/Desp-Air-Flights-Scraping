
# Desp-Air-Flights-Scraping

Desp-Air-Flights is a university project I lead with a dedicated team of six. We aim to assist travelers who get stranded at airports by helping them reach their destinations on the same day their flights are canceled. Unlike Kayak.com or Google Flights, this service doesn't prioritize finding the best flight option by filtering out numerous possibilities. Instead, it focuses on identifying any available flights that can be linked together, even across different airlines, to ensure the users can get to their desired destination on the same day.

### Disclaimer 
This project was just meant for university and does not generate any money and is not in use. All data retrived by the scraping was deleted after the grade was given for the class.


## Features

### Getting flight data
Leveraging an online platform that provides live arrival and departure information for any airport, I utilized the requests library to retrieve the website's HTML data. Following this, I employed the BeautifulSoup library to extract the URLs of the flights, enabling me to access the flight arrival and departure times.

### Finding valid flight paths

Flight arrival and departure times then get placed into a database that uses a Traveling Salesman Algorithm to find valid flight paths.

### Getting tickets for the flights
We use the Selenium library on Kayak.com to obtain flight tickets for the routes returned by the algorithm. By employing various techniques to simulate human behavior to fool the site protections, the ticket linksfor airlines that have flights matching the previously retrieved flight numbers are extracted. These links are then passed to the Front-End.

