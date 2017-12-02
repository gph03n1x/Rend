Rend
====

Rend visualizes spatial data and offers plugins for operations like
searching in circles, nearest k neighbors. Rend provides the cardinal which
visualizes in the 2d space the points and the gui tools which provide the interface
needed to change/configure spatial indexes and search them.

### Images
![Cardinal][cardinal]
![Gui controls][rend_main]

### Data generation

Along with rend there is a script `generate.py` used for point generation.
The following command:
```bash
python generate.py points.dat 1000 -2000 2000
```
Creates 1000 random points ranging from -2000,-2000 to 2000,2000 and saves them in `points.dat`.
Points also include a UUID which can be any kind of information the point represents.

### Http access

### Plugin Example

Create a demo plugin inside the plugins folder `demo.py`

Then you need to create an index class with the following
methods: `add_points`.

We create the `PARAMETERS` class variable which is essential a dictionary.
* The `visual` value represents as a boolean if the data you have should be displayed using rend's cardinal.
* The `elements` value tells the rend gui that this plugin needs two variables named `Param1` and `Param2` and that
they should be visualized through the `LabelEditFloat` and `LabelEditString`.
* The `data` value is a bunch of placeholder values and that's where the user values are stored.

Components included are
* LabelEditFloat
* LabelEditString
* PointEdit


Let's say our class has two methods we want to expose to the user
`intersection` and `nearest`. From the `ACTIONS` class variable we can do that.
We name each action and we define in the `action` field the name of the method we are going to expose.
Like the `PARAMETERS` class variable we create an `elements` field and a `data` field.
Notice that `PointEdit` has its value separated by comma because we are defining multidimensional variables.
Also the elements are named after the method's parameters, in order to match them.

Example of our demo index should be like this.

```python
class DemoIndex:
    PARAMETERS = {
        "visual": True,
        "elements": {
            "Param1": "LabelEditFloat",
            "Param2": "LabelEditString"
        },

        "data": {
            "Param1": 1000,
            "Param2": "hey"
        },

    }
    ACTIONS = {
        "Point Intersection": {
            "action": "inside_circle",
            "elements": {
                "x,y": "PointEdit",
                "r": "LabelEditFloat"
            },
            "data": {}
        },
        "Nearest K": {
            "action": "nearest",
            "elements": {
                "x,y": "PointEdit",
                "k": "LabelEditFloat"
            },
            "data": {}
        }

    }

    def add_points(self, points):
        pass

    def intersection(self, x, y, r):
        return []

    def nearest(self, x, y, k):
        return []
````

Finally you have to load it in the `config.py`. Add the following lines.

```python
from plugins.demo import DemoIndex
PLUGINS["Demo"] = DemoIndex
```

### Testing

Tests the quadtree results if they are the same as exudative searching.

```bash
python rend.py -t
```

[rend_main]: https://raw.githubusercontent.com/gph03n1x/Rend/master/images/rend.png "Main gui of rend"
[cardinal]: https://raw.githubusercontent.com/gph03n1x/Rend/master/images/cardinal.png "Cardinal"