'use strict';

/* External modules */

var fs = require('fs');
var express = require('express');
var winston = require('winston');

/* Library modules */

var CampaignInfoStorage = require('./lib/storage/sqlite/campaign-info-storage');

/* Controllers */

var campaigninfoById = require('./controllers/campaigns').campaigninfoById;

/* App variables */

var app = express();
var config = JSON.parse(fs.readFileSync('config.json'));
var extern = { logger: winston };

/* Endpoints */

app.get('/campaigns/:id/info', function (req, res) {
  extern.backend = new CampaignInfoStorage(config.storage);
  campaigninfoById(extern, req, res);
});

/* Initialize */

app.listen(config.listen.port, config.listen.address, function () {
  extern.logger.log('info', 'API listening on port %d', config.listen.port);
});
