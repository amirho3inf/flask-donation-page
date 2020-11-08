# An simple donation website using [Flask](https://github.com/pallets/flask/) and [Webpay](https://github.com/amirho3inf/python-webpay/)

### Screenshots
|1|2|
|-|-|
|![](/screenshots/screenshot_1.png?raw=true)|![](/screenshots/screenshot_2.png?raw=true)|

### Setup and Run
Clone this repository: 
```bash 
git clone https://github.com/amirho3inf/flask-donation-page.git
```
Go to the directory and install requirements:
```bash 
cd flask-donation-page
pip install -r requirements
```
Customize the configuration in `config.py` file
And finally run the migrations:
```bash
flask db upgrade
```
Now you can run it:
```bash
flask run
```