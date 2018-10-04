/* Quadrilateral Transform - (c) Ken Nilsen, CC3.0-Attr */
corners = [
        {x: 100, y: 20},           // ul
        {x: 520, y: 20},           // ur
        {x: 520, y: 380},          // br
        {x: 100, y: 380}           // bl
      ]
stepEl = document.querySelector("input"),
stepTxt = document.querySelector("span"),
c = document.querySelector("canvas"),
ctx = c.getContext("2d"),
//radius = 10, cPoint, timer,  // for mouse handling
step = 1;  

function loadImg(url) {
  img = new Image();  
  img.onload = onLoad;
  img.src = url;
}

function setCorners(ul, ur, br, bl) {
  corners = []
  corners.push(ul);
  corners.push(ur);
  corners.push(br);
  corners.push(bl);
  render();
}

function onLoad() {
  render();
  //drawCorners()
}

// render image to quad using current settings
function render() {
  
  var p1, p2, p3, p4, y1c, y2c, y1n, y2n,
      w = img.width - 1,         // -1 to give room for the "next" points
      h = img.height - 1;

  ctx.clearRect(0, 0, c.width, c.height);

  for(y = 0; y < h; y += step) {
    for(x = 0; x < w; x += step) {
      y1c = lerp(corners[0], corners[3],  y / h);
      y2c = lerp(corners[1], corners[2],  y / h);
      y1n = lerp(corners[0], corners[3], (y + step) / h);
      y2n = lerp(corners[1], corners[2], (y + step) / h);

      // corners of the new sub-divided cell p1 (ul) -> p2 (ur) -> p3 (br) -> p4 (bl)
      p1 = lerp(y1c, y2c,  x / w);
      p2 = lerp(y1c, y2c, (x + step) / w);
      p3 = lerp(y1n, y2n, (x + step) / w);
      p4 = lerp(y1n, y2n,  x / w);

      ctx.drawImage(img, x, y, step, step,  p1.x, p1.y, // get most coverage for w/h:
          Math.ceil(Math.max(step, Math.abs(p2.x - p1.x), Math.abs(p4.x - p3.x))) + 1,
          Math.ceil(Math.max(step, Math.abs(p1.y - p4.y), Math.abs(p2.y - p3.y))) + 1)
    }
  }
}

// function drawCorners() {
//   ctx.strokeStyle = "#09f"; 
//   ctx.lineWidth = 2;
//   ctx.beginPath();
//   // border
//   for(var i = 0, p; p = corners[i++];) ctx[i ? "lineTo" : "moveTo"](p.x, p.y);
//   ctx.closePath();
//   // circular handles
//   for(i = 0; p = corners[i++];) {
//     ctx.moveTo(p.x + radius, p.y); 
//     ctx.arc(p.x, p.y, radius, 0, 6.28);
//   }
//   ctx.stroke()
// }

function lerp(p1, p2, t) {
  return {
    x: p1.x + (p2.x - p1.x) * t, 
    y: p1.y + (p2.y - p1.y) * t
  }
}