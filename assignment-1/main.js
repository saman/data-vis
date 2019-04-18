var fs = require('fs');
var Canvas = require('canvas');
var chroma = require('chroma-js');
var outputFile = __dirname + '/image.png';
var sourceFile = __dirname + '/field2.irreg';

// configs
var scale = 5000;
var dataSize = 5000;
var boardSize = 6000;
var boardSizeHeight = 7000;
var margin = 500;
var axisX = margin;
var axisY = margin + dataSize + 400;
var axisH = 100;
var axisW = 5000;

var min = 0;
var max = 0;

var dataCanvas = Canvas.createCanvas(dataSize, dataSize);
var dataCtx = dataCanvas.getContext('2d');
var boardCanvas = Canvas.createCanvas(boardSize, boardSizeHeight);
var boardCtx = boardCanvas.getContext('2d');


// fix cordination of html canvas
dataCtx.translate(0, dataCanvas.height);
dataCtx.scale(1, -1);

// opening the file
fs.readFile(sourceFile, 'utf8', (err, data) => {
  if (err) {
    throw err;
  }

  // get data base on enter
  data = data.split('\n');

  var colors = ['#2C5F77', '#3C809F', '#48A0C9', '#4AA487', '#53B8A0', '#78EFBF', '#FAD649', '#F5B76E', '#F18E35', '#E06339', '#EC5745', '#B83129', '#922D61'];
  var fcolors = chroma.scale(colors).domain([0, scale]);

  dataCtx.lineWidth = 5;

  for (var i=7; i < data.length; i++) {
    if (data[i] !== undefined) {

      // get current line and scale each element
      var line = data[i].split(' ').map(x => parseInt(parseFloat(x) * scale));

      var pos_x = line[0];
      var pos_y = line[1];
      var mov_u = line[3];
      var mov_v = line[4];

      var new_pos_x = mov_u + pos_x;
      var new_pos_y = mov_v + pos_y;

      var a = pos_x - new_pos_x;
      var b = pos_y - new_pos_y;
      var length = Math.sqrt(a * a + b * b);

      // calculate min and max
      if (i == 7) {
        min = length;
        max = length;
      }

      if (length < min) {
        min = length;
      }

      if (length > max) {
        max = length;
      }

      dataCtx.strokeStyle = fcolors(length);

      drawLineWithArrowhead(dataCtx, { x: pos_x, y: pos_y }, { x: new_pos_x, y: new_pos_y }, 30);
    }
  }

  // background
  boardCtx.fillStyle = 'white';
  boardCtx.rect(0, 0, boardSize, boardSizeHeight);
  boardCtx.fill();

  // put author's name
  boardCtx.font = 'normal 100px sans-serif';
  boardCtx.textAlign = 'right';
  boardCtx.fillStyle = '#333';
  boardCtx.fillText('Saman Soltani', boardSize - 100, boardSizeHeight - 300);
  boardCtx.fillText('Paderborn University', boardSize - 100, boardSizeHeight - 200);
  boardCtx.fillText('Interactive Data Visualization', boardSize - 100, boardSizeHeight - 100);

  // merge board and data
  boardCtx.drawImage(dataCanvas, margin, margin);


  // 2D cordinate system
  for (var i = 0; i < scale + 25; i += 500) {
    // top line
    x = i + margin - 10;
    y = margin - 50;
    boardCtx.fillRect(x, y, 10, 30);

    boardCtx.textAlign = 'center';
    // top axis
    boardCtx.fillText(i / scale, x + 10, dataSize + y + 210);

    // left line
    x = margin - 50;
    y = i + margin - 10;
    boardCtx.fillRect(x, y, 30, 10);

    boardCtx.textAlign = 'right';
    // left axis
    boardCtx.fillText(i / scale, x - 50, boardSize - y + 20);

    // right line
    x = dataSize + margin + 20;
    y = i + margin - 10;
    boardCtx.fillRect(x, y, 30, 10);

    // bottom line
    x = i + margin - 10;
    y = margin + scale + 20;
    boardCtx.fillRect(x, y, 10, 30);
  }

  // create the axis
  boardCtx.textAlign = 'left';
  boardCtx.fillText(min / scale, axisX - 100, axisY + 80);
  boardCtx.fillText(max / scale, axisX + axisW + 50, axisY + 80);
  boardCtx.fillText('Length', (axisX + axisW) / 2, axisY + 200);

  // make gradient based on colors
  var axisGradient = boardCtx.createLinearGradient(0, 0, axisW, 0);
  for (k = 0; k < scale; k += scale / 10) {
    var color = fcolors(k).rgb();
    axisGradient.addColorStop(k / 5000, `rgb(${color[0]}, ${color[1]}, ${color[2]}`);
  }

  boardCtx.fillStyle = axisGradient;
  boardCtx.fillRect(axisX, axisY, axisW, axisH);


  // saving the file
  out = fs.createWriteStream(outputFile);
  stream = boardCanvas.pngStream();

  stream.on('data', function (chunk) { out.write(chunk); });
  stream.on('end', function () { console.log(`'${outputFile}' Saved!`); });

});


function drawLineWithArrowhead(ctx, p0, p1, headLength) {

  // constants (could be declared as globals outside this function)
  var PI = Math.PI;
  var degreesInRadians225 = 225 * PI / 180;
  var degreesInRadians135 = 135 * PI / 180;

  // calc the angle of the line
  var dx = p1.x - p0.x;
  var dy = p1.y - p0.y;
  var angle = Math.atan2(dy, dx);

  // calc arrowhead points
  var x225 = p1.x + headLength * Math.cos(angle + degreesInRadians225);
  var y225 = p1.y + headLength * Math.sin(angle + degreesInRadians225);
  var x135 = p1.x + headLength * Math.cos(angle + degreesInRadians135);
  var y135 = p1.y + headLength * Math.sin(angle + degreesInRadians135);

  // draw line plus arrowhead
  ctx.beginPath();
  // draw the line from p0 to p1
  ctx.moveTo(p0.x, p0.y);
  ctx.lineTo(p1.x, p1.y);
  // draw partial arrowhead at 225 degrees
  ctx.moveTo(p1.x, p1.y);
  ctx.lineTo(x225, y225);
  // draw partial arrowhead at 135 degrees
  ctx.moveTo(p1.x, p1.y);
  ctx.lineTo(x135, y135);
  // stroke the line and arrowhead
  ctx.stroke();
}
