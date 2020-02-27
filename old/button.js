var Gpio = require('onoff').Gpio;
const exec = require('child_process').exec;
console.log('started...');

var pushButton = new Gpio(14, 'in', 'none', { debounceTimeout: 100 });

pushButton.watch(function (err, value) {
  if (err) { //if an error
    console.error('There was an error', err);
    return;
  } else {
    if (value == 0) {
      console.log('Click:', value);
      exec('sh takepic.sh');
    } else {
      console.log('UnClick:', value);
    }
  }
});

function unexportOnClose() {
  pushButton.unexport();
};

process.on('SIGINT', unexportOnClose);