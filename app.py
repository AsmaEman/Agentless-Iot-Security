from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os.path import join, dirname, realpath
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER





@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        uploaded_file = request.files['file']
        inputFilePath = uploaded_file #mention path+Name of the pcap file
        outputFilePath = inputFilePath,'_.csv'

        frame_Features = "-e frame.time_delta -e frame.time_relative -e frame.len "
        flow_Features = "-e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e ip.proto -e ip.ttl "
        tcp_Features = "-e tcp.flags -e tcp.time_delta -e tcp.len -e tcp.ack -e tcp.connection.fin -e tcp.connection.rst -e tcp.connection.synack -e tcp.connection.syn -e tcp.flags.ack -e tcp.flags.fin -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.urg -e tcp.hdr_len -e tcp.payload -e tcp.pdu.size -e tcp.window_size_value -e tcp.checksum "

        mqtt_Features = "-e  mqtt.clientid -e mqtt.clientid_len -e mqtt.conack.flags -e mqtt.conack.val -e mqtt.conflag.passwd -e mqtt.conflag.qos -e mqtt.conflag.reserved -e mqtt.conflag.retain -e  mqtt.conflag.willflag -e mqtt.conflags -e mqtt.dupflag -e mqtt.hdrflags -e mqtt.kalive -e mqtt.len -e mqtt.msg -e mqtt.msgtype -e mqtt.qos -e mqtt.retain -e mqtt.topic -e mqtt.topic_len -e mqtt.ver -e mqtt.willmsg_len "

        others = "-E header=y -E separator=, -E quote=d -E occurrence=f "



        allFeatures = frame_Features + flow_Features + tcp_Features + mqtt_Features + others    

        command = 'tshark -r ', inputFilePath , ' -T fields ' + allFeatures + '> ', outputFilePath
        print(f"--- Input File: {inputFilePath} ---")

        print('--Processing File--')

        print("=== Extracting Features and Generating CSV===")

        s=os.system(str(command))

        print("--- Done ---")
        
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # save the file
            
            def upload_file():
                if request.method == 'POST':
                    # check if the post request has the file part
                    if 'file' not in request.files:
                        
                        return redirect(request.url)
                    file = request.files['file']
                    # if user does not select file, browser also
                    # submit a empty part without filename
                    if file.filename == '':
                        
                        return redirect(request.url)
                    if file :
                        
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return redirect(url_for('uploaded_file',
                                                filename=filename))
                return 
            todo = Todo(title=title, desc=desc, )
            db.session.add(todo)
            db.session.commit()
        
            
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    
   # uploaded_file = request.files['file']
    
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} "



@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
@app.route('/predict/<int:sno>', methods=['GET', 'POST'])
def predict(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)