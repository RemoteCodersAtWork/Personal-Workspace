from app import app

if __name__ == "__main__" :
    app.secret_key = "secretkey"
    from app import db
    db.create_all()
    app.run(debug = True)