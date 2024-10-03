from datetime import datetime, timedelta

start_date = datetime(2024, 10, 3)
day_labels = [ "Oct 3" ]
hours_played_each_day = [ 2 ]
xp_per_hour = [ 405, 319 ]
xp = sum(xp_per_hour)

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
f.write('<table><tr><th>XP</th><th>Current Level</th><th>Hours Played</th><th>Avg. XP / Hour</th><th>Run Start Date</th><th>Days Elapsed</th><th>Avg. Hours / Day</th><th>Avg. XP / Day</th></tr>')
f.write('<td>' + str(xp) + '</td>')
f.write('<td>' + str(levelatxpn(xp)) + '</td>')
f.write('<td>' + str(len(xp_per_hour)) + '</td>')
if (len(xp_per_hour) > 0):
  f.write('<td>' + str(round(sum(xp_per_hour) / len(xp_per_hour), 2)) + '</td>')
else:
  f.write('<td>0</td>')
f.write('<td>' + start_date.strftime('%d %b %Y') + '</td>')
f.write('<td>' + str(days_elapsed) + '</td>')
f.write('<td>' + str(round(len(xp_per_hour) / days_elapsed, 2)) + '</td>')
f.write('<td>' + str(round(xp / days_elapsed, 2)) + '</td>')
f.write('</table>')
f.write('</div>')

# Info per series table
f.write('<div>')
f.write('<table><tr><td style="border: none;"><th>Completion</th><th>Expected Total Hours to Finish</th><th>Expected Date of Completion</th></tr>')
def print_time_to_finish_series(name, required_level):
  if sum(xp_per_hour) > 0:
    hours_estimate = int((xptoleveln(required_level) / sum(xp_per_hour)) * len(xp_per_hour))
    percentage = round((len(xp_per_hour) / hours_estimate) * 100.0, 2)
  else:
    hours_estimate = "?"
  f.write('<tr>')
  f.write('<th>' + name + '</th>')
  if hours_estimate != "?":
    f.write('<td style="width: 1000px;"><div style="background-color:lightgrey; width:100%;"><div style="float:left; margin-left:50%; margin-top:15px;">' + str(percentage) + '%</div><div style="background-color:#4287f5; width:' + str(percentage) + '%;">&nbsp</div></div></td>')
  else:
    f.write('<td></td>')
  f.write('<td>' + str(hours_estimate) + '</td>')
  if hours_estimate != "?":
    f.write('<td>' + str((start_date + timedelta(days=hours_estimate / avg_hours_per_day)).strftime('%d %b %Y')) + '</td>')
  else:
    f.write('<td></td>')
  f.write('</tr>')
print_time_to_finish_series('Breaking Bad', 69)
print_time_to_finish_series('Better Call Saul', 134)
print_time_to_finish_series('Metastises', 197)
f.write('</tr></table>')
f.write('</div>')

# XP/Hour graph
f.write('<h3 style="text-align:center;">XP Gained Each Hour Played</h3>')
f.write('<div id="canvasContainer" style="flex-grow:1;">')
f.write('<canvas id="canvas" style="background-color:lightgrey;"></canvas>')
f.write('</div>')
f.write(
"""<script>

function drawCanvas() {
  var xp_per_hour = """ + str(xp_per_hour) + """;
  var hours_played_each_day = """ + str(hours_played_each_day) + """;
  var day_labels = """ + str(day_labels) + """;
  var cc = document.getElementById("canvasContainer");
  var c = document.getElementById("canvas");
  c.width = cc.offsetWidth;
  c.height = cc.offsetHeight;
  var cw = c.width - 40;
  var ch = c.height - 40;
  var ctx = c.getContext("2d");
  ctx.lineWidth = 5;
  ctx.font = "20px Arial";
  ctx.textBaseline = "middle";

  ctx.fillStyle = "#cccccc";
  ctx.fillRect(0, 0, c.width, c.height);

  var stepx = cw / (xp_per_hour.length - 1);
  var max = Math.max(...xp_per_hour);
  var min = Math.min(...xp_per_hour);

  function calcWidth(i) {
    return i * stepx + 20;
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

  function getDayColor() {
    var rgb = hslToRgb((current_day * 0.417) % 1.0, 0.5, 0.5);
    return '#' + rgb[0].toString(16) + rgb[1].toString(16) + rgb[2].toString(16);
  }

  for (var i = 0; i < xp_per_hour.length; ++i) {
    ctx.strokeStyle = getDayColor(i);

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
      ctx.fillStyle = getDayColor(i);
    }
    hrs_per_day++;
  }

  current_day = -1;
  hrs_per_day = 0;
  for (var i = 0; i < xp_per_hour.length; ++i) {
    var x = calcWidth(i);
    var y = calcHeight(xp_per_hour[i]);

    if (current_day == -1 || hrs_per_day >= hours_played_each_day[current_day]) {
      current_day++;
      hrs_per_day = 0;

      if (current_day < day_labels.length) {
        var text = day_labels[current_day];
        var textWidth = ctx.measureText(text).width;

        ctx.beginPath();
        ctx.fillStyle = "#cccccc";
        ctx.fillRect(x, y + 20, textWidth, 18);
        ctx.stroke();

        ctx.beginPath();
        ctx.fillStyle = getDayColor(i);
        ctx.fillText(text, x, y + 30);
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
    var text = xp_per_hour[i].toString();
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