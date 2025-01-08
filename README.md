
# Desp-Air-Flights-Scraping

Desp-Air-Flights is a university project I lead with a team of 6 to help those that get stranded in Airports when their flights get cancelled. This service finds all avaliable flights from the departure airport (where the user is) to the arrival airport (where they want to go). It does this by web scraping flights from airport's departure and arrivals screens. All these flights are then placed into a Travelling Salesman Algorithm to find avaliable paths to a destination the user wants to get to. It then matches the airline names and flight numbers returned by the Algorithm with ones on Kayak.com to find tickets for the user. What differentiates this service from Kayak.com or Google Flights is that this service doesn't seek the best flight option by ignoring many possibilities. It simply finds what ever flights that arrive and depart from airports that can be chained together to get the user to where they want to go regardless if it's on different airlines and a hassle. This service is meant only for those that are desperate to get to where they want to be on the same day.

- Disclaimer: This project was just meant for university and does not generate any money and is not in use. All data retrived by the scraping was deleted after the grade was given for the class.

## Web Scraping

- Using an online website that contains live arrivales and departures for any airport. I used the requests library to get the website HTML data, and then used the BeautifulSoup library to extract the urls of the flights from the website to get the flight arrival and departure time.

- Flight arrival and departure times then get placed into a database that uses a Traveling Salesman Algorithm to find valid flight paths.

- The Selenium library is then used on Kayak.com to get flight tickets for the flight paths returned by the Algorithm. Utilizing various methods to fool the website into thinking the scraper was a human, it got the ticket links to the airlines that had flights matching the flight number of what was retrieved ealier.

- These links are then passed to the Front-End.



