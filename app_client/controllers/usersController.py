from flask import (render_template, redirect, make_response)
import requests


def userAdminGet(id, request):

    url = "http://localhost:5000/auth/" + str(id) + "/update"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('userAdmin.html', error=error['message'], id=id)
    else:
        response = response.json()
        return render_template('userAdmin.html', users=response, id=id)


def userAdminPut(id, request):
    url = "http://localhost:5000/auth/" + str(id) + "/update"
    payload = "username=" + request.form['username'] + '&email=' + request.form['email'] + '&password=' + request.form['password']
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }

    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('userAdmin.html', error=error['message'])
    else:
        return redirect('http://localhost:3000/' + str(id) + '/userAdmin')


def userAdminDelete(id, request):

    url = "http://localhost:5000/auth/" + str(id) + "/update"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }
    response = requests.request("DELETE", url, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('userAdmin.html', error=error['message'])
    else:
        return redirect('http://localhost:3000/login')


def userLoginForm():
    return render_template('login.html')


def userLoginPost(request):

    url = "http://localhost:5000/auth/login"

    payload = "username=" + request.form['username'] + "&password=" + request.form['password']
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('login.html', error=error['message'])
    else:
        response = response.json()
        id = response[0]['id']
        token = response[0]['token']
        res = make_response(redirect('http://localhost:3000/' + id + '/articles'))
        res.set_cookie('token', token, max_age=10 * 3600)
        return res


def userRegisterForm():
    return render_template('register.html')


def userRegisterMake(request):

    url = "http://localhost:5000/auth/register"

    payload = "username=" + request.form['username'] + "&email=" + request.form['email'] + "&password=" + request.form['password']

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code != 200:
        response = response.json()
        error = response['message']
        return render_template('register.html', error=error)

    return redirect('http://localhost:3000/login')


def userLogout():
    res = make_response(redirect('http://localhost:3000/login'))
    res.set_cookie('token', '', max_age=10 * 3600)
    return res
