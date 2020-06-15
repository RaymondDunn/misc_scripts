import requests
import os
import time


v = 1
seg = range(1, 2000)
delay = 0.05

payload = {}
headers = {}

output_dur = 'video_{}_output'.format(v)
try:
    os.mkdir(output_dur)
except FileExistsError as err:
    pass

with open(output_dur + '/filelist.txt.', 'w') as filelist:

    for s in seg:

        if s % 20 == 0:
            print('Segment {}'.format(s))

        # get general http request captured from postman, fill out as appropriate
        url = "https://cfvod.kaltura.com/scf/hls/p/1467031/sp/146703100/serveFlavor/entryId/0_eu2o3f9b/v/2/ev/3/flavorId/0_vfpkwa6i/name/a.mp4/seg-{}-v{}-a1.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTQ2NzAzMS9zcC8xNDY3MDMxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2V1Mm8zZjliL3YvMi9ldi8zL2ZsYXZvcklkLzBfdmZwa3dhNmkvbmFtZS9hLm1wNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTkxNjgwMzk3fX19XX0_&Signature=XmleBT4PSRIYpIjX7tiz8GJCOEX2T7Xe0Z26XCCIft1UMxE6d2aBY53fup3-mPEwxyKsOhut0viL1xCpEWRkf85~2cL5cg8ClvqynRlyeqpCxa9JQwyrTUOnmxK7g5cP2GrRaPb~wAxagisCBqF0iMKfER1mBeNB39BQ4NyakA3vyKrpQnE4HTTzomTDlJgkgbBXYTQyr0dtpBTBTYs9JolEmw94BtBQDZ9ClD0Y9aAXK6WauPIb4Ln5vythkKwLY4Rt9iq4zqo6BGl-wKFWITAdUywrFHbuR5zvsH~4ER~~cOguBI8S7gQTIbG6DkJO7B1vvhxd9aNGZYNQwggvrw__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A".format(s, v)

        response = requests.request("GET", url, headers=headers, data = payload)
        
        if response.ok:
            ct = response.content

            # write output data file
            output_fnum = str(s).zfill(10)
            output_fname = '{}.ts'.format(output_fnum)
            with open(output_dur + '/' + output_fname, 'wb') as f:
                f.write(ct)
                f.close()
                time.sleep(delay)

            # append entry to file list
            filelist.write("file '{}'\n".format(output_fname))

        else:
            break

    filelist.close()

## ffmpeg
# ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4