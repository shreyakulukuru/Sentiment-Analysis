from flask import Flask, render_template_string, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Sentiment Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <style>
        body{
            background: -webkit-linear-gradient(#e6dfff, #fbf9ff);
            background:    -moz-linear-gradient(#e6dfff, #fbf9ff);
            background:         linear-gradient(#e6dfff, #fbf9ff);
            font-family: 'Trebuchet MS', sans-serif;
        }
        .input-box {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .pie-chart {
            display: block;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img src="{{ url_for('static', filename='logo.png') }}" height="70vh" alt="Your Logo"/>
                <img src="{{ url_for('static', filename='logo-name.png') }}" height="50vh" alt="Your Logo"/>
            </a>
            <div class="collapse navbar-collapse justify-content-end" id="navbarNav" style="color:black">
                <ul class="navbar-nav" >
                    <li class="nav-item" >
                        <a style="color:black!important;" class="nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item" >
                        <a style="color:black!important;" class="nav-link" href="#">About</a>
                    </li>
                    <li class="nav-item" >
                        <a style="color:black!important;" class="nav-link" href="#">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    

    <section class="pageHeader" style="background-color:transparent">
        <div class="container-fluid m-5" style="width: 100%;">
            <div class="row align-items-center">
                <div class="col-md-5">
                    <h1>Elevate Insights with Emotion Intelligence</h1>
                    <br>
                    <h5> Harness the magic of AI to decode sentiments, from joy to sadness, in real-time.</h5>
                </div>
                <div class="col-md-7 align-items-center mx-auto align-content-center text-center justify-content-center">
                    <img src="{{ url_for('static', filename='header_banner.jpg') }}" alt="" width=80%>
                </div>
            </div>
        </div>
    </section>
    <div class="container align-items-center justify-content-center" style="background-color:transparent">        
        <section class="inputSection">
        <form method="post">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="d-flex align-items-center col-md-9 align-items-center mx-auto align-content-center text-center justify-content-center">
                        <textarea name="sentence" placeholder="Enter a sentence" class="input-box" rows="4"></textarea>
                    </div>
                    <!--  align-items-center justify-content-center -->
                    <div class=" d-flex align-items-center col-md-3 align-items-center mx-auto align-content-center text-center justify-content-center">
                        <button type="submit" class="btn btn-primary">Analyze</button>
                    </div>
                </div>
            </div>
        </form>
    </section>
    <section class="outputSection" style="background-color:transparent">
    {% if sentiment %}
        <div class="container-fluid m-5 mx-auto" style="width: 80%;">
            <div class="row align-items-center">
                <div class="col-md-5">
                    <h4>Sentence: {{ sentence }}</h4>
                    <h3>Sentiment: {{ sentiment }}</h3>
                    <img src="{{ url_for('static', filename=sentiment +'.jpg') }}" alt="" width=88%>
                </div>
                <div class="col-md-7 align-items-center mx-auto align-content-center text-center justify-content-center">
                    <img src="data:image/png;base64,{{ chart }}" alt="Pie Chart" class="pie-chart" height=400px>
                </div>
            </div>
        </div>
    {% endif %}
    </section>
        
    </div>
</body>
</html>
"""

def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    pos = int(sentiment_dict['pos'] * 100)
    neg = int(sentiment_dict['neg'] * 100)
    neu = int(sentiment_dict['neu'] * 100)
    sentiment = ""
    if sentiment_dict['compound'] >= 0.05:
        sentiment = "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Create a pie chart
    fig = Figure()
    ax = fig.add_axes([0, 0, 1, 1])
    data_set = [pos, neg, neu]
    sentiment_labels = ["Positive", "Negative", "Neutral"]
    ax.pie(data_set, labels=sentiment_labels, autopct='%1.1f%%', explode=[0.02, 0.02, 0.02], shadow=True)
    ax.set_title("Sentiment Analysis")

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return sentiment, img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sentence = request.form['sentence']
        sentiment, chart = sentiment_scores(sentence)
        return render_template_string(html_template, sentence=sentence, sentiment=sentiment, chart=chart)
    return render_template_string(html_template, sentiment=None, chart=None)

if __name__ == '__main__':
    app.run(debug=True)