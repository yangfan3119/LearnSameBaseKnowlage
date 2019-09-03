> 表单查询以及数据库相关操作，还有模板相关操作，重定向啊之类

![](../../mdPic/1567523588157.png)

项目思路:
1. 配置数据库
    a.导入SQLAlchemy扩展
    b.创建db对象，并配置参数
    c.终端创建数据库
2. 添加书和作者模型
    a. 模型继承与db.Model
    b. __tablename__表名
    c. db.Column:字段
    d. db.relationship:关系引用
3. 添加数据
4. 使用模板显示数据库查询的数据
    a. 查询所有的作者信息，让信息传递给模板
    b. 模板中按照格式，依次for循环作者和数据即可（作者获取书籍， 用的是关系引用）
5. 使用WTF显示表单
    a. 自定义表单类
    b. 模板中显示
    c. secret_key / 编码 / csrf_token
6. 实现相关的增删逻辑
    a. 增加数据
    b. 删除书籍--> 网页中删除 --> 点击需要发送书籍的id给后台



**app.py**

```python
# encoding=utf-8
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/flask_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'yangfan'


# 创建数据库对象
db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__='authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    books = db.relationship('Book', backref='author')

    def __repr__(self):
        print('Author: %r %r %r'%(self.id, self.name, self.books))


class Book(db.Model):
    __tablename__='books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        print('Book: %r %r %r'%(self.id, self.name, self.author_id))


def DB_Create():
    db.drop_all()
    db.create_all()
    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老李')
    au3 = Author(name='老赵')
    db.session.add_all([au1, au2, au3])
    db.session.commit()

    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少', author_id=au2.id)
    bk3 = Book(name='你别骗我', author_id=au2.id)
    bk4 = Book(name='如何才能让自己更骚', author_id=au1.id)
    bk5 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk6 = Book(name='如何政府英俊少男', author_id=au3.id)

    db.session.add_all([bk1, bk2, bk3, bk4, bk6, bk5])
    db.session.commit()

# 自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者', validators=[DataRequired()])
    book = StringField('书籍', validators=[DataRequired()])
    submit = SubmitField('提交')

DB_Create()

@app.route('/delete_book/<book_id>', methods=['GET'])
def delete_book(book_id):
    # 查询数据库是否存在该id，如果有就删除，没有就提示错误
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            flash('删除书籍出错')
            db.session.rollback()
    else:
        flash('书籍找不到')

    # 重定向: url_for('index'),传入视图函数

    return redirect(url_for('hello_world'))


@app.route('/', methods=['GET','POST'])
def hello_world():
    # 创建表单类
    author_form = AuthorForm()

    '''
    验证逻辑：
    1. 调用WTF的函数实现验证
    2. 验证通过获取数据
    3. 判断作者是否存在
    4. 如果作者存在，判断数据存在，存在则提示重复，否则添加
    5. 作者不存在，添加作者数据
    '''
    if request.method == 'POST':
        #1. 调用WTF的函数实现验证
        if author_form.validate_on_submit():
            # 2. 获取数据
            author_name = author_form.author.data
            book_name = author_form.book.data
            # 3. 判断作者是否存在
            author = Author.query.filter_by(name=author_name).first()

            if author:
                # 4.如果作者存在，判断书籍是否存在
                book = Book.query.filter_by(name=book_name, author_id=author.id).first()
                if book:
                    flash("重复书籍")
                else:
                    try:
                        bk = Book(name=book_name, author_id=author.id)
                        db.session.add(bk)
                        db.session.commit()
                    except Exception as e:
                        flash("添加书籍失败")
                        db.session.rollback()
            else:
                try:
                    # 5. 如果作者不存在，则添加作者，再添加书籍
                    auth = Author(name=author_name)
                    db.session.add(auth)
                    db.session.commit()

                    book = Book(name=book_name, author_id=auth.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    flash("添加书籍失败")
                    db.session.rollback()
        else:
            flash('参数不全')


    # 查询所有的作者信息，让信息传递给模板
    authors = Author.query.all()
    return render_template('books.html', authors=authors, form=author_form)


if __name__ == '__main__':
    app.run()
```

**books.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<hr>
<form method="post">
    {{ form.csrf_token() }}
    {{ form.author.label }}{{ form.author }}<br>
    {{ form.book.label }}{{ form.book }}<br>
    {{ form.submit }}<br>
    {% for message in get_flashed_messages() %}
        {{ message }}
    {% endfor %}
</form>

<ul>
{% for auth in authors %}
    <li>{{ auth.name }}</li>
    <ul>
        {% for book in auth.books %}
            <li>
                {{ book.name }}
                <a href="{{ url_for('delete_book', book_id=book.id) }}" >删除</a>
            </li>
        {% else %}
            <li>无</li>
        {% endfor %}
    </ul>
{% endfor %}
</ul>
</body>
</html>
```

