var fs = require('fs');
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

//------------------------------------------------------------------------------
//  Global variables
//------------------------------------------------------------------------------
var port=3001

//------------------------------------------------------------------------------
//  Start from here
//------------------------------------------------------------------------------

main();

//------------------------------------------------------------------------------
//  All the implementation goes below
//------------------------------------------------------------------------------


function onUpdateCorners(data) {
  io.sockets.emit('corners', data); 
}

function onClientDisconnect() {
  console.log('client disconnect');
}

function main() {
  io.on('connection', function(client) {
    console.log('client has connected');
    // streamer_id = client.handshake.query.id; // cached to global //THIS IS PRETTY FUCKING BAD
    // streamer_twitch_login = client.handshake.query.twitch_login_name; // cached to global //THIS IS PRETTY FUCKING BAD
    // streamer_access_token = client.handshake.query.access_token;
    client.on('update_corners', onUpdateCorners);
    client.on('disconnect', onClientDisconnect);
  });
  server.listen(port);
}

