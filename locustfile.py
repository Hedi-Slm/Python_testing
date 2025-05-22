from locust import HttpUser, task, between


CLUB_NAME = "Simply Lift"
CLUB_EMAIL = "john@simplylift.co"
FUTURE_COMPETITION = "Spring Festival"
PAST_COMPETITION = "Fall Classic"


class ProjectUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        self.client.get("/")
        # Log in
        self.client.post("/showSummary", data={"email": CLUB_EMAIL})

    @task
    def index(self):
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Index route too slow")

    @task
    def show_summary(self):
        with self.client.post("/showSummary", data={"email": CLUB_EMAIL}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Login too slow")

    @task
    def dashboard(self):
        with self.client.get("/dashboard", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Dashboard too slow")

    @task
    def book_future_competition(self):
        with self.client.get(f"/book/{FUTURE_COMPETITION}/{CLUB_NAME}", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Booking (future comp) too slow")

    @task
    def purchase_places(self):
        with self.client.post("/purchasePlaces", data={
            "competition": FUTURE_COMPETITION,
            "club": CLUB_NAME,
            "places": "1"
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Purchase too slow")

    @task
    def points(self):
        with self.client.get("/points", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Points route too slow")

    @task
    def logout(self):
        with self.client.get("/logout", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Logout too slow")
