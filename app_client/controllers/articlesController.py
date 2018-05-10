from flask import (render_template, redirect)
import requests


def articlesGet(id, request):
    url = "http://localhost:5000/articles/" + str(id) + "/show"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('articles.html', error=error['message'], id=id)
    else:
        response = response.json()
        return render_template('articles.html', articles=response, id=id)


def articleCreateGet(id):
    return render_template('articleCreate.html', id=id)


def articleCreatePost(id, request):

    url = "http://localhost:5000/articles/" + str(id) + "/create"

    payload = "title=" + request.form['title'] + "&body=" + request.form['body']
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('articleCreate.html', error=error['message'])
    else:
        return render_template('articleCreate.html', id=id)


def articlesAdminGet(id, request):

    url = "http://localhost:5000/articles/" + str(id) + "/admin"

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }

    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('articlesAdmin.html', error=error['message'], id=id)
    else:
        response = response.json()
        articles = response
        return render_template('articlesAdmin.html', articles=articles, id=id)


def articlesAdminDelete(id, request):

    url = "http://localhost:5000/articles/" + str(id) + "/admin"

    payload = "article_id=" + request.form['delete']

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'x-access-token': request.cookies.get('token')
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)
    if response.status_code != 200:
        error = response.json()
        return render_template('articlesAdmin.html', error=error['message'])
    else:
        return redirect("http://localhost:3000/" + str(id) + "/articlesAdmin")
