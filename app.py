# Python file script
from flask import Flask, render_template, request, redirect, abort, session, flash
from flask_mail import Mail, Message
import yaml
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-scroll-safe-secret"  # Required for session

# Mail configuration
app.config.update(
    MAIL_SERVER="smtp.yourprovider.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="your@email.com",
    MAIL_PASSWORD="your-password"
)
mail = Mail(app)

# --- Utility Functions ---

def load_yaml_scroll(path):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        return []

def save_custom_request(name, email, request_text):
    scroll_path = "scrolls/custom_requests.yaml"
    existing = load_yaml_scroll(scroll_path)
    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "email": email,
        "request": request_text
    }
    existing.append(new_entry)
    with open(scroll_path, "w") as f:
        yaml.dump(existing, f, sort_keys=False)

def filter_by_material(pulls, selected_material):
    return [p for p in pulls if selected_material in p.get("materials", [])]

def add_to_cart(pull_id):
    cart = session.get("cart", [])
    if pull_id not in cart:
        cart.append(pull_id)
    session["cart"] = cart

# --- Data Loaders ---

def load_zipper_pulls():
    return load_yaml_scroll("scrolls/zipper_pulls.yaml")

def load_collections():
    return load_yaml_scroll("scrolls/collections.yaml")

def load_footer_items():
    return load_yaml_scroll("scrolls/footer_items.yaml")

# --- Routes ---

@app.route("/collections/<collection_id>")
def collection_view(collection_id):
    selected_material = request.args.get("material")
    all_pulls = load_zipper_pulls()
    all_collections = load_collections()
    collection = next((c for c in all_collections if c["id"] == collection_id), None)
    if not collection:
        abort(404)
    matching_pulls = [p for p in all_pulls if p.get("collection") == collection["label"]]
    if selected_material:
        matching_pulls = filter_by_material(matching_pulls, selected_material)
    if not matching_pulls:
        print(f"No pulls found for collection: {collection_id}")
    return render_template("collection_view.html", collection=collection, pulls=matching_pulls)

@app.route("/carousel")
def carousel():
    zipper_pulls = load_zipper_pulls()
    footer_items = load_footer_items()
    return render_template("carousel.html", zipper_pulls=zipper_pulls, footer_items=footer_items)

@app.route("/store/<pull_id>")
def store_drop(pull_id):
    all_pulls = load_zipper_pulls()
    pull = next((p for p in all_pulls if p["id"] == pull_id), None)
    if not pull:
        abort(404)
    # Related pulls by collection or material
    related_pulls = [
        p for p in all_pulls
        if p["id"] != pull_id and (
            p.get("collection") == pull.get("collection") or
            any(mat in p.get("materials", []) for mat in pull.get("materials", []))
        )
    ][:3]  # Limit to 3
    return render_template("store_drop.html", pull=pull, related_pulls=related_pulls)

@app.route("/cart/add/<pull_id>")
def cart_add(pull_id):
    all_pulls = load_zipper_pulls()
    pull = next((p for p in all_pulls if p["id"] == pull_id), None)
    if not pull:
        abort(404)
    add_to_cart(pull_id)
    return redirect("/cart")

@app.route("/cart")
def cart_view():
    all_pulls = load_zipper_pulls()
    cart_ids = session.get("cart", [])
    cart_items = [p for p in all_pulls if p["id"] in cart_ids]
    return render_template("cart.html", cart_items=cart_items)

@app.route("/cart/remove/<pull_id>")
def cart_remove(pull_id):
    cart = session.get("cart", [])
    if pull_id in cart:
        cart.remove(pull_id)
    session["cart"] = cart
    return redirect("/cart")

@app.route("/custom-order", methods=["GET", "POST"])
def custom_order():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        request_text = request.form.get("request")
        # Send email
        msg = Message("New Custom Pull Request",
                      sender=app.config["MAIL_USERNAME"],
                      recipients=["your@email.com"])
        msg.body = f"From: {name} <{email}>\n\nRequest:\n{request_text}"
        mail.send(msg)
        # Save to YAML scroll
        save_custom_request(name, email, request_text)
        flash("Your request has been received. The glyphs are listening.")
        return redirect("/custom-order")
    return render_template("custom_order.html")