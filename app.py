from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # add
from datetime import datetime  # add

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # add
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # add


# add
class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name

# From CRUD, this func covers CR - create, read
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        # form name will be created later.
        # User input from the form
        name=request.form['name']
        new_stuff = Grocery(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new staff."
    # if method is not POST, running GET
    else:
        groceries=Grocery.query.order_by(Grocery.created_at).all()
        return render_template('index.html', groceries=groceries)

# From CRUD, this func covers D - delete
@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."

# From CRUD, this func covers U - update/edit
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Date"
        return render_template('update.html', title=title, grocery=grocery)

if __name__=='__main__':
    app.run(debug=True)