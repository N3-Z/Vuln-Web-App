from asyncio.windows_events import NULL
from flask import Flask, request, render_template_string
import mysql.connector
import urllib
from subprocess import PIPE, run

api = Flask(__name__)
api.config["DEBUG"] = True
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="testing"
    )
except:
    db = NULL

@api.route('/ssrf', methods=['GET'])
def ssrf():
    url = request.args.get('url')
    if url:
        return urllib.request.urlopen(url).read()
    
    return "No Url"

@api.route('/ssti', methods=['GET'])
def ssti():
    data = request.args.get('data')
    if data:
        return render_template_string(data)
    
    return "No data"

@api.route('/xss', methods=['GET'])
def xss():
    text = request.args.get('text')
    if text:
        tag = "<h2>"+text+"</h2>"
        return tag
    return "No text parameter"

@api.route('/sqli', methods=['GET'])
def sqli():
    if not db.is_connected() or db is NULL:
        return "DB is not connected" 
    userid = request.args.get('userid')

    if userid:
        query = "select * from transactionheader where userid='"+str(userid)+"'"
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        data = ""
        for i in results:
            data += "<tr><td>" + str(i[0]) + "</td><td>" + str(i[1]) + "</td><td>"+ str(i[2]) + "</td>" + "</tr>"
        
        return '<style>table,tr,td{border: 1px solid black;}</style><table>'+data+'</table>'

    return "No userid parameter"

@api.route('/csrf', methods=['GET'])
def csrf():
    return """
        <form action="" method="post">
            <input type="email" name="email" id="">
            <input type="button" value="Forget Password">
        </form>
    """

@api.route('/commandinjection', methods=['GET'])
def commandinjection():
    ip = request.args.get('ip')
    if ip:
        res = run("ping -n 1 " + ip, stdout=PIPE, stderr=PIPE, shell=True)
        return res.stdout
    return "No ip parameter"

@api.route('/fileinjection', methods=['GET','POST'])
def fileinjection():
    return "No file injection"    

@api.route('/', methods=['GET'])
def index():
    data = """
        <ul>
            <li><a href="/ssrf">SSRF</a></li>
            <li><a href="/ssti">SSTI</a></li>
            <li><a href="/xss">XSS</a></li>
            <li><a href="/sqli">SQLI</a></li>
            <li><a href="/csrf">CSRF</a></li>
            <li><a href="/commandinjection">Command Injection</a></li>
            <li><a href="/fileinjection">File Injection</a></li>
        </ul>
    """
    return data

def main():
    api.run('127.0.0.1', 9999)

if __name__ == '__main__':
    main()