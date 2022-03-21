from flask import Flask, render_template, redirect

from forms.user import RegisterForm, LoginForm
from data.news import News
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route("/add_data")
def add_data():
    db_sess = db_session.create_session()

    # Добавление пользователей
    for i in range(5):
        user = User()
        user.name = f"Пользователь {i+1}"
        user.about = f"биография пользователя {i+1}"
        user.email = f"email{i+1}@email.ru"
        db_sess.add(user)
        print(user.email)

    print("5 пользвателей")
    # Добавление новостей
    news = News(title="Первая новость", content="Привет блог!", user_id=1, is_private=False)
    db_sess.add(news)
    # Несколько другой способ внесения связанных данных в БД
    user = db_sess.query(User).filter(User.id == 1).first()
    news = News(title="Вторая новость", content="Уже вторая запись!", user=user, is_private=False)

    db_sess.add(news)
    db_sess.commit()
    return "Данные добавлены!<p><a href='.'>назад</a></p>"


@app.route("/select_data")
def select_data():
    db_sess = db_session.create_session()
    for user1 in db_sess.query(User).all():
        print(user1)
    for user2 in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
        print(user2)
    return "Данные выбраны!<p><a href='.'>назад</a></p>"


@app.route("/delete_data")
def delete_data():
    db_sess = db_session.create_session()
    db_sess.query(User).filter(User.id >= 2).delete()
    db_sess.commit()
    return "Данные удалены!<p><a href='.'>назад</a></p>"


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Вход', form=form)


if __name__ == '__main__':
    main()
