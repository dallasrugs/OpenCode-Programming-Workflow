def blocked(busy=False, active=False, conflict=False, paused=False, dirty=False):
    return busy or active or conflict or paused
