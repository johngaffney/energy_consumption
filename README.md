# Architecture Note:

I decide to structure this python code as a package. The reason I did this is it can now be easily deployed in an AWS Lambda function which is triggered by an API GW as so this code can be quickly exposed as an API. 
However this might make testing the code locally slightly more tricky so I have provided steps below. 

The other decision I made when structuring the code was to assume this was the first API/function is a project that would grow and so I tried to structure the files in a manner which would allow more API handlers to be added without major code restructuring.

# Execution Flow
The function `get_energy_consumption_details` has two main stages

1 - get the consumption interval data from OpenVolt and build a dict containing an item for each half-hour period with consumption value

2 - get the carbon emissions from carbon intensity api for customer postcode. Note: I am calling this API once for each day as there seems to be a limit at approx 15 days which wasn't in the docs so to be safe I am using 1 day periods.
For each day response I have looping through the HH periods and using the intensity for that period and the consumption for the period (as retrieved in step 1) to calculate emissions for the period (Note: for intensity I am using the forecast field as the actual field is not available - could be a bug as API is in BETA or could be I need to use another API)

In step 2 I am also calculating the fuel mix used by the customer.

Finally structure the reponse to the client. 


# Getting Setup Locally
Once you have cloned the repo navigate to `energy_consumption/energy_consumption/src` in your terminal
run `python setup.py install` to install the package
run `python` to enter the REPL\
run `from energy_consumption.main import get_energy_consumption_details`
run `get_energy_consumption_details("6514167223e3d1424bf82742", "2023-01-01", "2023-01-31")`

Response should be:
```
{'meter_id': '6514167223e3d1424bf82742', 'start_date': '2023-01-01', 'end_date': '2023-01-31', 'total_energy_consumed': 98613.0, 'energy_consumption_unit': 'kWh', 'total_emissions': 16304.841, 'emissions_unit': 'kg CO2/kWh', 'fuel_mix_percentage_breakdown': {'biomass': 1.1707067019561315, 'coal': 0.8912029854076032, 'imports': 21.859328891728264, 'gas': 28.87762972427569, 'nuclear': 11.330397614918931, 'other': 0.0, 'hydro': 1.0643667670591093, 'solar': 1.4082788273351368, 'wind': 33.3952633019987}}
```

# Unit Tests
there is a single unit test which covers a basic path on `get_energy_consumption_details`
To run the test navigate to `energy_consumption`
run `pytest --cov=energy_consumption/src --cov-report=term-missing energy_consumption/tests -vv`

more detailed tested would be need for this function

# What's missing?
- get_energy_consumption_details could be refactored as its ~90 lines long already
- Use models to structure the API response instead of passing around dicts as it would be more type safe
- real unit tests
- expose the function as an api
- how I am extracting postcode from address is brittle