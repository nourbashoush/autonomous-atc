# main.py
WIDTH = 1200
HEIGHT = 600
FPS = 30
NORMAL_SPEED = False
AIRPORT_ICAO = "EGBB"
TAKEOFF_RUNWAY = "RNWY33-RNWY15"
LANDING_RUNWAY = "RNWY33-RNWY15"
PIXEL_TO_METRE = 2.5  # 1 pixel = 2.5 meters

RUNWAY_OCCUPATION = 0
PLANES = []
LANDING_PLANES = []
PLANES_QUEUE_FOR_RUNWAY = []

LANDING_DISTANCE = 4000
APPROACH_DISTANCE = 1900
FINAL_DISTANCE = 900
TIME_BETWEEN_LANDINGS = 90

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

BOUNDING_BOXES = []
AIRPORT_IMG = None

RENDER_NODES = True
RENDER_EDGES = True
RENDER_STANDS = True
RENDER_DATA = True
RENDER_PREDICTION = True
RENDER_BOXES = True
PUSHBACK_PROBABILITY = 1_000
LANDING_PROBABILITY = 2_000

FRAME = 0
LAST_SPAWN = 0

COLLISION_THRESHOLD = 36 # Planes are 17x17 pixels
SEPERATION_THRESHOLD = 28
HOLD_PERIOD = 2 * FPS
HOLDING_DISTANCE = 8

# plane.py
GROUND_IMG_PATH = "assets/images/plane_ground.png"
GROUND_IMG = None
AIRBORNE_IMG_PATH = "assets/images/plane_airborne.png"
AIRBORNE_IMG = None

THRUST_CHANGE_RATE = 2      # Rate of thrust adjustment
MAX_SPEED = 150             # Maximum velocity in m/s
LANDING_DRAG = 0.04
TAKEOFF_DRAG = 0.06
GROUND_DRAG = 0.25
MAX_ACCELERATION = 5        # Maximum acceleration in m/s²
BRAKE_MULTIPLIER = 0.98     # Speed reduction factor when braking
FRICTION = 10               # Ground friction proportional to velocity
TIME_STEP = 1 / FPS         # Frame time (30 FPS)
MAX_TURN_ANGLE = 1          # Maximum turn angle in degrees
TURN_SPEED_SCALING = 0.05   # Scaling factor for speed-dependent turning
SLOW_DISTANCE = 10          # Distance at which to slow down to stop      # TODO remove these 3
SLOW_SPEED = 15             # knots
TAXI_SPEED = 25             # knots

# taxi_model.py
TAXI_MODEL_PATH = "models/taxi_model.pth"
TAXI_MODEL = None
MAX_DEVIATION = 4

# lstm_model.py
LSTM_MODEL_PATH = "models/lstm_model.pth"
LSTM_MODEL = None

YOLO_MODEL_PATH = "models/yolo.pt"
YOLO_MODEL = None
