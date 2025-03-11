import os
import threading
import queue
from plane import Plane
import configuration as config
from utils import *


class ATCCommunicator:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.speaking_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.speaking_thread.start()

    def _process_queue(self):
        while True:
            command, message, plane = (
                self.message_queue.get()
            )
            os.system(f'say "{message}"')
            self.message_queue.task_done()
            self._issue_command(command, plane)

    def say(self, command: str, message: str, plane: Plane):
        self.message_queue.put((command, message, plane))

    def _extract_plane_ref(self, plane: Plane):
        airline = config.CALLSIGNS_DICT.get(plane.id[:2], "Unknown")
        flight_number = " ".join(plane.id[2:])
        return f"{airline} {flight_number}"
    
    def _issue_command(self, command: str, plane: Plane):
        if command == "pushback":
            pass
        elif command == "hold-pushback":
            pass
        elif command == "taxi":
            pass

    def issue_pushback(self, plane: Plane):
        plane_ref = self._extract_plane_ref(plane)

        message = f"Pushback and start approved, {plane_ref}."
        self.say("pushback", message, plane)

    def deny_pushback(self, plane: Plane):
        plane_ref = self._extract_plane_ref(plane)

        message = f"Hold pushback, {plane_ref}."
        self.say("hold-pushback", message, plane)

    def issue_taxi(self, plane: Plane):
        plane_ref = self._extract_plane_ref(plane)
        runway = get_edge_object(config.TAKEOFF_RUNWAY).start.id[4:]

        if runway[-1] in ['R', 'L', 'C']:
            alignment = {'R': 'right', 'L': 'left', 'C': 'center'}[runway[-1]]
            runway = f"{' '.join(runway[:-1])} {alignment}"
        else:
            runway = ' '.join(runway)

        message = f"Taxi to runway {runway} approved, {plane_ref}."
        self.say("taxi", message, plane)
