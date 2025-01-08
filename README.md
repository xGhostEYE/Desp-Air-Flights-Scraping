
# Desp-Air-Flights-Scraping

Desp-Air-Flights is a university project I lead with a dedicated team of six. We aim to assist travelers who get stranded at airports by helping them reach their destinations on the same day their flights are canceled. Unlike Kayak.com or Google Flights, this service doesn't prioritize finding the best flight option by filtering out numerous possibilities. Instead, it focuses on identifying any available flights that can be linked together, even across different airlines, to ensure the users can get to their desired destination on the same day.

### Disclaimer 
This project was just meant for university and does not generate any money and is not in use. All data harvested by the scraper was deleted after the grade was given for the class.


## Features

### Getting flight data
- Arrivals and Departures: Using requests to retrieve HTML from an online platform (airports-worldwide.info), the code parses real-time flight information with BeautifulSoup.
  
- Flight Information: Departure and arrival times, flight numbers, airline codes, and statuses are extracted and stored as structured data in a database.

### Finding valid flight paths
- Algorithmic approach: Traveling Salesman Algorithm ensures that all same-day flights are considered, connecting multiple airports and carriers if necessary.

- No preference: The algorithm doesn’t prioritize cost or airline preference but purely focuses on feasibility. This way a passenger can feasibly hop from flight to flight to get to their destination within the same day.

### Getting tickets
- Kayak scraping with Selenium: The Selenium library is used on Kayak.com to obtain flight tickets for the flights returned by the algorithm.

- Anti-Bot Measures: Random user agents, wait times, and browser configurations are used to mimic real user behavior.

- Ticket links: Direct URLs are extracted to airline booking sites which the front-end can present to the user.

