from app import app
import config

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

print "test"

print "test2"

print "dfdfdff"


app.run(

    	debug=config.DEBUG,
    	host="0.0.0.0",
    	port=int("800"),
	use_reloader=False
)
