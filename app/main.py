# Entry point for the application
from flask import Flask, jsonify, render_template
from app.routes.upload_routes import upload_bp
#from app.routes.analytics_routes import analytics_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(upload_bp, url_prefix="/upload")
    #app.register_blueprint(analytics_bp, url_prefix="/analytics")
    @app.route("/")  # Default route
    def home():
        return render_template("index.html")

    return app
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
