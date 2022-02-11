# pycad

Autocad automation cli for simple actions.

## Installation
Version of python `3.7`

`pip install -r requirements.txt`

## Usage

Main purpose is to execute defined actions by running:

`python main.py {action_name} {action_kwargs}`

For fetching the listing of all actions run:

`pyton main.py --help`

For each `action` you can also fetch more info about its keyword arguments by running:

`pyton main.py {some_action_name} --help`

If used action returns anything it will also be printed on standard output.

## Actions

### draw_square

Draws a square on the current Autocad drawing

### extract_rectangles

Extracts all rectangles from the current Autocad drawing

### iki_specification

Simple parser for evaluating python scripts defined in the passed config.json file e.g. 
```json
{
  "inputs": {
    "Please input A": "a",
    "Please input B": "b",
  },
  "outputs": {
    "c" : "a+b",
    "d" : "f'This is really a D {d}//n'"
  },
  "returns": "d"
}
```
This config will evaluate in asking user for inputs `a` and `b` by prompting bound dict keys,
evaluating `c` and `d` by the bound dict values as python expressions and then finally returning result specified in `returns` and store it in a file that was passed in the kwargs.

## Notes

- Each action that requires an Autocad session will fail if Autocad is not open.
- Each action that requires an Autocad session will fail it the current Autocad drawing is being used e.g. clicking on surface of the layer
or creating some object.
- iki_specification is pretty modular but will fail if the given expressions are invalid or are referencing something that has not yet been defined in the scope of the config.
- iki_specification won't work if `f` is used as an output binding e.g. you can see that `f1` was used in the source test.