from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory to save uploaded images

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    college_email = db.Column(db.String(100), nullable=False, unique=True)
    personal_email = db.Column(db.String(100))
    phone = db.Column(db.String(15), nullable=False)
    alt_phone = db.Column(db.String(15))
    address = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(100))  # New column for image filename

# Create the database and tables if they don’t exist
with app.app_context():
    db.create_all()

# Page routing 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    # Sample data for the demo purpose
    data = {
        "name": "Alex Johnson",
        "student_id": "STU12345",
        "department": "Bachelor of Engineering in Computer Science",
        "year": 3,
        "dob": "20/11/2001",
        "college_email": "alex.johnson@example.com",
        "phone": "+1 555-123-4567",
        "address": "123 Main St, Apt 4B, Central City, USA",
        "due": 2,  # Add the due books count
        "fine": 15.00  # Add the fine amount
    }
    return render_template('profile.html', data=data)

# Function to get student by ID
def get_student_by_id(student_id):
    return Student.query.filter_by(student_id=student_id).first()

# Registration Route 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name')
        last_name = request.form['last_name']
        gender = request.form['gender']
        student_id = request.form['student_id']
        department = request.form['department']
        year = request.form['year']
        dob = request.form['dob']
        college_email = request.form['college_email']
        personal_email = request.form.get('personal_email')
        phone = request.form['phone']
        alt_phone = request.form.get('alt_phone')
        address = request.form['address']

        # Handle image upload
        filename = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Create a new Student object
        new_student = Student(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            gender=gender,
            student_id=student_id,
            department=department,
            year=int(year),
            dob=dob,
            college_email=college_email,
            personal_email=personal_email,
            phone=phone,
            alt_phone=alt_phone,
            address=address,
            profile_picture=filename  # Save the filename
        )
        
        # Add to database and commit
        db.session.add(new_student)
        db.session.commit()

        # Redirect to the newly created student's profile
        return redirect(url_for('view_student', student_id=new_student.student_id))

    return render_template('student_form.html')

# View Student Profile Route
@app.route('/view_student/<student_id>')
def view_student(student_id):
    student = get_student_by_id(student_id)  # Fetch the student using the helper function
    if student is None:
        return "Student not found", 404  # Return an error if student is not found

    # Set a default picture if none exists
    if student.profile_picture is None:
        student.profile_picture = 'default.jpg'
    return render_template('view.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
