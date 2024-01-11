from sys import path
from unittest.mock import patch
from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from model.user import LoginReq, RegisterReq
from services.andrzej import getPolandFromDataSet, getPolishShareInTheWorldMarket, RegionGdpPerYear
from services.michal import allTimeHigh, allTimeLow, halvings, first_halving, second_halving, miniAllTimeHigh, miniAllTimeLow, miniHalvings, mini_first_halving
from services.adrian import plotHistoricalPrices, plotLowestPriceSince2000, plotBestTimeToTrade2000_2015, plotTrendSince2005


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "RANDOM_STRING"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False, unique = True)
    password = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.id
    
def createDatabase():
    db.create_all()
    print("Database was created")

@login_manager.user_loader
def loud_user(id):
    return db.session.get(User, int(id))

@app.route("/", methods=["GET", "POST"])
def login():    
    if request.method == "POST":
        loginReq = LoginReq
        for field in  ['login', 'password']:
            setattr(loginReq, field, request.form.get(field))
            
        for field in [x for x in vars(loginReq) if not x.startswith("__")]:
            if getattr(loginReq, field) == "":
                flash(f"Pole: {field} nie może być puste", category='error')
                return render_template("index.html", base_url=base_url)
        
        user = User.query.filter_by(login=loginReq.login).first()
        if user:
            if check_password_hash(user.password,loginReq.password):
                login_user(user, remember=True)
                return redirect(url_for("main"))
            else:
                flash("Login lub hasło są nieprawidłowe.", category="error")
        else:
            flash("Login lub hasło są nieprawidłowe.", category="error")
            
    return render_template("index.html", base_url=base_url)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Wylogowano pomyślnie!", category="success")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        registerReq = RegisterReq
        for field in  ['login', 'password', 'rePassword']:
            setattr(registerReq, field, request.form.get(field))
        
        for field in [x for x in vars(registerReq) if not x.startswith("__")]:
            if getattr(registerReq, field) == "":
                flash(f"Pole: {field} nie może być puste", category='error')
                return render_template("register.html", base_url=base_url)
            
        user = User.query.filter_by(login=registerReq.login).first()
        if user:
            flash(f"Login jest zajęty.", category='error')
            return render_template("register.html", base_url=base_url)
            
        if registerReq.password != registerReq.rePassword:            
            flash("Nieprawidłowe Hasło.", category='error')
            return render_template("register.html", base_url=base_url)
            
        user = User()
        user.login = registerReq.login
        user.password = generate_password_hash(registerReq.password)
        db.session.add(user)
        db.session.commit()
                    
        flash("Stworzono użytkownika!", category='success')
        return redirect(url_for("login"))
        
    return render_template("register.html", base_url=base_url)

@app.route("/main")
@login_required
def main():
    page = request.args.get('page')
    match page:
        case 'andrzej':
            return render_template(
                "andrzej.html",
                base_url = base_url,
                polandGdp = getPolandFromDataSet(),
                polandShare1990 = getPolishShareInTheWorldMarket(1990),
                polandShare2020 = getPolishShareInTheWorldMarket(2020),
                region1990 = RegionGdpPerYear(1990),
                region2020 = RegionGdpPerYear(2020)
                )
        case 'michal':
            return render_template(
                "michal.html",
                base_url = base_url,
                # Zmienne z mojego pliku michl.py
                ath = allTimeHigh(),
                atl = allTimeLow(),
                halvings = halvings(),
                first_halving = first_halving(),
                second_halving = second_halving(),
                miniath = miniAllTimeHigh(),
                miniatl = miniAllTimeLow(),
                minihalvings = miniHalvings(),
                minifirst_halving = mini_first_halving(),
                )
        case 'adrian':
            return render_template(
                "adrian.html",
                base_url = base_url,
                php = plotHistoricalPrices(), 
                plps2000 = plotLowestPriceSince2000(),
                pbttt = plotBestTimeToTrade2000_2015(),
                pts2005 = plotTrendSince2005(),
                # NAZWAZMIENNEJ = importFunkcji(),
                )
        case _:
            return render_template("main-page.html", base_url=base_url)


if __name__ == "__main__":
    createDatabase()
    debug = True
    if debug:
        base_url = "http://127.0.0.1:5000"
        app.run(debug=True)
       
