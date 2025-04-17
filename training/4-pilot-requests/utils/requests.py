import random


def generate_request(flights, request_class=-1):
    flight = random.choice(flights)

    if request_class == -1:
        request_class = random.randint(0, 3)  # ← fix here

    if request_class == 0:
        templates = PUSHBACK_TEMPLATES
    elif request_class == 1:
        templates = TAXI_TEMPLATES
    elif request_class == 2:
        templates = TAKEOFF_TEMPLATES
    elif request_class == 3:
        templates = LANDING_TEMPLATES

    return (
        random.choice(templates).format(flight=flight),
        flight,
        request_class,
        flights,
    )


# Class 0: Pushback
PUSHBACK_TEMPLATES = [
    "Tower, this is {flight}, currently parked at gate Alpha Seven, requesting clearance for pushback and startup procedures.",
    "Ground control, {flight} at terminal gate requesting permission to commence pushback for scheduled departure.",
    "{flight} requesting pushback clearance from stand Four Two, systems all checked and ready.",
    "{flight} to ground, we are at gate Bravo Two and ready for pushback when approved.",
    "Ground, {flight}, fully boarded and ready at gate, requesting pushback followed by taxi instructions.",
    "{flight} at parking bay Two Five requesting permission for pushback, engines to be started during movement.",
    "This is {flight} on stand One Zero requesting pushback and engine start for departure to Dubai.",
    "{flight}, gate checks complete, requesting pushback and startup for outbound leg.",
    "Ground, this is {flight}, request pushback clearance, passengers onboard and doors secured.",
    "Tower, {flight} is fully loaded and ready at gate, requesting clearance to push and start engines.",
]

# Class 1: Taxi
TAXI_TEMPLATES = [
    "{flight} requesting taxi clearance to runway Two Seven Left, ready at holding point Charlie.",
    "Tower, this is {flight}, pushback complete, requesting taxi instructions to active runway.",
    "{flight} at apron Four, ready to taxi for departure, requesting route and holding point.",
    "{flight} to ground, pushback complete and brakes released, requesting taxi clearance.",
    "Ground, {flight}, ready for taxi, requesting taxiway routing to departure runway.",
    "Tower, {flight}, request taxi clearance to runway Zero Six Right, we're ready and holding.",
    "This is {flight}, engines running and pushback complete, request permission to taxi for departure.",
    "{flight}, brakes released and steering engaged, request taxi route to holding point Alpha Four.",
    "Tower, {flight}, aircraft on the move, request taxi clearance to the designated departure runway.",
    "Ground, this is {flight}, requesting clearance to taxi to runway via standard routing.",
]

# Class 2: Takeoff
TAKEOFF_TEMPLATES = [
    "Tower, {flight} ready at runway Two Seven Left, requesting takeoff clearance for outbound leg.",
    "{flight} holding short of runway, ready for immediate departure, requesting takeoff clearance.",
    "This is {flight}, aligned on runway One Eight, requesting clearance for takeoff.",
    "{flight}, fully ready at the hold line, requesting clearance for departure from runway.",
    "Tower, {flight}, we are ready for takeoff, requesting final clearance and departure heading.",
    "{flight}, brakes set and engines stable, request takeoff clearance from active runway.",
    "Tower, {flight}, ready for departure to destination, requesting immediate takeoff approval.",
    "This is {flight}, clear of all checks, requesting takeoff clearance from runway Zero Nine.",
    "{flight} holding at Alpha Two, request departure clearance and wind direction confirmation.",
    "Tower, {flight}, all systems go, request takeoff from runway Three Three Right."
]

# Class 3: Landing
LANDING_TEMPLATES = [
    "{flight}, inbound on final for runway Three Three Right, requesting landing clearance.",
    "Tower, this is {flight}, established on ILS approach, request landing clearance and wind check.",
    "{flight}, six miles out, aligned with runway Zero Nine, requesting final landing clearance.",
    "Tower, {flight}, inbound at one thousand five hundred feet, requesting permission to land.",
    "{flight} on approach to runway One Eight, requesting clearance and confirmation of traffic.",
    "This is {flight}, visual with the runway, requesting immediate clearance to land.",
    "Tower, {flight}, on final approach, gear down and locked, requesting landing instructions.",
    "Inbound aircraft {flight}, requesting confirmation for final approach to runway and landing clearance.",
    "{flight}, twenty miles out on standard arrival path, requesting descent and landing permission.",
    "Tower, this is {flight}, fully configured for landing, request immediate clearance to touch down."
]
