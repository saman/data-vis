var fs = require('fs');
var Canvas = require('canvas');
var outputFile = 'image.png';

// configs
var dataSize = 400;
var pixelSize = 1;
var boardSize = 600;
var margin = 100;
var axisX = 20;
var axisY = 530;
var axisH = 50;
var axisW = 20;

var dataCanvas = Canvas.createCanvas(dataSize, dataSize);
var dataCtx = dataCanvas.getContext('2d');
var boardCanvas = Canvas.createCanvas(boardSize, boardSize);
var boardCtx = boardCanvas.getContext('2d');
var min = 0;
var max = 0;

// opening the file
fs.open('./colorado_elev.vit', 'r', function (err, fd) {
  if (err) {
    throw err;
  }

  // allocate just byte for buffer
  var buffer = Buffer.alloc(1);

  // reading after 268 because of the header
  var pos = 268;

  // fill the data (here is 400*400 based on dataSize)
  for (var y = 0; y < dataSize; y += pixelSize) {
    for (var x = 0; x < dataSize; x += pixelSize) {

      // calculate min and max
      if (pos == 268) {
        min = buffer[0];
        max = buffer[0];
      }

      if (buffer[0] < min) {
        min = buffer[0];
      }

      if (buffer[0] > max) {
        max = buffer[0];
      }

      // reading a byte from the file
      var num = fs.readSync(fd, buffer, 0, 1, pos);
      if (num === 0) {
        break;
      }

      // set color to exact value
      dataCtx.fillStyle = `rgb(25, ${buffer[0]}, 25})`;

      // draw the pixel
      dataCtx.fillRect(x, y, pixelSize, pixelSize);

      // reading next byte
      pos++;
    }
  }

  // background
  boardCtx.fillStyle = 'white';
  boardCtx.rect(0, 0, boardSize, boardSize);
  boardCtx.fill();

  // put author's name
  boardCtx.textAlign = 'right';
  boardCtx.fillStyle = '#333';
  boardCtx.fillText('Saman Soltani', boardSize - 10, boardSize - 30);
  boardCtx.fillText('Paderborn University', boardSize - 10, boardSize - 20);
  boardCtx.fillText('Interactive Data Visualization', boardSize - 10, boardSize - 10);

  // merge board and data
  boardCtx.drawImage(dataCanvas, margin, margin);

  // 2D cordinate system
  boardCtx.lineWidth = 2;

  for (var i = 0; i < dataSize + 25; i += 25) {
    // top line
    x = i + margin - 1;
    y = margin - 5;
    boardCtx.fillRect(x, y, 1, 3);
    
    // top axis
    boardCtx.fillText(i, x + 5, y - 7);

    // left line
    x = margin - 5;
    y = i + margin - 1;
    boardCtx.fillRect(x, y, 3, 1);

    // left axis
    boardCtx.fillText(i, x - 5, y + 4);

    // right line
    x = dataSize + margin + 2;
    y = i + margin - 1;
    boardCtx.fillRect(x, y, 3, 1);

    // bottom line
    x = i + margin - 1;
    y = margin + dataSize + 3;
    boardCtx.fillRect(x, y, 1, 3);
  }

  // create the axis
  boardCtx.textAlign = 'left';
  boardCtx.fillText(min, axisX + axisW + 5, axisY + 5);
  boardCtx.fillText(max, axisX + axisW + 5, axisY + axisH + 5);

  // make gradient based on min and max of data
  var axisGradient = boardCtx.createLinearGradient(0, axisY, 0, axisY + axisH);
  axisGradient.addColorStop(0, `rgb(25, ${min}, 25)`);
  axisGradient.addColorStop(1, `rgb(25, ${max}, 25)`);
  boardCtx.fillStyle = axisGradient;
  boardCtx.fillRect(axisX, axisY, axisW, axisH);

  // saving the file
  out = fs.createWriteStream(`./${outputFile}`);
  stream = boardCanvas.pngStream();

  stream.on('data', function (chunk) { out.write(chunk); });
  stream.on('end', function () { console.log(`'${outputFile}' Saved!`); });

});
