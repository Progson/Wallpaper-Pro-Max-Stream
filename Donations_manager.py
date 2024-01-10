import threading

class Donation_manager:
    def __init__(self):
        self.donations = []  # id, name, amount, prompt, url
        self.donations_lock = threading.Lock()

    def access_donations(self, action="", args=[]):
        with self.donations_lock:
            if action == "get_length":
                return len(self.donations)
            elif action == "delete":
                if len(args) == 1:
                    self.donations.pop(args[0])
                else:
                    self.donations.pop()
            elif action == "append":
                self.donations.append(args)
            elif action == "read":
                return self.donations[args[0]]
            elif action == "copy":
                return self.donations.copy()
