

CONFIG = {
    "green_time"  : 30,     # seconds
    "red_time"    : 20,
    "yellow_time" : 5,
    "threshold"   : 0.6,    # sensor sensitivity 0-1
    "sample_rate" : 44100,
    "directions"  : ["North", "South", "East", "West"],
    "log_file"    : "traffic_log.json",

    
    "gpio": {
        "North": (23, 24),
        "South": (25, 8),
        "East" : (7,  1),
        "West" : (12, 16)
    }
}
