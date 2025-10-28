import tomli
from utils.db_util import connect_to_db, create_new_database
from datetime import datetime



#spliting names to compent parts
def sep_name(name):
    # Initialize empty lists
    first_names = []
    middle_names = []
    last_names = []

    for full_name in names:
        parts = full_name.strip().split()
    
        if len(parts) == 1:
           # Only first name
            first_names.append(parts[0])
            middle_names.append("")
            last_names.append("")
        elif len(parts) == 2:
            # First and last name
            first_names.append(parts[0])
            middle_names.append("")
            last_names.append(parts[1])
        else:
         # First, middle, and last (handles multiple middle names too)
            first_names.append(parts[0])
            middle_names.append(" ".join(parts[1:-1]))
            last_names.append(parts[-1])

    return first_names, middle_names, last_names

#spliting address to componet part
def sep_addr(addr):
    num = []
    street = []
    city = []
    state = []
    z = []
    for n in addr
        sepN = n.strip()..split()
        num.append(sepN[0])
        street.append(sepN[1])
        city.append(sepN[2])
        if(len(sepN[3]) > 2) #if not 2 format change
            state.append(state_to_abbreviation(sepN[3]))
        else
            state.append(sepN[3])
        z.append(sepN[4])

    return num, street, city, state, z

state_abbreviations = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY"
}
def state_to_abbreviation(state_name: str) -> str:
    """Convert a lowercase U.S. state name to its abbreviation."""
    return state_abbreviations.get(state_name.lower(), "Invalid state name")

#time conversion


def convert_datetime(dt_str, input_format, output_format):
    """
    Converts a date/time string from one format to another.
    
    Args:
        dt_str (str): The original date/time string.
        input_format (str): The format of the input date/time string.
        output_format (str): The desired output format.
        
    Returns:
        str: The converted date/time string.
    """
    try:
        # Parse the input date/time string
        dt_obj = datetime.strptime(dt_str, input_format)
        # Convert to the desired output format
        return dt_obj.strftime(output_format)
    except ValueError as e:
        return f"Error: {e}"
        
#distants conversions
def convert_miles_KM(miles):
    km = miles * 1.60934
    return km

def convert_meters_KM(miles):
    km = meters / 1000
    return km 

def convert_in_feet(in):
    feet = in / 12
    return feet

def convert_feet_meters(feet):
    meters = feet *0.305
    return meters

#temp conversions
def convert_fah_cel(fah):
    cel = 5/9 * (33 * fah -32)
    return cel
def convert_cel_K
    K = cel -273.15
    return K

def main():
    


if __name__ == "__main__":
    main()
