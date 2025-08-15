# Python file script
@app.route('/carousel')
def carousel():
    return render_template('carousel.html')

# Add images in this fashion
zipper_pulls = [
    {
        "image_filename": "glacier-glow.png",
        "caption": "Glacier Glow",
        "glyph_class": "fog-shimmer"
    },
    {
        "image_filename": "tundra-twist.png",
        "caption": "Tundra Twist",
        "glyph_class": "glyph-overlay"
    },
    # Add more pulls here
]
