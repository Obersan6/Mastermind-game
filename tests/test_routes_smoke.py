# Smoke test for the Flask app.
# Verifies that the home route ("/") responds with HTTP 200.

def test_home_smoke():
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        r = c.get("/")
        assert r.status_code == 200

