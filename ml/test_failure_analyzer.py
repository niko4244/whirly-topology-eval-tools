import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class TestFailureAnalyzer:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.trained = False

    def fit(self, test_data: pd.DataFrame):
        X = test_data.drop("failure_type", axis=1)
        y = test_data["failure_type"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        self.trained = True
        print(f"Model accuracy: {self.model.score(X_test, y_test):.2f}")

    def predict(self, sample: dict):
        if not self.trained:
            raise ValueError("Model not trained.")
        features = pd.DataFrame([sample])
        return self.model.predict(features)[0]

    def recommend_action(self, failure_type):
        # Map failure type to recommended actions
        actions = {
            "timeout": "Increase test timeout or check resource utilization.",
            "flaky": "Enable test retries and log environment state.",
            "assertion": "Verify test setup and expected values.",
            "dependency": "Mock or isolate external dependencies.",
        }
        return actions.get(failure_type, "Review test failure in detail.")