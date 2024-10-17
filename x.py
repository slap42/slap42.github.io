# player.removeallitems

# Vampire buffs to remove
# player.removespell ...
# 000f5b54
# 0010f1e7
# 000ed0a8
# 000ed09e
# 0010fb30
# 000ed0a3

from datetime import datetime, timedelta

# XP
xp_this_hour = sum([ 61, ])
xp_per_hour = [ 
  [ 412, 565, ],
  [ 349, 402, 598, 375, ],
  [ 463, 530, 493, 298, 401, 266, 322, ],
  [ 484, 285, 313, ],
  [ 316, 554, 439, 268, 182, ],
  [ 400, 209, 297, 365, ],
  [ 313, 494, 212, 314, 232, 200, 272, 333, 354, 289, ],
  [ ]
  ]

# Dates played
start_date = datetime(2024, 10, 9)
day_labels = [
  datetime(2024, 10,  9),
  datetime(2024, 10, 10),
  datetime(2024, 10, 11),
  datetime(2024, 10, 13),
  datetime(2024, 10, 14),
  datetime(2024, 10, 15),
  datetime(2024, 10, 16),
  ]
hours_played_each_day = [ ]
for x in xp_per_hour:
  hours_played_each_day.append(len(x))

# To be filled on completion of a sub-challenge
dates_completed = {
  # "Breaking Bad" : datetime(2025, 2, 17),
  }
hours_completed = {
  # "Breaking Bad" : 127,
  }

sum_xp_per_hour = 0
for x in xp_per_hour:
  sum_xp_per_hour += sum(x)
xp = xp_this_hour + sum_xp_per_hour

xp_per_hour_arr = []
for x in xp_per_hour:
  for y in x:
    xp_per_hour_arr.append(y)

print("xp_this_hour: " + str(xp_this_hour))

def xptoleveln(n):
  return 12.5 * n ** 2 + 62.5 * n - 75

def levelatxpn(n):
  level = 1000
  while xptoleveln(level) > n:
    level -= 1
  return level

days_elapsed = (datetime.now() - start_date).days + 1
avg_hours_per_day = len(xp_per_hour) / days_elapsed

f = open('index.html', 'w')
f.write('<html><body>')
f.write('<style>body { font-family:Arial; } th, td { border: 1px solid; } table { width: 100%; text-align: center; margin-bottom: 30px;}</style>')
f.write('<div style="display:flex; flex-flow:column; height:100%;">')

# Overall info table
f.write('<div>')
f.write('<table><tr><th>XP</th><th>Current Level</th><th>XP to Next Level</th><th>Hours Played</th><th>Avg. XP / Hour</th><th>Run Start Date</th><th>Days Elapsed</th><th>Avg. Hours / Day</th><th>Avg. XP / Day</th></tr>')
f.write('<td>' + str(xp) + '</td>')
f.write('<td>' + str(levelatxpn(xp)) + '</td>')
f.write('<td>' + str(-int(xp - xptoleveln(levelatxpn(xp) + 1))) + '</td>')
f.write('<td>' + str(len(xp_per_hour_arr)) + '</td>')
if (len(xp_per_hour_arr) > 0):
  f.write('<td>' + str(round(sum_xp_per_hour / len(xp_per_hour_arr), 2)) + '</td>')
else:
  f.write('<td>0</td>')
f.write('<td>' + start_date.strftime('%d %b %Y') + '</td>')
f.write('<td>' + str(days_elapsed) + '</td>')
f.write('<td>' + str(round(len(xp_per_hour_arr) / days_elapsed, 2)) + '</td>')
f.write('<td>' + str(round(xp / days_elapsed, 2)) + '</td>')
f.write('</table>')
f.write('</div>')

# Info per series table
f.write('<div>')
f.write('<table><tr><td style="border: none;"><th>XP to Complete</th><th colspan=2>Completion</th><th>Hours to Complete</th><th>Date of Completion</th></tr>')
def print_time_to_finish_series(name, required_level, color):
  percentage = 0
  if sum_xp_per_hour > 0:
    hours_estimate = int((xptoleveln(required_level) / sum_xp_per_hour) * len(xp_per_hour_arr))
    percentage = min(round((len(xp_per_hour_arr) / hours_estimate) * 100.0, 2), 100)
    if percentage == 100: hours_estimate = 0
  else:
    hours_estimate = "?"
  f.write('<tr>')
  f.write('<th>' + name + '</th>')
  f.write('<td>' + str(int(xptoleveln(required_level))) + '</td>')
  f.write('<td>' + str(percentage) + '%</td>')
  if hours_estimate != "?":
    f.write('<td style="width: 1000px;"><div style="background-color:lightgrey; height:100%; width:100%;"><div style="background-color:' + color + '; width:' + str(percentage) + '%;">&nbsp</div></div></td>')
  else:
    f.write('<td></td>')
  if name in hours_completed:
    f.write('<td>' + str(hours_completed[name]) + '</td>')
  else:
    f.write('<td>' + str(hours_estimate) + ' (Est.)</td>')
  if hours_estimate != "?":
    if name in dates_completed:
      f.write('<td>' + str((dates_completed[name]).strftime('%d %b %Y')) + '</td>')
    else:
      f.write('<td>' + str((start_date + timedelta(days=hours_estimate / avg_hours_per_day)).strftime('%d %b %Y')) + ' (Est.)</td>')
  else:
    f.write('<td></td>')
  f.write('</tr>')
print_time_to_finish_series('Breaking Bad', 69, "#369457")
print_time_to_finish_series('Better Call Saul', 137, "#ab5454")
print_time_to_finish_series('Metastises', 200, "#fcba03")
f.write('</tr></table>')
f.write('</div>')

# XP/Hour graph
day_labels_str = []
for d in day_labels:
  day_labels_str.append(d.strftime('%d %b %Y'))

f.write('<h3 style="text-align:center;">XP Gained Each Hour Played</h3>')
f.write('<div id="canvasContainer" style="flex-grow:1;">')
f.write('<canvas id="canvas" style="background-color:lightgrey;"></canvas>')
f.write('</div>')
f.write(
"""<script>

function drawCanvas() {
  var xp_per_hour = """ + str(xp_per_hour_arr) + """;
  var hours_played_each_day = """ + str(hours_played_each_day) + """;
  var day_labels = """ + str(day_labels_str) + """;
  var cc = document.getElementById("canvasContainer");
  var c = document.getElementById("canvas");
  c.width = cc.offsetWidth;
  c.height = cc.offsetHeight;
  var cw = c.width - 40;
  var ch = c.height - 60;
  var ctx = c.getContext("2d");
  ctx.lineWidth = 5;
  ctx.font = "20px Arial";
  ctx.textBaseline = "middle";

  ctx.fillStyle = "#cccccc";
  ctx.fillRect(0, 0, c.width, c.height);

  var stepx = cw / (xp_per_hour.length);
  var max = Math.max(...xp_per_hour);
  var min = Math.min(...xp_per_hour);

  function calcWidth(i) {
    return (i + 1) * stepx + 20;
  }

  function calcHeight(xp) {
    var r = (xp - min) / (max - min);
    return ch - r * ch + 20;
  }

  function hslToRgb(h, s, l) {
    let r, g, b;

    if (s === 0) {
      r = g = b = l; // achromatic
    } else {
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hueToRgb(p, q, h + 1/3);
      g = hueToRgb(p, q, h);
      b = hueToRgb(p, q, h - 1/3);
    }

    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
  }

  function hueToRgb(p, q, t) {
    if (t < 0) t += 1;
    if (t > 1) t -= 1;
    if (t < 1/6) return p + (q - p) * 6 * t;
    if (t < 1/2) return q;
    if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
    return p;
  }

  var current_day = -1;
  var hrs_current_day = 0;
  if (hours_played_each_day[0] > 0) {
    hours_played_each_day[0]--;
  }

  function getDayColor(day) {
    var rgb = hslToRgb((day * 0.417) % 1.0, 0.5, 0.5);
    var color = '#' + rgb[0].toString(16) + rgb[1].toString(16) + rgb[2].toString(16);
    return color;
  }

  if (xp_per_hour.length > 0) {
    ctx.beginPath();
    ctx.strokeStyle = getDayColor(0);
    ctx.moveTo(calcWidth(-1), calcHeight(min)); 
    ctx.lineTo(calcWidth(0), calcHeight(xp_per_hour[0]));
    ctx.stroke();
  }

  for (var i = 0; i < xp_per_hour.length; ++i) {
    ctx.strokeStyle = getDayColor(current_day);

    ctx.beginPath();

    var oi = i - 1 < 0 ? 0 : i - 1;
    var ox = calcWidth(oi);
    var oy = calcHeight(xp_per_hour[oi]);
    ctx.moveTo(ox, oy); 

    var x = calcWidth(i);
    var y = calcHeight(xp_per_hour[i]);
    ctx.lineTo(x, y);
    ctx.stroke();

    if (current_day == -1 || hrs_per_day >= hours_played_each_day[current_day]) {
      current_day++;
      hrs_per_day = 0;
      ctx.fillStyle = getDayColor(current_day);
    }
    hrs_per_day++;
  }

  current_day = -1;
  hrs_per_day = 0;
  for (var i = 0; i < xp_per_hour.length; ++i) {
    if (current_day == -1 || hrs_per_day >= hours_played_each_day[current_day]) {
      var x = calcWidth(i);
      var y = calcHeight(xp_per_hour[i]);
      if (current_day == -1) {
        x = calcWidth(-1);
        y = calcHeight(min);
      }

      current_day++;
      hrs_per_day = 0;

      if (current_day < day_labels.length) {
        var text = day_labels[current_day];
        var textWidth = ctx.measureText(text).width;

        ctx.beginPath();
        ctx.fillStyle = "#cccccc";
        ctx.fillRect(x, y + 10, textWidth, 18);
        ctx.stroke();

        ctx.beginPath();
        ctx.fillStyle = getDayColor(current_day);
        ctx.fillText(text, x, y + 20);
        ctx.stroke();
      }
    }

    hrs_per_day++;
  }

  ctx.beginPath();
  ctx.fillStyle = "#000000";
  for (var i = 0; i < xp_per_hour.length; ++i) {
    var x = calcWidth(i);
    var y = calcHeight(xp_per_hour[i]);
    var text = xp_per_hour[i];
    var textWidth = ctx.measureText(text).width;
    ctx.fillText(text, x - textWidth / 2, y);
  }
  ctx.stroke();
}

drawCanvas();
window.addEventListener("resize", drawCanvas);

</script>""")

f.write('</div>')
f.write('</body></html>')
f.close()