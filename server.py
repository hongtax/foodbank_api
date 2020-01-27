import web
import ast
from geopy.distance import geodesic
import json
import html

def return_nearest_foodbanks_to_given_location (location_lat_long, number_of_foodbanks_to_return):
		list_of_foodbanks_and_distance_away_from_location = [] # Return list will contain foodbank name and distance away, in ascending order of distance.
		for foodbank in list_of_dictionaries_containing_information_on_all_foodbanks:
			if 'error' in list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]:
				continue # Skip the foodbank if it has an error
			else:
				foodbank_lat_long = (list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["latitude"], list_of_dictionaries_containing_information_on_all_foodbanks[foodbank]["longitude"])
				distance_between_points = geodesic(location_lat_long, foodbank_lat_long).miles
				distance_between_points = round(distance_between_points)
				list_of_foodbanks_and_distance_away_from_location.append([foodbank, distance_between_points])
		list_of_foodbanks_and_distance_away_from_location.sort(key = return_second_element) # Sort the list by its second element (distance)
		return(list_of_foodbanks_and_distance_away_from_location[0:number_of_foodbanks_to_return]) # Return the number of foodbanks requested

def return_second_element (input_list): # Return the second element of an input list. Used when sorting by distance
	return(input_list[1])

def return_relevant_information_for_given_list_of_foodbanks(list_of_foodbanks_to_print):
	dictionary_to_return = {}
	for nearby_foodbank in list_of_foodbanks_to_print: # Add some information before returning
		if 'error' in list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]:
			continue # Skip the foodbank if it has an error 
			## TODO: For places without a website, return a phone number and suggest giving them a ring? Error will be "No website given by master list"
		else:
			tidy_foodbank_name =  html.unescape(nearby_foodbank[0])
			dictionary_to_return[tidy_foodbank_name] = {"Distance" : str(nearby_foodbank[1]) + " miles", "Address" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["address"],  "Website" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["website"].replace("\\", ""),  "Items needed" : list_of_dictionaries_containing_information_on_all_foodbanks[nearby_foodbank[0]]["items_needed"], }
	return json.dumps(dictionary_to_return)

def show_nearby_foodbanks_and_items_needed (location_tuple, number_of_foodbanks_to_show):
	list_of_nearby_foodbanks = return_nearest_foodbanks_to_given_location(location_tuple, number_of_foodbanks_to_show)
	return return_relevant_information_for_given_list_of_foodbanks(list_of_nearby_foodbanks)

def return_items_needed_by_given_foodbank (name_of_foodbank): # Give a foodbank name. Get back a list of items needed
	if (name_of_foodbank in list_of_dictionaries_containing_information_on_all_foodbanks):
		dictionary_to_return = {"Foodbank name" : name_of_foodbank, "Items needed" : list_of_dictionaries_containing_information_on_all_foodbanks[name_of_foodbank]["items_needed"]}
		return json.dumps(dictionary_to_return)
	else:
		return "This foodbank isn't in our database, sorry"
	
urls = (
	'/', 'index',
	'/individual_foodbank_information', 'individual_foodbank_information',
	'/nearest_foodbanks', 'nearest_foodbanks'
)

class index:
	def GET(self):
		return "Hello! This is an API that gives information on nearby food banks and the items they need. Check out the documentation, when it exists..."

class documentation:
	def GET(self):
		return 
	<!DOCTYPE html>
<html>
<body>

<h1 id="Foodbank API">Foodbank API</h1>
<p>Contains information about individual food items needed by a Trussell Trust food bank specified by name or location. 

<h2 id="Base URL">Base URL</h2>
<p>http://whatfoodbanksneed.org.uk</p>

<h3 id="Endpoint 1">Endpoint 1</h3>
<p>GET /Individual_foodbank_information</p>

<h4 id="Description">Description</h4>
<p>This returns the food bank name and the food items needed for the named food bank.</p>

<h4 id="Query string parameters">Query string parameters</h4>

<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>
</head>
<body>

<table style="width:100%">
  <tr>
    <th>Query string parameter</th>
    <th>Required/optional</th> 
    <th>Description</th>
    <th>Type</th>
  </tr>
  <tr>
    <td>foodbank_name</td>
    <td>Required</td> 
    <td>Name of food bank</td>
    <td>string</td>
  </tr>
</table>

<h4 id="Response">Response</h4>

<table style="width:100%">
  <tr>
    <th>Field</th>
    <th>Description</th> 
    <th>Data type</th>
    <th>Example</th>
  </tr>
  <tr>
    <td>foodbank_name</td>
    <td>Name of food bank</td> 
    <td>String</td>
    <td>"Mid Norfolk Foodbank"</td>
  </tr>
   <tr>
    <td>Items_needed</td>
    <td>List of food items needed for specified food bank</td> 
    <td>array [string]</td>
    <td>"tinned fruit", "tinned rice pudding"</td>
  </tr>
</table>

<h4 id="Input error">Input error</h4>
<p>If the food bank doesn't exist, it will return the following string:
<blockquote>"This food bank isn't in our database, sorry."</blockquote></p>

<h3 id="Endpoint 2">Endpoint 2</h3>
<p>GET /nearest_foodbanks</p>

<h4 id="Description">Description</h4>
Returns information about food banks near to your specified location in ascending order of distance, which includes food bank name, distance to inputted location in miles, food bank address, food bank website and food items needed.

<h4 id="Query string parameters">Query string parameters</h4>

<table style="width:100%">
  <tr>
    <th>Query string parameter</th>
    <th>Required/optional</th> 
    <th>Description</th>
    <th>Type</th>
  </tr>
  <tr>
    <td>Latitude</td>
    <td>Required</td> 
    <td>Latitude of the search area [needs range of numbers that will be supported]</td>
    <td>Decimal</td>
  </tr>
   <tr>
    <td>Longitude</td>
    <td>Required</td> 
    <td>Longitude of the search area</td>
    <td>Decimal</td>
  </tr>
   <tr>
    <td>number_of_foodbanks_to_return</td>
    <td>Required</td> 
    <td>To limit the number of food banks that appear based on what the user has inputted [Martin to confirm max number]</td>
    <td>Integer</td>
  </tr>
    </table>
  
<h4 id="Response">Response</h4>
 
 <table style="width:100%"> 
  <tr>
    <th>Field</th>
    <th>Description</th> 
    <th>Data type</th>
    <th>Example</th>
  </tr>
  <tr>
    <td>name_of_foodbank</td>
    <td>Food bank name</td> 
    <td>String</td>
    <td>"Mid Norfolk Foodbank</td>
  </tr>
   <tr>
    <td>list_of_nearby_foodbanks</td>
    <td>List of nearby foodbanks</td> 
    <td>Array of objects in ascending order of distance (the fields for that object are nearby_foodbank; website; items_needed) </td>
    <td></td>
  </tr>
   <tr>
    <td>nearby_foodbank</td>
    <td>Distance from the user's location in miles</td> 
    <td>String</td>
    <td>"15 miles"</td>
  </tr>
   <tr>
    <td>website</td>
    <td>Food bank website</td> 
    <td>URL</td>
    <td>http://midnorfolk.foodbank.org.uk/</td>
  </tr>
   </tr>
   <tr>
    <td>items_needed</td>
    <td>Food items needed</td> 
    <td>Array[String]</td>
    <td>“tinned fruit”,
		“tinned riced pudding”</td>
  </tr>

</table>
 
  <h4 id="Input error">Input error</h4>
  <p>If no food banks are found an empty list will be returned.
	If the inputs are the wrong type or if they are missing then it will return the following string: 
<blockquote>"Please make a GET request to this endpoint with latitude, longitude, and a 'number_of_foodbanks_to_show' integer"</blockquote></p>
	
	</body>
	</html>	
	
class individual_foodbank_information:
	def GET(self):
		user_data = web.input()
		try:
			return(return_items_needed_by_given_foodbank(user_data.foodbank_name))
		except: 
			return("Please make a GET request to this endpoint with a 'foodbank_name' value given")

class nearest_foodbanks:
	def GET(self):
		user_data = web.input()
		try: # Raise an exception if we can't cast all 3 inputs as the right type below
			given_location = (float(user_data.latitude), float(user_data.longitude))
			return(show_nearby_foodbanks_and_items_needed(given_location, int(user_data.number_of_foodbanks_to_show)))
		except:
			return("Please make a GET request to this endpoint with latitude, longitude, and a 'number_of_foodbanks_to_show' integer")

with open("foodbank_data_storage.txt", "r") as data_storage_file:
		list_of_dictionaries_containing_information_on_all_foodbanks = ast.literal_eval(data_storage_file.readline())
		print("Information loaded from file\n")
		
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
