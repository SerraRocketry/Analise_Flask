import os

watched_files = []

print("")
print("* Watched:")
for path in [ "./templates", "./static/css", "./static/js" ]:
        for file in os.listdir(f"{path}"):
            print( f"\t{path}/{file}" )
            watched_files.append( f"{path}/{file}" )
print("")

bind = "0.0.0.0:8140"
accesslog = "persistence/logs/access.log"
errorlog = "persistence/logs/error.log"
workers = 2
reload = True
reload_extra_files = watched_files
