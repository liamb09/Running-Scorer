import PyPDF2
import math

# Open and read PDF
scoring_pdf = open("worldAthleticsScoringTables.pdf", "rb")
pdf_reader = PyPDF2.PdfReader(scoring_pdf)

def remove_whitespace (page):
    cnt = 0
    result = []
    while cnt < len(page):
        if page[cnt] != "":
            result.append(page[cnt])
        if cnt < len(page)-1:
            if (page[cnt] == "2" or page[cnt] == "10") and page[cnt+1] == "Miles":
                result[len(result)-1] += " Miles"
                cnt += 1
        cnt += 1
    return result

def get_rows (page, num_columns):
    result = []
    for i in range(0, len(page)):
        if i % num_columns == 0:
            result.append([])
        #print(page)
        if i < num_columns:
            result[0].append(page[i])
        else:
            result[len(result)-1].append(time_to_seconds(page[i]))
    return result

def time_to_seconds (time):
    if time != "-":
        num_places = len(time.split(":"))-1
        seconds = 0.0
        for place in time.split(":"):
            seconds += float(place) * (60 ** num_places)
            num_places -= 1
        return seconds
    return time

def seconds_to_time(seconds):
    result = ""
    if seconds >= 3600:
        result += str(math.floor(seconds/3600)) + ":"
    if seconds >= 60:
        minutes = math.floor((seconds%3600)/60)
        if minutes == 0:
            result += "00:"
        elif minutes < 10:
            result += "0" + str(minutes) + ":"
        else:
            result += str(minutes) + ":"
        num_seconds = seconds % 60
        if num_seconds == 0:
            result += "00"
        elif num_seconds < 10:
            result += "0" + str(num_seconds)
        else:
            result += str(num_seconds)
    else:
        result = str(seconds)
    if result.find(".") != -1:
        result = result.split(".")[0] + "." + result.split(".")[1][:2]
    return result

def get_pages_range (first, last, num_columns):
    """Returns a list of rows from pages [first, last)"""
    pages = []
    for i in range (first, last):
        raw_page = pdf_reader.pages[i].extract_text().split("\n")[1]
        current_page = raw_page[raw_page.index(" ")+1:]
        page_rows = get_rows(remove_whitespace(current_page.split(" ")), num_columns)
        pages.append(page_rows)
    return pages

def get_all_pages (section):
    """
    Returns a list of all the rows of all the pages of a specified section.
    Section names are as follows (add m or w to beginning to specify gender):
        - Sprints, Hurdles, and Relays              = shr
        - Middle Distances                          = md
        - Long Distances and Steeplechase           = lds
        - Road Running - Part I                     = rr1
        - Road Running - Part II                    = rr2
        - Race Walking on Road                      = rwr
        - Race Walking on Track - Part I            = rwt1
        - Race Walking on Track - Part II           = rwt2
        - Jumping and Throwing events and Decathlon = jtd
    """
    page_offset = 0 # to add to change to women
    if section[0] == "w":
        page_offset = 270
    starting_numbers = {
        "shr": 8,
        "md": 38,
        "lds": 68,
        "rr1": 98,
        "rr2": 128,
        "rwr": 158,
        "rwt1": 188,
        "rwt2": 218,
        "jtd": 248
    }
    num_columns = {
        "shr": 11,
        "md": 7,
        "lds": 7,
        "rr1": 6,
        "rr2": 6,
        "rwr": 9,
        "rwt1": 5,
        "rwt2": 5,
        "jtd": 10
    }
    starting_page = starting_numbers.get(section[1:]) + page_offset
    return get_pages_range(starting_page, starting_page + 28, num_columns.get(section[1:]))

def get_points (section, event, mark):
    pages = get_all_pages(section)
    mark_num = time_to_seconds(mark)
    closest_mark = -1
    closest_mark_diff = 10000000
    for page in pages:
        points_column = page[0].index("Points")
        event_column = page[0].index(event)
        for row in page[1:]:
            if row[event_column] != "-":
                diff = row[event_column] - mark_num
                if 0 < diff < closest_mark_diff:
                    closest_mark = row[points_column]
                    closest_mark_diff = diff
    return closest_mark

def get_equivalent_marks (points, gender):
    sections = ["shr", "md", "lds", "rr1", "rr2", "rwr", "rwt1", "rwt2", "jtd"]
    marks = []
    for section in sections:
        for page in get_all_pages(gender + section):
            points_column = page[0].index("Points")
            for row in page[1:]:
                if row[points_column] == points:
                    cnt = 0
                    if points_column == 0:
                        events = row[1:]
                        cnt = 1
                    else:
                        events = row[:len(row)-1]
                    for event in events:
                        if event != "-":
                            if page[0][cnt] != "Decathlon":
                                marks.append([seconds_to_time(event), page[0][cnt]])
                            else:
                                marks.append([event, page[0][cnt]])
                        cnt += 1

    return marks