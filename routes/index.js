const express = require('express');
const router = express.Router();
const { exec } = require("child_process");
const { execFile } = require("child_process");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/', function(req, res, next) {
  execFile("/usr/bin/python3", ["main2.py", req.body.API_KEY,
      req.body.SECRET_KEY ,
      req.body.USDT ,
      req.body.rate ,
      req.body.multipler ,
      req.body.wait ,
      req.body.symbol]
      , (error, stdout, stderr) => {
    if (error) {
      res.send(`error: ${error.message}`);
      return;
    }
    if (stderr) {
      res.send(`stderr: ${stderr}`);
      return;
    }
    res.send(`stdout: ${stdout}`);
  });
  // res.send(req.body);
});

router.post('/test',function(req,res,next){
  const schedule   = require('node-schedule');
  const mailer = require('nodemailer');
  const moment = require('moment');
  process.env.TZ = 'Europe/Amsterdam'
  var date = Date.now();
  var newdate = moment(date).set({hour:req.body.hour,minute:req.body.minute,second:0,millisecond:0}).toDate();

  const transporter = mailer.createTransport({
    host: "smtp.mailtrap.io",
    port: 2525,
    auth: {
      user: "1661d6903d8c30",
      pass: "e78996e77caea5"
    }
  });
  function sendEmail(message){
      //sending the email
      transporter.sendMail({
          from: 'peter@kayere.com',
          to: 'turgutsimarmaz@gmail.com',
          subject: 'Scheduled Email',
          text: message
      })
          .then(_ => {console.log("Email will send on " + newdate)})
          .catch(error => {console.log(error)});
  }
  sendEmail("testmailiiii" + Date.now());
  schedule.scheduleJob(newdate,function(){
    sendEmail("testmailiiii" + Date.now())
  });
});

module.exports = router;
