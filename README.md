# Days at Home

This project takes a CSV file of hotel stay data, and generates an SVG chart comparing days spent traveling to days spent at home.

## CSV Input

Accepts a CSV file with one row for each hotel stay. Each row should have three columns:

* A `Checkout Date` (in `YYYY-MM-DD` format)
* The hotel's `City`
* The number of `Nights` spent at the hotel

By default, the hotel data should be saved in `data/hotels.csv`.

### Example CSV

```
Checkout Date,City,Nights
2020-01-06,"New York, NY",3
2020-01-23,London,5
2020-01-25,Paris,2
2020-02-05,"Chicago, IL",4
```
