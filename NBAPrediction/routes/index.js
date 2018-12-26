var express = require('express');
var router = express.Router({});
var connection = require('./mysql');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'NBA' });
});


module.exports = router;
