from flask import Flask, render_template,url_for
app =Flask(__name__)

data ={
    "name": "Alex Johnson",
    "student_id": "STU12345",
    "department": "Bachelor of Engineering in Computer Science",
    "year": 3,
    "total_books_read": 45,
    "due": 4,
    "fine": 45.3434, 
    "dob": "20/11/2001",
    "email": "alex.johnson@example.com",
    "ph1": "+1 555-123-4567",
    "ph2": "+1 555-123-4567",
    "address": "123 Main St, Apt 4B, Central City, USA"
}


@app.route('/')
def index ():
    return render_template('index.html')

@app.route('/')
@app.route('/profile')
def profile():
    return render_template('profile.html',data = data)     
    
if __name__=="__main__":
    app.run(debug=True)