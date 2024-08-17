from flask import Flask, jsonify

app = Flask(__name__)

# List of recycling centers by category
recycling_centers = {
    'small_electronics': ['Center A', 'Center B', 'Center G'],
    'large_appliances': ['Center C', 'Center D', 'Center H'],
    'batteries': ['Center E', 'Center F', 'Center I']
}

@app.route('/centers/<category>', methods=['GET'])
def get_centers(category):
    centers = recycling_centers.get(category, [])
    return jsonify(centers)

if __name__ == "__main__":
    app.run(port=5000)
