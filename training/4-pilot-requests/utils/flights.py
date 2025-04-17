import random

def generate_flights(num_flights=10):
    flights = []

    for _ in range(num_flights):
        airline = random.choice(AIRLINES)
        flight_number = random.randint(100, 999)
        flight = f"{airline} {' '.join(DIGITS[digit] for digit in str(flight_number))}".strip()

        while flight in flights:
            flight_number = random.randint(100, 999)
            flight = f"{airline} {' '.join(DIGITS[digit] for digit in str(flight_number))}".strip()

        flights.append(flight)
    
    return flights


AIRLINES = [
    "American",
    "Delta",
    "United",
    "Southwest",
    "Speedbird",
    "Air France",
    "Lufthansa",
    "Qantas",
    "Emirates",
    "Cathay",
    "KLM",
    "All Nippon",
    "Singapore",
    "Iberia",
    "Alitalia",
    "Turkish",
    "EgyptAir",
]

DIGITS = {
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "0": "zero",
}