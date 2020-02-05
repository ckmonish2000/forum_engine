from flask import Flask,render_template,request,redirect,session,url_for
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,ForeignKey,text


engine = create_engine('sqlite:///testforum.db', echo = True)
meta=MetaData()


testforum=Table(
	"testforum",meta,
	Column("id",Integer,primary_key=True),
	Column("question",String),
	Column("author",String))

comment=Table(
	"comments",meta,
	Column("id",Integer,primary_key=True),
	Column("comment",String),
	Column("forum_id",Integer,ForeignKey("testforum.id"))
	)

user=Table(
	"user",meta,
	Column("id",Integer,primary_key=True),
	Column("username",String),
	Column("password",String)
)

meta.create_all(engine)



app=Flask(__name__)


# signup
@app.route("/signup",methods=["POST","GET"])
def signup():
	if request.method=="POST":
		username=request.form.get("Username")
		pwd=request.form.get("pwd")
		x=user.insert().values(username=username,password=pwd)
		conn=engine.connect()
		conn.execute(x)
		return redirect("/login")
	return render_template("signup.html")	

# login
@app.route("/",methods=["POST","GET"])
def login():
	if request.method=="POST":
		
		try:
			username=request.form.get("Username")
			pwd=request.form.get("pwd")
			uname=text("select username,password from user where user.username=:x and user.password=:y")
			conn=engine.connect()
			x1=conn.execute(uname,x=username,y=pwd)
			u=x1.fetchall()
			print(u[0][0])
			print(u[0][1])
			if(username==u[0][0] and pwd==u[0][1]):
				return redirect("/home")
				
				
			else:
				return "invalid user"
		except:
			return "invalid user"
	return render_template("login.html")
	

# index 
@app.route("/home")
def index():
		conn=engine.connect()
		sel=testforum.select()
		x=conn.execute(sel)
		xx=x.fetchall()
		print(xx)
		

		return render_template("index.html",value=xx)

# ui for questions 
@app.route("/questions")
def q():
	return render_template("questionpost.html")

# gonna push questions into the database
@app.route("/post",methods=["POST"])
def postquestion():
	authors=request.form.get("name")
	questions=request.form.get("question")
	print(questions)
	print(authors)
	conn=engine.connect()
	ins=testforum.insert().values(question=questions,author=authors)
	conn.execute(ins)
	x=testforum.select()
	y=conn.execute(x)
	y1=y.fetchall()
	print(y1)

	return "done"


@app.route("/pst/<int:num>")
def pst(num):
	conn=engine.connect()
	sel=testforum.select().where(testforum.c.id==num)
	x=conn.execute(sel)
	xx=x.fetchall()

	# comment data
	sel1=comment.select().where(comment.c.forum_id==num)
	x1=conn.execute(sel1)
	x2=x1.fetchall()
	print(x2)

	print(xx)
	return render_template("interact.html",value=xx,value2=x2)

@app.route("/comment/<int:num>",methods=["POST"])
def comm(num):
	conn=engine.connect()
	val=request.form.get("comm")
	print(val)
	print(num)
	ins=comment.insert().values(comment=val,forum_id=num)
	print(ins)
	conn.execute(ins)
	return redirect(f"/pst/{num}")



if __name__=="__main__":
    app.run(debug=True)