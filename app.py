from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
import sys

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def garage():

    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='garage')
    
    cursor=connection.cursor()

    bm_data=''
    yc_data=''
    tf_data=''
    
    if request.method=='POST':
        carmodel=request.form.get('carmodel')
        carbrand=request.form.get('carbrand')
        caryear=request.form.get('caryear')
        carcolor=request.form.get('carcolor')
        transmissiontype=request.form.get('transmissiontype').capitalize()
        fueltype=request.form.get('fueltype').capitalize()

        cursor.execute('INSERT INTO bm_of_car (brand, model) VALUES (%s, %s)', (carbrand, carmodel))
        bm_id=cursor.lastrowid
        cursor.execute('INSERT INTO yc_of_car (year, color, brand_model_id) VALUES (%s, %s, %s)', (caryear, carcolor, bm_id))
        cursor.execute('INSERT INTO tf_type_of_car (transmission, fuel, brand_model_id) VALUES (%s, %s, %s)', (transmissiontype, fueltype, bm_id))
        connection.commit()

        cursor.execute("SELECT bm_of_car.id, bm_of_car.brand, bm_of_car.model, tf_type_of_car.id, tf_type_of_car.transmission, tf_type_of_car.fuel, yc_of_car.id, yc_of_car.year, yc_of_car.color FROM bm_of_car LEFT JOIN tf_type_of_car ON bm_of_car.id = tf_type_of_car.brand_model_id LEFT JOIN yc_of_car ON bm_of_car.id = yc_of_car.brand_model_id;")
        bm_data = cursor.fetchall()
        print(bm_data)

        cursor.close()
        connection.close()
    return render_template('index.html',bm_data=bm_data)
app.run()