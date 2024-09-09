from flask import request
import shutil
import os
from werkzeug.utils import secure_filename
from models import db, Contact, Image, File, Video, Page

def handle_form_data(form):

    # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
    print(request.form)
    print(request.values)
    print(request.args)
    print(request.get_data())
    # file_path0 = os.environ['UPLOAD_DIRECTORY']
    # print(file_path0)
   
    file = request.form.get('file')
    filename = request.form.get('filename')
    
    if file and filename:
        filename = secure_filename(filename)
   
        with open(filename, 'w') as f:
            f.write(file)
        f.close()
	
        # Create a new Upload record
        upload = Upload(filename=filename, path=file_path, file_type=file_type)
        db.session.add(upload)
        db.session.commit()
        
        file_path0 = file_path0 + '/%s' % filename
        file_path = os.getcwd()
        file_path = file_path + '/%s' % filename
        shutil.copy(file_path, file_path0)
        shutil.move(file_path, file_path0)


def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    import random
    import string

    db.drop_all()
    db.create_all()

    # Create sample contacts
    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]
    locations = [
        ("Shanghai", "China"),
        ("Istanbul", "Turkey"),
        ("Karachi", "Pakistan"),
        ("Mumbai", "India"),
        ("Moscow", "Russia"),
        ("Sao Paulo", "Brazil"),
        ("Beijing", "China"),
        ("Tianjin", "China"),
        ("Guangzhou", "China"),
        ("Delhi", "India"),
        ("Seoul", "South Korea"),
        ("Shenzhen", "China"),
        ("Jakarta", "Indonesia"),
        ("Tokyo", "Japan"),
        ("Mexico City", "Mexico"),
        ("Kinshasa", "Democratic Republic of the Congo"),
        ("Bangalore", "India"),
        ("New York City", "United States"),
        ("London", "United Kingdom"),
        ("Bangkok", "Thailand"),
        ("Tehran", "Iran"),
        ("Dongguan", "China"),
        ("Lagos", "Nigeria"),
        ("Lima", "Peru"),
        ("Ho Chi Minh City", "Vietnam"),
    ]

    for i in range(len(first_names)):
        contact = Contact()
        contact.first_name = first_names[i]
        contact.last_name = last_names[i]
        contact.email = contact.first_name.lower() + "@example.com"
        tmp = ''.join(random.choice(string.digits) for i in range(10))
        contact.phone = "(" + tmp[0:3] + ") " + tmp[3:6] + " " + tmp[6::]
        contact.city = locations[i][0]
        contact.country = locations[i][1]
        contact.is_admin = (i % 5 == 0)
        db.session.add(contact)

    # Create sample images
    images = ["Buffalo", "Elephant", "Leopard", "Lion", "Rhino"]
    for name in images:
        image = Image()
        image.name = name
        image.path = name.lower() + ".jpg"
        db.session.add(image)

    # Create sample files
    for i in range(3):
        file = File()
        file.name = f"Example File {i+1}"
        file.path = f"example_{i+1}.pdf"
        db.session.add(file)

    # Create sample videos
    for i in range(3):
        video = Video()
        video.name = f"Example Video {i+1}"
        video.path = f"example_video_{i+1}.mp4"
        db.session.add(video)

    # Create sample pages
    for i in range(3):
        page = Page()
        page.name = f"Example Page {i+1}"
