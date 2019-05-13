// const bodyParser = require("body-parser");
path = require('path')

// initialize app
const {app, BrowserWindow} = require('electron')
//app.set('view engine', 'ejs')


// helper function spawn a python process to run a given script
function runPython(funcName){

  var interpreter =  'C:/Users/rldun/AppData/Local/Continuum/anaconda3/envs/wb-live/python'
  var python = require('child_process').spawn(interpreter, [funcName])
  python.stdout.on('data', function(data){
    console.log('data was: ', data.toString('utf8'))
  })

}

// make instance of browser window
function createWindow () {
    window = new BrowserWindow({width: 800, height: 600})
    window.loadFile('index.html')
    runPython('hello_image.py')
}

// close app on window closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin'){
        app.quit()
    }
})

app.get('/submit-params-button', function(req, res){
  //reqBody = req.body
  runPython('hello.py')
  res.render('./views/pages/index2')

})


// instantiate app
app.on('ready', createWindow)
