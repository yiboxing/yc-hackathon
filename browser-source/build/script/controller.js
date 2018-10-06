
loadImg("https://onyx.tv/img/384.png");

var socket = io('http://127.0.0.1:3001');
socket.on('connect', function(){});
socket.on('corners', function(data){
  setCorners(data[0], data[1], data[2], data[3])
})
socket.on('disconnect', function(){});

// setCorners(  
//   {x: 100, y: 20},           // ul
//   {x: 520, y: 20},           // ur
//   {x: 220, y: 380},          // br
//   {x: 100, y: 380}
// );           // bl)

