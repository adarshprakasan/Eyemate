from flask import Flask, render_template,request,redirect,session
from DBConnection import Db

app = Flask(__name__)
app.secret_key="abc"

@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        name=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login WHERE username='"+name+"'and password='"+password+"'")
        if res is not None:
            if res['usertype']=='admin':
                session['lg']="lo"
                return redirect('/view_adminhome')
            else:
                return "invalid user"
        else:
            return "User not exist"
    else:
        return render_template('login.html')

@app.route('/view_review')
def view_review():
    if session['lg']=="lo":
        db=Db()
        res=db.select("select * from reviews,caretaker where reviews.ct_id=caretaker.ct_id")
        return render_template('Admin/review.html',data=res)
    return redirect('/')

@app.route('/view_blindlist')
def view_blindlist():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from blind")
        return render_template('Admin/viewblindlist.html',data=res)
    return redirect('/')

@app.route('/view_caretaker')
def view_caretaker():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from caretaker")
        return render_template('Admin/viewcaretaker.html',data=res)
    return redirect('/')


@app.route('/verify_caretaker')
def verify_caretaker():
    if session['lg'] == "lo":
        db=Db()
        res=db.select("select * from caretaker,login where login.login_id=caretaker.ct_id and login.usertype='Pending'")
        return render_template('Admin/vnvcaretaker.html',data=res)
    return redirect('/')

@app.route('/approve_ct/<id>')
def approve(id):
    if session['lg'] == "lo":
        db=Db()
        res=db.update("update login set usertype='caretaker' where login_id='"+id+"'")
        return '<script>alert("approved successfully");window.location="/view_caretaker"</script>'
    return redirect('/')

@app.route('/reject_ct/<id>')
def reject(id):
    if session['lg'] == "lo":
        db=Db()
        res=db.update("update login set usertype='rejected' where login_id='"+id+"'")
        return '<script>alert("caretaker rejected");window.location="/view_caretaker"</script>'
    return redirect('/')

@app.route('/view_changepass',methods=['get','post'])
def view_changepass():
    if session['lg'] == "lo":
        if request.method=="POST":
            curpassword= request.form['textfield']
            newpassword = request.form['textfield2']
            conpassword= request.form['textfield3']
            db = Db()
            res = db.selectOne("select * from login WHERE password='"+curpassword+"'and usertype='admin'")
            if res is not None:
                if newpassword==conpassword:
                    db=Db()
                    db.update("update login set password='"+conpassword+"'where usertype='admin'")
                    return '<script>alert("Password changed Successfully");window.location="/"</script>'
                else:
                    return '<script>alert("Password mismatched");window.location="/view_changepass"</script>'
            else:
                return '<script>alert("incorrect password");window.location="/view_changepass"</script>'
        else:
            return render_template('Admin/changepass.html')
    return redirect('/')

@app.route('/view_adminhome')
def view_adminhome():
    if session['lg'] == "lo":
        return render_template('Admin/adminhome.html')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    session['lg']=""
    return redirect('/')

if __name__ == '__main__':
    app.run()
