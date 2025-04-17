# main.py
WIDTH = 1200
HEIGHT = 600
FPS = 30
RENDER = True

DATA_FONT = None
SCORE_FONT = None
EPISODE_LENGTH_MULTIPLIER = FPS / 2.5

MAX_DEVIATION = 10
DISTANCE_CHECKPOINTS = 3

# plane.py
THRUST_CHANGE_RATE = 2      # Rate of thrust adjustment
MAX_SPEED = 100             # Maximum velocity in m/s
FLIGHT_DRAG = 0.25          # DRAG_COEFFICIENT = 0.25  # Air drag proportional to v²
GROUND_DRAG = 0.05
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
