# Python file script
import yaml

def load_zipper_pulls():
    with open("scrolls/zipper_pulls.yaml", "r") as f:
        return yaml.safe_load(f)

@app.route("/carousel")
def carousel():
    zipper_pulls = load_zipper_pulls()
    return render_template("carousel.html", zipper_pulls=zipper_pulls)

