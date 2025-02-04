# main.py
WIDTH = 1200
HEIGHT = 600
FPS = 60
AIRPORT_ICAO = "EGBB"
RUNWAY_IN_USE = "RNWY33-RNWY15"
PLANES = []
PUSHBACK_PROBABILITY = 2000

# airport.py
MARK_FONT = None
DATA_FONT = None
NODE_LIST = []
EDGE_LIST = []
STAND_LIST = []
NODE_DICT = {}
EDGE_DICT = {}
STAND_DICT = {}

RENDER_NODES = True
RENDER_EDGES = True
RENDER_STANDS = True

# plane.py
THRUST_CHANGE_RATE = 2  # Rate of thrust adjustment
MAX_SPEED = 150  # Maximum velocity in m/s
FLIGHT_DRAG = 0.05 # DRAG_COEFFICIENT = 0.25  # Air drag proportional to v²
GROUND_DRAG = 0.25
MAX_ACCELERATION = 5  # Maximum acceleration in m/s²
BRAKE_MULTIPLIER = 0.98  # Speed reduction factor when braking
FRICTION = 10  # Ground friction proportional to velocity
PIXEL_TO_METRE = 2.5  # 1 pixel = 2.5 meters
TIME_STEP = 1 / FPS  # Frame time (30 FPS)
MAX_TURN_ANGLE = 1  # Maximum turn angle in degrees
TURN_SPEED_SCALING = 0.05  # Scaling factor for speed-dependent turning
SLOW_DISTANCE = 10  # Distance at which to slow down to stop
SLOW_SPEED = 15 # knots
TAXI_SPEED = 25 # knots
