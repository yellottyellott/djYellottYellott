var gulp = require('gulp');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var minifycss = require('gulp-minify-css');
var rename = require('gulp-rename');
var gzip = require('gulp-gzip');


var gzip_options = {
    threshold: "1kb",
    gzipOptions: {
        level: 9
    }
};


gulp.task('sass', function() {
    var src = 'yellottyellott/static/scss/*.scss';
    var dest = 'yellottyellott/static/css';

    return gulp.src(src)
        .pipe(sass())
        .pipe(gulp.dest(dest))
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest(dest))
        .pipe(gzip(gzip_options))
        .pipe(gulp.dest(dest))
        ;
});


gulp.task('watch', ['sass'], function() {
    gulp.watch('**/scss/*.scss', ['sass']);
});


gulp.task('default', ['watch']);
