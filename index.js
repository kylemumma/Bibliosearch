let capture;
let button;

function setup() {
  createCanvas(640, 480);
  background(255);

  capture = createCapture(VIDEO);
  capture.size(640, 480);
  //capture.hide();
  pixelDensity(1);

  button = createButton('take picture');
  button.mousePressed(takePhoto);
}

function takePhoto() {
    capture.loadPixels();

    let image = createImage(capture.width, capture.height);
    image.loadPixels();

    for(let i = 0; i < capture.pixels.length; i++) {
        image.pixels[i] = capture.pixels[i];
    }

    image.updatePixels();

    save(image, 'capture.jpg');
}

function draw() {
 // background(255);

 // capture.loadPixels();

 // capture.updatePixels();

  //image(capture, 0, 0);
}