from google.adk.tools import Tool


class GoogleMapsTool(Tool):
    def __init__(self):
        super().__init__(
            name="get_directions",
            description="Get directions from an origin to a destination.",
            fn=self.get_directions,
            input_schema={"origin": str, "destination": str},
        )

    def get_directions(self, origin: str, destination: str) -> str:
        """
        A placeholder function to get directions.
        In a real implementation, this would call the Google Maps API.
        """
        return f"Directions from {origin} to {destination}: Head north, then east. You have arrived."


google_maps_tool = GoogleMapsTool()