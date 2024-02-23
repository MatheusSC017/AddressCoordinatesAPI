# Address Coordinates API

![Linguagem mais usada](https://img.shields.io/github/languages/top/MatheusSC017/AddressCoordinatesAPI)
![Numero de lingaugens usadas](https://img.shields.io/github/languages/count/MatheusSC017/AddressCoordinatesAPI)
![Lincense](https://img.shields.io/github/license/MatheusSC017/AddressCoordinatesAPI)
![Tamanho do projeto](https://img.shields.io/github/languages/code-size/MatheusSC017/AddressCoordinatesAPI)

This API has been developed with the specific intent of serving as a microservice within another project featured in my portfolio.

## Technologies
Key technologies employed in the construction of this API include:

- Flask
- PyJWT
- Pymongo (MongoDB)
- Dotenv

## Documentation
Regarding the available endpoints, you can view them in the Swagger documentation at this [link](https://address-coordinates-cd0a1a6282b5.herokuapp.com/v1/ui/)

## Requirements
To run this project, make sure you have the below software installed on your device
- Python >= 3.10

## Installation

### On-premises installation
1. Clone the repository on your device

2. Go to the repository of the cloned project on your device

3. Create a virtual environment on your device and activate it (command for linux OS)
> python -m venv venv
> 
> . venv/bin/activate

4. Install the libraries saved in the requirements.txt file, if you are using the PIP package manager you can use the following command
> pip install -r requirements.txt

5. The last step is to define the settings, for this create a file named **.env** and define the parameters below

~~~
SECRET_KEY = ''
MONGO_URI = ''
GOOGLE_MAPS_SECRET_KEY = ''
~~~

The purpose of each parameter is described below

* SECRET_KEY: This parameter defines a key for the project used for the purpose of creating and validating tokens for project users
* MONGO_URI: Information for connecting mongoDB dataset, you can use your local mongoDB through [compass](https://www.mongodb.com/products/tools/compass) or you can use [online service](https://www.mongodb.com/online)
* GOOGLE_MAPS_SECRET_KEY: Secret key to connect to Google's geocoding service, to create the key access this [link](https://developers.google.com/maps/documentation/geocoding/?hl=pt_BR)

6. The final step is to run the application, to do this run the command below:
> flask --app address run 

## Obtaining an API Key Token

To get an API key token, run the ApiKey.py file and enter the name you want to use as identification, it will print the JWT token at the prompt that you can use
