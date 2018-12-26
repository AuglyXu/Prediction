var mysql = require('mysql');

exports.ttconnect = function(){
    return connection = mysql.createConnection({
        host:"localhost",
        port:"3306",
        user:"root",
        password:'213xuxianzhe213',
        database:'nba'
    });
};

