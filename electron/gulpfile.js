'use strict';

var gulp = require('gulp');
var electron = require('electron-connect').server.create();

// var electron = require('../../').server.create({
//   useGlobalElectron: true,
//   verbose: true
// });

gulp.task('serve', function () {
  // Start browser process
  electron.start();

  // // Add an argument
  // electron.start('Hoge!');

  // // Add list of arguments
  // electron.start(['Hoge', 'foo']);

  // // Callback
  // electron.start(function () {
  //   console.log('started');
  // });

  // Restart browser process
  gulp.watch('app.js', electron.restart);

  // Reload renderer process
  gulp.watch(['main.js', 'index.html', 'js/script.js', 'js/lyric_engine.js'], electron.reload);
});

gulp.task('reload:browser', function () {
  // Restart main process
  electron.restart();
});

gulp.task('reload:renderer', function () {
  // Reload renderer process
  electron.reload();
});

gulp.task('default', ['serve']);
