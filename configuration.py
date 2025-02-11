# main.py
WIDTH = 1200
HEIGHT = 600
FPS = 30
AIRPORT_ICAO = "EGBB"
RUNWAY_IN_USE = "RNWY33-RNWY15"
PLANES = []

# airport.py
MARK_FONT = None
DATA_FONT = None
NODE_LIST = []
EDGE_LIST = []
STAND_LIST = []
NODE_DICT = {}
EDGE_DICT = {}
STAND_DICT = {}
EXIT_DICT = {}

RENDER_NODES = True
RENDER_EDGES = True
RENDER_STANDS = True
RENDER_DATA = False
RENDER_PREDICTION = True
PUSHBACK_PROBABILITY = 200
LANDING_PROBABILITY = 2000

FRAME = 0
LAST_SPAWN = 0

COLLISION_THRESHOLD = 36 # Planes are 17x17 pixels

# plane.py
GROUND_IMG = "images/plane_ground.png"
AIRBORNE_IMG = "images/plane_airborne.png"

THRUST_CHANGE_RATE = 2      # Rate of thrust adjustment
MAX_SPEED = 150             # Maximum velocity in m/s
LANDING_DRAG = 0.04
TAKEOFF_DRAG = 0.05
GROUND_DRAG = 0.25
MAX_ACCELERATION = 5        # Maximum acceleration in m/s²
BRAKE_MULTIPLIER = 0.98     # Speed reduction factor when braking
FRICTION = 10               # Ground friction proportional to velocity
PIXEL_TO_METRE = 2.5        # 1 pixel = 2.5 meters
TIME_STEP = 1 / FPS         # Frame time (30 FPS)
MAX_TURN_ANGLE = 1          # Maximum turn angle in degrees
TURN_SPEED_SCALING = 0.05   # Scaling factor for speed-dependent turning
SLOW_DISTANCE = 10          # Distance at which to slow down to stop
SLOW_SPEED = 15             # knots
TAXI_SPEED = 25             # knots

# taxi_model.py
TAXI_MODEL_PATH = "models/taxi_model.pth"
TAXI_MODEL = None
MAX_DEVIATION = 5

# lstm_model.py
LSTM_MODEL_PATH = "models/lstm_model.pth"
LSTM_MODEL = None