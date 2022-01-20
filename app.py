from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


# Database model
class Inventory(db.Model):
    item_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(200),nullable=False)
    item_description = db.Column(db.String(200), nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False)


    
# Display list of items
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        item_name = request.form["item_name"]
        item_description = request.form["item_description"]
        item_quantity = int(request.form["item_quantity"])
        # Ensure quantity is not less than zero
        if item_quantity > 0:
            inventory = Inventory(item_name=item_name,item_description=item_description,item_quantity=item_quantity)
            db.session.add(inventory)
            db.session.commit()
        else:
            return render_template("error.html")
    # Fetch all items in database
    all_inventory = Inventory.query.all()
    return render_template("index.html", inventory=all_inventory)
 

# Create item
@app.route("/create")
def create():
    return render_template("create.html")

# Delete an item
@app.route("/delete/<int:item_id>")
def delete(item_id):
    # Select item to delete
    delete_item = Inventory.query.filter_by(item_id=item_id).first()
    # Delete from DB
    db.session.delete(delete_item)
    db.session.commit()
    return redirect("/")

# Update an item
@app.route("/update/<int:item_id>", methods=["GET","POST"])
def update(item_id):
    if request.method == 'POST':
        update_item = Inventory.query.filter_by(item_id=item_id).first()
        item_name = request.form["item_name"]
        item_description = request.form["item_description"]
        item_quantity = int(request.form["item_quantity"])
        inventory = Inventory(item_name=item_name,item_description=item_description,item_quantity=item_quantity)
        # Update items
        update_item.item_name = item_name
        update_item.item_description = item_description
        update_item.item_quantity = item_quantity
        db.session.commit()
        return redirect("/")
    update_item = Inventory.query.filter_by(item_id=item_id).first()
    return render_template('update.html',update_item=update_item)


# Export product data to CSV
@app.route("/export")
def export():
    all_inventory = Inventory.query.all()
    # Open csv file to write
    with open('prodcut.csv', 'w') as f:
        writer = csv.writer(f)
        # Write each row from resultset to csv file
        for row in all_inventory:
            writer.writerow([row.item_name,row.item_description,row.item_quantity]) 
    return render_template("success.html")