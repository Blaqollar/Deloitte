import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    converted_data = {}

    # Extract device ID and device type
    converted_data["deviceID"] = jsonObject["deviceID"]
    converted_data["deviceType"] = jsonObject["deviceType"]

    # Convert timestamp from milliseconds to ISO format
    timestamp = jsonObject["timestamp"] / 1000  # Divide by 1000 to convert milliseconds to seconds
    converted_data["timestamp"] = datetime.datetime.fromtimestamp(timestamp).isoformat()


    # Extract location information
    location = jsonObject["location"].split("/")
    converted_data["location"] = {
        "country": location[0],
        "city": location[1],
        "area": location[2],
        "factory": location[3],
        "section": location[4]
    }

    # Extract data information
    converted_data["data"] = {
        "status": jsonObject["operationStatus"],
        "temperature": jsonObject["temp"]
    }

    return converted_data



def convertFromFormat2(jsonObject):
    converted_data = {}

    # Extract device ID and device type from the nested "device" object
    converted_data["deviceID"] = jsonObject["device"]["id"]
    converted_data["deviceType"] = jsonObject["device"]["type"]

    # Convert timestamp from ISO format to milliseconds
    timestamp = datetime.datetime.strptime(jsonObject["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    converted_data["timestamp"] = int(timestamp.timestamp() * 1000)  # Multiply by 1000 to convert seconds to milliseconds

    # Extract location information
    converted_data["location"] = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }

    # Extract data information
    converted_data["data"] = {
        "status": jsonObject["data"]["status"],
        "temperature": jsonObject["data"]["temperature"]
    }

    return converted_data



def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
