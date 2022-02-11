import math
import json
from definitions import ROOT_DIR


def iki_specification(questions_input_path: str = f"{ROOT_DIR}/iki_config.json", output_file: str = "iki_output.txt"):
    with open(questions_input_path, "r") as fp:
        config = json.load(fp)

    # Needs more validation
    assert "inputs" in config and "outputs" in config and "returns" in config

    inputs = config["inputs"]
    outputs = config["outputs"]
    returns = config["returns"]

    assert isinstance(inputs, dict) and isinstance(outputs, dict) and isinstance(returns, str)
    assert returns in outputs

    bindings = dict()

    # Parse input
    for label, binding_key in inputs.items():
        while True:
            try:
                value_input = input(label)
                value_parsed = int(value_input)
            except ValueError:
                print("Enter a valid integer")
            except EOFError:
                print("Aborting")
                return
            else:
                bindings[binding_key] = value_parsed
                break

    # Bind inputs
    for key, value in bindings.items():
        to_execute = f"{key}={value}" if not isinstance(value, str) else f"{key}={repr(value)}"
        exec(to_execute)

    # Parse outputs
    for binding_key, expr in outputs.items():
        tmp = eval(expr)
        bindings[binding_key] = tmp

        to_execute = f"{binding_key}={tmp}" if not isinstance(tmp, str) else f"{binding_key}={repr(tmp)}"
        exec(to_execute)

    result = bindings[returns]

    with open(output_file, "w") as f:
        f.write(result)


if __name__ == "__main__":
    iki_specification()
