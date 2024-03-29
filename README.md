[![LinkedIn][linkedin-shield]][linkedin-url] [![web][web-shield]][web-url] 
[![web][resume-shield]][resume-url]


<h1>Investment 101 Portfolio</h1>
Create, Buy, Sell your stock portfolio in a real-time value.

<br>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>Introduction</li>
    <li>Usage</li>
    <li>Breakdown</li>
  </ol>
</details>
<h2>Introduction</h2>

* Developed a Banking Stock Exchange Simulation project, aiming to provide users with a platform resembling popular investment platforms like Wealth Simple, Scotia iTrade, and Questrade.
* Utilized HTML, CSS, and JavaScript to create an intuitive and visually appealing web interface, enhancing user experience and engagement.
* Implemented backend functionality using Python Flask and Jinja to handle stock transaction actions.
Integrated the Yahoo Finance API to fetch real-time stock data and validate symbols.
* Employed MySQL as the database management system for storing and retrieving user data, portfolio
information, and transaction history.

<img src="./project-img/Main Page (Portfolio).png" alt="project image">

<h2>Usage</h2>
Required to install

* Flask Framework
* Python Bcrypt
* Python yfinance

```

  pip install Flask 
  pip install yfinance
  pip install Flask-Bcrypt

```


<h2>Breakdown</h2>

<h3>App.py</h3>
Route Direction, User Session and Transaction Proceed. <br>
In the main page, a user session is checked to redirect client one of the cases:

- Login Page
- Portfolio Summary

<img src="./project-img/Signup Page.png" style="height: 200px">
<img src="./project-img/Login Page.png" style="height: 200px">

The client can sign up for an account and passwords are hashed using Bcrypt. <br>

Functionality:
1. Buy Stocks
2. Sell Stocks
3. Gain Loss on individual stock and total portfolio

<img src="./project-img/Buy Page.png" style="height: 200px"><img src="./project-img/Sell Page.png" style="height: 200px">
<img src="./project-img/Main Page (Portfolio).png" style="height: 200px">

<h3>Helper.py</h3>

Primary work to call query of REST API for checking symbols, Market Prices. MySQL script to create table is executed every time launching a server (if not exist). 

Retrieve users and send back to app.py by list of dictionaries. Convert the tuples from SQL Execution to dictionary and ![.append()] to ![list]

<h3>Script.js</h3>

Change color based on the gain and loss of the individual stock. ![green] means gain and ![red] means loss.

<h3>MySQL</h3>

MySQL is used to store user and stock data. Required on having SQL Server local.

Database: stockbase

Table stock:

* stock_id is the PRIMARY key with auto increment
* stock_symbol is from 1 to 8 character
* stock_book_value is the price of buying
* stock_shares is total shares
* stock_user_id is FOREIGN key for linking to specific users

Table user:
* user_id is the PRIMARY key with auto increment
* user_username used for login
* user_password is decode when saved and encode when retrieve
* user_total_value initially $10,000





[linkedin-url]: https://www.linkedin.com/in/harryph8605/
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge
[web-url]: https://devhuypham.me
[web-shield]:https://img.shields.io/badge/Harry_Pham-F96167?style=for-the-badge
[resume-url]: https://drive.google.com/file/d/1NxrqI-Wi9R3qad9Qz-mI5z1zJ5Yu6m_a/view?usp=sharing
[resume-shield]: https://img.shields.io/badge/Resume-F9E795?style=for-the-badge
[.append()]: https://img.shields.io/badge/.append()-orange?style=flat-square
[list]: https://img.shields.io/badge/list_%5B%5D-orange?style=flat-square
[green]: https://img.shields.io/badge/Green-green?style=flat-square
[red]: https://img.shields.io/badge/Red-red?style=flat-square



