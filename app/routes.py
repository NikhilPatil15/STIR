from flask import Blueprint, jsonify, render_template
import subprocess

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return render_template("index.html")

@routes.route('/scrape_twitter', methods=['GET'])
def scrape_twitter():
    """Route to handle scraping and return the data."""
    try:
        
        result = subprocess.run(
            ['python', 'app/selenium_script.py'],
            capture_output=True,
            text=True,
            
        )
        
        print(result.stdout)


        return jsonify(result.stdout), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

