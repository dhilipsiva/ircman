###
# app.coffee
# Copyright (C) 2014 dhilipsiva <dhilipsiva@gmail.com>
#
# Distributed under terms of the MIT license.
###

Sequelize = require 'sequelize'
parseArgs = require 'minimist'
celery = require 'node-celery'
socketIO = require 'socket.io'
redis = require 'redis'
irc = require 'irc'

port = 8008
argv = parseArgs process.argv
redisPort = argv.port or 6379
redisHost = argv.host or 'localhost'
io = socketIO port
redisClient = redis.createClient parseInt(redisPort), redisHost
channels = {}


getChannelsItem = (client, channel) ->
  channelID = "#{client.opt.server}:#{client.opt.nick}"
  console.log channelID

setupClient = (userChannel)->

  ircClient = new irc.Client userChannel.userServer.server.host,
    userChannel.userServer.nickname,
    autoConnect: false
    password: userChannel.userServer.password
    port: userChannel.userServer.port

  ircClient.userChannel = userChannel

  ircClient.connect 5, (input) ->
    console.log 'Connected!'
    @join userChannel.channel.name, (input) ->
      console.log 'Joined #ircman'

  ircClient.addListener 'message', (from, to, text) ->
    console.log @userChannel
    console.log 'm: ' + from + ' => ' + to + ': ' + text
    @say userChannel.channel.name, 'Echo: ' + text
    console.log @opt.server

  ircClient.addListener 'pm', (from, text) ->
    console.log 'pm: ' + from + ' => ' + text

  ircClient.addListener 'error', (message) ->
    console.log 'error: ', message

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

redisClient.on 'message', (channel, message) ->

  console.log 'channel:%s - message:%s', channel, message
  data = JSON.parse message

  switch channel
    when 'notify'
      data.rooms.forEach (room) ->
        io.sockets.in(room).emit data.event, data.data

    when 'tasks'
      console.log 'SOME TASKS SENT'

    when 'setupClient'
      setupClient data.data

redisClient.subscribe 'notify'

redisClient.subscribe 'tasks'

redisClient.subscribe 'setupClient'

###
# Usage on client side
#
# socket.send("subscribe", { room: "user uuid" });
#
###

celeryClient = celery.createClient
  CELERY_BROKER_URL: 'amqp://guest:guest@localhost:5672//'

celeryClient.on 'error', (err) ->
    console.log err

celeryClient.on 'connect', ->
    celeryClient.call 'core.tasks.init'
