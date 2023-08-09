import json
import threading
import time


class SessionMonitorThread(threading.Thread):
    def __init__(
        self,
        username,
        signout_function,
        sessionId,
        session_id_file="users.json",
        check_interval=5,
    ):
        super().__init__()
        self.session_id_file = session_id_file
        self.signout_function = signout_function
        self.check_interval = check_interval
        self.username = username
        self.stopped = False
        self.sessionId = sessionId

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            try:
                with open(self.session_id_file, "r") as file:
                    session_data = json.load(file)

                for user in session_data:
                    if user["username"] == self.username:
                        current_session_id = user.get("sessionId", "")
                        print(f"I am checking {self.username}")
                        if current_session_id != self.sessionId:
                            self.signout_function()

                            self.stop()
                        break

            except FileNotFoundError:
                pass  # File doesn't exist yet, no need to worry

            time.sleep(self.check_interval)
