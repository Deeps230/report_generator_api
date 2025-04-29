import yaml
import os

def load_transformation_rules(path="config/transformation_rules.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)
