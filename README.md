Overkill-bspwm
==============

Overkill-bspwm contains a BspwmSource that publishes bspwm status updates.
Specifically, it publishes monitor and desktop updates as follows:

Given:

```python
class Desktop:
  name
  focused
  occupied

class Monitor:
  name
  focused
```

BspwmSource publishes the following:

"monitors":
```python
[ Monator ] # all monitors
```

"desktops":
```python
[ Desktop ] # all desktops
```

("desktops", monitor\_name):
```python
[ Desktop ] # desktops in monitor_name
```


