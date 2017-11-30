Rend
====

Rend visualizes spatial data and offers plugins for operations like
searching in circles, nearest k neighboors. Rend provides the cardinal which
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
Points also include a UUID with can be anykind of information the point represents.

### Plugin Example (Out-Dated)

Create a demo plugin inside the plugins folder `demo.py`

Then you need to create an index class with the following
methods: `add_points`, `intersection`, `nearest`

You also need to create a class variable named `GUI` which is
a dictionary with variables that can be configured from the user.
If there are no parameters then you just create an empty dictionary
like this `GUI = {}`.

Another class variable being used is the `VISUAL` variable. This variable
takes a boolean value and indicates if the index can be represented in the
cardinal window.

Example of our demo index should be like this.

```python
class DemoIndex:
    GUI = {"parameter1": 0, "parameter2": 0}
    VISUAL = True

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