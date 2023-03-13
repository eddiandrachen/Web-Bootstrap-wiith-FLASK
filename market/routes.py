from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, login_required, logout_user, current_user

@app.route("/")
def home_base():
    return render_template('homebase.html')

@app.route('/home')
def home_page():
    return render_template('home45.html')

@app.route('/market', methods=['GET','POST'])
@login_required
#form subbmission supaya ngga terjadi input Get / Post saat melakukan refresh form.
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Pembelian item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You Purchased the item {p_item_object.name} for Rp. {p_item_object.price}", category='success')
            else:
                flash(f"Maaf uang kamu kureng sangat buat beli {p_item_object.name}", category='danger')
        #Sell Item Logic
        sold_item=request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! Anda menjual barang anda {s_item_object.name} untuk Rp. {s_item_object.price}",
                      category='success')
            else:
                flash(f"Sepertinya ada yang salah, coba ulang kembali", category='danger')

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('home.html',items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/base')
def base_page():
    return render_template('base.html')

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Anda login sebagai {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        #jika di sana ngga ada error dari validationnya
        for err_msg in form.errors.values():
            flash(f'error gan maap, akunnya ngga bener: {err_msg}', category='danger')
    return render_template('register.html', form=form)
#    return "<p>Hello, World!!!</p>"
#@app.route("/about/<username>") #Its a dynamic route using de f var to show the username
#def about_page(username):
#    return f"<h1>Page of {username}</h1>"

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Met datang kembali ayang {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Anda yakin mempunyai username dan password di web kami?', category='danger')

    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('Yahh, Anda telah keluar', category='info')
    return redirect(url_for('home_base'))


#buat nyalain web server local host
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6010)