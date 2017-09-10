import base64,hashlib, urllib,api
import requests as request2
from flask import Flask, render_template, request
from wtforms import Form, StringField, TextAreaField, validators

app = Flask(__name__)

# global veriables
api_key = 'x2aGsyOtOUr3wnSDeUmqAShOpzFX.6DjLt'
secrete = 'q6bXiUd9QhacL8wJC_VhlNWjUQxnEJWT-uhhk2ag'
base_Url = 'https://api.ooyala.com/v2/'
part_2 = '?api_key=x2aGsyOtOUr3wnSDeUmqAShOpzFX.6DjLt&expires=1507412437&signature='
expires_t = '1507412437'





@app.route("/get_users")
def get_users():
    get_sig = sig_generator()
    params = {'api_key': api_key, 'expires': expires_t}
    sig = get_sig.generate_signature('q6bXiUd9QhacL8wJC_VhlNWjUQxnEJWT-uhhk2ag', 'get', '/v2/users/', params,
                                    '')
    request_url = base_Url + 'users/' + part_2 + sig
    print(request_url)
    response = request2.get(request_url)
    user_json = response.json()
    return render_template('get_users.html', user_json=user_json)


@app.route("/get_assets")
def get_assets():
    get_sig = sig_generator()
    params = {'api_key': api_key, 'expires': expires_t}
    sig = get_sig.generate_signature(secrete, 'get', '/v2/assets/', params,
                                     '')
    request_url = base_Url + 'assets/' + part_2 + sig
    print(request_url)
    response = request2.get(request_url)
    asset_json = response.json()
    return render_template('get_assets.html', asset_json=asset_json)


@app.route("/get_players")
def get_players():
    get_sig = sig_generator()
    params = {'api_key': api_key, 'expires': expires_t}
    sig = get_sig.generate_signature(secrete, 'get', '/v2/players/', params,
                                     '')
    request_url = base_Url + 'players/' + part_2 + sig
    print(request_url)
    response = request2.get(request_url)
    player_json = response.json()
    return render_template('get_players.html', player_json=player_json)


class PlayerForm(Form):
    title = StringField('Name', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route("/get_assets/<string:id>/", methods=['GET', 'POST'])
def set_asset(id):
    if request.method == 'POST':
        username = request.form['username']
        print username
      #  payload = {"name":str(username)}
        api_mod = api.OoyalaAPI(api_key,secrete)
        test = api_mod.patch('assets/' + id,{'name':username})
        if (test == None):
            return render_template('set_asset.html', test="Something went wrong")
        else:
            return  render_template('set_asset.html', test="Name changed")
    if request.method == 'GET':
        return render_template('set_asset.html', test=id)


@app.route("/disable_player_email/<string:id>/")
def disable_player_email(id):
    api_mod = api.OoyalaAPI(api_key, secrete)
    test = api_mod.patch('players/' + id,{ "ooyala_branding": {"twitter_sharing": "false"}})
    print str(test)
    get_sig = sig_generator()
    params = {'api_key': api_key, 'expires': expires_t}
    sig = get_sig.generate_signature(secrete, 'get', '/v2/players/', params,
                                     '')
    request_url = base_Url + 'players/' + part_2 + sig
    print(request_url)
    response = request2.get(request_url)
    player_json = response.json()
    return render_template('get_players.html', player_json=player_json)


@app.route("/enable_player_email/<string:id>/")
def enable_player_email(id):
        api_mod = api.OoyalaAPI(api_key,secrete)
        test = api_mod.patch('players/' + id,{ "ooyala_branding": {"twitter_sharing": "true"}})
        print str(test)
        get_sig = sig_generator()
        params = {'api_key': api_key, 'expires': expires_t}
        sig = get_sig.generate_signature(secrete, 'get', '/v2/players/', params,                                         '')
        request_url = base_Url + 'players/' + part_2 + sig
        print(request_url)
        response = request2.get(request_url)
        player_json = response.json()
        return render_template('get_players.html', player_json=player_json)


@app.route("/get_players/<string:id>/", methods=['GET', 'POST'])
def set_player(id):
    if request.method == 'POST':
        username = request.form['username']
        print username
      #  payload = {"name":str(username)}
        api_mod = api.OoyalaAPI(api_key,secrete)
        test = api_mod.patch('players/' + id,{'name':username})
        if (test == None):
            return render_template('set_player.html', test="Something went wrong")
        else:
            return  render_template('set_player.html', test="Name changed")
    if request.method == 'GET':
        return render_template('set_player.html', test=id)



        # get_sig = sig_generator()
        # params = {'api_key': api_key, 'expires': expires_t}
        # sig = get_sig.generate_signature(secrete, 'patch', '/v2/players/'+id+'/',
        #                                  params,
        #                                  str(payload))
        # request_url = base_Url + "players/" + str(id + '/') + part_2 + sig
        # print(request_url)
        # response = request2.patch(request_url,json=(payload))
        # id = response.json()
        # print id
        # if response.status_code==200:
        #     return 'Done'
        # else:
        #     return render_template('set_player.html', id=id)



class sig_generator(object):
    def generate_signature(self, secret_key, http_method, request_path, query_params, request_body):
        # type: (object, object, object, object, object) -> object

        signature = secret_key + http_method.upper() + request_path
        for key, value in sorted(query_params.iteritems()):
            signature += key + '=' + value
        signature = signature.encode('ascii')
        signature += request_body
        print signature
        signature = base64.b64encode(hashlib.sha256(signature).digest())[0:43]
        signature = urllib.quote_plus(signature)
        return signature


@app.route("/backlot_api")
def backlot_into():
    return render_template('backlot_welcome.html')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/welcome")
def welcome():
    return render_template('welcome.html')


@app.route("/phaseone")
def phaseone():
    return render_template('page_one.html')


@app.route("/phasetwo")
def phasetwo():
    return render_template('phase_2.html')


@app.route("/phasethree")
def phasethree():
    return render_template('phase_three_2.html')


@app.route("/pagetwo")
def pagetwo():
    return render_template('page_two.html')


if __name__ == "__main__":
    app.run(debug=True,port=80)
