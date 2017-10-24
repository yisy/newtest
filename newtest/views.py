# -*- encoding=UTF-8 -*-
from newtest import app,db
from models import Image,User
from flask import render_template,request,flash,redirect,get_flashed_messages,send_from_directory
import random,hashlib,json,uuid,os
from flask_login import login_user,logout_user,current_user,login_required
from qiniusdk import qiniu_upload_file

@app.route('/index/<int:p>/')
@login_required
def index(p):
    pageinate = Image.query.paginate(page=p, per_page=3)
    hasNext = pageinate.has_next
    images = pageinate.items
    return render_template('index.html',images = images, p = p, hasNext = hasNext)

@app.route('/detail/<int:id>/')
def detail(id):
    return "image is " + str(id)

@app.route('/reloginpage/')
def reloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False,category_filter=['relogin']):
        msg = msg + m
    return render_template('login.html',msg = msg)

def redirect_with_msg(target,message,category):
    flash(message,category = category)
    return redirect(target)

@app.route('/reg/',methods=['get','post'])
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/reloginpage/',u'用户名和密码不能为空','relogin')

    user = User.query.filter_by(username=username).first()

    if user != None:
        return redirect_with_msg('/reloginpage/',u'用户名已存在','relogin')

    slat = '.'.join(random.sample('0123325435dfsdfa',5))
    m = hashlib.md5()
    m.update(password+slat)
    password = m.hexdigest()

    user = User(username,password,slat)
    db.session.add(user)
    db.session.commit()
    
    login_user(user)

    return redirect('/index/1/')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/reloginpage/')


@app.route('/login/',methods=['get','post'])
def login():

    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    user = User.query.filter_by(username=username).first()

    if user == None:
        return redirect_with_msg('/reloginpage/',u'用户不存在','relogin')

    m = hashlib.md5()
    m.update(password+user.slat)

    logout_user()
    
    if(m.hexdigest() != user.password):
        return redirect_with_msg('/reloginpage/',u'用户名密码错误','relogin')

    login_user(user)

    return redirect('/index/1/')


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>')
def user_images(user_id,page,per_page):
    pageinate = Image.query.filter_by(user_id=user_id).paginate(page=page,per_page=per_page)
    map = {'has_next':pageinate.has_next}
    images = []

    for image in pageinate.items:
        imgvo = {'id' : image.id,'url':image.url}
        images.append(imgvo)

    map['images'] = images

    return json.dumps(map)

def save_tolocal(file,filename):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, filename))
    return '/image/' + filename

@app.route('/upload/', methods=['post'])
def upload():
    file = request.files['file']

    file_ext = ''

    if file.filename.find('.') > 0 :
        file_ext = file.filename.rsplit('.',1)[1].strip().lower()

    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-','') + '.' + file.filename
        save_tolocal(file,file_name)
        url = qiniu_upload_file(file, file_name)
        if url != None:
            db.session.add(Image(url,1))
            db.session.commit()

    return '0k'


@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'],image_name)
