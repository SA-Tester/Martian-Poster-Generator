from crypt import methods
import flask
import tensorflow as tf

# load the model
model = tf.keras.models.load_model('model')

app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods = ["GET", "POST"])

def main():
    if flask.request.method == "GET":
        return (flask.render_template("main.html"))

    if flask.request.method == "POST":
        # color_me = []
        # for filename in os.listdir('images/black and white/256X256'):
        #         color_me.append(tf.keras.utils.img_to_array(tf.keras.utils.load_img('images/black and white/256X256/'+filename)))
        # color_me = np.array(color_me, dtype=float)
        # color_me = rgb2lab(1.0/255*color_me)[:,:,:,0]
        # color_me = color_me.reshape(color_me.shape+(1,))

        # Predict Images
        # output = model.predict(color_me)
        # output = output * 128

        # # Output colorizations
        # for i in range(len(output)):
        #     cur = np.zeros((256, 256, 3))
        #     cur[:,:,0] = color_me[i][:,:,0]
        #     cur[:,:,1:] = output[i]
        #     imsave("images/colored_results/img_"+str(i)+".jpg", lab2rgb(cur)*255)
        return

if __name__ == "__main__":
    app.run()