#!/usr/bin/env python
#coding:utf-8
from flask import Flask,redirect,request,render_template,session
from db import get_userlist,getuser,add_user,del_user,update_user,checkuser,getone,modpasswd,get_idclist,add_idc,del_idc,update_idc,getidc
import json

app=Flask(__name__)
app.secret_key='www.123'


@app.route("/")
@app.route("/index")
def index():
	username=session.get("name")
	return render_template("index.html",username=username)


@app.route("/login",methods=['GET','POST'])
def login():
        if request.method =="GET":
                return render_template("login.html")
        if request.method =='POST':
                login_info = dict((k,v[0]) for k,v in dict(request.form).items())
                print login_info
                if not login_info.get("name",None) or not login_info.get("password",None):
                        errmsg = "username and password can not be empty"
                        return json.dumps({'code':'1','errmsg':errmsg})
#把数据库中所有的name拿出来存为一个list
                if login_info["name"] not in  [ n.values()[0] for n in get_userlist(["name"]) ]:
                        namelist=[ n.values()[0] for n in get_userlist(["name"]) ]
                        print namelist
                        print login_info["name"]
                        errmsg = "username not exist"
                        return json.dumps({'code':'1','errmsg':errmsg})
                if login_info["password"] != checkuser(login_info["name"]):
                        errmsg = "password is error"
                        return json.dumps({'code':'1','errmsg':errmsg})
                
#判断session中的用户名与表单里面的用户名是否相同
                session['name']=login_info['name']
                return json.dumps({'code':'0','result':"login sucess"})




@app.route("/userlist")
def userlist():
#判断用户是否登录，如果没有登录就跳转到登录页
        if not session.get('name'):
                return redirect('/login')
        user_items=["id","name","name_cn","email","mobile","role","status"]
        username=session.get("name")
        if username == "admin":
                userlist=get_userlist(user_items)
                return render_template("userlist.html",users=userlist,username=username)
        else:
                users=getone(username)
                print users
                return render_template("userinfo.html",users=users,username=username)



@app.route("/adduser",methods=['GET','POST'])
def adduser():
        if request.method =="GET":
		username=session.get("name")
                return render_template("register.html",username=username)

#前端post请求，逻辑端通过request.form获取整个表单的值
        if request.method =="POST":
                userlist=dict((k,v[0]) for k,v in dict(request.form).items())
                print userlist
                print [ n.values()[0] for n in get_userlist(["name"]) ]
                print userlist["name"]
                if userlist["name"] in [ n.values()[0] for n in get_userlist(["name"]) ]:
                        errmsg = "username is exist"
                        return json.dumps({'code':'1','errmsg':errmsg})
                if not userlist["name"] or not userlist["password"]:
                        errmsg = "username and password is not empty"
                        return json.dumps({'code':'1','errmsg':errmsg})
                if userlist["password"] != userlist["re_password"]:
                        errmsg="password is error"
                        return json.dumps({'code':'1','errmsg':errmsg})
                fields = ["name","name_cn","password","mobile","email","role","status"]
                values = [ '%s'%userlist[x] for x in fields]
                print values
#[u'weixiaobao', u'weixiaobao', u'123', u'123123', u'123113', u'ops', u'0']
                userdict = dict([(k,values[i]) for i,k in enumerate(fields)])
                print userdict
#{'status': u'0', 'name': u'weixiaobao', 'mobile': u'123123', 'name_cn': u'weixiaobao', 'role': u'ops', 'password': u'123', 'email': u'123113'}
                add_user(userdict)
                return json.dumps({'code':'0','result':"register sucess"})


@app.route("/deluser")
def deluser():
        if not session.get('name'):
                return redirect('/login')
#前端get请求，逻辑端通过request.args.get获取参数
        uid=request.args.get("uid")
        print uid
        del_user(uid)
	return json.dumps({"code":0,"result":"delete user success"})

@app.route("/update",methods=['GET','POST'])
def updateuser():
        if not session.get('name'):
                return redirect('/login')
#通过id查询到要更新的数据，并渲染到更新页面
        if request.method =="GET":
                uid=request.args.get("uid")
                print uid
                userinfo=getuser(uid)
		print userinfo
		return json.dumps(userinfo)
#获取到更新页面表单的值，然后提交更新
        if request.method =="POST":
                userinfo={}
                userinfo["name"] = request.form['name']
                userinfo["name_cn"] = request.form['name_cn']
                userinfo["email"] = request.form['email']
                userinfo["mobile"] = request.form['mobile']
                userinfo["role"] = request.form['role']
                userinfo["status"] = request.form['status']
                update_user(userinfo)
		print update_user(userinfo)
		return json.dumps({"code":0})

@app.route("/modpasswd",methods=["GET","POST"])
def changepass():
        if request.method=="GET":
		username=session.get("name")
                return render_template("changepass.html",username=username)
        if request.method=="POST":
                passwd_info=dict((k,v[0]) for k,v in dict(request.form).items())
                if not passwd_info.get("password","None") or not passwd_info.get("oldpassword","None"):
                        errmsg = "password can not be empty"
                        return json.dumps({'code':'1','errmsg':errmsg})
                if passwd_info["oldpassword"] != checkuser(session.get("name")):
                        oldpassword=checkuser(session.get("name"))
                        print oldpassword
                        errmsg= "your input oldpassword is error"
                        return json.dumps({'code':'1','errmsg':errmsg})
                else:
                        name=session.get("name")
                        password=passwd_info["password"]
                        print name
                        print password
                        modpasswd(password,name)
                        return json.dumps({'code':'0','result':"change sucess"})


@app.route('/idc')
def idclist():
	#判断用户是否登录，如果没有登录就跳转到登录页
        if not session.get('name'):
                return redirect('/login')
	else:
		idc_items=["id","name","cabinets","hosts","contacts","telephone","remarks"]
		username=session.get("name")
		idclist=get_idclist(idc_items)
		print idclist
		return render_template("idclist.html",idcs=idclist,username=username)
	

@app.route("/addidc",methods=['GET','POST'])
def addidc():
        if request.method =="GET":
		username=session.get("name")
                return render_template("addidc.html",username=username)

#前端post请求，逻辑端通过request.form获取整个表单的值
        if request.method =="POST":
                idclist=dict((k,v[0]) for k,v in dict(request.form).items())
                if idclist["name"] in [ n.values()[0] for n in get_idclist(["name"]) ]:
                        errmsg = "idcname is exist"
                        return json.dumps({'code':'1','errmsg':errmsg})
                if not idclist["name"] or not idclist["telephone"]:
                        errmsg = "name and telephone is not empty"
                        return json.dumps({'code':'1','errmsg':errmsg})
                fields = ["name","cabinets","hosts","contacts","telephone","remarks"]
                values = [ '%s'%idclist[x] for x in fields]
                print values
                idcdict = dict([(k,values[i]) for i,k in enumerate(fields)])
                add_idc(idcdict)
                return json.dumps({'code':'0','result':"add sucess"})


@app.route("/delidc")
def delidc():
        if not session.get('name'):
                return redirect('/login')
#前端get请求，逻辑端通过request.args.get获取参数
        uid=request.args.get("uid")
        print uid
        del_idc(uid)
	return json.dumps({"code":0,"result":"delete idc success"})


@app.route("/updateidc",methods=['GET','POST'])
def updateidc():
        if not session.get('name'):
                return redirect('/login')
#通过id查询到要更新的数据，并渲染到更新页面
        if request.method =="GET":
                uid=request.args.get("uid")
                print uid
		idcinfo=getidc(uid)
		print idcinfo
		return json.dumps(idcinfo)
#获取到更新页面表单的值，然后提交更新
        if request.method =="POST":
                idcinfo={}
                idcinfo["name"] = request.form['name']
                idcinfo["cabinets"] = request.form['cabinets']
                idcinfo["hosts"] = request.form['hosts']
                idcinfo["contacts"] = request.form['contacts']
                idcinfo["telephone"] = request.form['telephone']
                idcinfo["remarks"] = request.form['remarks']
                update_idc(idcinfo)
		return json.dumps({"code":0})

@app.route('/server')
def server():
    return render_template("server.html")

@app.route('/cabinet')
def cabinet():
    return render_template("cabinet.html")

@app.route('/loginout')
def loginout():
#session是一个大字典，把当前页面对应的session移除
        session.pop('name')
        return redirect('/login')

if __name__=="__main__":
        app.run(host="0.0.0.0",port=8000,debug=True)
