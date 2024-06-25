
# Test Task on Fast API


## Setup instructions
Linux:

Make python envrionment and activate it

``` python3 -m venv <your_venv_name> ```

``` source <your_venv_name>/bin/activate ```

Install dependecies

``` pip install -r requirement.txt ```

Make sure to convert the example.env to .env and put all the required values to connect with the database


## How to Run the application

make sure you are in the project directory

``` uvicorn main:app --reload ```

## For running the test cases

make sure you are in the project directory

``` pytest ```
