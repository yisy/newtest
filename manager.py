from newtest import app,db
from flask_script import Manager
from newtest.models import User,Image,Comment
from sqlalchemy import or_,and_
import unittest

manager = Manager(app)

@manager.command
def run_test():
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)
    pass

@manager.command
def init_database():
    db.drop_all()
    db.create_all()

    for i in range(10):
        db.session.add(User('yisy' + str(i),'123'))
        for j in range(0,3):
            db.session.add(Image('www.baidu.com', str(i+1)))
            for k in range(0,3):
                db.session.add(Comment('This is a comment' + str(k), 1 + 3 * i + j ,i+1,0))
    db.session.commit()

    print User.query.all()
    print User.query.filter(User.username.endswith('0')).limit(3).all()
    print User.query.filter(or_(User.id == 8,User.id == 9)).all()
    print User.query.paginate(page=2,per_page=3).items
    print User.query.get(2).images
    print Image.query.get(1).user

    for i in range(1,9,2):
        user = User.query.get(i)
        user.username = '[New]' + user.username
    
    User.query.filter_by(id=1).update({'username':'yiu'})    

    db.session.commit()

    for i in range(1,9,2):
        comment = Comment.query.get(i)
        db.session.delete(comment)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
