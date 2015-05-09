/*
 * app.js
 * Copyright (C) 2014 dhilipsiva <dhilipsiva@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

var parseArgs = require('minimist')
  , port = 8008
  , io = require('socket.io')(port)
  , redis = require('redis')
  , argv = parseArgs(process.argv)
  , redisPort = argv.port || 6379
  , redisHost = argv.host || 'localhost'
  , client = redis.createClient(parseInt(redisPort), redisHost)
  , channels = {}
  , Sequelize = require('sequelize');


// var sequelize = new Sequelize('postgres://user:pass@foo.com:5432/dbname');

var sequelize = new Sequelize('', '', '', {
  dialect: 'sqlite',
  storage: '../db.sqlite3',
  define: {
    timestamps: false,
    freezeTableName: true
  }
})

var User = sequelize.define('core_user', {
  username: {
    type: Sequelize.STRING,
    field: 'username'
  }
});

User.findAll().then(function(users) {
  for (i = 0; i < users.length; i++) {
    console.log(users[i].username);
  }
})

var getChannelsItem = function(client, channel) {
  var channelID = client.opt.server + ":" + client.opt.nick;
};

console.log('server listens on port ' + port);

io.sockets.on('connection', function (socket) {

  socket.on('subscribe', function(data) {
    socket.join(data.room);
    console.log("User joined the room: ", data);
  })

  socket.on('unsubscribe', function(data) {
    socket.leave(data.room);
    console.log("User left the room: ", data);
  })

  socket.on('disconnect', function(data) {
    socket.leave(data.room);
    console.log("User quit the room: ", data);
  })

});

client.on("message", function (channel, message) {

  console.log("channel:%s - message:%s",channel, message);
  data = JSON.parse(message);

  switch (channel) {
    case 'notify':
      data.rooms.forEach(function(room) {
        io.sockets.in(room).emit(data.event, data.data);
      });
    break;
    case 'tasks':
      console.log("SOME TASKS SENT")
    break;
    default:

  }

});

client.subscribe("notify");
client.subscribe("tasks");

/*
 * Usage on client side
 *
 * socket.send("subscribe", { room: "user uuid" });
 *
 */

var irc = require('irc');

var ircClient = new irc.Client('0.0.0.0', 'foopygoo2', {
  autoConnect: false
});

ircClient.connect(5, function(input) {
  console.log("Connected!");
  this.join('#ircman', function(input) {
    console.log("Joined #ircman");
  });
});

ircClient.addListener('message', function (from, to, text) {
  console.log("m: " + from + ' => ' + to + ': ' + text);
  this.say('#ircman', "Echo: "+text);
  console.log(this.opt.server);
});

ircClient.addListener('pm', function (from, text) {
  console.log("pm: " + from + ' => ' + text);
  ircClient.say('#ircman', "Echo: "+text);
});

ircClient.addListener('error', function(message) {
  console.log('error: ', message);
});
