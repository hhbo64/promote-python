import promote
from schema import Schema

USERNAME = "colin"
API_KEY = "789asdf879h789a79f79sf79s"
PROMOTE_URL = "https://sandbox.c.yhat.com/"

p = promote.Promote(USERNAME, API_KEY, PROMOTE_URL)

# load our ensemble model weights
from sklearn.externals import joblib
ENSEMBLE = joblib.load('./objects/ensemble.pkl')

# ensure that data sent to our model is only ints or floats
@promote.validate_json(Schema([[int, float]]))
def promoteModel(data):
    preds = ENSEMBLE.predict_proba(data).tolist()
    res = []
    for i in preds:
        res.append({"predicted": i})
    return res


TESTDATA = [[5.1, 3.5], [6.7, 3.1]]
promoteModel(TESTDATA)

# name and deploy our model
p.deploy("EnsembleClassifier", promoteModel, TESTDATA, confirm=True, dry_run=True, verbose=0)

# once our model is deployed and online, we can send data and recieve predictions
# p.predict("EnsembleClassifier", TESTDATA)