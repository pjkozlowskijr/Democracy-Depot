from app import db, login
from flask_login import UserMixin, current_user
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

cart = db.Table("cart",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    cart = db.relationship(
        "Product",
        secondary="cart",
        backref="users",
        lazy="dynamic"
        )
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User: {self.email} | {self.id}"

    def __str__(self):
        return f"<User: {self.email} | {self.first_name} {self.last_name}"

    def hash_pass(self, orig_pass):
        return generate_password_hash(orig_pass)

    def confirm_pass(self, login_pass):
        return check_password_hash(self.password, login_pass)

    def profile_form_to_db(self, data):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = self.hash_pass(data["password"])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_to_cart(self, product):
        self.cart.append(product)
        db.session.commit()

    def remove_from_cart(self, prod_id):
        db.session.query(cart).filter(current_user.id == cart.c.user_id, cart.c.product_id == prod_id).delete()
        db.session.commit()

    def clear_cart(self):
        db.session.query(cart).filter(current_user.id == cart.c.user_id).delete()
        db.session.commit()

    def item_quantity(self, prod_id):
        quantity = self.cart.filter(cart.c.product_id == prod_id).count()
        return quantity

    def total_cost(self):
        costs = []
        for item in self.cart:
            item_cost = self.item_quantity(item.id) * item.price
            costs.append(item_cost)
        return sum(costs)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    img = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    category_id = db.Column(db.ForeignKey("category.id"))

    def __rep__(self):
        return f"<Product: {self.name} | {self.id}"

    def product_to_db(self, prod_dict):
        self.name = prod_dict["name"]
        self.desc = prod_dict["desc"]
        self.price = prod_dict["price"]
        self.img = prod_dict["img"]
        self.category_id = prod_dict["category_id"]
    
    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def rem_product(self, name):
        db.session.query(Product).filter(Product.name == name).delete()
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    products = db.relationship("Product",
        backref="category", 
        lazy="dynamic", 
        cascade="all, delete-orphan"
        )

    def cat_to_db(self, cat_dict):
        self.name = cat_dict["name"]
    
    def save_cat(self):
        db.session.add(self)
        db.session.commit()

    def rem_cat(self, name):
        db.session.query(Category).filter(Category.name == name).delete()
        db.session.commit()