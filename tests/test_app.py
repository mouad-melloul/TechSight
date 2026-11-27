from streamlit.testing.v1 import AppTest


def test_accueil_page_loads():
    at = AppTest.from_file("app.py", default_timeout=60).run()
    assert not at.exception


def test_analytics_page_loads():
    at = AppTest.from_file("app.py", default_timeout=60)
    at.session_state["page"] = "Analytics"
    at.run()
    assert not at.exception


# AppTest exécute votre app.py sans navigateur et échoue si une exception Streamlit est levée. C'est le moyen le plus simple de tester un dashboard.