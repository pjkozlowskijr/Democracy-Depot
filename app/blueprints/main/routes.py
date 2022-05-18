from flask import redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .import bp as main
from ...models import Product
from .forms import FilterSortForm

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")

@main.route("/view_all_products", methods=["GET", "POST"])
def view_all_products():
    form = FilterSortForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            filter_choice = form.category.data
            sort_choice = form.sort.data
            if filter_choice == "goods":
                filter = 2
            elif filter_choice == "services":
                filter = 3
            products = Product.query.filter_by(category_id=filter)
            if sort_choice:
                if sort_choice == "asc_name":
                    sort = Product.name
                elif sort_choice == "desc_name":
                    sort = Product.name.desc()
                elif sort_choice == "asc_price":
                    sort = Product.price
                elif sort_choice == "desc_price":
                    sort = Product.price.desc()
            else:
                sort = Product.name
            if sort:
                products = products.order_by(sort).all()
            else:
                products = products.all()
            return render_template("view_all_products.html.j2", products=products, form=form)
        except:
            flash("There was an unexpected error in sort/filter. Please try again.", "danger")
            return redirect(url_for("main.view_all_products"))
    products = Product.query.order_by(Product.name).all()
    return render_template("view_all_products.html.j2", products=products, form=form)

# @main.route("/filter_category/<int:cat_id>")
# def filter_category(cat_id):
#     products = Product.query.filter_by(category_id=cat_id).order_by(Product.name).all()
#     return render_template("view_all_products.html.j2", products=products)

# @main.route("/sort_by/<string:method>")
# def sort_by(method):
#     products = Product.query.order_by(method).all()
#     return render_template("view_all_products.html.j2", products=products, Product=Product())

@main.route("/view_product/<int:id>")
def view_product(id):
    product = Product().query.get(id)
    return render_template("view_product.html.j2", product=product)

@main.route("/add_to_cart/<int:id>")
@login_required
def add_to_cart(id):
    try:
        product = Product().query.get(id)
        current_user.add_to_cart(product)
        flash(f"You added {product.name} to your cart.", "success")
        return redirect(url_for("main.view_cart"))
    except:
        flash("There was an unexpected error. Please try again.", "danger")
        return redirect(url_for("main.view_product", name=product.name))

@main.route("/view_cart")
@login_required
def view_cart():
    cart = current_user.cart
    total = current_user.total_cost()
    return render_template("view_cart.html.j2", cart=cart, total=total)

@main.route("/remove_from_cart/<int:id>")
@login_required
def remove_from_cart(id):
    try:
        product = Product.query.get(id)
        current_user.remove_from_cart(id)
        flash(f"You removed {product.name} from your cart.", "success")
        return redirect(url_for("main.view_cart", id=current_user.id))
    except:
        flash("There was an unexpected error. Please try again.", "danger")
        return redirect(url_for("main.view_cart", id=current_user.id))

@main.route("/clear_cart")
@login_required
def clear_cart():
    current_user.clear_cart()
    flash("Your cart is now empty.", "success")
    return redirect(url_for("main.index"))
