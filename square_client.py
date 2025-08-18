from square.client import Client

def get_square_client():
    return Client(
        access_token="YOUR_SQUARE_ACCESS_TOKEN",
        environment="sandbox"  # or "production"
    )

def get_items_by_category(category_id):
    client = get_square_client()
    response = client.catalog.search_catalog_objects(
        body={
            "object_types": ["ITEM"],
            "query": {
                "exact_query": {
                    "attribute_name": "category_id",
                    "attribute_value": category_id
                }
            }
        }
    )
    if response.is_success():
        return response.body.get("objects", [])
    else:
        print("Error:", response.errors)
        return []


@app.route("/collections")
def collections_grid():
    all_collections = load_collections()
    for col in all_collections:
        col["inventory_items"] = get_items_by_category(col["category_id"])
    return render_template("collections_grid.html", collections=all_collections)
