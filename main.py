from functions import *

# Get user gender
user_gender = input("Enter your gender (m/f): ").lower()

# Get section and event
user_type = ""
while True:
    user_type = input("Enter your event type (enter h to see list of event types): ").lower()
    if user_type == "h":
        print("Event types:\n  - Running (r)\n  - Race Walking (rw)\n  - Jumping/Throwing/Decathlon (jtd)\n")
    else:
        break

user_surface = ""
user_section = ""
if user_type == "r" or user_type == "rw":
    user_surface = input("Track or road (t/r)? ").lower()
else:
    user_section = user_type

track_running_events = ["100m",  "200m",  "300m",  "400m",  "500m",  "100mH",  "400mH",  "4x100m",  "4x200m",  "4x400m",  "600m",  "800m",  "1000m",  "1500m",  "Mile",  "2000m",  "2000mSC",  "3000m",  "3000mSC",  "2 Miles",  "5000m",  "10,000m"]
road_running_events = ["5km", "10km", "15km", "10 Miles", "20km", "HM", "25km", "30km", "Marathon", "100km"]
track_race_walking_events = ["3000mW", "5000mW", "10,000mW", "15,000mW", "20,000mW", "30,000mW", "35,000mW", "50,000mW"]
road_race_walking_events = ["3kmW", "5kmW", "10kmW", "15kmW", "20kmW", "30kmW", "35kmW", "50kmW"]
jtd_events = ["HJ", "PV", "LJ", "TJ", "SP", "DT", "HT", "JT", "Decathlon"]

user_event = ""
while True:
    user_event = input("Enter your event (enter h to see list of events): ")
    if user_event == "h":
        events = []
        if user_type == "r":
            if user_surface == "t":
                print("Track Running Events:")
                events = track_running_events
            elif user_surface == "r":
                print("Road Running Events:")
                events = road_running_events
        elif user_type == "rw":
            if user_surface == "t":
                print("Track Race Walking Events:")
                events = track_race_walking_events
            elif user_surface == "r":
                print("Road Race Walking Events")
                events = road_race_walking_events
        elif user_type == "jtd":
            print("Jumping/Throwing/Decathlon Events:")
            events = jtd_events
        for event in events:
            print("  - " + event)
        print("")
    else:
        if user_type == "r":
            if user_surface == "t":
                if track_running_events.index(user_event) < 10:
                    user_section = "shr"
                elif track_running_events.index(user_event) < 16:
                    user_section = "md"
                else:
                    user_section = "lds"
            elif user_surface == "r":
                if road_running_events.index(user_event) < 5:
                    user_section = "rr1"
                else:
                    user_section = "rr2"
        elif user_type == "rw":
            if user_surface == "t":
                if track_race_walking_events.index(user_event) < 4:
                    user_section = "rwt1"
                else:
                    user_section = "rwt2"
            elif user_surface == "r":
                user_section = "rwr"
        break
user_final_section = user_gender + user_section

# Get user time
user_mark = input("Enter your mark: ")

# Get user points
user_points = get_points(user_final_section, user_event, user_mark)
if user_points == -1:
    print("No matching time")
    exit(0)
print(str(user_mark) + " for " + user_event + " is a score of " + str(user_points) + ", which is equivalently impressive to:")
for mark in get_equivalent_marks(user_points, user_gender):
    print("  - " + str(mark[0]) + " for " + mark[1])