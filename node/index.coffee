###
# app.coffee
# Copyright (C) 2014 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
###

Sequelize = require 'sequelize'
parseArgs = require 'minimist'
io = require('socket.io') port
redis = require 'redis'
irc = require 'irc'

port = 8008
argv = parseArgs process.argv
redisPort = argv.port or 6379
redisHost = argv.host or 'localhost'
client = redis.createClient parseInt(redisPort), redisHost
channels = {}

console.log 'server listens on port ' + port

io.sockets.on 'connection', (socket) ->
  socket.on 'subscribe', (data) ->
    socket.join data.room
    console.log 'User joined the room: ', data

  socket.on 'unsubscribe', (data) ->
    socket.leave data.room
    console.log 'User left the room: ', data

  socket.on 'disconnect', (data) ->
    socket.leave data.room
    console.log 'User quit the room: ', data

client.on 'message', (channel, message) ->
  console.log 'channel:%s - message:%s', channel, message
  data = JSON.parse message

  switch channel
    when 'notify'
      data.rooms.forEach (room) ->
        io.sockets.in(room).emit data.event, data.data

    when 'tasks'
      console.log 'SOME TASKS SENT'

client.subscribe 'notify'

client.subscribe 'tasks'

###
# Usage on client side
#
# socket.send("subscribe", { room: "user uuid" });
#
###

# var sequelize = new Sequelize('postgres://user:pass@foo.com:5432/dbname');

sequelize = new Sequelize '', '', '',
  dialect: 'sqlite'
  storage: '../db.sqlite3'
  define:
    timestamps: false
    freezeTableName: true

User = sequelize.define 'core_user',
  id:
    type: Sequelize.BIGINT
    primaryKey: true
  username: Sequelize.STRING

Server = sequelize.define 'core_server',
  id:
    type: Sequelize.BIGINT
    primaryKey: true
  host: Sequelize.STRING
  port: Sequelize.BIGINT
  isSsl:
    type: Sequelize.BOOLEAN
    field: 'is_ssl'
  isSasl:
    type: Sequelize.BOOLEAN
    field: 'is_sasl'

UserServer = sequelize.define 'core_userserver',
  id:
    type: Sequelize.BIGINT
    primaryKey: true
  label: Sequelize.STRING
  username: Sequelize.STRING
  password: Sequelize.STRING
  nickname: Sequelize.STRING
  realname: Sequelize.STRING

UserServer.belongsTo Server,
  foreignKey: 'server_id'

Server.hasMany UserServer,
  foreignKey: 'server_id'
  # through: 'UserServers'

UserServer.findAll().then (objects) ->
  for object in objects
    console.log Object.keys object
    console.log object.server_id

getChannelsItem = (client, channel) ->
  channelID = client.opt.server + ':' + client.opt.nick

ircClient = new irc.Client '0.0.0.0', 'foopygoo2', autoConnect: false

ircClient.connect 5, (input) ->
  console.log 'Connected!'
  @join '#ircman', (input) ->
    console.log 'Joined #ircman'

ircClient.addListener 'message', (from, to, text) ->
  console.log 'm: ' + from + ' => ' + to + ': ' + text
  @say '#ircman', 'Echo: ' + text
  console.log @opt.server

ircClient.addListener 'pm', (from, text) ->
  console.log 'pm: ' + from + ' => ' + text
  ircClient.say '#ircman', 'Echo: ' + text

ircClient.addListener 'error', (message) ->
  console.log 'error: ', message
