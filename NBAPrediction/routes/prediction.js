var connection = require('./mysql');
var express = require('express');
var router = express.Router();

router.post('/prediction',function (req,res,next) {

    var dbConnection = connection.ttconnect();
    console.log(req.body);
    dbConnection.query('SELECT * FROM resultprediction WHERE WIN = ? and LOSE = ?', [req.body.winTeam,req.body.loseTeam],function (err, rows) {
        if (err) {
            console.log(err);
            dbConnection1.end();
            throw err;
        }else {
            res.send(rows)
        }
    });
    dbConnection.end()
});

module.exports = router;


