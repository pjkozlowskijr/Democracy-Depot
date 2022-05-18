from flask import render_template, request, flash, redirect, url_for, g
# from helpers import require_admin
from .forms import RegisterForm, LoginForm, ProductForm, CategoryForm, EditProfileForm, RemCategoryForm, RemProductForm
from ...models import User, Product, Category
from flask_login import login_required, login_user, current_user, logout_user
from .import bp as auth

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
            }
            new_user_object = User()
            new_user_object.profile_form_to_db(new_user_data)
            new_user_object.save()
        except:
            flash("There was an unexpected error creating your account. Please try again.", "danger")
            return render_template("register.html.j2", form=form)
        flash("Your account was created successfully.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html.j2", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            email = form.email.data.lower()
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user and user.confirm_pass(password):
                login_user(user)
                flash("Login successful.", "success")
                return redirect(url_for("main.index"))
            flash("Incorrect email or password.", "danger")
            return render_template("login.html.j2", form=form)
        except:
            flash("There was an unexpected error. Please try again.", "danger")
            return render_template("login.html.j2", form=form)
    return render_template("login.html.j2", form=form)

@auth.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data,
        }
        user = User.query.filter_by(email=new_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash("Email is already in use.", "danger")
            return redirect(url_for("auth.edit_profile"))
        try:
            current_user.profile_form_to_db(new_user_data)
            current_user.save()
        except:
            flash("There was an unexpected error. Please try again.", "danger")
            return render_template("edit_profile.html.j2", form=form)
        flash("Your profile was updated successfully.", "success")    
        return redirect(url_for("main.index"))
    return render_template("edit_profile.html.j2", form=form)

@auth.route("/logout")
@login_required
def logout():
    if current_user:
        logout_user()
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("auth.login"))

@auth.route("/admin_tools")
@login_required
def admin_tools():
    return render_template("admin_tools.html.j2")

@auth.route("/add_category", methods=["GET", "POST"])
@login_required
def add_category():
    cat_form = CategoryForm()
    if request.method == "POST" and cat_form.validate_on_submit():
        try:
            new_cat_data = {
                "name": cat_form.name.data.lower(),
            }
            new_cat_object = Category()
            new_cat_object.cat_to_db(new_cat_data)
            new_cat_object.save_cat()
        except:
            flash("There was an unexpected error creating the category. Please try again.", "danger")
            return render_template("add_category.html.j2", cat_form=cat_form)
        flash("Category created successfully.", "success")
        return redirect(url_for("auth.admin_tools"))
    return render_template("add_category.html.j2", cat_form=cat_form)

@auth.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    prod_form = ProductForm()
    if request.method == "POST" and prod_form.validate_on_submit():
        try:
            new_prod_data = {
                "name": prod_form.name.data.lower(),
                "desc": prod_form.desc.data,
                "price": prod_form.price.data,
                "img": prod_form.img.data,
                "category_id": prod_form.category_id.data
            }
            new_prod_object = Product()
            new_prod_object.product_to_db(new_prod_data)
            new_prod_object.save_product()
        except:
            flash("There was an unexpected error adding the project. Please try again.", "danger")
            return render_template("add_product.html.j2", prod_form=prod_form)
        flash("Product added successfully.", "success")
        return redirect(url_for("auth.admin_tools"))
    return render_template("add_product.html.j2", prod_form=prod_form)

@auth.route("/remove_category", methods=["GET", "POST"])
@login_required
def remove_category():
    rem_cat_form = RemCategoryForm()
    if request.method == "POST" and rem_cat_form.validate_on_submit():
        try:
            cat_to_remove = rem_cat_form.name.data.lower()
            Category().rem_cat(cat_to_remove)
        except:
            flash("There was an unexpected error removing the category. Please try again.", "danger")
            return render_template("remove_category.html.j2", rem_cat_form=rem_cat_form)
        flash("Category has been removed.", "success")
        return redirect(url_for("auth.admin_tools"))
    return render_template("remove_category.html.j2", rem_cat_form=rem_cat_form)

@auth.route("/remove_product", methods=["GET", "POST"])
@login_required
def remove_product():
    rem_prod_form = RemProductForm()
    if request.method == "POST" and rem_prod_form.validate_on_submit():
        try:
            prod_to_remove = rem_prod_form.name.data.lower()
            Product().rem_product(prod_to_remove)
        except:
            flash("There was an unexpected error removing the product. Please try again.", "danger")
            return render_template("remove_product.html.j2", rem_prod_form=rem_prod_form)
        flash("Product has been removed.", "success")
        return redirect(url_for("auth.admin_tools"))
    return render_template("remove_product.html.j2", rem_prod_form=rem_prod_form) 