#Importing Required Libraries
from flask import *
import mysql.connector
import cv2
import mediapipe as mp
import numpy as np
import os
import datetime 

app = Flask(__name__)
app.secret_key="vto"

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vto"
)
cursor = db.cursor()

#Home Page
@app.route('/')
def index():
    return render_template('index.html')

#About Page
@app.route('/about')
def about():
    return render_template('about.html')

#Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#Login Session
@app.route('/index')
def home():
    print(session)
    return render_template('index.html')

# Logout 
@app.route('/logout', methods=['GET'])
def logout():
    session['user']=None 
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

#SignUP Page
@app.route('/login2', methods=['POST'])
def login2():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'error': 'Please provide email and password'}), 400

    # Check if email exists in the database
    query = "SELECT * FROM members WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'Invalid email '}), 401

    # Check if the password matches
    if password != user[3]:
        return jsonify({'error': 'Invalid email or password'}), 401

    # User authenticated successfully
    session['email']=user[2]
    session['name']=user[1]
    session['user']=user[1]
    session['uid']=user[0]
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    cursor.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if not name or not email or not password:
        return "error"
    print(name, email, password)
    # Insert data into the database
    query = "INSERT INTO members (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)
    cursor.execute(query, values)
    db.commit()
    session['msg']='registersuccess'
    return render_template('login.html')


#Boy shop
@app.route('/shop')
def shop():
    query = "SELECT * FROM products WHERE id in (1,2,7,8)"
    cursor.execute(query, ())
    products = cursor.fetchall()
    print(products)
    return render_template('shop.html', products=products)


@app.route('/sproduct')
def sproduct():
    return render_template('sproduct.html')

@app.route('/sproductv2')
def sproductv2():
    query = "SELECT * FROM products WHERE id = %s"
    id=request.args.get('id')
    cursor.execute(query, (id,))
    product = cursor.fetchone()
    session['id']=id 
    session['clothpic']=product[2]
    print(product)

    return render_template('sproductv2.html', product=product )

@app.route('/shop2')
def shop2():
    query = "SELECT * FROM products WHERE id in (3,4,5,6)"
    #id=request.args.get('id')
    cursor.execute(query, ())
    products = cursor.fetchall()
    print(products)
    return render_template('shop2.html', products=products)

@app.route('/shop3')
def shop3():
    query = "SELECT * FROM products WHERE id in (9,10,11,12)"
    #id=request.args.get('id')
    cursor.execute(query, ())
    products = cursor.fetchall()
    print(products)
    return render_template('shop3.html', products=products )

@app.route('/shop4')
def shop4():
    query = "SELECT * FROM products WHERE id in (13,14,15,16)"
    #id=request.args.get('id')
    cursor.execute(query, ())
    products = cursor.fetchall()
    print(products)
    return render_template('shop4.html', products=products)

#Cart Management

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method=='POST':
        query = "INSERT INTO cart (mid, pid, qty, cdate) VALUES (%s, %s, %s, %s)"
        values = (session['uid'], session['id'], request.form['qty'], datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') )
        cursor.execute(query, values)
        db.commit()

        cartitems = getcartitems()
        print('cartitems p' , cartitems)
        return render_template('cart.html', cartitems=cartitems)
    else:
        cartitems = getcartitems() 
        print('cartitems g' , cartitems)
        return render_template('cart.html', cartitems=cartitems)

def getcartitems():
        query = "SELECT * FROM cart join members on members.id=cart.mid join products on products.id=cart.pid where cart.mid="+str(session['uid'])
        #id=request.args.get('id')
        print('query', query)
        cursor.execute(query, ())
        cartitems = cursor.fetchall()
        print('cartitems -get cart items ', cartitems)
        return cartitems 

#Rendering Cloths for Try On
@app.route('/tryon', methods=['GET' , 'POST'])
def tryon():
    person_filename=''

    shirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']
    
    if request.method=='POST':
        
        person = request.files['file'] 
        # Save the uploaded files to the UPLOAD_FOLDER directory
        person_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads",person.filename)
        print(person_filename)
        person.save(person_filename)

        result_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", "_"+person.filename)
        print(result_filename)
        person.save(result_filename)

        # Initialize MediaPipe Pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

        # Read image
        image = cv2.imread(person_filename)

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]] for lm in landmarks])

            # Get shoulder points
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            # Calculate chest position
            chest_position = (left_shoulder + right_shoulder) / 2

            # Calculate chest width
            chest_width = np.linalg.norm(left_shoulder - right_shoulder)

            # Calculate chest height (example: distance between chest position and neck)
            neck_position = landmark_positions[mp_pose.PoseLandmark.NOSE.value]
            # np.linalg.norm(chest_position - neck_position)

            print("Chest Position:", chest_position)
            print("Chest Width:", chest_width)
            print("left_shoulder:", left_shoulder)
            print("right_shoulder:", right_shoulder)

            # Get waist points
            left_hip = landmark_positions[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmark_positions[mp_pose.PoseLandmark.RIGHT_HIP.value]

            # Calculate waist width
            waist_width = np.linalg.norm(left_hip - right_hip)


            print("Waist Width:", waist_width)
            print("left_hip:", left_hip)
            print("right_hip:", right_hip)

        chest_height = right_hip[1] - right_shoulder[1]

        shirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']

        # Load person's imagee
        person_image = cv2.imread(person_filename)

        # Load shirt image with transparent background
        print("shirtfile", shirtfile)

        shirt_image = cv2.imread(shirtfile, cv2.IMREAD_UNCHANGED)
        print('shirt_image', shirt_image)

        aspect_ratio = shirt_image.shape[1]/shirt_image.shape[0]
        # Convert the image to RGB
        person_image_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(person_image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * person_image.shape[1], lm.y * person_image.shape[0]] for lm in landmarks])

            # Get bounding box around shoulders and chest region
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            top_chest = min(left_shoulder[1], right_shoulder[1])
            bottom_chest = max(left_hip[1], right_hip[1])

            # Resize shirt image to fit bounding box
            shirt_width = left_shoulder[0] - right_shoulder[0]
            shirt_height = bottom_chest - top_chest
            print('---',shirt_width, shirt_height)
            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))
            
            # Calculate position for shirt overlay
            y_offset = int(top_chest)
            x_offset = int(right_shoulder[0])

            shirt_width = int(shirt_width*2.5)
            shirt_height = int(shirt_width/aspect_ratio)
            # Choose the position where you want to place the resized image on the second image
            x_offset = int(x_offset*.35)  # specify the x-coordinate
            y_offset = int(y_offset*0.65)   # specify the y-coordinate
            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))

            # Overlay shirt image onto person's image
            for c in range(0, 3):
                person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] = (
                    resized_shirt[:, :, c] * (resized_shirt[:, :, 3] / 255.0) +
                    person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] *
                    (1.0 - resized_shirt[:, :, 3] / 255.0)
                )
        # Display the resulting image
        # cv2.imshow("Result",person_image)
        cv2.imwrite(result_filename, person_image)

        return render_template('tryon2.html', resultpic=result_filename[63:],personpic=person_filename[63:] )
        
        pass 

    clothtype='tryon'
    if('g_pant' in session['clothpic']):
        clothtype='pant_tryon2'
    elif('g_shirt' in session['clothpic']):
        clothtype = 'shirt_tryon'
    elif('_pant' in session['clothpic']):
        clothtype = 'tryon2'

    return render_template('tryon.html', clothtype=clothtype )

@app.route('/tryon2', methods=['GET' , 'POST'])
def tryon2():
    person_filename=''
    if request.method=='POST':
        
        person = request.files['file'] 
        # Save the uploaded files to the UPLOAD_FOLDER directory
        person_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", person.filename)
        print(person_filename)
        # person_resized = cv2.resize(person,)
        person.save(person_filename)

        result_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", "_"+person.filename)
        print(result_filename)
        person.save(result_filename)

        # Initialize MediaPipe Pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

        # Read image
        image = cv2.imread(person_filename)

        # Resize Image
        image_resize = cv2.resize(image,(427,646))
        
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]] for lm in landmarks])

            # Get shoulder points
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            # Calculate chest position
            chest_position = (left_shoulder + right_shoulder) / 2

            # Calculate chest width
            chest_width = np.linalg.norm(left_shoulder - right_shoulder)

            # Calculate chest height (example: distance between chest position and neck)
            neck_position = landmark_positions[mp_pose.PoseLandmark.NOSE.value]
            # np.linalg.norm(chest_position - neck_position)

            print("Chest Position:", chest_position)
            print("Chest Width:", chest_width)
            print("left_shoulder:", left_shoulder)
            print("right_shoulder:", right_shoulder)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]] for lm in landmarks])

            # Get waist points
            left_hip = landmark_positions[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmark_positions[mp_pose.PoseLandmark.RIGHT_HIP.value]

            # Calculate waist width
            waist_width = np.linalg.norm(left_hip - right_hip)

            # Get leg heights (example: distance between hip and ankle)
            left_ankle = landmark_positions[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = landmark_positions[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            left_leg_height = np.linalg.norm(left_hip - left_ankle)
            right_leg_height = np.linalg.norm(right_hip - right_ankle)

            print("Waist Width:", waist_width)
            print("Left Leg Height:", left_leg_height)
            print("Right Leg Height:", right_leg_height)
            print("left_hip:", left_hip)
            print("right_hip:", right_hip)

        chest_height = right_hip[1] - right_shoulder[1]
        
        shirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']

        # Load person's imagee
        person_image = cv2.imread(person_filename)

        # Load shirt image with transparent background
        print("shirtfile", shirtfile)

        shirt_image = cv2.imread(shirtfile, cv2.IMREAD_UNCHANGED)
        aspect_ratio = shirt_image.shape[1]/shirt_image.shape[0]
        shirt_image = cv2.resize(shirt_image,(500,500))
        print('shirt_image', shirt_image)
        # Convert the image to RGB
        person_image_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(person_image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * person_image.shape[1], lm.y * person_image.shape[0]] for lm in landmarks])

            # Get bounding box around shoulders and chest region
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            top_chest = min(left_shoulder[1], right_shoulder[1])
            bottom_chest = max(left_hip[1], right_hip[1])

            # Resize shirt image to fit bounding box
            shirt_width = waist_width # left_shoulder[0] - right_shoulder[0]
            shirt_height = right_leg_height # bottom_chest - top_chest
            print('---',shirt_width, shirt_height)
            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))
            
            # Calculate position for shirt overlay
            y_offset = int(right_hip[1])
            x_offset = int(right_hip[0])

            
            shirt_width = int(shirt_width*5.2)
            shirt_height = int(shirt_height*1.3)
            # # Choose the position where you want to place the resized image on the second image
            x_offset = int(x_offset*.12)  # specify the x-coordinate
            y_offset = int(y_offset*0.85)   # specify the y-coordinate

            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))

            print('values ', x_offset, y_offset, shirt_width, shirt_height)

            # Overlay shirt image onto person's image
            for c in range(0, 3):
                person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] = (
                    resized_shirt[:, :, c] * (resized_shirt[:, :, 3] / 255.0) +
                    person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] *
                    (1.0 - resized_shirt[:, :, 3] / 255.0)
                )
        # Display the resulting image
        # cv2.imshow("Result",person_image)
        cv2.imwrite(result_filename, person_image)

        return render_template('tryon2.html', resultpic=result_filename[63:],personpic=person_filename[63:] )
        
        pass 
    return render_template('tryon.html')

@app.route('/shirt_tryon',methods = ['GET','POST'])
def shirt_tryon():
    person_filename=''
    
    shirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']
    
    if request.method=='POST':
        
        person = request.files['file'] 
        # Save the uploaded files to the UPLOAD_FOLDER directory
        person_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads",person.filename)
        print(person_filename)
        person.save(person_filename)

        result_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", "_"+person.filename)
        print(result_filename)
        person.save(result_filename)

        # Initialize MediaPipe Pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

        # Read image
        image = cv2.imread(person_filename)

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(image_rgb)

        # Extract pose landmarks

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]] for lm in landmarks])

            # Get shoulder points
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            # Calculate chest position
            chest_position = (left_shoulder + right_shoulder) / 2

            # Calculate chest width
            chest_width = np.linalg.norm(left_shoulder - right_shoulder)

            # Calculate chest height (example: distance between chest position and neck)
            neck_position = landmark_positions[mp_pose.PoseLandmark.NOSE.value]
            # np.linalg.norm(chest_position - neck_position)

            # Get waist points
            left_hip = landmark_positions[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmark_positions[mp_pose.PoseLandmark.RIGHT_HIP.value]

            # Calculate waist width
            waist_width = np.linalg.norm(left_hip - right_hip)
            print("Chest Position:", chest_position)
            print("Chest Width:", chest_width)
            print("left_shoulder:", left_shoulder)
            print("right_shoulder:", right_shoulder)
            print("Waist Width:", waist_width)
            print("left_hip:", left_hip)
            print("right_hip:", right_hip)

        chest_height = right_hip[1] - right_shoulder[1]

        shirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']

        # Load person's imagee
        person_image = cv2.imread(person_filename)

        # Load shirt image with transparent background
        print("shirtfile", shirtfile)

        shirt_image = cv2.imread(shirtfile, cv2.IMREAD_UNCHANGED)
        print('shirt_image', shirt_image)

        aspect_ratio = shirt_image.shape[1]/shirt_image.shape[0]
        # Convert the image to RGB
        person_image_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(person_image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * person_image.shape[1], lm.y * person_image.shape[0]] for lm in landmarks])

            # Get bounding box around shoulders and chest region
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            top_chest = min(left_shoulder[1], right_shoulder[1])
            bottom_chest = max(left_hip[1], right_hip[1])

            # Resize shirt image to fit bounding box
            shirt_width = left_shoulder[0] - right_shoulder[0]
            shirt_height = bottom_chest - top_chest
            print('---',shirt_width, shirt_height)
            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))
            
            # Calculate position for shirt overlay
            y_offset = int(top_chest)
            x_offset = int(right_shoulder[0])

            shirt_width = int(shirt_width*3.1)
            shirt_height = int(shirt_height*3.2)
            # Choose the position where you want to place the resized image on the second image
            x_offset = int(x_offset*0.4)  # specify the x-coordinate
            y_offset = int(y_offset*0.85)   # specify the y-coordinate

            resized_shirt = cv2.resize(shirt_image, (int(shirt_width), int(shirt_height)))


            # Overlay shirt image onto person's image
            for c in range(0, 3):
                person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] = (
                    resized_shirt[:, :, c] * (resized_shirt[:, :, 3] / 255.0) +
                    person_image[y_offset:y_offset + resized_shirt.shape[0], x_offset:x_offset + resized_shirt.shape[1], c] *
                    (1.0 - resized_shirt[:, :, 3] / 255.0)
                )

        cv2.imwrite(result_filename, person_image)

        return render_template('tryon2.html', resultpic=result_filename[63:],personpic=person_filename[63:] )
        
        pass 
    return render_template('tryon.html')

@app.route('/pant_tryon2',methods = ['GET','POST'])
def pant_tryon2():
    person_filename = ''

    shhtcoeff=1.1
    shwdcoeff=5.2
    xoffcoeff=.4
    yoffcoeff=.7 

    if request.method=='POST':
        
        person = request.files['file'] 
        # Save the uploaded files to the UPLOAD_FOLDER directory
        person_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", person.filename)
        print(person_filename)
        # person_resized = cv2.resize(person,)
        person.save(person_filename)

        result_filename = os.path.join(r"C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\uploads", "_"+person.filename)
        print(result_filename)
        person.save(result_filename)

        # Initialize MediaPipe Pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

        # Read image
        image = cv2.imread(person_filename)

        # Resize Image
        image_resize = cv2.resize(image,(427,646))
        
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(image_rgb)

        

        # Draw pose landmarks on the image
        if results.pose_landmarks:
            mp_drawing = mp.solutions.drawing_utils
            annotated_image = image.copy()
            mp_drawing.draw_landmarks(
                annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * image.shape[1], lm.y * image.shape[0]] for lm in landmarks])

            # Get waist points
            left_hip = landmark_positions[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmark_positions[mp_pose.PoseLandmark.RIGHT_HIP.value]

            # Calculate waist width
            waist_width = np.linalg.norm(left_hip - right_hip)

            # Get leg heights (example: distance between hip and ankle)
            left_ankle = landmark_positions[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = landmark_positions[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            left_leg_height = np.linalg.norm(left_hip - left_ankle)
            right_leg_height = np.linalg.norm(right_hip - right_ankle)

            print("Waist Width:", waist_width)
            print("Left Leg Height:", left_leg_height)
            print("Right Leg Height:", right_leg_height)
            print("left_hip:", left_hip)
            print("right_hip:", right_hip)

        mp_drawing = mp.solutions.drawing_utils
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(
            annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # cv2.imshow( annotated_image)
        skirtfile=r'C:\Users\PURUSHOTHAM REDDY\OneDrive\Desktop\Major Project\vtrv2\static\images\product'+'\\'+session['clothpic']

        # Load person's imagee
        person_image = cv2.imread(person_filename)

        # Load skirt image with transparent background
        print("skirtfile", skirtfile)

        skirt_image = cv2.imread(skirtfile, cv2.IMREAD_UNCHANGED)

        aspect_ratio = skirt_image.shape[1]/skirt_image.shape[0]
        # skirt_image = cv2.resize(skirt_img,(736,736))
        print('skirt_image', skirt_image)
        # Convert the image to RGB
        person_image_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)

        # Perform pose estimation
        results = pose.process(person_image_rgb)

        # Extract pose landmarks
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get landmark positions
            landmark_positions = np.array([[lm.x * person_image.shape[1], lm.y * person_image.shape[0]] for lm in landmarks])

            # Get bounding box around shoulders and chest region
            left_shoulder = landmark_positions[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmark_positions[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            top_chest = min(left_shoulder[1], right_shoulder[1])
            bottom_chest = max(left_hip[1], right_hip[1])

            skirt_width = waist_width # left_shoulder[0] - right_shoulder[0]
            skirt_height = right_leg_height # bottom_chest - top_chest
            print('---',skirt_width, skirt_height)
            #resized_skirt = cv2.resize(skirt_image, (int(skirt_width), int(skirt_height)))
    
            # Calculate position for skirt overlay
            y_offset = int(right_hip[1])
            x_offset = int(right_hip[0])

            # skirt_height = int(skirt_height*shhtcoeff)
            skirt_width = int(skirt_width*4.5)
            skirt_height = int(skirt_width/aspect_ratio)


            # # # Choose the position where you want to place the resized image on the second image
            # print('---', x_offset, waist_width*shwdcoeff)

            x_offset = int(x_offset-skirt_width*xoffcoeff) # -waist_width*xoffcoeff)  # specify the x-coordinate
            y_offset = int(y_offset*0.75)   # specify the y-coordinate

            resized_skirt = cv2.resize(skirt_image, (int(skirt_width), int(skirt_height)))

            print('values ', x_offset, y_offset, skirt_width, skirt_height)

            # Overlay skirt image onto person's image
            for c in range(0, 3):
                person_image[y_offset:y_offset + resized_skirt.shape[0], x_offset:x_offset + resized_skirt.shape[1], c] = (
                    resized_skirt[:, :, c] * (resized_skirt[:, :, 3] / 255.0) +
                    person_image[y_offset:y_offset + resized_skirt.shape[0], x_offset:x_offset + resized_skirt.shape[1], c] *
                (1.0 - resized_skirt[:, :, 3] / 255.0)
                    )

        cv2.imwrite(result_filename, person_image)

        return render_template('tryon2.html', resultpic=result_filename[63:],personpic=person_filename[63:] )
        
        pass 
    return render_template('tryon.html')





UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(debug=True)