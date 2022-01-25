import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
from docx import Document
from werkzeug.utils import secure_filename
from glob import glob
from io import BytesIO
from zipfile import ZipFile
from flask import flash
import flask
import shutil

pliki = 'uploads/'
app = Flask(__name__, static_url_path="", static_folder="uploads")
app.config['UPLOAD_FOLDER'] = pliki




@app.route('/up/<foldername>', methods=['GET', 'POST'])
def upload_file(foldername):

    if request.method == 'POST':
        if foldername != "main":
            if 'files' not in request.files:
                flash('No file part')
                return redirect(request.url)

            files = request.files.getlist('files')

            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],foldername, filename))
            return redirect('/df/'+foldername)
        else:
            if 'files' not in request.files:
                flash('No file part')
                return redirect(request.url)

            files = request.files.getlist('files')

            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/files')
    if foldername == "main":
        jkhaha = "Main folder :)"
    else:
        jkhaha = foldername

    return render_template('index.html',name=jkhaha)

@app.route("/df/<filename>", methods = ['GET','POST'])
def download_file(filename):
    if os.path.isdir(os.path.join("uploads",filename)):

            wartosc = ""
            if request.method == 'POST':

                # ref = request.form.get("Refresh")
                zgoda = request.form.get("Yes")
                serch = request.form.get("szykanie")

                if serch != "":
                    global hh
                    hh = serch
                else:
                    hh = None
                # if ref != None:
                # hh = ""
                if request.form.get('ds') != None:
                    wartosc = request.form.get('ds')

                elif request.form.get('dels') != None:
                    wartosc = request.form.get('dels')

                elif request.form.get('delall') != None:
                    flash("Are you sure you want to delete all items?")

                    wartosc = request.form.get('delall')

                elif request.form.get('dall') != None:
                    wartosc = request.form.get('dall')

                lista = request.form.getlist('pliki_zazanaczone')

                if lista != []:
                    if wartosc == "Delete_selected":
                        for i in lista:
                            pp = os.path.join("uploads",filename, i)
                            if os.path.isfile(pp):
                                os.remove(pp)
                            else:
                                shutil.rmtree(pp)

                        return redirect("/df/"+filename)

                    elif wartosc == "Download_selected":
                        lista_dier = []
                        for i in lista:
                            lista_dier.append(os.path.join("uploads",filename, i))
                        stream = BytesIO()
                        with ZipFile(stream, 'w') as zf:
                            for file in lista_dier:
                                zf.write(file, os.path.basename(file))
                        stream.seek(0)
                        return send_file(
                            stream,
                            as_attachment=True,
                            attachment_filename='archive.zip'
                        )
                elif zgoda == "Yes":

                    to_dell = os.listdir(os.path.join(pliki,filename))
                    if to_dell != []:
                        for i in to_dell:
                            pp = os.path.join("uploads",filename, i)
                            if os.path.isfile(pp):
                                os.remove(pp)
                            else:
                                shutil.rmtree(pp)

                    return redirect("/df/"+filename)


                elif wartosc == "Download_all":
                    lista_dier = []
                    to_d = os.listdir(os.path.join(pliki,filename))
                    for i in to_d:
                        lista_dier.append(os.path.join("uploads",filename, i))
                    stream = BytesIO()
                    with ZipFile(stream, 'w') as zf:
                        for file in lista_dier:
                            zf.write(file, os.path.basename(file))
                    stream.seek(0)
                    return send_file(
                        stream,
                        as_attachment=True,
                        attachment_filename='archive.zip'
                    )

            try:
                if hh != None:
                    serch = hh
                    print(serch)
                else:
                    serch = ""
            except:
                serch = ""

            # try:
            # gg = bb
            # except :
            # gg = False

            arr = []
            arr2 = os.listdir(os.path.join(pliki,filename))
            if arr2 == []:
                arr = []
                a = "Empty for now but you can make it full :)"
            else:
                if serch != "":
                    for b in arr2:
                        if (b.endswith(serch)):
                            arr.append(b)
                else:
                    arr = arr2
                a = ""

            return render_template('index5.html',name=filename, value=arr, alert=a, ip=flask.request.remote_addr)
    else:
        return render_template('index2.html',value=filename)

@app.route("/")
def main_menu():
    return redirect("/files")

@app.route("/files", methods = ['GET', 'POST'])
def files():


    wartosc = ""
    if request.method == 'POST':

        #ref = request.form.get("Refresh")
        zgoda = request.form.get("Yes")
        serch = request.form.get("szykanie")



        if serch != "":
            global hh
            hh = serch
        else:
            hh = None
        #if ref != None:
          #hh = ""
        if request.form.get('ds') != None :
            wartosc = request.form.get('ds')
            
        elif request.form.get('dels') != None :
            wartosc = request.form.get('dels')

        elif request.form.get('delall') != None :
            flash("Are you sure you want to delete all items?")

            wartosc = request.form.get('delall')

        elif request.form.get('dall') != None :
            wartosc = request.form.get('dall')

            
        lista = request.form.getlist('pliki_zazanaczone')



        if lista != []:
            if wartosc == "Delete_selected":
                for i in lista:
                    pp = os.path.join("uploads", i)
                    if os.path.isfile(pp):
                        os.remove(pp)
                    else:
                        shutil.rmtree(pp)

                return redirect("/files")

            elif wartosc == "Download_selected":
                lista_dier = []
                for i in lista:
                    lista_dier.append(os.path.join("uploads", i))
                stream = BytesIO()
                with ZipFile(stream, 'w') as zf:
                    for file in lista_dier:

                            if os.path.isdir(file):
                                plkongi = os.listdir(file)
                                for hhh in plkongi:
                                    zf.write(os.path.join(file, hhh), os.path.basename(os.path.join(file, hhh)))
                            else:
                                zf.write(file, os.path.basename(file))

                stream.seek(0)
                return send_file(
                    stream,
                    as_attachment=True,
                    attachment_filename='archive.zip'
                )
        elif zgoda == "Yes":


            to_dell = os.listdir("uploads")
            if to_dell != []:
                for i in to_dell:
                    pp = os.path.join("uploads", i)
                    if os.path.isfile(pp):
                        os.remove(pp)
                    else:
                        shutil.rmtree(pp)


            return redirect("/files")


        elif wartosc == "Download_all":
            lista_dier = []
            to_d = os.listdir("uploads")
            for i in to_d:
                lista_dier.append(os.path.join("uploads", i))
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in lista_dier:
                    zf.write(file, os.path.basename(file))
            stream.seek(0)
            return send_file(
                stream,
                as_attachment=True,
                attachment_filename='archive.zip'
            )
    try:
        if hh != None:
            serch = hh
            print(serch)
        else:
            serch = ""
    except:
        serch = ""

    #try:
        #gg = bb
    #except :
        #gg = False


    arr = []
    arr2 = os.listdir(pliki)
    if arr2 == []:
        arr =[]
        a = "Empty for now but you can make it full :)"
    else:
        if serch != "" :
            for b in arr2:
                if (b.endswith(serch)):
                    arr.append(b)
        else:
            arr = arr2
        a = ""

    return render_template('index3.html',value=arr,alert=a,ip=flask.request.remote_addr)
#/look/{{value}}

@app.route("/folder", methods = ['GET', 'POST'])
def folder_look():
    if request.method == "POST":
        foldername = request.form.get("foldername")
        path = os.path.join(pliki,foldername)
        os.mkdir(path)
        return redirect("/files")


    return render_template('home.html')



    

@app.route('/look/<filename>')
def lookup_files(filename):
    arr = []
    image = ""
    file_path = pliki + filename
    if filename.endswith(".docx") or filename.endswith(".DOCX"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            arr.append(para.text)
        str = ""

    elif filename.endswith(".txt") or filename.endswith(".TXT"):
        with open(file_path,'r',encoding='utf-8') as r:
            arr.append(r.read())
            r.close()
        str = ""
    elif filename.endswith(".jpg") or filename.endswith(".JPG")or filename.endswith(".PNG")or filename.endswith(".png")or filename.endswith(".GIF")or filename.endswith(".gif"):
        image = file_path
        str = ""
    else:
        str = "For now I can only read .txt and .docx files :("
        arr = []



    
    return render_template('index4.html',array = arr, alarm=str,name=filename,im=image)



@app.route('/delete-files/<filename>')
def delete_files_tut(filename):
    file_path = pliki + filename
    os.remove(file_path)
    return redirect("/files")



@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = pliki + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    app.secret_key = 'tajne'
    app.run(host='0.0.0.0', port=8081)