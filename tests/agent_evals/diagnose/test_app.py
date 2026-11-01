from app import Notebook

def test_navigation_after_output():
    nb = Notebook()
    nb.receive_output("2")
    assert nb.output == "2"
    assert nb.leave() == "library"
