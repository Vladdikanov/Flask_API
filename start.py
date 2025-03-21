from app import app, db
import os
print(os.path.dirname(__name__))

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)