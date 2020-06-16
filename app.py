from flask import Flask, render_template, request
from flask_cors import CORS
from flask import send_file
import json
import time
import codecs
decode_hex = codecs.getdecoder("hex_codec")


import base64
import string
# import ssl
# connect to the db
import psycopg2
# ssl
from flask import Flask, jsonify

# cesar ecrypt
def encrypt(text,s): 
    result = "" 
    for i in range(len(text)): 
        char = text[i] 
        if (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65) 
        else: 
            result += chr((ord(char) + s - 97) % 26 + 97) 
    return result 
def decrypt(code, distance):
    plainText = ""
    for ch in code:
        ordvalue = ord(ch)
        ciphervalue = ordvalue - distance
        if ciphervalue < ord('a'):
            ciphervalue = ord('z') - (distance - (ord('a')-ordvalue - 1))
        plainText += chr(ciphervalue)
    return plainText
app = Flask(__name__)
CORS(app)
# kowert linku
def url_to_list(url):
    url_to_process=url[int(str(url)[1:].find("/"))+1:]
    flag=0
    list_req={}
    key=""
    value=""
    for i in url_to_process:
            if i =="=" or i == "%":
                    if i == "=":
                        list_req[key]=""
                        flag=1
                    if i== "%":
                        list_req[key]=value
                        key=""
                        value=""
                        flag=0
            else:
                    if flag ==0:
                        key+=i
                    if flag ==1:
                        value+=i

    return(list_req)

# bazkie
def add_data(sql):
	print("database connecting_add")
	con = psycopg2.connect(
	    host="localhost",
	    database="recycle",
	    user ='postgres',
	    password="qaz123",
	)
	con.autocommit = True
	# cursor
	print(sql)
	cur = con.cursor()
	print(cur.execute(sql))
	con.close()

def add_data_ret_id(sql):
	print("database connecting_add")
	con = psycopg2.connect(
	    host="localhost",
	    database="recycle",
	    user ='postgres',
	    password="qaz123",
	)
	con.autocommit = True
	# cursor
	cur = con.cursor()
	print(cur.execute(sql))
	id_of_new_row = cur.fetchone()[0]
	con.close()
	return id_of_new_row
 	

def get_data(sql,list_of_variables):
	print("database connecting")
	con = psycopg2.connect(
	    host="localhost",
	    database="recycle",
	    user ='postgres',
	    password="qaz123",
	)
	# cursor
	cur = con.cursor()
	cur.execute(sql)
	if(len(list_of_variables)==0):
		rows= list(cur.fetchall())
		return rows
	rows= list(cur.fetchall())
	to_return=dict.fromkeys(list_of_variables)
	

	for i in to_return.keys():
		to_return[i]=[]
	print(len(list_of_variables))
	print(rows)
	for r in rows:
		for i in range(0,len(list_of_variables)):
			temp=to_return[list_of_variables[i]]
			
			
			temp.append(r[i])
			

			to_return[list_of_variables[i]]=temp

	con.close()
	return to_return



# routes
@app.route('/')
def index():
    return 'Hello world'
@app.route('/login/<url>')
def login(url):
	requests=url_to_list(url)
	
	passwd=requests["password"]
	sql="select id_user from users where pass=crypt('"+passwd+"', pass) and  name= '"+requests["username"]+"';"
	
	if len(get_data(sql,["id"])["id"])==1:
		return json.dumps({'isCorrect':encrypt("true",6)})
	else:
		return json.dumps({'isCorrect':encrypt("false",6)})

@app.route('/items/<url>')
def items(url):
	requests=url_to_list(url)
	# print(requests)
	sql="select items_to_materials.id_item,name,material_name from items inner join items_to_materials on items.id_item=items_to_materials.id_item  inner join materials on materials.material_id=items_to_materials.id_material;"
	print(get_data(sql,["kod","name","material"]))
	# opracuj kosze     
	
    # send
	return json.dumps(get_data(sql,["kod","name","material_name"])).encode("utf-8")

@app.route('/scans/<url>')
def scans(url):
	requests=url_to_list(url)
	# print(requests)
	sql="select name,material_name from items inner join items_to_materials on items.id_item=items_to_materials.id_item  inner join materials on materials.material_id=items_to_materials.id_material where items.id_item ="+requests["kod"]+";"
	print(get_data(sql,["name","material"]))
	# opracuj kosze     
	
    # send
	return json.dumps(get_data(sql,["name","material_name"])).encode("utf-8")
@app.route("/upcycling/<url>")	
def upcycling(url):
	requests=url_to_list(url) 
	print(requests.keys())

	if(list(requests.keys())[0]== "user_id"):
		sql="select upcycling.name, upcycling.id_upcycling, upcycling.imgBase from users_to_upcycling inner join upcycling on users_to_upcycling.id_upcycling=upcycling.id_upcycling inner join users on users.id_user=users_to_upcycling.id_user where users_to_upcycling.id_user ="+requests["user_id"] +";"
		print(sql)
		return json.dumps(get_data(sql,["name","id_upcycling","imgBase"])).encode("utf-8")
	if(list(requests.keys())[0]== "id"):

		sql="SELECT id_upcycling,name, descrip, imgBase, link from upcycling where id_upcycling={};".format(requests["id"])
		print(sql)
	if(list(requests.keys())[0]=="filters"):
		filters=requests["filters"].split(',')
		print(filters)
		where=""
		for i in filters:
			where+=" descrip like '%"+str(i) +"%' or"
		where=where[:-2]
		sql="select id_upcycling,name,descrip,imgBase,link from upcycling where "+where+";"
	if(list(requests.keys())[0]=="show"):
		sql="select id_upcycling,name,descrip,imgBase,link from upcycling"
	print(sql)
	data=get_data(sql,["id_upcycling","name","descrip","imgBase","link"])
	return json.dumps(data).encode("utf-8")

@app.route('/facts/<url>')	
def facts(url):	
	print(url)
	requests=url_to_list(url) 
	print(requests,"\n--------------------")
	if requests["random"]=="true": 
		sql="SELECT descrip FROM facts ORDER BY RANDOM() LIMIT " +requests["quantity"]+";" 
		return json.dumps(get_data(sql,["descrip"]),ensure_ascii=False).encode("utf-8")
	else: 
		sql="select descrip,name_cate from facts_to_category inner join facts on facts_to_category.id_facts= facts.id_facts inner join category_to_facts on category_to_facts.id_category_to_facts= facts_to_category.id_category where name_cate like '" + requests["'category'"] +"' LIMIT "+ requests["quantity"] +";"
		print(sql)
		return json.dumps(get_data(sql,["descrip","name_cate"])).encode("utf-8")


@app.route('/goals/<url>')	
def goals(url):
	requests=url_to_list(url)
	sql="SELECT name, descrip FROM goals ORDER BY RANDOM() LIMIT "+requests["quantity"]+";"
	return json.dumps(get_data(sql,["name","desc"])).encode("utf-8")

@app.route('/user/<url>')	
def user(url):
	requests=url_to_list(url)
	print(requests)
	sql= "SELECT name FROM users WHERE id_user ="+requests["user_id"]+";"
	#json_send
	return json.dumps(get_data(sql,["name"])).encode("utf-8")

@app.route('/news/<url>')
def news(url):
	requests=url_to_list(url)
	order="DESC"
	if requests["sort_by"]=="oldest":
		order="ASC"
	sql="select news.title,news.descript,news.id_img,news.add_date, news.id_news from news Order by add_date "+order+" limit "+requests["quantity"]+ ";"
	data=get_data(sql,["title","descript","id_img","add_date","id_news"])
	data['id_img']= "http://62.171.181.96:5000/imgs/"+data['id_img'][0]
	return json.dumps(data, indent=4, sort_keys=True, default=str).encode("utf-8")

# @app.before_request
# def del_slah():
# 	contr=0
# 	to_return=""
# 	for i in request.path:
# 		# print(i)
# 		if i== "/":
# 			contr+=1
# 			if contr>=3:
# 				to_return+="*"
# 			else:
# 				to_return+=i
# 		else:
# 			to_return+=i
# 	request.path=to_return
# 	# print(to_return,"duu")
# 			# requests.path=to_retun

@app.route('/add/<url>')	
def add(url):
	requests=url_to_list(url)
	time.sleep(2)
	tab = requests["what"]
	if tab=="news":
		sql= "INSERT INTO public.news(title, descript, id_img, add_date) VALUES ('{}','{}', {},'{}') RETURNING id_news;".format(requests['name'],requests['opis'],requests["id_img"],requests['dzien'])
		news_id=add_data_ret_id(sql)
		print(news_id)
		return "news dodany"
	elif tab=="item":
		sql="INSERT INTO public.items(name, id_item) VALUES ('{}', {});".format(requests['name'], requests['code'])
		add_data(sql)
		mat=requests["materials"].split(',')
		for x in mat:
			sql = "INSERT INTO public.items_to_materials(id_item, id_material) VALUES ('{}', '{}');".format(requests['code'], x)
			add_data(sql)
		return("Dodano przedmiot")

	elif tab=="upcycling":
		decodedUrl = decode_hex(requests['link'])[0].decode('utf-8')
		sql="INSERT INTO public.upcycling(descrip, link, name) VALUES ('{}', '{}', '{}') RETURNING id_upcycling;".format(requests['opis'], decodedUrl,requests['name'])
		upcycling_id=add_data_ret_id(sql)
		sql="INSERT INTO public.users_to_upcycling(id_upcycling, id_user) VALUES ('{}', '{}');".format(upcycling_id, requests['uid'])
		add_data(sql)
		print("allalallalala", type(requests['imgbase64']), len(requests['imgbase64']))
		sql="UPDATE public.upcycling SET  imgbase='{}' WHERE id_upcycling={};".format(requests['imgbase64'], upcycling_id)
		add_data(sql)
		return json.dumps('Dodano upcycling')

	elif tab=="facts":
		sql="INSERT INTO public.facts(descrip) VALUES ('{}') RETURNING id_facts;".format(requests['opis'])
		fact_id=add_data_ret_id(sql)
		print(fact_id)
		cate=requests["kate"].split(',')
		for x in cate:
			sql="INSERT INTO public.facts_to_category(id_facts, id_category)VALUES ('{}','{}');".format(fact_id, x)
			add_data(sql)
		return('Dodano ciekawostke')
	elif tab=="objectives":
		sql="INSERT INTO public.goals(name, descrip) VALUES ('{}', '{}');".format(requests['name'], requests['opis'])
	# return add_data(sql)
	return json.dumps('ok')


@app.route('/drop/<url>')	
def drop(url):
	requests=url_to_list(url)
	tab = requests["what"]
	if tab=="news":
		sql= "DELETE FROM public.news WHERE id_news={};".format(requests['id'])
	elif tab=="item":
		sql="DELETE FROM public.items WHERE id_item={};".format(requests['id'])
		add_data(sql)
		sql = "DELETE FROM public.items_to_materials WHERE id_item={};".format(requests['id'])
	elif tab=="upcycling":
		sql="DELETE FROM public.upcycling WHERE id_upcycling={};".format(requests['id'])
		add_data(sql)
		sql="DELETE FROM public.users_to_upcycling WHERE id_upcycling={};".format(requests['id'])
	elif tab=="facts":
		sql="DELETE FROM public.facts WHERE id_facts={};".format(requests['id'])
		add_data(sql)
		sql="DELETE FROM public.facts_to_category WHERE id_facts={};".format(requests['id'])
	elif tab=="objectives":
		sql="DELETE FROM public.goals WHERE id_goals={};".format(requests['id'])
	add_data(sql)
	return json.dumps('Usunieto')

@app.route('/register/<url>')
def register(url):
	request=url_to_list(url)
# check in db
	sql="select * from users where users.name = '"+request['login']+"'"
	if get_data(sql,["login"])['login'] == []:
		sql="INSERT INTO users (name,pass,e_mail,pic ) VALUES (  '"+request['login']+ "',  crypt('"+request['login']+"', gen_salt('bf')),'"+request['mail']+"','"+request['link']+"');"
		add_data(sql)
		return json.dumps("Uzytkownik dodany").encode("utf-8")
	else:
		return json.dumps("Uzytkownik istnieje").encode("utf-8")

# @app.route('/img/<name>')
# def img(name):
#     try:
#     	return send_file('static\\images\\'+name+'.png')
#     except:
#     	return send_file('static\\images\\'+name+'.jpg')


@app.route('/update/<url>')	
def update(url):
	requests=url_to_list(url)
	tab = requests["what"]
	if tab=="news":
		sql= "UPDATE public.news SET title='{}', descript='{}' WHERE id_news = {};".format(requests['newname'], requests["newdesc"], requests["newid"])
	elif tab=="item":
		pass
	elif tab=="upcycling":
		pass
	elif tab=="facts":
		pass
	elif tab=="objectives":
		pass
	add_data(sql)
	return "True"
@app.route('/getusid/<url>')
def getusid(url):
	requests=url_to_list(url)
	sql= "SELECT id_user FROM users WHERE name ='"+requests["usname"]+"';"
	#json_send
	return json.dumps(get_data(sql,["id_user"])).encode("utf-8")
	

# @app.route('/img/facts/<url>')
# def query_img():

# @app.route('/img/facts/<url>')
# def query_img():

if __name__ == '__main__':
	app.run( host='62.171.181.96', threaded=True, ssl_context=("C:/Users/Administrator/Desktop/SSL/server.crt", "C:/Users/Administrator/Desktop/SSL/server.key"))
	app.url_map.strict_slashes = False
# ssl_context=context