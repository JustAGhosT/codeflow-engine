import json
from codeflow_engine.config.settings import CodeFlowSettings

def generate_schema():
    schema = CodeFlowSettings.model_json_schema()
    with open("/app/codeflow-desktop/src/schema.json", "w") as f:
        json.dump(schema, f, indent=2)

if __name__ == "__main__":
    generate_schema()
