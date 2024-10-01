from datetime import datetime, timedelta

start_date = datetime(2024, 9, 27)
xp_per_hour = [ 536, 363, 290, 306, 527, 451, 666, 493, 131, 172, 275, 316, 221, 381, 302, 323, 119, 579, 170 ] 
xp = sum(xp_per_hour)

def xptoleveln(n):
  return 12.5 * n ** 2 + 62.5 * n - 75

def levelatxpn(n):
  level = 1000
  while xptoleveln(level) > n:
    level -= 1
  return level

days_elapsed = (datetime.now() - start_date).days + 1
hours_per_day = len(xp_per_hour) / days_elapsed

f = open('index.html', 'w')
f.write('<html><body>')
f.write('<style>body { font-family:Arial; } th, td { border: 1px solid; } table { width: 100%; text-align: center; margin-bottom: 50px;}</style>')

# Overall info table
f.write('<table><tr><th>XP</th><th>Current Level</th><th>Hours Played</th><th>Avg. XP / Hour</th><th>Run Start Date</th><th>Days Elapsed</th><th>Avg. Hours / Day</th><th>Avg. XP / Day</th></tr>')
f.write('<td>' + str(xp) + '</td>')
f.write('<td>' + str(levelatxpn(xp)) + '</td>')
f.write('<td>' + str(len(xp_per_hour)) + '</td>')
f.write('<td>' + str(round(sum(xp_per_hour) / len(xp_per_hour), 2)) + '</td>')
f.write('<td>' + start_date.strftime('%d %b %Y') + '</td>')
f.write('<td>' + str(days_elapsed) + '</td>')
f.write('<td>' + str(round(len(xp_per_hour) / days_elapsed, 2)) + '</td>')
f.write('<td>' + str(round(xp / days_elapsed, 2)) + '</td>')
f.write('</table>')

# Info per series table
f.write('<table><tr><td style="border: none;"><th>Completion</th><th>Expected Total Hours to Finish</th><th>Expected Date of Completion</th></tr>')
def print_time_to_finish_series(name, required_level):
  hours_estimate = int((xptoleveln(required_level) / sum(xp_per_hour)) * len(xp_per_hour))
  f.write('<tr>')
  f.write('<th>' + name + '</th>')
  percentage = round((len(xp_per_hour) / hours_estimate) * 100.0, 2)
  f.write('<td style="width: 1000px;"><div style="background-color:lightgrey; width:100%;"><div style="float:left; margin-left:50%; margin-top:15px;">' + str(percentage) + '%</div><div style="background-color:darkviolet; width:' + str(percentage) + '%;">&nbsp</div></div></td>')
  f.write('<td>' + str(hours_estimate) + '</td>')
  f.write('<td>' + str((start_date + timedelta(days=hours_estimate / hours_per_day)).strftime('%d %b %Y')) + '</td>')
  f.write('</tr>')

print_time_to_finish_series('Breaking Bad', 69)
print_time_to_finish_series('Better Call Saul', 134)
print_time_to_finish_series('Metastises', 197)
f.write('</tr></table></body></html>')

# XP/Hour graph
f.write('<table><tr><th colspan=' + str(len(xp_per_hour)) + '>XP Gained Each Hour Played</th></tr><tr>')
max = max(xp_per_hour)
for h in xp_per_hour:
  colheight = (h / max) * 720
  f.write('<td style="height: 720px; border: none;">')
  f.write('<div style="background-color:cornflowerblue; margin-top:' + str(720 - colheight) + ';height:' + str(colheight) + 'px;">' + str(h) + '</div>')
  f.write('</td>')
f.write('</table>')

f.close()