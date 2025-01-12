from pygame.font import Font

# main.py
WIDTH = 1200
HEIGHT = 600
FPS = 30
AIRPORT_ICAO = "EGBB"
FONT = None
NODE_LIST = []
EDGE_LIST = []
NODE_DICT = {}
EDGE_DICT = {}

# plane.py
THRUST_CHANGE_RATE = 2  # Rate of thrust adjustment
MAX_SPEED = 100  # Maximum velocity in m/s
DRAG_COEFFICIENT = 0.5  # Air drag proportional to v²
MAX_ACCELERATION = 20
BRAKE_MULTIPLIER = 0.97
FRICTION = 10  # Ground friction proportional to velocity
PIXEL_TO_METRE = 2.5  # 1 pixel = 2.5 meters
TIME_STEP = 1 / FPS  # Frame time (30 FPS)
MAX_TURN_ANGLE = 1  # Maximum turn angle in degrees
TURN_SPEED_SCALING = 0.05  # Scaling factor for speed-dependent turning
SLOW_DISTANCE = 15  # Distance at which to slow down to stop
SLOW_SPEED = 10 # knotts
TAXI_SPEED = 25 # knotts
