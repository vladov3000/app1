//python3 schedule.py courses --subject math --course precalculus
var express = require('express')
  , logger = require('morgan')
  , app = express()
  , url = require('url')
  , expressValidator = require('express-validator')


app.use(logger('dev'))
app.use(expressValidator());



app.get('/courses', function (req, res, next) {
  try {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    
    var q = url.parse(req.url, true);
    console.log('path:'+q.pathname)
    console.log('subject:'+req.query.subject)

    var params = ['schedule.py']

    req.check('subject','Subject Required').notEmpty();
    req.check('course','Course Required').notEmpty();

    req.sanitize('subject').toString();
    req.sanitize('course').toString();

    params=params.concat(['courses','--subject',req.query.subject,'--course',req.query.course])
    console.log(params)

    var errors = req.validationErrors();
    if (errors) {
        var response = { errors: [] };
        errors.forEach(function(err) {
          response.errors.push(err.msg);
        });
        res.statusCode = 400;
        return res.json(response);
    }

    var spawn = require('child_process').spawn;
    var cmd = params 
    console.log(cmd)
    var prc = spawn('python3',  cmd);

    prc.stdout.setEncoding('utf8');
    prc.stdout.on('data', function (data) {
        var str = data.toString()
        console.log(str)
        res.write(str + '\r\n');
    });

    prc.on('close', function (code) {
        console.log('process exit code ' + code);
        res.end();
    });



  } catch (e) {
    next(e)
  }
});

app.get('/prereqs', function (req, res, next) {
  try {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    
    var q = url.parse(req.url, true);
    console.log('path:'+q.pathname)
    console.log('subject:'+req.query.subject)
    console.log('courses:'+req.query.courses)

    var params = ['schedule.py']

    req.check('subject','Subject Required').notEmpty();
    req.check('courses','Course Required').notEmpty();

    req.sanitize('subject').toString();
    req.sanitize('courses').toString();

    params=params.concat(['prereqs','--subject',req.query.subject,'--courses'])
    params=params.concat(req.query.courses.split(','))
    console.log(params)

    var errors = req.validationErrors();
    if (errors) {
        var response = { errors: [] };
        errors.forEach(function(err) {
          response.errors.push(err.msg);
        });
        res.statusCode = 400;
        return res.json(response);
    }

    var spawn = require('child_process').spawn;
    var cmd = params 
    console.log(cmd)
    var prc = spawn('python3',  cmd);

    prc.stdout.setEncoding('utf8');
    prc.stdout.on('data', function (data) {
        var str = data.toString()
        console.log(str)
        res.write(str + '\r\n');
    });

    prc.on('close', function (code) {
        console.log('process exit code ' + code);
        res.end();
    });



  } catch (e) {
    next(e)
  }
})

app.listen(process.env.PORT || 3000, function () {
  console.log('Listening on http://localhost:' + (process.env.PORT || 3000))
})
